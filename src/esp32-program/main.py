# micropython
from machine import Pin, PWM
import sys
import select
import time
import math

# ===== GPIO 定义 =====
led = PWM(Pin(3), freq=1000)
led.duty(0)
BREATH_MAX = 50  # 30% of 1023
BREATH_MIN = 10  # 10% of 1023

# ===== 状态 =====
STATE_IDLE = 0    # 空闲，灭灯
STATE_WORKING = 1 # 工作中，常亮
STATE_INPUT = 2   # 等待用户输入，闪烁

state = STATE_IDLE

# ===== 非阻塞串口读取 =====
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

# ===== 控制函数 =====
def set_idle():
    global state
    state = STATE_IDLE
    led.duty(0)

def set_working():
    global state
    state = STATE_WORKING

def set_input():
    global state
    state = STATE_INPUT

# ===== 主循环 =====
last_blink = 0
blink_interval = 200  # ms
breath_step = 0.0

while True:
    # 1. 检查串口输入（USB CDC）
    if poll.poll(10):
        cmd = sys.stdin.readline().strip()
        if not cmd:
            continue
        print("RECV:", cmd)

        if cmd == "WORKING":
            set_working()
        elif cmd == "INPUT":
            set_input()
        elif cmd == "IDLE":
            set_idle()

    # 2. 状态驱动
    if state == STATE_WORKING:
        breath_step += 0.1
        duty = int(BREATH_MIN + (math.sin(breath_step) + 1) / 2 * (BREATH_MAX - BREATH_MIN))
        led.duty(duty)
    elif state == STATE_INPUT:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_blink) > blink_interval:
            led.duty(BREATH_MAX if led.duty() == 0 else 0)
            last_blink = now

    time.sleep_ms(10)

