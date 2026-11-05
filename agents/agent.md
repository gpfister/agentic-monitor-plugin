---
name: coding-monitoring-catalog
description: Architecture overview and catalog for the agentic-task-monitoring-plugin subagents.
enable_write_tools: false
enable_subagent_tools: false
enable_mcp_tools: false
tools:
  - read_file
  - list_dir
---

# Coding - Monitoring Subagents & Telemetry Architecture (agents/agent.md)

This document defines the subagent architecture and catalog for the **`agentic-task-monitoring-plugin`** (also referenced as `agentic-monitoring-plugin`).

---

## 1. Architectural Overview

The `agentic-task-monitoring-plugin` provides continuous stream surveillance, log observation, and anomaly detection capabilities for Google Antigravity. By isolating monitoring into dedicated subagents, long-running processes (serial consoles, Docker containers, application logs) can be observed continuously without blocking the main conversational flow or software development pipeline.

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
| **`@coding-monitor`** | [`agents/coding-monitor/`](file:///Users/gpfister/Development/Projects/gpfister/agentic/agentic-task-monitoring-plugin/agents/coding-monitor/) | `True` | `True` | `False` | `run_command`, `manage_task`, `read_file`, `list_dir`, `ask_question`, `invoke_subagent`, `send_message` | Dual-mode background surveillance worker watching logs, serial consoles, and container streams with anomaly pause gates (via Question Relay Protocol `[QUESTION_RELAY_REQUEST]` / `[QUESTION_RELAY_RESPONSE]` when running as a subagent, or `ask_question` when standalone), `@coding-investigate` invocation, and `@coding-document` handoff. |

---

## 3. Telemetry & Pause Gate Protocol

```text
Stream Surveillance ──> Anomaly Detected? ──(No)──> Continue Streaming
                               │
                             (Yes)
                               ▼
                    Pause Stream Surveillance
                    & Formulate MonitoringAlert
                               │
                               ▼
                     Dual-Mode Intervention Gate
             ┌─────────────────┴─────────────────┐
             ▼                                   ▼
      [Subagent Mode]                     [Standalone Mode]
  Relay via send_message                 Prompt directly via
  [QUESTION_RELAY_REQUEST]                  ask_question
             │                                   │
  Await [QUESTION_RELAY_RESPONSE]                │
             └─────────────────┬─────────────────┘
                               ▼
                      Human Choice Made:
     ┌──────────────────┬──────┴───────────┬──────────────┐
     ▼                  ▼                  ▼              ▼
Invoke Investigator  Restart Target     Ignore & Resume   Abort Surveillance
(@coding-investigate) Process/Container Surveillance      & Document Session
```

### 3.1 Target Attachment
- Application log files (`tail -f /path/to/log`)
- Container output streams (`docker logs -f <container>`)
- Hardware serial streams (`/dev/tty*` at configured baud rates)

### 3.2 Anomaly Detection
- Scans stream chunks in real-time for panics, exceptions, FATAL errors, and stack traces.

### 3.3 Dual-Mode Intervention Gate & Question Relay Protocol
When an anomaly or error is detected, `@coding-monitor` pauses surveillance and seeks human guidance:
1. **Subagent Mode (Question Relay Protocol)**:
   - When running as a background subagent with a parent orchestrator (caller ID present), it does NOT call `ask_question` directly.
   - Relays anomaly choices to the parent orchestrator via `send_message`:
     ```text
     [QUESTION_RELAY_REQUEST]
     Question: ...
     Options: ...
     Context: ...
     ```
   - Awaits `[QUESTION_RELAY_RESPONSE]\nAnswer: ...` to decide whether to spawn `@coding-investigate`, restart, continue, or abort.
2. **Standalone Fallback Mode**:
   - When executed directly as a top-level session without a parent orchestrator, it prompts the user directly via `ask_question`.

### 3.4 Cross-Plugin Investigation & Documentation
- **Issue Investigation Gate (`@coding-investigate`)**:
  - If `agentic-issue-investigation-plugin` is installed: offers the choice to invoke `@coding-investigate` to investigate root causes. If confirmed, invokes `@coding-investigate` (`TypeName="coding-investigate"`).
  - If `agentic-issue-investigation-plugin` is NOT installed: presents manual inspection, restart, ignore, or abort options without offering `@coding-investigate`.
- **End-of-Monitoring Documentation (`@coding-document`)**:
  - When monitoring terminates, stops, or completes:
    - If `agentic-project-documenting-plugin` (or `agentic-obsidian-plugin`) is installed: invokes `@coding-document` to record monitoring session logs, telemetry, and alerts in `agentic-obsidian/monitoring/`.
    - If not installed: outputs the monitoring summary and alerts directly in chat.
