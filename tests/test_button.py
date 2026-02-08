"""Tests for Easy@Home button platform."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.easyathome.button import SyncTimeButton, SetCelsiusButton


@pytest.mark.asyncio
async def test_sync_time_button_creation(hass: HomeAssistant) -> None:
    """Test sync time button creation."""
    mock_coordinator = MagicMock()
    mock_coordinator.device = AsyncMock()

    button = SyncTimeButton(mock_coordinator)

    assert button.unique_id.endswith("_sync_time")
    assert button.entity_description.key == "sync_time"


@pytest.mark.asyncio
async def test_sync_time_button_press(hass: HomeAssistant) -> None:
    """Test sync time button press."""
    mock_coordinator = MagicMock()
    mock_coordinator.device = AsyncMock()
    mock_coordinator.device.set_datetime = AsyncMock()

    button = SyncTimeButton(mock_coordinator)
    await button.async_press()

    mock_coordinator.device.set_datetime.assert_called_once()


@pytest.mark.asyncio
async def test_set_celsius_button_creation(hass: HomeAssistant) -> None:
    """Test set Celsius button creation."""
    mock_coordinator = MagicMock()
    mock_coordinator.device = AsyncMock()

    button = SetCelsiusButton(mock_coordinator)

    assert button.unique_id.endswith("_set_celsius")
    assert button.entity_description.key == "set_celsius"


@pytest.mark.asyncio
async def test_set_celsius_button_press(hass: HomeAssistant) -> None:
    """Test set Celsius button press."""
    mock_coordinator = MagicMock()
    mock_coordinator.device = AsyncMock()
    mock_coordinator.device.set_unit = AsyncMock()

    button = SetCelsiusButton(mock_coordinator)
    await button.async_press()

    mock_coordinator.device.set_unit.assert_called_once_with(celsius=True)
