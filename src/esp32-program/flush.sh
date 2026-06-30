#!/bin/bash
#

set -e

export PYENV_VERSION=3.10
USBPORT=$(ls -1 /dev/tty.usb*)
esptool.py --port $USBPORT erase_flash

# From then on program the firmware starting at address 0x0:
esptool.py --port $USBPORT write_flash -z 0x0 ESP32_GENERIC_C3-20240222-v1.22.2.bin

mpremote cp main.py :
