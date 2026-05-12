#!/bin/bash
# CCLight Status Indicator Plugin 安装脚本

set -e

echo "🔧 CCLight Status Indicator Plugin 安装"
echo "========================================"

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

echo "✅ Python 3 已安装"

# 检查 pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ 错误: 未找到 pip"
    echo "请先安装 pip"
    exit 1
fi

echo "✅ pip 已安装"

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install pyserial || pip install pyserial

# 检查 ESP32 设备
echo ""
echo "🔍 检查 ESP32 设备连接..."

python3 -c "
import serial.tools.list_ports
found = False
for p in serial.tools.list_ports.comports():
    if p.vid in (0x10C4, 0x1A86, 0x303A):
        print(f'✅ 找到 ESP32 设备: {p.device}')
        found = True
        break
if not found:
    print('⚠️  警告: 未找到 ESP32 设备')
    print('请确保 ESP32 设备已连接并通过 USB')
"

echo ""
echo "🎉 安装完成！"
echo ""
echo "使用方法:"
echo "1. 确保插件已安装到 Claude Code"
echo "2. 连接 ESP32 设备"
echo "3. 重启 Claude Code"
echo ""
echo "状态说明:"
echo "• 🔴 灭灯 - 空闲状态"
echo "• 🟢 常亮 - 工作中"
echo "• 🟡 闪烁 - 等待用户输入"
echo ""
echo "如需测试，可以运行:"
echo "  python3 cclight.py working"
echo "  python3 cclight.py idle"
echo "  python3 cclight.py input"