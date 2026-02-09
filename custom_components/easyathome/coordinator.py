"""Coordinator for the easyathome integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import TypeAlias

from easyathome_ble import EasyHomeDevice, TemperatureMeasurement
from bleak.exc import BleakError

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import DOMAIN

EasyHomeConfigEntry: TypeAlias = ConfigEntry

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=30)


class EasyHomeDataUpdateCoordinator(DataUpdateCoordinator[TemperatureMeasurement | None]):
    """Coordinator to manage data updates for Easy@Home device.

    This class handles the communication with Easy@Home EBT-300 thermometer.
    Data is updated via GATT notifications from the device.
    """

    config_entry: EasyHomeConfigEntry

    def __init__(self, hass: HomeAssistant, entry: EasyHomeConfigEntry) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="EasyHomeDataUpdateCoordinator",
            update_interval=SCAN_INTERVAL,
            config_entry=entry,
        )

        available_scanners = bluetooth.async_scanner_count(hass, connectable=True)

        if available_scanners == 0:
            raise ConfigEntryNotReady(
                translation_domain=DOMAIN,
                translation_key="no_bleak_scanner",
            )

        self.device = EasyHomeDevice(
            address=entry.data[CONF_ADDRESS],
            notify_callback=self._handle_notification,
        )

    def _handle_notification(self, measurement: TemperatureMeasurement) -> None:
        """Handle temperature notification from device.

        Args:
            measurement: Temperature measurement from device

        """
        _LOGGER.debug(
            "Received temperature: %.2f°C at %s (live=%s)",
            measurement.temperature,
            measurement.timestamp,
            measurement.is_live,
        )
        self.async_set_updated_data(measurement)

    async def _async_update_data(self) -> TemperatureMeasurement | None:
        """Connect to the Easy@Home device on a set interval.

        This method is called periodically to maintain connection.
        Data updates are handled by notifications via _handle_notification.
        """
        # Already connected, data comes via notifications
        if self.device.connected:
            return self.data

        # Device not connected, try to connect
        ble_device = bluetooth.async_ble_device_from_address(
            self.hass, self.config_entry.data[CONF_ADDRESS], connectable=True
        )

        if not ble_device:
            _LOGGER.debug(
                "Could not find BLE device: %s",
                self.config_entry.data[CONF_ADDRESS],
            )
            self.device.device_disconnected_handler(notify=False)
            return self.data

        self.device.update_ble_device(ble_device)

        try:
            await self.device.connect()
            _LOGGER.info(
                "Connected to Easy@Home device: %s",
                self.config_entry.data[CONF_ADDRESS],
            )
            # Refresh device clock to Home Assistant time via custom service
            try:
                await self.device.set_datetime(dt_util.now())
            except (BleakError, ValueError) as err:
                _LOGGER.debug("Failed to sync device time: %s", err)
        except (BleakError, TimeoutError) as ex:
            _LOGGER.debug(
                "Could not connect to Easy@Home device: %s, Error: %s",
                self.config_entry.data[CONF_ADDRESS],
                ex,
            )
            self.device.device_disconnected_handler(notify=False)

        return self.data

    async def async_shutdown(self) -> None:
        """Shutdown coordinator and disconnect device."""
        if self.device.connected:
            await self.device.disconnect()
