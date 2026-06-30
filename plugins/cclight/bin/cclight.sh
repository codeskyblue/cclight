#!/bin/bash
set -e
if ! command -v cclight &>/dev/null; then
    echo "cclight not found, installing via pip3..."
    pip3 install cclight
fi
exec cclight "$@"
