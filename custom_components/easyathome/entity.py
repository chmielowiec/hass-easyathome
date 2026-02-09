"""Easy@Home base entity type."""

from homeassistant.const import CONF_ADDRESS
from homeassistant.helpers.device_registry import (
    CONNECTION_BLUETOOTH,
    DeviceInfo,
    format_mac,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EasyHomeDataUpdateCoordinator


class EasyHomeEntity(CoordinatorEntity[EasyHomeDataUpdateCoordinator]):
    """Base class for Easy@Home entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: EasyHomeDataUpdateCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)

        address = coordinator.config_entry.data[CONF_ADDRESS]
        normalized_address = format_mac(address)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, normalized_address)},
            name="Easy@Home EBT-300",
            manufacturer="Easy@Home",
            model="EBT-300",
            connections={(CONNECTION_BLUETOOTH, address)},
        )
        self._normalized_address = normalized_address

    @property
    def available(self) -> bool:
        """Return True if the entity is available."""
        return super().available and self.coordinator.device.connected
