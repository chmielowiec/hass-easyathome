# Easy@Home for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/chmielowiec/hass-easyathome.svg)](https://github.com/chmielowiec/hass-easyathome/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Home Assistant integration for the [Easy@Home EBT-300](https://www.easy-home.com/) basal body temperature thermometer, built on top of the [easyathome-ble](https://github.com/chmielowiec/easyathome-ble) library.

## Supported devices

| Device  | Description                                             |
| ------- | ------------------------------------------------------- |
| EBT-300 | Basal body temperature thermometer (fertility tracking) |

## Features

- Automatic Bluetooth discovery (no manual address entry needed)
- Real-time temperature pushed via BLE GATT notifications
- Measurement timestamp and live/historical reading flag exposed as attributes
- Last known state restored after Home Assistant restart
- Requires Home Assistant 2024.1+

## Installation

### HACS (recommended)

1. In Home Assistant, open **HACS → Integrations**
2. Click the three-dot menu → **Custom repositories**
3. Add `https://github.com/chmielowiec/hass-easyathome` with category **Integration**
4. Search for **Easy@Home** and click **Download**
5. Restart Home Assistant

### Manual

1. Copy `custom_components/easyathome/` into your Home Assistant `custom_components/` directory
2. Restart Home Assistant

## Setup

The integration discovers the EBT-300 automatically via Bluetooth once Home Assistant detects it.

1. Power on the EBT-300 and bring it within Bluetooth range
2. Go to **Settings → Devices & Services**
3. The device will appear as a discovered integration — click **Configure** and confirm

Alternatively, click **Add Integration**, search for **Easy@Home**, and select the device from the list.

**Requirements:**
- Home Assistant host with a Bluetooth Low Energy (BLE) adapter
- No other app connected to the device at setup time

## Entities

### Sensor

| Entity      | Unit | Description                 |
| ----------- | ---- | --------------------------- |
| Temperature | °C   | Current temperature reading |

**Attributes:**

| Attribute          | Type               | Description                                                         |
| ------------------ | ------------------ | ------------------------------------------------------------------- |
| `measurement_time` | ISO 8601 timestamp | Time of the measurement                                             |
| `is_live_reading`  | boolean            | `true` for real-time readings, `false` for recalled historical data |

## Troubleshooting

### Device not discovered

- Confirm the EBT-300 is powered on and within range
- Ensure no other app (e.g. the official Easy@Home app) is connected to the device
- Check that your Home Assistant host has a working Bluetooth adapter
- Restart the thermometer and wait 30 seconds

### No sensor data after setup

- The device sends data via BLE notifications; the integration connects and waits for the device to push a reading
- Data is only pushed when a measurement is taken on the device
- Check logs for connection errors (see debug logging below)

### Enable debug logging

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.easyathome: debug
    easyathome_ble: debug
```

## Development

### Architecture

The integration uses a `DataUpdateCoordinator` that maintains a persistent BLE connection to the device. Temperature data arrives asynchronously through GATT notifications rather than being polled. A periodic update cycle (every 30 s) reconnects the device if the connection drops.

```
Home Assistant
└── EasyHomeDataUpdateCoordinator  (manages BLE connection)
    └── EasyHomeDevice             (easyathome-ble library)
        └── BLE GATT notifications → temperature readings
```

### Running tests

```bash
pip install -r requirements_test.txt
pytest tests/
```

### Contributing

Contributions are welcome — please open an issue or pull request on GitHub.

## License

MIT — see [LICENSE](LICENSE) for details.

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by Easy@Home. Easy@Home is a trademark of its respective owner.
