"""Tests for the Bed Manager integration."""
import pytest
from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.components import cover
from homeassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TOGGLE,
    STATE_OPEN,
    STATE_CLOSED,
)

from custom_components.bed_manager import (
    DOMAIN,
    SERVICE_SET_HEAD_POSITION,
    SERVICE_SET_FEET_POSITION,
    SERVICE_CALIBRATE,
    SERVICE_DIAGNOSTICS,
)

@pytest.fixture
def mock_hass():
    """Create a mock hass object."""
    hass = AsyncMock(spec=HomeAssistant)
    hass.states = AsyncMock()
    hass.services = AsyncMock()
    return hass

@pytest.fixture
def mock_device():
    """Create a mock device."""
    device = AsyncMock()
    device.async_setup = AsyncMock()
    device.async_unload = AsyncMock()
    device.async_set_head_position = AsyncMock()
    device.async_set_feet_position = AsyncMock()
    device.async_calibrate = AsyncMock()
    device.async_diagnostics = AsyncMock()
    return device

async def test_setup_entry(mock_hass, mock_device):
    """Test setting up the integration."""
    from custom_components.bed_manager import async_setup_entry
    
    entry = AsyncMock()
    entry.data = {
        "name": "Test Bed",
        "mac_address": "00:11:22:33:44:55",
        "bed_type": "octo_bed",
    }
    
    with patch("custom_components.bed_manager.BedManagerDevice", return_value=mock_device):
        result = await async_setup_entry(mock_hass, entry)
        
        assert result is True
        mock_device.async_setup.assert_called_once()
        mock_hass.data[DOMAIN][entry.entry_id] == mock_device

async def test_set_head_position(mock_hass, mock_device):
    """Test setting head position."""
    from custom_components.bed_manager.services import async_set_head_position
    
    call = AsyncMock()
    call.data = {
        "entity_id": "cover.test_bed_head",
        "position": 50.0,
    }
    
    registry = AsyncMock()
    entity = AsyncMock()
    entity.platform = DOMAIN
    entity.config_entry_id = "test_entry"
    registry.async_get.return_value = entity
    
    with patch("homeassistant.helpers.entity_registry.async_get", return_value=registry):
        mock_hass.data[DOMAIN] = {"test_entry": mock_device}
        await async_set_head_position(mock_hass, call)
        
        mock_device.async_set_head_position.assert_called_once_with(50.0)

async def test_set_feet_position(mock_hass, mock_device):
    """Test setting feet position."""
    from custom_components.bed_manager.services import async_set_feet_position
    
    call = AsyncMock()
    call.data = {
        "entity_id": "cover.test_bed_feet",
        "position": 75.0,
    }
    
    registry = AsyncMock()
    entity = AsyncMock()
    entity.platform = DOMAIN
    entity.config_entry_id = "test_entry"
    registry.async_get.return_value = entity
    
    with patch("homeassistant.helpers.entity_registry.async_get", return_value=registry):
        mock_hass.data[DOMAIN] = {"test_entry": mock_device}
        await async_set_feet_position(mock_hass, call)
        
        mock_device.async_set_feet_position.assert_called_once_with(75.0)

async def test_calibrate(mock_hass, mock_device):
    """Test calibration."""
    from custom_components.bed_manager.services import async_calibrate
    
    call = AsyncMock()
    call.data = {
        "entity_id": "cover.test_bed_head",
        "calibration_mode": 1,
    }
    
    registry = AsyncMock()
    entity = AsyncMock()
    entity.platform = DOMAIN
    entity.config_entry_id = "test_entry"
    registry.async_get.return_value = entity
    
    with patch("homeassistant.helpers.entity_registry.async_get", return_value=registry):
        mock_hass.data[DOMAIN] = {"test_entry": mock_device}
        await async_calibrate(mock_hass, call)
        
        mock_device.async_calibrate.assert_called_once_with(1)

async def test_diagnostics(mock_hass, mock_device):
    """Test diagnostics."""
    from custom_components.bed_manager.services import async_diagnostics
    
    call = AsyncMock()
    call.data = {
        "entity_id": "cover.test_bed_head",
    }
    
    registry = AsyncMock()
    entity = AsyncMock()
    entity.platform = DOMAIN
    entity.config_entry_id = "test_entry"
    registry.async_get.return_value = entity
    
    mock_device.async_diagnostics.return_value = {
        "name": "Test Bed",
        "type": "octo_bed",
        "connected": True,
    }
    
    with patch("homeassistant.helpers.entity_registry.async_get", return_value=registry):
        mock_hass.data[DOMAIN] = {"test_entry": mock_device}
        result = await async_diagnostics(mock_hass, call)
        
        assert result == {
            "name": "Test Bed",
            "type": "octo_bed",
            "connected": True,
        } 