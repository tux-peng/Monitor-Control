Monitor Control (DDC/CI)
A lightweight Python GUI to control monitor hardware settings like Brightness and Contrast using ddcutil. This project includes two versions: a modern PyQt6 interface and a lightweight Tkinter interface.

Features
Multi-Monitor Support: Automatically detects and switches between multiple displays.

Hardware-Level Control: Communicates directly with monitor hardware via I2C (DDC/CI).

No Sudo Required: Once configured, you can adjust settings without root privileges.

Bi-directional Sync: Reads current hardware values on startup.

Prerequisites
1. Install System Dependencies (Arch Linux)
Bash

sudo pacman -S ddcutil i2c-tools python-pyqt6
2. Configure Permissions (Crucial)
To run these scripts without sudo, your user must have access to the I2C bus:

Add your user to the i2c group:

Bash

sudo usermod -aG i2c $USER
Load the i2c-dev module:

Bash

sudo modprobe i2c-dev
To make this permanent, create /etc/modules-load.d/i2c.conf and add i2c-dev inside.

Reboot or Log out/in for group changes to take effect.

Usage
PyQt6 Version (Recommended)
Offers a modern look and feel with responsive sliders.

Bash

python_monitor_control_qt.py
Tkinter Version
A zero-dependency, lightweight alternative.

Bash

python monitor_control_tk.py
Troubleshooting
"No monitors detected": Ensure your monitor supports DDC/CI and that it is enabled in the monitor's Physical OSD (On-Screen Display) menu.

Permission Denied: Double-check that your user is in the i2c group by running the groups command.

Slow Response: DDC/CI is a serial protocol; it is normal for hardware updates to take ~0.5 seconds.

License
MIT
