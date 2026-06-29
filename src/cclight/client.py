"""Client：写入状态文件，自动启动 daemon"""

import os

from cclight.config import CONFIG_DIR, PID_FILE, STATE_FILE
from cclight.daemon import daemon_start
from cclight.pidfile import cleanup_if_stale, is_running, read_pid


def is_daemon_running():
    """检查 daemon 是否在运行"""
    pid, err = read_pid(PID_FILE)
    if pid is None:
        return False
    if not is_running(pid):
        cleanup_if_stale(PID_FILE)
        return False
    return True


def client_run(state, port=None):
    """Client：确保 daemon 在运行，然后写入状态"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(state)

    if not is_daemon_running():
        print("daemon 未运行，正在启动...")
        daemon_start(port=port) # 后面都不会执行了


