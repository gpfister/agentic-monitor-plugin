# agentic-task-monitoring-plugin

Telemetry, stream surveillance, and log monitoring companion plugin for [Google Antigravity](https://antigravity.google).

## Overview
`agentic-task-monitoring-plugin` provides dedicated subagents and progressive-disclosure skills to watch application logs, Docker containers, and serial ports (`/dev/tty*`) continuously in the background. It intercepts errors and crashes early with interactive pause gates.

## Features
- **Declarative Subagent (`@coding-monitor`)**: Background streaming worker defined in [`agents/coding-monitor/agent.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-task-monitoring-plugin/agents/coding-monitor/agent.md) (aliases: `@coding-monitoring`).
- **Progressive Skill (`coding-monitor`)**: Surveillance runbook and trigger instructions in [`skills/coding-monitor/SKILL.md`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-task-monitoring-plugin/skills/coding-monitor/SKILL.md).
- **Interactive Anomaly Gate & Investigation (@coding-investigate)**: Immediately halts log cascading; if `agentic-investigate-plugin` is installed, asks user via `ask_question` whether to invoke `@coding-investigate`.
- **End-of-Monitoring Vault Archival (@coding-document)**: If `agentic-document-plugin` (or `agentic-obsidian-plugin`) is installed, documents telemetry and alerts in the Obsidian vault.
- **Rules (`rules/AGENTS.md`)**: Enforces safe log streaming, bounded buffers, and clean formatting.

## Installation & Activation

```bash
# Enable in Antigravity session:
agy plugin enable agentic-task-monitoring-plugin
```

## Contributing
See [CONTRIBUTING.md](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-task-monitoring-plugin/CONTRIBUTING.md) for contribution guidelines and testing practices.

## License
This project is licensed under the [MIT License](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-task-monitoring-plugin/LICENSE).
