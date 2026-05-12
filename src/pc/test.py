import argparse
import serial
import serial.tools.list_ports
import time

VALID_COMMANDS = ("IDLE", "WORKING", "INPUT")

def find_esp32():
    for p in serial.tools.list_ports.comports():
        if p.vid in (0x10C4, 0x1A86, 0x303A):
            return p.device
    return None

parser = argparse.ArgumentParser(description="ESP32 状态控制")
parser.add_argument("state", choices=[c.lower() for c in VALID_COMMANDS],
                    help="要切换的状态: idle, working, input")
args = parser.parse_args()

port = find_esp32()
if not port:
    print("未找到 ESP32 设备")
    exit(1)

print(f"连接: {port}")
ser = serial.Serial(port, 115200)
time.sleep(2)

cmd = args.state.upper()
ser.write((cmd + '\n').encode())
print(f"已发送: {cmd}")
ser.close()
