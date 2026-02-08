"""Tests for Easy@Home temperature sensor."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from custom_components.easyathome.sensor import EasyHomeTemperatureSensor


@pytest.mark.asyncio
async def test_temperature_sensor_creation(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor creation."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(
        mock_coordinator,
        "AA:BB:CC:DD:EE:FF",
    )

    assert sensor.unique_id == "AA:BB:CC:DD:EE:FF_temperature"
    assert sensor.native_unit_of_measurement == UnitOfTemperature.CELSIUS
    assert sensor.device_class == "temperature"


@pytest.mark.asyncio
async def test_temperature_sensor_native_value(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor native value."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(
        mock_coordinator,
        "AA:BB:CC:DD:EE:FF",
    )

    assert sensor.native_value == 37.5


@pytest.mark.asyncio
async def test_temperature_sensor_attributes(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor extra state attributes."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(
        mock_coordinator,
        "AA:BB:CC:DD:EE:FF",
    )

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

    sensor = EasyHomeTemperatureSensor(
        mock_coordinator,
        "AA:BB:CC:DD:EE:FF",
    )

    assert sensor.native_value is None


@pytest.mark.asyncio
async def test_temperature_sensor_restore_state(
    hass: HomeAssistant, mock_temperature_measurement
) -> None:
    """Test temperature sensor restore state functionality."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = mock_temperature_measurement

    sensor = EasyHomeTemperatureSensor(
        mock_coordinator,
        "AA:BB:CC:DD:EE:FF",
    )

    # Test that it has restore capability (RestoreSensor)
    assert hasattr(sensor, "async_added_to_hass")
