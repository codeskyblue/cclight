import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)

time.sleep(2)  # 等设备准备好

ser.write(b'RUNNING\n')
time.sleep(3)

ser.write(b'WAIT\n')
time.sleep(5)

ser.write(b'DONE\n')
