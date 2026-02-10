# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-08

### Added
- Initial release
- Support for Easy@Home EBT-300 basal body temperature thermometer
- Automatic Bluetooth discovery via service UUID
- Real-time temperature measurements via GATT notifications
- Temperature sensor with measurement time and live/historical indicator
- Sync time button for device time synchronization
- Set celsius button for temperature unit configuration
- Config flow for easy setup
- Sensor state restoration after restart
- Active BLE connection management with automatic reconnection

### Features
- Bluetooth discovery by service UUID `0000ffe0-0000-1000-8000-00805f9b34fb`
- Temperature readings in Celsius with 0.01°C precision
- Timestamped measurements
- Distinction between live and historical readings
- Device info with manufacturer, model, and connections
- Entity translations
- HACS integration

[0.1.0]: https://github.com/chmielowiec/hass-easyathome/releases/tag/v0.1.0

## [0.1.1] - 2026-02-10

### Fixed
- Update easyathome-ble dependency to 0.2.1
- Improve Bluetooth discovery matching for the device
- Keep the last measurement available after device power-off

[0.1.1]: https://github.com/chmielowiec/hass-easyathome/releases/tag/v0.1.1
