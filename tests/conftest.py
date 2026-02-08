"""Pytest configuration and fixtures for Easy@Home integration tests."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.easyathome.const import DOMAIN


@pytest.fixture
def mock_ble_device():
    """Create a mock BLE device."""
    device = MagicMock()
    device.address = "AA:BB:CC:DD:EE:FF"
    device.name = "EBT-300"
    return device


@pytest.fixture
def mock_advertisement_data():
    """Create mock advertisement data."""
    ad_data = MagicMock()
    ad_data.local_name = "EBT-300"
    ad_data.service_uuids = ["0000ffe0-0000-1000-8000-00805f9b34fb"]
    ad_data.rssi = -60
    return ad_data


@pytest.fixture
def mock_easy_home_device():
    """Create a mock EasyHomeDevice."""
    device = AsyncMock()
    device.address = "AA:BB:CC:DD:EE:FF"
    device.connected = False
    device.connect = AsyncMock()
    device.disconnect = AsyncMock()
    device.set_datetime = AsyncMock()
    device.set_unit = AsyncMock()
    return device


@pytest.fixture
def mock_temperature_measurement():
    """Create a mock TemperatureMeasurement."""
    from datetime import datetime, timezone

    measurement = MagicMock()
    measurement.temperature = 37.5
    measurement.timestamp = datetime(2024, 2, 9, 14, 30, 0, tzinfo=timezone.utc)
    measurement.is_live = True
    return measurement


@pytest.fixture
async def hass() -> HomeAssistant:
    """Create a Home Assistant instance."""
    hass = HomeAssistant("/tmp/homeassistant")
    yield hass
    await hass.async_block_till_done()
    await hass.async_block_till_done()


@pytest.fixture
def discovery_info():
    """Create discovery info."""
    return {
        "name": "EBT-300",
        "address": "AA:BB:CC:DD:EE:FF",
        "service_uuid": "0000ffe0-0000-1000-8000-00805f9b34fb",
    }
