"""Tests for Easy@Home integration setup and teardown."""

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.easyathome.const import DOMAIN


@pytest.mark.asyncio
async def test_async_setup_entry(
    hass: HomeAssistant, mock_easy_home_device
) -> None:
    """Test async_setup_entry."""
    from homeassistant.config_entries import ConfigEntry

    config_entry = ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="EBT-300",
        data={"address": "AA:BB:CC:DD:EE:FF"},
        options={},
        entry_id="test_entry_id",
        unique_id="AA:BB:CC:DD:EE:FF",
    )

    with patch(
        "custom_components.easyathome.EasyHomeDataUpdateCoordinator"
    ) as mock_coordinator_class:
        mock_coordinator = AsyncMock()
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()
        mock_coordinator_class.return_value = mock_coordinator

        result = await hass.config_entries.async_setup(config_entry)
        assert result is True


@pytest.mark.asyncio
async def test_async_unload_entry(
    hass: HomeAssistant, mock_easy_home_device
) -> None:
    """Test async_unload_entry."""
    from homeassistant.config_entries import ConfigEntry

    config_entry = ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="EBT-300",
        data={"address": "AA:BB:CC:DD:EE:FF"},
        options={},
        entry_id="test_entry_id",
        unique_id="AA:BB:CC:DD:EE:FF",
    )

    with patch(
        "custom_components.easyathome.EasyHomeDataUpdateCoordinator"
    ) as mock_coordinator_class:
        mock_coordinator = AsyncMock()
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()
        mock_coordinator.async_shutdown = AsyncMock()
        mock_coordinator_class.return_value = mock_coordinator

        # Setup
        await hass.config_entries.async_setup(config_entry)

        # Unload
        result = await hass.config_entries.async_unload_entry(config_entry)
        assert result is True
