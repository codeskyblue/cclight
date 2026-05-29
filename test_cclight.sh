#!/bin/bash
# cclight 端到端测试脚本

set -e

CONFIG_DIR="$HOME/.config/cclight"
STATE_FILE="$CONFIG_DIR/state.txt"
STATE_DIR="$HOME/.local/state/cclight"
LOG_FILE="$STATE_DIR/cclight.log"


uv run cclight daemon stop
rm $LOG_FILE
uv run cclight state working
cat $LOG_FIEL
