"""Tests for Easy@Home config flow."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from custom_components.easyathome.config_flow import EasyHomeConfigFlow
from custom_components.easyathome.const import DOMAIN


@pytest.mark.asyncio
async def test_bluetooth_discovery_flow(
    hass: HomeAssistant, discovery_info: dict
) -> None:
    """Test Bluetooth discovery flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=discovery_info,
    )

    assert result["type"] == FlowResult.FORM
    assert result["step_id"] == "bluetooth_confirm"
    assert result["data_schema"] is not None


@pytest.mark.asyncio
async def test_user_flow(hass: HomeAssistant, discovery_info: dict) -> None:
    """Test user initiated flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == FlowResult.FORM
    assert result["step_id"] == "user"


@pytest.mark.asyncio
async def test_flow_duplicate_abort(
    hass: HomeAssistant, discovery_info: dict
) -> None:
    """Test flow aborts for duplicate device."""
    with patch(
        "custom_components.easyathome.config_flow.EasyHomeConfigFlow._test_connection",
        return_value=True,
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

        assert result["type"] == FlowResult.ABORT
        assert result["reason"] == "already_configured"


@pytest.mark.asyncio
async def test_flow_entry_created(hass: HomeAssistant, discovery_info: dict) -> None:
    """Test flow creates config entry."""
    with patch(
        "custom_components.easyathome.config_flow.EasyHomeConfigFlow._test_connection",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=discovery_info,
        )

        assert result["type"] == FlowResult.FORM

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )

        assert result["type"] == FlowResult.CREATE_ENTRY
        assert result["title"] == "EBT-300 AA:BB:CC:DD:EE:FF"
        assert result["data"]["address"] == "AA:BB:CC:DD:EE:FF"
