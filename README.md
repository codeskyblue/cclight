# CCLight Status Indicator Plugin

> 通过 ESP32 LED 灯光显示 Claude Code 的工作状态

## 准备硬件

- 硬件代码在 src/esp32-program中可以找到。找台ESP32-C3的板子，刷micropython，然后将main.py刷到板子上。 LED灯负极接GND，正极接Pin(3)
- 电脑通过USB先直连ESP32-C3的板子

## 软件安装

### 1: 安装LED控制程序

```bash
# 使用 pip 或 pipx, 需要Python版本大于3.8
pip install cclight
# pipx install cclight
```

### 2：安装插件到Claude Code

```bash
# 国内
claude plugin marketplace add git@gitee.com:shxsun/cclight.git
claude plugin install cclight@cclight-marketplace

# 国外
claude plugin marketplace add codeskyblue/cclight
claude plugin install cclight@cclight-marketplace
```

## 测试

安装后 `cclight` 命令即可使用：

```bash
# 启动 daemon（首次使用会自动启动）
cclight state working
cclight state idle
cclight state input

# 手动管理 daemon
cclight daemon start
cclight daemon stop
cclight daemon status
```

> **开发调试？** 查看 [DEVELOP.md](DEVELOP.md) 了解本地开发和调试方法。

# 参考文档

- 创建marketplace: https://code.claude.com/docs/zh-CN/plugin-marketplaces#create-the-marketplace-file
- plugins参考: https://code.claude.com/docs/zh-CN/plugins-reference
- 类似项目: https://github.com/bobek-balinek/claude-lamp
