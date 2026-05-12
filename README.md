# Ref

- https://github.com/bobek-balinek/claude-lamp
- [Hooks系统完整指南](https://github.com/KimYx0207/AI-Coding-Guide-Zh/blob/main/docs/claude-code/05-Hooks%E7%B3%BB%E7%BB%9F%E5%AE%8C%E6%95%B4%E6%8C%87%E5%8D%97.md)

# 注册Hooks

~/.claude/settings.json

```
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook_wait.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook_running.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook_done.py"
          }
        ]
      }
    ]
  }
}
```
