"""Tests for Codex plugin configuration files."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CODEX_PLUGIN_DIR = PROJECT_ROOT / "plugins" / "cclight-codex"
CODEX_MARKETPLACE_FILE = PROJECT_ROOT / ".agents" / "plugins" / "marketplace.json"


class TestCodexPlugin:
    """Validate plugins/cclight-codex/ structure and configuration."""

    def test_directory_structure(self):
        assert (CODEX_PLUGIN_DIR / ".codex-plugin" / "plugin.json").exists(), "plugin.json missing"
        assert (CODEX_PLUGIN_DIR / "hooks" / "hooks.json").exists(), "hooks.json missing"
        assert (CODEX_PLUGIN_DIR / "bin" / "cclight.sh").exists(), "cclight.sh missing"
        assert CODEX_MARKETPLACE_FILE.exists(), "Codex marketplace.json missing"

    def test_cclight_sh_executable(self):
        p = CODEX_PLUGIN_DIR / "bin" / "cclight.sh"
        assert p.stat().st_mode & 0o111, "cclight.sh is not executable"

    def test_plugin_manifest_required_fields(self):
        manifest = json.loads((CODEX_PLUGIN_DIR / ".codex-plugin" / "plugin.json").read_text())
        assert manifest["name"] == "cclight-codex"
        assert CODEX_PLUGIN_DIR.name == manifest["name"]
        assert manifest["version"]
        assert manifest["description"]
        assert "hooks" not in manifest
        assert manifest["author"]["name"] == "codeskyblue"

    def test_plugin_manifest_interface(self):
        manifest = json.loads((CODEX_PLUGIN_DIR / ".codex-plugin" / "plugin.json").read_text())
        iface = manifest["interface"]
        assert iface["displayName"]
        assert iface["shortDescription"]
        assert iface["longDescription"]
        assert iface["developerName"]
        assert iface["category"]
        assert isinstance(iface["capabilities"], list)
        assert isinstance(iface["defaultPrompt"], list)
        assert iface["defaultPrompt"]

    def test_marketplace_entry(self):
        marketplace = json.loads(CODEX_MARKETPLACE_FILE.read_text())
        assert marketplace["name"] == "cclight-marketplace"
        assert marketplace["interface"]["displayName"]
        plugin = marketplace["plugins"][0]
        assert plugin["name"] == "cclight-codex"
        assert plugin["source"] == {
            "source": "local",
            "path": "./plugins/cclight-codex",
        }
        assert plugin["policy"] == {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        }
        assert plugin["category"] == "Productivity"

    def test_hooks_json_valid(self):
        hooks_file = json.loads((CODEX_PLUGIN_DIR / "hooks" / "hooks.json").read_text())
        hooks = hooks_file["hooks"]
        for event in ["SessionStart", "UserPromptSubmit", "PreToolUse",
                      "PostToolUse", "PermissionRequest", "Stop"]:
            assert event in hooks, f"Missing event: {event}"
            assert isinstance(hooks[event], list), f"{event} should be a list"
            assert len(hooks[event]) > 0, f"{event} has no matcher groups"

    def test_hook_commands_valid(self):
        hooks_file = json.loads((CODEX_PLUGIN_DIR / "hooks" / "hooks.json").read_text())
        hooks = hooks_file["hooks"]
        valid_states = {"idle", "working", "input"}
        for event_name, matcher_groups in hooks.items():
            for group in matcher_groups:
                for hook in group["hooks"]:
                    assert hook["type"] == "command", f"hook type must be 'command', got {hook['type']}"
                    cmd = hook["command"]
                    assert cmd.startswith("cclight state "), f"Unexpected command: {cmd}"
                    state = cmd.split()[-1]
                    assert state in valid_states, f"Invalid state in command: {state}"

    def test_session_start_matchers(self):
        hooks_file = json.loads((CODEX_PLUGIN_DIR / "hooks" / "hooks.json").read_text())
        sessions = hooks_file["hooks"]["SessionStart"]
        matchers = {g.get("matcher") for g in sessions if "matcher" in g}
        assert "startup|resume" in matchers, "Missing startup|resume matcher"
        assert "clear|compact" in matchers, "Missing clear|compact matcher"

    def test_pre_tool_use_tool_matchers(self):
        hooks_file = json.loads((CODEX_PLUGIN_DIR / "hooks" / "hooks.json").read_text())
        pre_tool = hooks_file["hooks"]["PreToolUse"]
        matchers = {g.get("matcher") for g in pre_tool if "matcher" in g}
        tool_matchers_found = False
        input_matchers_found = False
        for m in matchers:
            if "AskUserQuestion" in m:
                input_matchers_found = True
            if "Bash" in m:
                tool_matchers_found = True
        assert tool_matchers_found, "No Bash/Read/Write tool matcher found"
        assert input_matchers_found, "No AskUserQuestion input matcher found"

    def test_permission_request_idle(self):
        hooks_file = json.loads((CODEX_PLUGIN_DIR / "hooks" / "hooks.json").read_text())
        pr = hooks_file["hooks"]["PermissionRequest"]
        assert len(pr) == 1
        assert len(pr[0]["hooks"]) == 1
        assert "input" in pr[0]["hooks"][0]["command"]

    def test_stop_idle(self):
        hooks_file = json.loads((CODEX_PLUGIN_DIR / "hooks" / "hooks.json").read_text())
        st = hooks_file["hooks"]["Stop"]
        assert len(st) == 1
        assert len(st[0]["hooks"]) == 1
        assert "idle" in st[0]["hooks"][0]["command"]


class TestClaudeCodePlugin:
    """Validate existing cclight plugin structure (unchanged)."""

    CCLIGHT_PLUGIN_DIR = PROJECT_ROOT / "plugins" / "cclight"

    def test_plugin_json_exists(self):
        assert (self.CCLIGHT_PLUGIN_DIR / ".claude-plugin" / "plugin.json").exists()

    def test_hooks_json_exists(self):
        assert (self.CCLIGHT_PLUGIN_DIR / "hooks" / "hooks.json").exists()

    def test_cclight_sh_exists(self):
        assert (self.CCLIGHT_PLUGIN_DIR / "bin" / "cclight.sh").exists()
