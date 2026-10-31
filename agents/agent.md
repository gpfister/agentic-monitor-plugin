---
name: coding-monitoring-catalog
description: Architecture overview and catalog for the agentic-monitor-plugin subagents.
enable_write_tools: false
enable_subagent_tools: false
enable_mcp_tools: false
tools:
  - read_file
  - list_dir
---

# Coding - Monitoring Subagents & Telemetry Architecture (agents/agent.md)

This document defines the subagent architecture and catalog for the **`agentic-monitor-plugin`** (also referenced as `agentic-monitoring-plugin`).

---

## 1. Architectural Overview

The `agentic-monitor-plugin` provides continuous stream surveillance, log observation, and anomaly detection capabilities for Google Antigravity. By isolating monitoring into dedicated subagents, long-running processes (serial consoles, Docker containers, application logs) can be observed continuously without blocking the main conversational flow or software development pipeline.

### Directory Structure
```text
agents/
├── agent.md                    # Master subagent guide (this file)
└── coding-monitor/             # Telemetry & Stream Surveillance Subagent
    └── agent.md
```

---

## 2. Subagent Catalog

| Agent Handle | Directory | `enable_write_tools` | `enable_subagent_tools` | `enable_mcp_tools` | Allowed Tools | Description |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`@coding-monitor`** | [`agents/coding-monitor/`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-monitor-plugin/agents/coding-monitor/) | `True` | `True` | `False` | `run_command`, `manage_task`, `read_file`, `list_dir`, `ask_question`, `invoke_subagent`, `send_message` | Background surveillance worker watching logs, serial consoles, and container streams with anomaly pause gates, `@coding-investigate` invocation, and `@coding-document` handoff. |

---

## 3. Telemetry & Pause Gate Protocol

1. **Target Attachment**:
   - Application log files (`tail -f /path/to/log`)
   - Container output streams (`docker logs -f <container>`)
   - Hardware serial streams (`/dev/tty*` at configured baud rates)
2. **Anomaly Detection**:
   - Scans stream chunks in real-time for panics, exceptions, FATAL errors, and stack traces.
3. **Interactive Pause Gate & Issue Remediation**:
   - Immediately pauses stream surveillance upon anomaly discovery.
   - Formulates a structured `MonitoringAlert` JSON summarizing timestamp, stream source, error excerpt, and severity.
   - **Cross-Plugin Gate**:
     - If `agentic-investigate-plugin` is installed: asks the user via `ask_question` if they want to invoke `@coding-investigate` to investigate the issue. If the user confirms, invokes `@coding-investigate` (TypeName="coding-investigate").
     - If `agentic-investigate-plugin` is NOT installed: presents manual inspection, restart, ignore, or abort options.
4. **End-of-Monitoring Documentation**:
   - When monitoring terminates or completes:
     - If `agentic-document-plugin` (or `agentic-obsidian-plugin`) is installed: invokes `@coding-document` to record monitoring session logs and telemetry in `agentic-obsidian/monitoring/`.
     - If not installed: outputs the monitoring summary directly in the chat.
