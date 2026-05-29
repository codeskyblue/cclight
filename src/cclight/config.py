"""路径常量（XDG 规范）"""

import os

VALID_STATES = ("idle", "working", "input")

CONFIG_DIR = os.path.join(
    os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
    "cclight",
)
STATE_FILE = os.path.join(CONFIG_DIR, "state.txt")

STATE_DIR = os.path.join(
    os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state")),
    "cclight",
)
PID_FILE = os.path.join(STATE_DIR, "cclight.pid")
LOG_FILE = os.path.join(STATE_DIR, "cclight.log")

POLL_INTERVAL = 0.2  # seconds
