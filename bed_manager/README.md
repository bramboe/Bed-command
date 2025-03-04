# Bed Manager for Home Assistant

A Home Assistant integration for managing your Octo Bed with ESPHome.

## Features

- Control head and feet positions (0-100%)
- Calibration support for both head and feet sections
- Movement state tracking
- Diagnostic information
- Easy configuration through Home Assistant UI

## Installation

1. Copy the `bed_manager` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Go to Settings > Devices & Services > Add Integration
4. Search for "Bed Manager"
5. Follow the configuration wizard

## Configuration

The integration requires the following information:
- Name: A friendly name for your bed
- MAC Address: The MAC address of your ESPHome device
- Device Name: The name of your bed (defaults to "RC2")
- PIN: The PIN code for your bed (if required)

## Services

### Set Head Position
```yaml
service: bed_manager.set_bed_head_position
data:
  entity_id: cover.your_bed_head
  position: 50  # 0-100%
```

### Set Feet Position
```yaml
service: bed_manager.set_bed_feet_position
data:
  entity_id: cover.your_bed_feet
  position: 50  # 0-100%
```

### Calibrate
```yaml
service: bed_manager.calibrate
data:
  entity_id: cover.your_bed_head
  calibration_mode: 1  # 0=none, 1=head, 2=feet
```

### Diagnostics
```yaml
service: bed_manager.diagnostics
data:
  entity_id: cover.your_bed_head
```

## Troubleshooting

1. Check the Home Assistant logs for any error messages
2. Verify your ESPHome device is online and accessible
3. Ensure the MAC address and PIN are correct
4. Try restarting Home Assistant if the integration stops working

## Support

For issues and feature requests, please create an issue in the GitHub repository. 