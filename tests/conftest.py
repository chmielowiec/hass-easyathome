"""Pytest configuration and fixtures for Easy@Home integration tests."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak

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
    ad_data.service_uuids = ["00001809-0000-1000-8000-00805f9b34fb"]
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
    name = "EBT-300"
    address = "AA:BB:CC:DD:EE:FF"
    rssi = -60
    manufacturer_data: dict[int, bytes] = {}
    service_data: dict[str, bytes] = {}
    service_uuids = ["00001809-0000-1000-8000-00805f9b34fb"]
    source = "local"

    device = BLEDevice(address, name, None)
    advertisement = AdvertisementData(
        local_name=name,
        manufacturer_data=manufacturer_data,
        service_data=service_data,
        service_uuids=service_uuids,
        tx_power=None,
        rssi=rssi,
        platform_data=(),
    )
    return BluetoothServiceInfoBleak(
        name,
        address,
        rssi,
        manufacturer_data,
        service_data,
        service_uuids,
        source,
        device,
        advertisement,
        True,
        0.0,
        None,
        None,
    )
