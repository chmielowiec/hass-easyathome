# Easy@Home Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/chmielowiec/hass-easyathome.svg)](https://github.com/chmielowiec/hass-easyathome/releases)

Home Assistant integration for Easy@Home Bluetooth devices.

## Supported Devices

- **EBT-300**: Basal body temperature thermometer for fertility tracking

## Features

- ✅ Automatic Bluetooth discovery via service UUID
- ✅ Real-time temperature measurements
- ✅ Timestamped readings
- ✅ Historical data support  
- ✅ Time synchronization button
- ✅ Temperature unit configuration button
- ✅ Sensor state restoration after restart

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/chmielowiec/hass-easyathome`
6. Select category: "Integration"
7. Click "Add"
8. Find "Easy@Home" in the integration list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/easyathome` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

### Automatic Discovery

The integration will automatically discover Easy@Home EBT-300 devices via Bluetooth.

1. Ensure Bluetooth is enabled on your Home Assistant device
2. Turn on your EBT-300 thermometer
3. Go to **Settings** → **Devices & Services**
4. Click **Add Integration**
5. Search for "Easy@Home"
6. Follow the configuration wizard

### Device Requirements

- Bluetooth Low Energy (BLE) capable Home Assistant host
- EBT-300 thermometer within Bluetooth range
- Working Bluetooth adapter

## Entities

### Sensor

- **Temperature**: Current temperature reading in Celsius
  - Attributes:
    - `measurement_time`: Timestamp of the measurement
    - `is_live_reading`: Whether this is a live vs historical reading

### Buttons

- **Sync time**: Synchronize device time with Home Assistant
- **Set celsius**: Set temperature unit to Celsius

## Usage

Once configured, the integration will:

1. Automatically connect to your EBT-300 device
2. Receive temperature notifications in real-time
3. Display current temperature and measurement time
4. Maintain connection and reconnect if necessary
5. Restore last known state after Home Assistant restart

## Troubleshooting

### Device Not Discovered

- Ensure the EBT-300 is powered on and within range
- Check that Bluetooth is enabled on your Home Assistant device
- Verify no other apps are connected to the device
- Try restarting the thermometer

### Connection Issues

- The device uses an active BLE connection (not passive)
- Only one connection at a time is supported
- If connection fails, the integration will retry automatically
- Check Home Assistant logs for detailed error messages

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.easyathome: debug
    easyathome_ble: debug
```

## Development

### Library

This integration uses the [easyathome-ble](https://github.com/chmielowiec/easyathome-ble) library.

### Contributing

Contributions are welcome! Please open an issue or pull request.

## License

MIT License - see LICENSE file

## Credits

- Developed by Robert Chmielowiec
- Uses [bleak](https://github.com/hbldh/bleak) for Bluetooth communication
- Inspired by the Home Assistant probe_plus integration

## Support

- [Report Issues](https://github.com/chmielowiec/hass-easyathome/issues)
- [Home Assistant Community](https://community.home-assistant.io/)

---

## Disclaimer

This is not an official Easy@Home product. Easy@Home is a trademark of its respective owner.
