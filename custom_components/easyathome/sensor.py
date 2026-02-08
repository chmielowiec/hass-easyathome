"""Support for Easy@Home BLE sensors."""

from __future__ import annotations

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import EasyHomeConfigEntry
from .entity import EasyHomeEntity

# Coordinator handles updates
PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EasyHomeConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Easy@Home sensors."""
    coordinator = entry.runtime_data
    async_add_entities([EasyHomeTemperatureSensor(coordinator)])


class EasyHomeTemperatureSensor(EasyHomeEntity, RestoreSensor, SensorEntity):
    """Representation of an Easy@Home temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "temperature"

    def __init__(self, coordinator: EasyHomeConfigEntry) -> None:
        """Initialize the temperature sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self.device_info['connections']}_temperature"

    @property
    def native_value(self) -> float | None:
        """Return the temperature value."""
        if self.coordinator.data:
            return self.coordinator.data.temperature
        return None

    @property
    def extra_state_attributes(self) -> dict[str, str | bool] | None:
        """Return extra state attributes."""
        if not self.coordinator.data:
            return None

        return {
            "measurement_time": self.coordinator.data.timestamp.isoformat(),
            "is_live_reading": self.coordinator.data.is_live,
        }

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()

        # Restore last sensor data if available
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            self._attr_native_value = last_sensor_data.native_value
