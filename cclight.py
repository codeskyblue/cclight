#!/usr/bin/env python3
"""
CCLight Status Indicator Plugin
控制 ESP32 设备上的 LED 灯光来显示 Claude Code 的工作状态
"""

import argparse
import serial
import serial.tools.list_ports
import time
import logging
import os
import sys

# 配置日志
logger = logging.getLogger(__name__)

VALID_COMMANDS = ("IDLE", "WORKING", "INPUT")

def find_esp32():
    """查找连接的 ESP32 设备"""
    for p in serial.tools.list_ports.comports():
        # 常见的 ESP32 开发板 Vendor IDs
        if p.vid in (0x10C4, 0x1A86, 0x303A):
            return p.device
    return None

def send_command(command: str, port: str = None):
    """发送命令到 ESP32 设备"""
    if not command.upper() in VALID_COMMANDS:
        logger.error(f"无效的命令: {command}")
        return False

    # 如果没有指定端口，自动查找
    if not port:
        port = find_esp32()
        if not port:
            logger.warning("未找到 ESP32 设备，命令将被忽略")
            return False

    try:
        logger.info(f"连接到: {port}")
        ser = serial.Serial(port, 115200)
        time.sleep(0.1)  # 等待连接稳定

        cmd = command.upper()
        ser.write((cmd + '\n').encode())
        logger.info(f"已发送命令: {cmd}")
        ser.close()
        return True
    except serial.SerialException as e:
        logger.error(f"串口通信错误: {e}")
        return False
    except Exception as e:
        logger.error(f"发送命令时发生错误: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="CCLight 状态指示器控制")
    parser.add_argument("state",
                       choices=[c.lower() for c in VALID_COMMANDS],
                       help="要切换的状态: idle, working, input")
    parser.add_argument("--port",
                       help="指定串口设备（可选）")
    parser.add_argument("--verbose", "-v",
                       action="store_true",
                       help="显示详细日志")

    args = parser.parse_args()

    # 配置日志级别
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

    # 发送命令
    success = send_command(args.state, args.port)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()