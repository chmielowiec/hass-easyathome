"""Tests for Easy@Home temperature sensor."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import STORAGE_KEY as RESTORE_STATE_KEY
from homeassistant.util.json import JsonObjectType

from custom_components.easyathome.sensor import EasyHomeTemperatureSensor


@pytest.mark.asyncio
async def test_temperature_sensor_creation(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor creation."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    assert sensor.native_unit_of_measurement == UnitOfTemperature.CELSIUS
    assert sensor.device_class == "temperature"


@pytest.mark.asyncio
async def test_temperature_sensor_native_value(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor native value."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    assert sensor.native_value == 37.5


@pytest.mark.asyncio
async def test_temperature_sensor_attributes(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor extra state attributes."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    attributes = sensor.extra_state_attributes

    assert attributes["measurement_time"] == "2024-02-09T14:30:00+00:00"
    assert attributes["is_live_reading"] is True


@pytest.mark.asyncio
async def test_temperature_sensor_no_data(
    hass: HomeAssistant,
) -> None:
    """Test temperature sensor with no data."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = None

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    assert sensor.native_value is None

@pytest.mark.asyncio
async def test_temperature_sensor_available_with_last_value(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Sensor stays available with last measurement after device powers off."""

    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    assert sensor.available is True


@pytest.mark.asyncio
async def test_temperature_sensor_restore_state(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor restore state functionality."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    # Test that it has restore capability (RestoreSensor)
    assert hasattr(sensor, "async_added_to_hass")


@pytest.mark.asyncio
async def test_temperature_sensor_restores_last_value_on_startup(
    hass: HomeAssistant,
) -> None:
    """Test that temperature sensor restores last value after HA restart."""
    # Create a mock coordinator with no data (simulating device being offline)
    mock_coordinator = MagicMock()
    mock_coordinator.data = None
    mock_coordinator.config_entry = MagicMock()
    mock_coordinator.config_entry.data = {"address": "AA:BB:CC:DD:EE:FF"}

    # Create sensor
    sensor = EasyHomeTemperatureSensor(mock_coordinator)
    
    # Mock the restore state functionality
    last_sensor_data = MagicMock()
    last_sensor_data.native_value = 36.8
    
    with patch.object(
        sensor, "async_get_last_sensor_data", return_value=last_sensor_data
    ), patch.object(sensor, "async_write_ha_state"):
        await sensor.async_added_to_hass()

    # Verify that the sensor restored the last value
    assert sensor.native_value == 36.8
    

@pytest.mark.asyncio
async def test_temperature_sensor_updates_value_when_new_data_arrives(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test that sensor updates value when new data arrives from coordinator."""
    # Create a mock coordinator with no data initially
    mock_coordinator = MagicMock()
    mock_coordinator.data = None
    mock_coordinator.config_entry = MagicMock()
    mock_coordinator.config_entry.data = {"address": "AA:BB:CC:DD:EE:FF"}

    # Create sensor
    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    # Mock the restore state functionality with old value
    last_sensor_data = MagicMock()
    last_sensor_data.native_value = 36.8

    with patch.object(
        sensor, "async_get_last_sensor_data", return_value=last_sensor_data
    ), patch.object(sensor, "async_write_ha_state"):
        await sensor.async_added_to_hass()

    # Verify that the sensor restored the old value
    assert sensor.native_value == 36.8

    # Simulate new data arriving from the coordinator
    mock_coordinator.data = mock_temperature_measurement

    # Verify that the sensor now shows the new value
    assert sensor.native_value == 37.5


@pytest.mark.asyncio
async def test_temperature_sensor_writes_ha_state_after_restore(
    hass: HomeAssistant,
) -> None:
    """Test that async_write_ha_state is called after restoring a previous value.

    This ensures the restored value is pushed into the HA state machine
    immediately on startup, before the BLE device connects.
    """
    mock_coordinator = MagicMock()
    mock_coordinator.data = None
    mock_coordinator.config_entry = MagicMock()
    mock_coordinator.config_entry.data = {"address": "AA:BB:CC:DD:EE:FF"}

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    last_sensor_data = MagicMock()
    last_sensor_data.native_value = 36.8

    with patch.object(
        sensor, "async_get_last_sensor_data", return_value=last_sensor_data
    ), patch.object(sensor, "async_write_ha_state") as mock_write_state:
        await sensor.async_added_to_hass()

    mock_write_state.assert_called_once()
    assert sensor._attr_native_value == 36.8


@pytest.mark.asyncio
async def test_temperature_sensor_no_write_ha_state_without_restore_data(
    hass: HomeAssistant,
) -> None:
    """Test that async_write_ha_state is not called when there is no saved state.

    When no previous state exists (e.g. first ever startup), the sensor
    should not trigger a redundant state write.
    """
    mock_coordinator = MagicMock()
    mock_coordinator.data = None
    mock_coordinator.config_entry = MagicMock()
    mock_coordinator.config_entry.data = {"address": "AA:BB:CC:DD:EE:FF"}

    sensor = EasyHomeTemperatureSensor(mock_coordinator)

    with patch.object(
        sensor, "async_get_last_sensor_data", return_value=None
    ), patch.object(sensor, "async_write_ha_state") as mock_write_state:
        await sensor.async_added_to_hass()

    mock_write_state.assert_not_called()
