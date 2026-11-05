---
name: coding-monitor
description: >-
  Background telemetry, application log surveillance, Docker container observation,
  and serial console monitoring with automatic error detection and interactive pause gates.
---

# Telemetry & Stream Monitoring (`@coding-monitor`)

The `coding-monitor` skill provides runbooks and operational procedures for streaming continuous output sources to intercept crashes, errors, or anomalies early.

## Capabilities

- **Log & Stream Surveillance**: Tails application logs, Docker stdout, or serial port streams (`/dev/tty*`).
- **Error Detection**: Detects exceptions, stack traces, panics, and custom alert conditions.
- **Intervention Gate & Question Relay Protocol (@coding-investigate)**:
  - Pauses monitoring immediately when an anomaly is discovered, formulating a structured `MonitoringAlert`.
  - **Dual-Mode Handling (Question Relay Protocol)**:
    * **Subagent Mode**: When running as a background subagent under a caller orchestrator (e.g., `@coding` or `@coding-deploy`), does NOT call `ask_question` directly. Relays anomaly alert choices to the parent orchestrator via `send_message` with `[QUESTION_RELAY_REQUEST]\nQuestion: ...\nOptions: ...\nContext: ...` and awaits `[QUESTION_RELAY_RESPONSE]\nAnswer: ...` before acting (spawning `@coding-investigate`, restarting, continuing, or aborting).
    * **Standalone Fallback Mode**: When executed directly at the top level without a caller, prompts the user directly via `ask_question`.
  - If `agentic-issue-investigation-plugin` is installed: includes option to invoke `@coding-investigate` to investigate root causes.
  - If `agentic-issue-investigation-plugin` is NOT installed: presents manual inspection, restart, ignore, or abort options without offering `@coding-investigate`.
- **Multiple Concurrent Instances**: Run separate monitors simultaneously, differentiated by target identifiers (e.g., `coding-monitor-serial`, `coding-monitor-backend`).
- **Obsidian Archival (@coding-document)**:
  - When `agentic-project-documenting-plugin` (or `agentic-obsidian-plugin`) is installed, invokes `@coding-document` at the end to record monitoring telemetry, stream summaries, and alert records in `agentic-obsidian/monitoring/`.
  - If not installed, outputs the monitoring report directly in chat.

## Triggering Monitoring

- Type `@coding-monitor watch serial port /dev/ttyUSB0 at 115200 baud`
- Or prompt: "Start monitoring server logs at /var/log/app.log and alert me on any 5xx errors."
