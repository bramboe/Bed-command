"""Constants for the Bed Manager integration."""
from typing import Final

DOMAIN: Final = "bed_manager"

# Configuration
CONF_BED_TYPE: Final = "bed_type"
CONF_MAC_ADDRESS: Final = "mac_address"
CONF_NAME: Final = "name"
CONF_DEVICE_NAME: Final = "device_name"
CONF_TARGET_MAC: Final = "target_mac"
CONF_STORED_PIN: Final = "stored_pin"

# Bed Types
BED_TYPES: Final = ["octo_bed"]

# Services
SERVICE_SET_HEAD_POSITION: Final = "set_bed_head_position"
SERVICE_SET_FEET_POSITION: Final = "set_bed_feet_position"
SERVICE_CALIBRATE: Final = "calibrate"
SERVICE_DIAGNOSTICS: Final = "diagnostics"

# Attributes
ATTR_POSITION: Final = "position"
ATTR_HEAD_POSITION: Final = "head_position"
ATTR_FEET_POSITION: Final = "feet_position"
ATTR_CALIBRATION_MODE: Final = "calibration_mode"
ATTR_MOVEMENT_TYPE: Final = "movement_type"

# Movement Types
MOVEMENT_TYPES: Final = {
    0: "no_movement",
    1: "head_up",
    2: "head_down",
    3: "feet_up",
    4: "feet_down",
    5: "both_up",
    6: "both_down"
}

# Default Values
DEFAULT_HEAD_DURATION: Final = 30000  # 30 seconds in ms
DEFAULT_FEET_DURATION: Final = 30000  # 30 seconds in ms
DEFAULT_DEVICE_NAME: Final = "RC2"

# Logging
LOG_LEVEL: Final = "DEBUG"
LOG_FORMAT: Final = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 