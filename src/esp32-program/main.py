from machine import Pin
import sys
import select
import time

# ===== GPIO 定义 =====
green_led = Pin(2, Pin.OUT)
red_led = Pin(3, Pin.OUT)

# ===== 状态 =====
STATE_IDLE = 0
STATE_RUNNING = 1
STATE_WAIT = 2

state = STATE_IDLE

# ===== 非阻塞串口读取 =====
poll = select.poll()
poll.register(sys.stdin, select.POLLIN)

# ===== 控制函数 =====
def set_running():
    global state
    state = STATE_RUNNING
    green_led.on()
    red_led.off()

def set_wait():
    global state
    state = STATE_WAIT
    green_led.off()

def set_done():
    global state
    state = STATE_IDLE
    green_led.off()
    red_led.off()

# ===== 主循环 =====
last_blink = 0
blink_interval = 500  # ms

while True:
    # 1. 检查串口输入（USB CDC）
    if poll.poll(10):
        cmd = sys.stdin.readline().strip()

        if cmd == "RUNNING":
            set_running()
        elif cmd == "WAIT":
            set_wait()
        elif cmd == "DONE":
            set_done()

    # 2. 状态驱动
    if state == STATE_WAIT:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_blink) > blink_interval:
            red_led.value(not red_led.value())
            last_blink = now

    time.sleep_ms(10)
