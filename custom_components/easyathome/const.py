"""Constants for the Easy@Home integration."""

DOMAIN = "easyathome"

# Primary custom service/characteristics used by the device
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_WRITE_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_NOTIFY_UUID = "0000ffe2-0000-1000-8000-00805f9b34fb"

# Discovery helpers: device advertises standard 0x1809 and 0xFef5 plus its
# custom service; we match any of them and optionally filter by name.
DISCOVERY_SERVICE_UUIDS = {
	SERVICE_UUID,
	"00001809-0000-1000-8000-00805f9b34fb",
	"0000fef5-0000-1000-8000-00805f9b34fb",
}

# Device advertises as yuncheng_a33 per captured data
DISCOVERY_NAMES = {"yuncheng_a33"}
