"""Easy@Home button platform."""

from __future__ import annotations

from datetime import datetime

from easyathome_ble import EasyHomeDevice

from homeassistant.components.bluetooth import async_ble_device_from_address
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util.dt import now

from .coordinator import EasyHomeConfigEntry
from .entity import EasyHomeEntity

PARALLEL_UPDATES = 1  # One connection at a time


BUTTON_DESCRIPTIONS = (
    ButtonEntityDescription(
        key="sync_time",
        translation_key="sync_time",
        icon="mdi:calendar-clock",
        entity_category=EntityCategory.CONFIG,
    ),
    ButtonEntityDescription(
        key="set_celsius",
        translation_key="set_celsius",
        icon="mdi:temperature-celsius",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EasyHomeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Easy@Home button platform."""
    coordinator = entry.runtime_data
    async_add_entities(
        EasyHomeButtonEntity(coordinator, description)
        for description in BUTTON_DESCRIPTIONS
    )


class EasyHomeButtonEntity(EasyHomeEntity, ButtonEntity):
    """Representation of an Easy@Home button."""

    def __init__(
        self,
        coordinator: EasyHomeConfigEntry,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{self.device_info['connections']}_{description.key}"
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        address = self.coordinator.config_entry.data["address"]
        ble_device = async_ble_device_from_address(
            self.hass, address, connectable=True
        )

        if not ble_device:
            return

        device = EasyHomeDevice(
            address=address,
            notify_callback=lambda _: None,  # No callback needed for commands
            ble_device=ble_device,
        )

        try:
            await device.connect()

            if self.entity_description.key == "sync_time":
                await device.set_datetime(now())
            elif self.entity_description.key == "set_celsius":
                await device.set_unit(celsius=True)

        finally:
            await device.disconnect()
