"""Device class for Bed Manager integration."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_BED_TYPE,
    CONF_MAC_ADDRESS,
    CONF_NAME,
    CONF_DEVICE_NAME,
    CONF_TARGET_MAC,
    CONF_STORED_PIN,
    DEFAULT_DEVICE_NAME,
    DEFAULT_HEAD_DURATION,
    DEFAULT_FEET_DURATION,
)

_LOGGER = logging.getLogger(__name__)

class BedManagerDevice:
    """Device class for Bed Manager."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the device."""
        self.hass = hass
        self.entry = entry
        self._name = entry.data[CONF_NAME]
        self._mac_address = entry.data[CONF_MAC_ADDRESS]
        self._bed_type = entry.data[CONF_BED_TYPE]
        self._device_name = entry.data.get(CONF_DEVICE_NAME, DEFAULT_DEVICE_NAME)
        self._target_mac = entry.data.get(CONF_TARGET_MAC, "")
        self._stored_pin = entry.data.get(CONF_STORED_PIN, "0000")
        self._device_info: Optional[DeviceInfo] = None
        self._presets: Dict[str, Dict[str, Any]] = {}
        self._connected = False
        
        # Position tracking
        self._head_position = 0.0
        self._feet_position = 0.0
        self._target_head_position = 0.0
        self._target_feet_position = 0.0
        
        # Movement state
        self._movement_in_progress = False
        self._current_movement_type = 0
        self._calibration_mode = 0

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        if self._device_info is None:
            self._device_info = DeviceInfo(
                identifiers={(DOMAIN, self._mac_address)},
                name=self._name,
                model=self._bed_type,
                manufacturer="Octo Bed",
                via_device=(DOMAIN, self._mac_address),
            )
        return self._device_info

    async def async_setup(self) -> None:
        """Set up the device."""
        try:
            # Initialize ESPHome connection
            await self._async_connect()
            self._connected = True
            _LOGGER.info("Successfully connected to bed %s", self._name)
        except Exception as err:
            _LOGGER.error("Failed to connect to bed %s: %s", self._name, err)
            self._connected = False

    async def async_unload(self) -> None:
        """Unload the device."""
        if self._connected:
            await self._async_disconnect()
            self._connected = False

    async def _async_connect(self) -> None:
        """Connect to the bed via ESPHome."""
        # Implement ESPHome connection logic here
        pass

    async def _async_disconnect(self) -> None:
        """Disconnect from the bed."""
        # Implement ESPHome disconnection logic here
        pass

    async def async_save_preset(self, preset_name: str, position: Dict[str, Any], 
                              massage_level: int, massage_zone: str) -> None:
        """Save a preset position."""
        if not self._connected:
            raise RuntimeError("Device not connected")

        preset_data = {
            "position": position,
            "massage_level": massage_level,
            "massage_zone": massage_zone,
        }
        self._presets[preset_name] = preset_data
        _LOGGER.info("Saved preset %s for bed %s", preset_name, self._name)

    async def async_load_preset(self, preset_name: str) -> None:
        """Load a preset position."""
        if not self._connected:
            raise RuntimeError("Device not connected")

        if preset_name not in self._presets:
            raise ValueError(f"Preset {preset_name} not found")

        preset_data = self._presets[preset_name]
        # Implement bed-specific preset loading logic here
        _LOGGER.info("Loaded preset %s for bed %s", preset_name, self._name)

    async def async_set_head_position(self, position: float) -> None:
        """Set the head position (0-100%)."""
        if not self._connected:
            raise RuntimeError("Device not connected")

        if not 0 <= position <= 100:
            raise ValueError("Position must be between 0 and 100")

        self._target_head_position = position
        # Implement ESPHome command to move head
        _LOGGER.info("Setting head position to %.1f%% for bed %s", position, self._name)

    async def async_set_feet_position(self, position: float) -> None:
        """Set the feet position (0-100%)."""
        if not self._connected:
            raise RuntimeError("Device not connected")

        if not 0 <= position <= 100:
            raise ValueError("Position must be between 0 and 100")

        self._target_feet_position = position
        # Implement ESPHome command to move feet
        _LOGGER.info("Setting feet position to %.1f%% for bed %s", position, self._name)

    async def async_calibrate(self, mode: int = 0) -> None:
        """Calibrate the bed.
        
        Args:
            mode: 0=none, 1=head calibrating, 2=feet calibrating
        """
        if not self._connected:
            raise RuntimeError("Device not connected")

        if not 0 <= mode <= 2:
            raise ValueError("Calibration mode must be 0, 1, or 2")

        self._calibration_mode = mode
        # Implement ESPHome calibration command
        _LOGGER.info("Starting calibration mode %d for bed %s", mode, self._name)

    async def async_diagnostics(self) -> Dict[str, Any]:
        """Get diagnostic information."""
        if not self._connected:
            raise RuntimeError("Device not connected")

        return {
            "name": self._name,
            "type": self._bed_type,
            "mac_address": self._mac_address,
            "device_name": self._device_name,
            "connected": self._connected,
            "head_position": self._head_position,
            "feet_position": self._feet_position,
            "target_head_position": self._target_head_position,
            "target_feet_position": self._target_feet_position,
            "movement_in_progress": self._movement_in_progress,
            "current_movement_type": self._current_movement_type,
            "calibration_mode": self._calibration_mode,
            "presets": list(self._presets.keys()),
        } 