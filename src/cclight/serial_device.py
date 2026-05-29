"""ESP32 串口通信"""

import time

import serial
import serial.tools.list_ports


def find_esp32():
    """查找连接的 ESP32 设备"""
    for p in serial.tools.list_ports.comports():
        if p.vid in (0x10C4, 0x1A86, 0x303A):
            return p.device
    return None


def send_serial(port, command):
    """通过串口发送命令"""
    ser = serial.Serial(port, 115200)
    time.sleep(0.1)
    ser.write((command.upper() + "\n").encode())
    return ser
