"""Tests for Easy@Home data coordinator."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.easyathome.coordinator import EasyHomeDataUpdateCoordinator
from custom_components.easyathome.const import DOMAIN


@pytest.mark.asyncio
async def test_coordinator_init(hass: HomeAssistant, mock_easy_home_device) -> None:
    """Test coordinator initialization."""
    coordinator = EasyHomeDataUpdateCoordinator(
        hass,
        mock_easy_home_device,
    )

    assert coordinator.data is None
    assert coordinator.hass == hass


@pytest.mark.asyncio
async def test_coordinator_async_update_data(
    hass: HomeAssistant, mock_easy_home_device, mock_temperature_measurement
) -> None:
    """Test coordinator async_update_data."""
    mock_easy_home_device.connected = True

    coordinator = EasyHomeDataUpdateCoordinator(
        hass,
        mock_easy_home_device,
    )

    # Simulate notification callback
    coordinator._notification_handler(mock_temperature_measurement)
    await hass.async_block_till_done()


@pytest.mark.asyncio
async def test_coordinator_notification_handler(
    hass: HomeAssistant, mock_easy_home_device, mock_temperature_measurement
) -> None:
    """Test coordinator notification handler."""
    coordinator = EasyHomeDataUpdateCoordinator(
        hass,
        mock_easy_home_device,
    )

    coordinator._notification_handler(mock_temperature_measurement)

    assert coordinator.data == mock_temperature_measurement


@pytest.mark.asyncio
async def test_coordinator_async_shutdown(
    hass: HomeAssistant, mock_easy_home_device
) -> None:
    """Test coordinator async_shutdown."""
    coordinator = EasyHomeDataUpdateCoordinator(
        hass,
        mock_easy_home_device,
    )

    await coordinator.async_shutdown()

    mock_easy_home_device.disconnect.assert_called_once()
