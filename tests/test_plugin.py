"""Tests for agentic-task-monitoring-plugin structure and specifications."""

import json
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def test_plugin_manifest_valid():
    manifest_file = PLUGIN_ROOT / "plugin.json"
    assert manifest_file.exists(), "plugin.json must exist"
    data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert data.get("name") == "agentic-task-monitoring-plugin"
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
    assert "agentic-task-monitoring-plugin" in content


def test_monitoring_agent_exists():
    agent_file = PLUGIN_ROOT / "agents" / "coding-monitor" / "agent.md"
    assert agent_file.exists(), "agents/coding-monitor/agent.md must exist"
    
    legacy_dir = PLUGIN_ROOT / "agents" / "monitoring"
    assert not legacy_dir.exists(), "agents/monitoring must NOT exist"
    
    content = agent_file.read_text(encoding="utf-8")
    assert "name: coding-monitor" in content
    assert "Coding - Monitor Expert" in content

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
    assert "Coding - Monitoring Subagents" in content


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


def test_no_stale_companion_references():
    stale_patterns = [
        "agentic-investigate-plugin",
        "agentic-document-plugin",
        "agentic-research-plugin",
        "agentic-triage-plugin",
    ]
    files_to_check = [
        PLUGIN_ROOT / "README.md",
        PLUGIN_ROOT / "rules" / "AGENTS.md",
        PLUGIN_ROOT / "agents" / "agent.md",
        PLUGIN_ROOT / "agents" / "coding-monitor" / "agent.md",
        PLUGIN_ROOT / "skills" / "coding-monitor" / "SKILL.md",
    ]
    for file_path in files_to_check:
        assert file_path.exists(), f"File {file_path} must exist"
        content = file_path.read_text(encoding="utf-8")
        for stale in stale_patterns:
            assert stale not in content, f"Found stale reference '{stale}' in {file_path}"


def test_question_relay_protocol_in_agent():
    agent_file = PLUGIN_ROOT / "agents" / "coding-monitor" / "agent.md"
    assert agent_file.exists(), "agents/coding-monitor/agent.md must exist"
    content = agent_file.read_text(encoding="utf-8")

    # Verify tools frontmatter contains both send_message and ask_question
    assert "send_message" in content, "send_message must be an allowed tool"
    assert "ask_question" in content, "ask_question must be an allowed tool"

    # Verify Question Relay Protocol envelopes and fields
    assert "[QUESTION_RELAY_REQUEST]" in content
    assert "[QUESTION_RELAY_RESPONSE]" in content
    assert "Question Relay Protocol (Dual-Mode)" in content or "Question Relay Protocol" in content
    assert "Question:" in content
    assert "Options:" in content
    assert "Context:" in content
    assert "Answer:" in content

    # Verify Dual-mode execution paths
    assert "Subagent Mode" in content
    assert "Standalone Fallback Mode" in content or "Standalone Mode" in content
    assert 'Recipient="<caller_id>"' in content


def test_question_relay_protocol_in_rules_and_skill():
    rules_file = PLUGIN_ROOT / "rules" / "AGENTS.md"
    assert rules_file.exists(), "rules/AGENTS.md must exist"
    rules_content = rules_file.read_text(encoding="utf-8")
    assert "Question Relay Protocol" in rules_content
    assert "[QUESTION_RELAY_REQUEST]" in rules_content
    assert "[QUESTION_RELAY_RESPONSE]" in rules_content
    assert "Subagent Mode" in rules_content
    assert "Standalone Fallback Mode" in rules_content

    skill_file = PLUGIN_ROOT / "skills" / "coding-monitor" / "SKILL.md"
    assert skill_file.exists(), "skills/coding-monitor/SKILL.md must exist"
    skill_content = skill_file.read_text(encoding="utf-8")
    assert "Question Relay Protocol" in skill_content
    assert "[QUESTION_RELAY_REQUEST]" in skill_content
    assert "[QUESTION_RELAY_RESPONSE]" in skill_content
    assert "Subagent Mode" in skill_content
    assert "Standalone Fallback Mode" in skill_content


def test_question_relay_protocol_in_central_guide():
    central_file = PLUGIN_ROOT / "agents" / "agent.md"
    assert central_file.exists(), "agents/agent.md must exist"
    content = central_file.read_text(encoding="utf-8")
    assert "Dual-mode" in content or "dual-mode" in content
    assert "Question Relay Protocol" in content
    assert "[QUESTION_RELAY_REQUEST]" in content
    assert "[QUESTION_RELAY_RESPONSE]" in content
    assert "Subagent Mode" in content
    assert "Standalone Fallback Mode" in content


