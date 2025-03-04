"""Services for the Bed Manager integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_registry as er

from .const import (
    DOMAIN,
    ATTR_POSITION,
    ATTR_CALIBRATION_MODE,
)

_LOGGER = logging.getLogger(__name__)

async def async_set_head_position(hass: HomeAssistant, call: ServiceCall) -> None:
    """Set the head position of a bed."""
    entity_id = call.data["entity_id"]
    registry = er.async_get(hass)
    entity = registry.async_get(entity_id)
    
    if not entity or entity.platform != DOMAIN:
        raise ValueError(f"Entity {entity_id} not found or not a bed")

    device = hass.data[DOMAIN][entity.config_entry_id]
    await device.async_set_head_position(call.data[ATTR_POSITION])

async def async_set_feet_position(hass: HomeAssistant, call: ServiceCall) -> None:
    """Set the feet position of a bed."""
    entity_id = call.data["entity_id"]
    registry = er.async_get(hass)
    entity = registry.async_get(entity_id)
    
    if not entity or entity.platform != DOMAIN:
        raise ValueError(f"Entity {entity_id} not found or not a bed")

    device = hass.data[DOMAIN][entity.config_entry_id]
    await device.async_set_feet_position(call.data[ATTR_POSITION])

async def async_calibrate(hass: HomeAssistant, call: ServiceCall) -> None:
    """Calibrate a bed."""
    entity_id = call.data["entity_id"]
    registry = er.async_get(hass)
    entity = registry.async_get(entity_id)
    
    if not entity or entity.platform != DOMAIN:
        raise ValueError(f"Entity {entity_id} not found or not a bed")

    device = hass.data[DOMAIN][entity.config_entry_id]
    mode = call.data.get(ATTR_CALIBRATION_MODE, 0)
    await device.async_calibrate(mode)

async def async_diagnostics(hass: HomeAssistant, call: ServiceCall) -> dict[str, Any]:
    """Get diagnostic information for a bed."""
    entity_id = call.data["entity_id"]
    registry = er.async_get(hass)
    entity = registry.async_get(entity_id)
    
    if not entity or entity.platform != DOMAIN:
        raise ValueError(f"Entity {entity_id} not found or not a bed")

    device = hass.data[DOMAIN][entity.config_entry_id]
    return await device.async_diagnostics() 