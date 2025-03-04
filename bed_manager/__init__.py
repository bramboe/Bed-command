"""The Bed Manager integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    SERVICE_SET_HEAD_POSITION,
    SERVICE_SET_FEET_POSITION,
    SERVICE_CALIBRATE,
    SERVICE_DIAGNOSTICS,
    ATTR_POSITION,
    ATTR_CALIBRATION_MODE,
)
from .device import BedManagerDevice
from .services import (
    async_set_head_position,
    async_set_feet_position,
    async_calibrate,
    async_diagnostics,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.COVER,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.BUTTON,
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bed Manager from a config entry."""
    device = BedManagerDevice(hass, entry)
    await device.async_setup()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = device

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_HEAD_POSITION,
        async_set_head_position,
        schema={
            "entity_id": str,
            ATTR_POSITION: float,
        },
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_FEET_POSITION,
        async_set_feet_position,
        schema={
            "entity_id": str,
            ATTR_POSITION: float,
        },
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CALIBRATE,
        async_calibrate,
        schema={
            "entity_id": str,
            ATTR_CALIBRATION_MODE: int,
        },
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DIAGNOSTICS,
        async_diagnostics,
        schema={
            "entity_id": str,
        },
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        device = hass.data[DOMAIN].pop(entry.entry_id)
        await device.async_unload()

    return unload_ok 