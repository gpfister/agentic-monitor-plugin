# Contributing to agentic-task-monitoring-plugin

Thank you for contributing to **`agentic-task-monitoring-plugin`**! This plugin provides background telemetry and stream surveillance capabilities for Google Antigravity.

---

## 1. Core Guidelines
- Adhere to the standards defined in [`rules/AGENTS.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-task-monitoring-plugin/rules/AGENTS.md).
- Keep subagent definitions modular, declarative, and isolated in `agents/<agent>/agent.md`.
- Skills must include valid YAML frontmatter (`name`, `description`) matching the skill directory name.

---

## 2. Directory Structure

```text
agentic-task-monitoring-plugin/
├── plugin.json         # Plugin manifest
├── pyproject.toml      # Project metadata & test dependencies
├── README.md           # Documentation
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contribution guidelines
├── agents/             # Subagent definitions
│   ├── agent.md        # Central subagent & architecture specification
│   └── coding-monitor/ # Telemetry surveillance worker (@coding-monitor)
│       └── agent.md
├── skills/             # Progressive-disclosure skills
│   └── coding-monitor/ # Stream surveillance skill & runbooks
│       └── SKILL.md
├── rules/              # Plugin-scoped rules
│   └── AGENTS.md
└── tests/              # Test suite
    └── test_plugin.py
```

---

## 3. Testing
Run tests using `uv`:

```bash
uv run pytest
```

Validate plugin structure with `agy`:

```bash
agy plugin validate .
```
