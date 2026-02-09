"""Tests for Easy@Home data coordinator."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.easyathome.coordinator import EasyHomeDataUpdateCoordinator
from custom_components.easyathome.const import DOMAIN


@pytest.mark.asyncio
async def test_coordinator_init(hass: HomeAssistant, mock_easy_home_device) -> None:
    """Test coordinator initialization."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"address": "AA:BB:CC:DD:EE:FF"},
    )
    mock_entry.add_to_hass(hass)

    with patch(
        "custom_components.easyathome.coordinator.bluetooth.async_scanner_count",
        return_value=1,
    ), patch(
        "custom_components.easyathome.coordinator.EasyHomeDevice",
        return_value=mock_easy_home_device,
    ):
        coordinator = EasyHomeDataUpdateCoordinator(hass, mock_entry)

        assert coordinator.data is None
        assert coordinator.hass == hass


@pytest.mark.asyncio
async def test_coordinator_async_update_data(
    hass: HomeAssistant, mock_easy_home_device, mock_temperature_measurement
) -> None:
    """Test coordinator async_update_data."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"address": "AA:BB:CC:DD:EE:FF"},
    )
    mock_entry.add_to_hass(hass)
    mock_easy_home_device.connected = True

    with patch(
        "custom_components.easyathome.coordinator.bluetooth.async_scanner_count",
        return_value=1,
    ), patch(
        "custom_components.easyathome.coordinator.EasyHomeDevice",
        return_value=mock_easy_home_device,
    ):
        coordinator = EasyHomeDataUpdateCoordinator(hass, mock_entry)

        # Simulate notification callback
        coordinator._handle_notification(mock_temperature_measurement)
        await hass.async_block_till_done()


@pytest.mark.asyncio
async def test_coordinator_notification_handler(
    hass: HomeAssistant, mock_easy_home_device, mock_temperature_measurement
) -> None:
    """Test coordinator notification handler."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"address": "AA:BB:CC:DD:EE:FF"},
    )
    mock_entry.add_to_hass(hass)

    with patch(
        "custom_components.easyathome.coordinator.bluetooth.async_scanner_count",
        return_value=1,
    ), patch(
        "custom_components.easyathome.coordinator.EasyHomeDevice",
        return_value=mock_easy_home_device,
    ):
        coordinator = EasyHomeDataUpdateCoordinator(hass, mock_entry)

        coordinator._handle_notification(mock_temperature_measurement)

        assert coordinator.data == mock_temperature_measurement


@pytest.mark.asyncio
async def test_coordinator_async_shutdown(
    hass: HomeAssistant, mock_easy_home_device
) -> None:
    """Test coordinator async_shutdown."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"address": "AA:BB:CC:DD:EE:FF"},
    )
    mock_entry.add_to_hass(hass)
    mock_easy_home_device.connected = True

    with patch(
        "custom_components.easyathome.coordinator.bluetooth.async_scanner_count",
        return_value=1,
    ), patch(
        "custom_components.easyathome.coordinator.EasyHomeDevice",
        return_value=mock_easy_home_device,
    ):
        coordinator = EasyHomeDataUpdateCoordinator(hass, mock_entry)

        await coordinator.async_shutdown()

        mock_easy_home_device.disconnect.assert_called_once()


@pytest.mark.asyncio
async def test_coordinator_syncs_time_on_connect(
    hass: HomeAssistant, mock_easy_home_device
) -> None:
    """Ensure coordinator syncs time after connecting via custom service."""

    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={"address": "AA:BB:CC:DD:EE:FF"},
    )
    mock_entry.add_to_hass(hass)

    ble_device = MagicMock()

    with patch(
        "custom_components.easyathome.coordinator.bluetooth.async_scanner_count",
        return_value=1,
    ), patch(
        "custom_components.easyathome.coordinator.bluetooth.async_ble_device_from_address",
        return_value=ble_device,
    ), patch(
        "custom_components.easyathome.coordinator.EasyHomeDevice",
        return_value=mock_easy_home_device,
    ):
        coordinator = EasyHomeDataUpdateCoordinator(hass, mock_entry)

        await coordinator._async_update_data()

        mock_easy_home_device.update_ble_device.assert_called_once_with(ble_device)
        mock_easy_home_device.connect.assert_awaited_once()
        mock_easy_home_device.set_datetime.assert_awaited()
