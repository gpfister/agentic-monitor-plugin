# Monitoring Guidelines & Standards — agentic-task-monitoring-plugin

This rule set applies whenever the `agentic-task-monitoring-plugin` is active in an Antigravity session.

---

## 1. Stream Surveillance & Safety
- **Non-Destructive Observation**: Monitoring workers must strictly perform read/tail operations on target streams. Do not kill or alter target processes unless explicitly requested by the user during a pause gate.
- **Buffer & Resource Management**: Guard against unbound in-memory buffering when tailing high-throughput log streams. Process logs in bounded windows.

---

## 2. Interactive Pause Gate & Investigation Protocol
- When an anomaly or error is detected:
  1. Halt surveillance immediately to prevent log cascading.
  2. Synthesize an actionable `MonitoringAlert` capturing the root error, timestamp, stream source, and stack trace.
  3. Prompt the user via `ask_question`:
     - If `agentic-investigate-plugin` is installed: ask the user if they want to invoke `@coding-investigate` to investigate the root cause. If confirmed, invoke `@coding-investigate`.
     - If `agentic-investigate-plugin` is NOT installed: present manual inspection, restart, ignore, or abort choices without offering `@coding-investigate`.

---

## 3. Communication & Links
- Keep alert summaries high-signal and concise.
- Always provide clickable markdown links using the `file://` scheme when referencing local log files, configuration paths, or source files implicated in stack traces.

---

## 4. Documentation Archival with @coding-document
- When `agentic-document-plugin` (or `agentic-obsidian-plugin`) is active, `@coding-monitor` must invoke `@coding-document` at the end of the monitoring to record monitoring results, telemetry summaries, and anomaly alerts in `agentic-obsidian/monitoring/`.
- If `agentic-document-plugin` (or `agentic-obsidian-plugin`) is not installed, output the monitoring report and alert summary directly in chat without invoking subagents.
