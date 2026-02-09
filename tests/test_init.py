"""Tests for Easy@Home integration setup and teardown."""

import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.easyathome.const import DOMAIN

# Skip all init tests on macOS since integration requires bluetooth component (Linux DBus)
pytestmark = pytest.mark.skipif(
    sys.platform == "darwin",
    reason="Integration setup requires bluetooth component (DBus/Linux only)",
)


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    return MockConfigEntry(
        domain=DOMAIN,
        title="EBT-300",
        data={"address": "AA:BB:CC:DD:EE:FF"},
        unique_id="AA:BB:CC:DD:EE:FF",
    )


@pytest.mark.asyncio
async def test_async_setup_entry(
    hass: HomeAssistant, mock_config_entry, mock_easy_home_device
) -> None:
    """Test async_setup_entry."""
    with patch(
        "custom_components.easyathome.coordinator.EasyHomeDevice",
        return_value=mock_easy_home_device,
    ), patch(
        "custom_components.easyathome.coordinator.bluetooth.async_scanner_count",
        return_value=1,
    ):
        mock_config_entry.add_to_hass(hass)
        result = await hass.config_entries.async_setup(mock_config_entry.entry_id)
        assert result is True


@pytest.mark.asyncio
async def test_async_unload_entry(
    hass: HomeAssistant, mock_config_entry, mock_easy_home_device
) -> None:
    """Test async_unload_entry."""
    mock_easy_home_device.connected = True

    with patch(
        "custom_components.easyathome.coordinator.EasyHomeDevice",
        return_value=mock_easy_home_device,
    ), patch(
        "custom_components.easyathome.coordinator.bluetooth.async_scanner_count",
        return_value=1,
    ):
        mock_config_entry.add_to_hass(hass)
        await hass.config_entries.async_setup(mock_config_entry.entry_id)

        # Unload
        result = await hass.config_entries.async_unload(mock_config_entry.entry_id)
        assert result is True
        mock_easy_home_device.disconnect.assert_called()
