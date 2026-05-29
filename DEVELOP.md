# 开发调试指南

本文档介绍如何本地开发和调试 CCLight Status Indicator Plugin。

## 环境准备

### 使用 uv（推荐）

```bash
# 安装依赖
uv sync

# 运行 cclight
uv run cclight daemon status
```

### 使用 pip

```bash
# 安装依赖
pip install -e .

# 运行 cclight
cclight daemon status
```

## 本地安装

### 1. 添加本地 marketplace

在 Claude Code 中运行：

```bash
/plugin marketplace add ./
```

这将把当前目录作为 marketplace 添加到 Claude Code。

### 2. 安装插件

```bash
/plugin install cclight@cclight-marketplace
```

### 3. 验证安装

```bash
/plugin list
```

应该能看到 `cclight` 已启用。

## 开发调试流程

### 实时重载插件

修改代码后，重新加载插件：

```bash
/reload-plugins
```

### 查看插件详情

```bash
/plugin details cclight@cclight-marketplace
```

这会显示插件的所有组件（skills、agents、hooks 等）。

### 验证插件配置

```bash
/plugin validate ./
```

检查 `plugin.json`、`marketplace.json` 和组件配置是否符合规范。

### 调试模式

启动 Claude Code 时使用 `--debug` 参数查看详细的插件加载信息：

```bash
claude --debug
```

这会显示：
- 正在加载哪些插件
- 插件清单中的任何错误
- Skill、agent 和 hook 注册
- MCP server 初始化

## 开发最佳实践

### 1. 文件结构

确保项目结构符合规范：

```
cclight/
├── .claude-plugin/
│   ├── plugin.json          # 插件清单
│   └── marketplace.json      # Marketplace 配置
├── hooks/                    # Hook 配置
│   └── hooks.json
├── src/
│   ├── cclight/              # Python 包
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── config.py
│   │   ├── daemon.py
│   │   ├── client.py
│   │   └── serial_device.py
│   └── esp32-program/        # ESP32 固件
│       └── main.py
├── pyproject.toml            # 包配置
├── DEVELOP.md                # 本文档
└── README.md
```

### 2. 测试 Hook

修改 hooks 后，可以触发相应事件来测试：

```bash
# 例如：PostToolUse hook 在任何工具调用后触发
# 只要在 Claude Code 中执行任何操作即可触发
```

### 3. 版本管理

版本号在两个地方定义：
- `pyproject.toml` 中的 `version` 字段
- `src/cclight/__init__.py` 中的 `__version__`

发布时保持两者一致。

## 常见问题

### 插件未加载

**症状**：运行 `/plugin list` 看不到插件

**解决方案**：
1. 检查 `plugin.json` 语法是否正确
2. 运行 `/plugin validate ./` 查看具体错误
3. 使用 `claude --debug` 查看详细日志

### 修改后不生效

**症状**：修改代码后没有变化

**解决方案**：
1. 运行 `/reload-plugins` 重新加载
2. 如果还不行，尝试卸载后重新安装：
   ```bash
   /plugin uninstall cclight@cclight-marketplace
   /plugin install cclight@cclight-marketplace
   ```

### Hook 未触发

**症状**：配置的 hook 没有执行

**解决方案**：
1. 检查 `hooks/hooks.json` 语法
2. 确认事件名称大小写正确（如 `PostToolUse` 不是 `postToolUse`）
3. 确认 `cclight` 命令已安装且在 PATH 中

## 发布流程

### 1. 验证配置

```bash
/plugin validate ./
```

### 2. 构建包

```bash
uv build
```

### 3. 发布到 PyPI

```bash
uv publish
```

### 4. 提交代码

```bash
git add .
git commit -m "Release v1.0.0"
git push
```

### 5. 打标签（可选）

```bash
git tag v1.0.0
git push --tags
```

## 相关资源

- [Plugins 参考](https://code.claude.com/docs/zh-CN/plugins-reference)
- [Plugin Marketplaces](https://code.claude.com/docs/zh-CN/plugin-marketplaces)
- [Hooks 参考](https://code.claude.com/docs/zh-CN/hooks-reference)
