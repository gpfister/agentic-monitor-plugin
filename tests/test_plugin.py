"""Tests for agentic-monitoring-plugin structure and specifications."""

import json
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def test_plugin_manifest_valid():
    manifest_file = PLUGIN_ROOT / "plugin.json"
    assert manifest_file.exists(), "plugin.json must exist"
    data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert data.get("name") == "agentic-monitoring-plugin"
    assert data.get("license") == "MIT"


def test_license_exists():
    license_file = PLUGIN_ROOT / "LICENSE"
    assert license_file.exists(), "LICENSE must exist"
    content = license_file.read_text(encoding="utf-8")
    assert "MIT License" in content
    assert "Greg PFISTER" in content


def test_contributing_exists():
    contrib_file = PLUGIN_ROOT / "CONTRIBUTING.md"
    assert contrib_file.exists(), "CONTRIBUTING.md must exist"
    content = contrib_file.read_text(encoding="utf-8")
    assert "agentic-monitoring-plugin" in content


def test_monitoring_agent_exists():
    agent_file = PLUGIN_ROOT / "agents" / "coding-monitor" / "agent.md"
    assert agent_file.exists(), "agents/coding-monitor/agent.md must exist"
    
    legacy_dir = PLUGIN_ROOT / "agents" / "monitoring"
    assert not legacy_dir.exists(), "agents/monitoring must NOT exist"
    
    content = agent_file.read_text(encoding="utf-8")
    assert "name: coding-monitor" in content
    assert "Telemetry Monitor" in content

    # Check aliases
    aliases = []
    in_aliases = False
    for line in content.splitlines():
        if line.startswith("aliases:"):
            in_aliases = True
            continue
        if in_aliases:
            if line.startswith("  - "):
                aliases.append(line.replace("  - ", "").strip())
            elif line.startswith(" ") or line.startswith("\t"):
                continue
            else:
                break

    assert len(aliases) > 0, "At least one alias should be defined"
    assert "monitoring" not in aliases, "Legacy alias 'monitoring' must not be present"
    for alias in aliases:
        assert re.match(r"^coding(-.*)?$", alias), f"Alias '{alias}' must match ^coding(-.*)?$"


def test_central_agent_guide_exists():
    central_file = PLUGIN_ROOT / "agents" / "agent.md"
    assert central_file.exists(), "agents/agent.md must exist"
    content = central_file.read_text(encoding="utf-8")
    assert "name: agent" in content or "name: monitoring-catalog" in content or "name: coding-monitoring-catalog" in content
    assert "Monitoring Subagents" in content


def test_monitoring_skill_exists():
    skill_file = PLUGIN_ROOT / "skills" / "coding-monitor" / "SKILL.md"
    assert skill_file.exists(), "skills/coding-monitor/SKILL.md must exist"
    
    legacy_skill_dir = PLUGIN_ROOT / "skills" / "monitoring"
    assert not legacy_skill_dir.exists(), "skills/monitoring must NOT exist"
    
    content = skill_file.read_text(encoding="utf-8")
    assert "name: coding-monitor" in content
    assert "Intervention Gate" in content


def test_rules_exist():
    rules_file = PLUGIN_ROOT / "rules" / "AGENTS.md"
    assert rules_file.exists(), "rules/AGENTS.md must exist"
    content = rules_file.read_text(encoding="utf-8")
    assert "Monitoring Guidelines" in content
