# CCLight Status Indicator Plugin

> 🚨 通过 ESP32 LED 灯光显示 Claude Code 的工作状态

# 安装方法

## 从 GitHub 安装

```bash
# 1. 添加 GitHub marketplace
/plugin marketplace add codeskyblue/esp32-claude-status

# 2. 安装插件
/plugin install cclight-status-indicator@cclight-marketplace
```

> 💡 **开发调试？** 查看 [DEVELOP.md](DEVELOP.md) 了解本地开发和调试方法。

## 验证安装

安装成功后，在 Claude Code 中运行：

```bash
/plugin list
```

应该能看到 `cclight-status-indicator` 已启用。

# 参考文档

- 创建marketplace: https://code.claude.com/docs/zh-CN/plugin-marketplaces#create-the-marketplace-file
- plugins参考: https://code.claude.com/docs/zh-CN/plugins-reference
- 类似项目: https://github.com/bobek-balinek/claude-lamp
