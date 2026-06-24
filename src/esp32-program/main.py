# micropython
from machine import Pin
import sys
import select
import time

# ===== GPIO 定义 =====
led = Pin(8, Pin.OUT, value=1)   # 低电平触发，初始高电平=灭
led2 = Pin(3, Pin.OUT, value=1)  # 低电平触发，初始高电平=灭

def set_leds(on: bool):
    """同时设置两个 LED：True=亮，False=灭"""
    led.value(0 if on else 1)
    led2.value(0 if on else 1)

def toggle_leds():
    """同时反转两个 LED 的状态"""
    v = led.value()
    led.value(not v)
    led2.value(not v)

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
    set_leds(False)  # 灭

def set_working():
    global state
    state = STATE_WORKING

def set_input():
    global state
    state = STATE_INPUT

# ===== 主循环 =====
last_blink = 0
blink_interval = 200  # ms

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
        set_leds(True)  # 亮
    elif state == STATE_INPUT:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_blink) > blink_interval:
            toggle_leds()
            last_blink = now

    time.sleep_ms(10)

