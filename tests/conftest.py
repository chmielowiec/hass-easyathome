"""Pytest configuration and fixtures for Easy@Home integration tests."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.components.bluetooth import BluetoothServiceInfo

from custom_components.easyathome.const import DOMAIN

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests."""
    yield


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
    measurement = MagicMock()
    measurement.temperature = 37.5
    measurement.timestamp = datetime(2024, 2, 9, 14, 30, 0, tzinfo=timezone.utc)
    measurement.is_live = True
    return measurement


@pytest.fixture
def discovery_info():
    """Create discovery info."""
    return BluetoothServiceInfo(
        name="EBT-300",
        address="AA:BB:CC:DD:EE:FF",
        rssi=-60,
        manufacturer_data={},
        service_data={},
        service_uuids=["0000ffe0-0000-1000-8000-00805f9b34fb"],
        source="local",
    )
