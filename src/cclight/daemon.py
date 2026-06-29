"""Daemon 进程管理"""

import logging
import os
import signal
import sys
import time

import serial

from cclight.config import (
    CONFIG_DIR,
    LOG_FILE,
    PID_FILE,
    POLL_INTERVAL,
    STATE_DIR,
    STATE_FILE,
    VALID_STATES,
)
from cclight.pidfile import cleanup_if_stale, is_running, read_pid
from cclight.serial_device import find_esp32, send_serial


def daemon_loop(port=None, logger=None):
    """Daemon 主循环：轮询 state.txt，变化时发送串口命令"""
    if logger is None:
        logger = logging.getLogger("cclight.daemon")

    current_state = None
    ser = None
    stop_flag = False

    def handle_stop(signum, frame):
        nonlocal stop_flag
        stop_flag = True
        logger.info("收到停止信号")

    # 注册 SIGTERM 信号处理函数
    signal.signal(signal.SIGTERM, handle_stop)

    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w") as f:
            f.write("idle")

    while True:
        try:
            with open(STATE_FILE, "r") as f:
                state = f.read().strip().lower()

            if state not in VALID_STATES:
                state = "idle"

            if state != current_state:
                target_port = port or find_esp32()
                if target_port:
                    try:
                        if ser and ser.is_open:
                            ser.close()
                        ser = send_serial(target_port, state)
                        logger.info(
                            "状态变更: %s -> %s (port=%s)",
                            current_state,
                            state,
                            target_port,
                        )
                    except serial.SerialException as e:
                        logger.warning("串口错误: %s", e)
                        ser = None
                else:
                    logger.debug("未找到 ESP32 设备，跳过发送")
                current_state = state

        except FileNotFoundError:
            logger.debug("state.txt 不存在，等待...")
        except Exception as e:
            logger.error("daemon 循环异常: %s", e)

        if stop_flag:
            if current_state == "idle":
                logger.info("当前状态已是 idle，准备退出")
                break
            else:
                with open(STATE_FILE, "w") as f:
                    f.write("idle")

        time.sleep(POLL_INTERVAL)

    # 退出前清理
    if ser and ser.is_open:
        ser.close()
    logger.info("daemon 循环退出")


def daemon_start(port=None, fg=False):
    """启动 daemon 进程"""
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(CONFIG_DIR, exist_ok=True)

    if fg:
        logger = logging.getLogger("cclight.daemon")
        logger.info("daemon 前台启动")
        try:
            daemon_loop(port=port, logger=logger)
        except KeyboardInterrupt:
            logger.info("daemon 停止")
        return

    if not cleanup_if_stale(PID_FILE):
        print("daemon 已在运行")
        raise SystemExit(1)

    import daemon
    import daemon.pidfile

    log_fp = open(LOG_FILE, "a+")

    ctx = daemon.DaemonContext(
        pidfile=daemon.pidfile.TimeoutPIDLockFile(PID_FILE),
        stdout=log_fp,
        stderr=log_fp,
        signal_map={
            signal.SIGTERM: lambda signum, frame: sys.exit(0),
        },
    )

    with ctx:
        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s"))
        logger = logging.getLogger("cclight.daemon")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
        logger.info("daemon 启动, pid=%d", os.getpid())
        daemon_loop(port=port, logger=logger)


def daemon_stop():
    """停止 daemon 进程"""
    pid, err = read_pid(PID_FILE)
    if err:
        print("daemon 未运行（{}）".format(err))
        return False

    if not is_running(pid):
        cleanup_if_stale(PID_FILE)
        print("daemon 未运行（进程不存在），已清理 PID 文件")
        return False

    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        print("无法向 daemon (pid={}) 发送信号".format(pid))
        return False

    for _ in range(50):
        if not is_running(pid):
            break
        time.sleep(0.1)
    else:
        print("警告: daemon (pid={}) 未在 5s 内退出".format(pid))
        return False
    print("daemon 已停止 (pid={})".format(pid))
    return True


def daemon_status():
    """查看 daemon 状态"""
    pid, err = read_pid(PID_FILE)
    if err:
        if err == "PID 文件不存在":
            print("daemon 未运行")
        else:
            print("daemon 未运行（PID 文件无效）")
        return False

    if not is_running(pid):
        cleanup_if_stale(PID_FILE)
        print("daemon 未运行（pid={} 进程不存在）".format(pid))
        return False

    print("daemon 运行中 (pid={})".format(pid))
    try:
        with open(STATE_FILE, "r") as f:
            state = f.read().strip()
        print("当前状态: {}".format(state))
    except FileNotFoundError:
        print("当前状态: (state.txt 不存在)")
    return True
