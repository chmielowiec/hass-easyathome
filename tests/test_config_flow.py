"""Tests for Easy@Home config flow."""

import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.easyathome.config_flow import EasyHomeConfigFlow
from custom_components.easyathome.const import DOMAIN

# Skip all config flow tests on macOS since bluetooth component requires Linux DBus
pytestmark = pytest.mark.skipif(
    sys.platform == "darwin",
    reason="Bluetooth component requires DBus (Linux only)",
)


@pytest.mark.asyncio
async def test_bluetooth_discovery_flow(
    hass: HomeAssistant, discovery_info: BluetoothServiceInfoBleak
) -> None:
    """Test Bluetooth discovery flow."""
    # Mock bluetooth component being loaded
    with patch(
        "custom_components.easyathome.config_flow.async_discovered_service_info",
        return_value=[discovery_info],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=discovery_info,
        )

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "bluetooth_confirm"


@pytest.mark.asyncio
async def test_user_flow(
    hass: HomeAssistant, discovery_info: BluetoothServiceInfoBleak
) -> None:
    """Test user initiated flow."""
    with patch(
        "custom_components.easyathome.config_flow.async_discovered_service_info",
        return_value=[discovery_info],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "user"


@pytest.mark.asyncio
async def test_flow_duplicate_abort(
    hass: HomeAssistant, discovery_info: BluetoothServiceInfoBleak
) -> None:
    """Test flow aborts for duplicate device."""
    with patch(
        "custom_components.easyathome.config_flow.async_discovered_service_info",
        return_value=[discovery_info],
    ):
        # Create first entry
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=discovery_info,
        )

        await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
        await hass.async_block_till_done()

        # Try to create duplicate
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=discovery_info,
        )

        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "already_configured"


@pytest.mark.asyncio
async def test_flow_entry_created(
    hass: HomeAssistant, discovery_info: BluetoothServiceInfoBleak
) -> None:
    """Test flow creates config entry."""
    with patch(
        "custom_components.easyathome.config_flow.async_discovered_service_info",
        return_value=[discovery_info],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=discovery_info,
        )

        assert result["type"] == FlowResultType.FORM

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )

        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert "Easy@Home" in result["title"]
        assert result["data"]["address"] == "AA:BB:CC:DD:EE:FF"
