---
name: observability
description: Use observability tools (logs and traces) to investigate errors and system health
always: false
---

# Observability Skill

Use the observability tools to investigate errors, system health, and failures.

## Available Tools

You have access to these observability tools via the `obs` MCP server:

- **logs_search** — Search logs in VictoriaLogs using LogsQL queries
- **logs_error_count** — Count errors per service over a time window
- **traces_list** — List recent traces for a service
- **traces_get** — Fetch a specific trace by ID with span details

## When to Use

### User asks "What went wrong?" or "Check system health"

When the user asks investigation questions like:
- "What went wrong?"
- "Check system health"
- "Why is the system failing?"
- "Diagnose the error"

**Investigation Flow:**
1. Call `logs_error_count(minutes=5, service="Learning Management Service")` to check for recent errors
2. Call `logs_search(query='_time:5m service.name:"Learning Management Service" severity:ERROR', limit=10)` to get error details
3. Extract the `trace_id` from the most recent error log
4. Call `traces_get(trace_id="<extracted_id>")` to fetch the full trace
5. Analyze the trace spans to identify the failing operation
6. Summarize findings citing BOTH log evidence AND trace evidence

**Response format for "What went wrong?":**
- Start with the root cause (e.g., "PostgreSQL connection failed")
- Cite log evidence: "Error logs show: [brief error message]"
- Cite trace evidence: "Trace shows [operation] failed with [error]"
- Mention the affected service and HTTP status if applicable
- Keep it to 3-5 sentences

### User asks about errors or system health

When the user asks questions like:
- "Any errors in the last hour?"
- "Is the system healthy?"
- "Show me recent failures"

**Strategy:**
1. Start with `logs_error_count` to see if there are recent errors and which services are affected
2. Use `logs_search` to inspect the relevant service logs and extract details
3. If you find a `trace_id` in the logs, use `traces_get` to inspect the full request flow
4. Summarize findings concisely — don't dump raw JSON

### User asks about a specific failure

When investigating a specific issue:
1. Use `logs_search` with relevant filters (service name, time range, severity)
2. Look for error-level logs and extract the `trace_id`
3. Use `traces_get` to see the full span hierarchy and identify where the failure occurred
4. Report the root cause (e.g., database connection failure, timeout, etc.)

## Query Examples

### Search for recent errors in LMS backend

```
logs_search(query='_time:10m service.name:"Learning Management Service" severity:ERROR')
```

### Count errors across all services

```
logs_error_count(minutes=60)
```

### List recent traces for a service

```
traces_list(service="Learning Management Service", limit=5)
```

### Get details of a specific trace

```
traces_get(trace_id="f900f56adf71b705b1ca8535fb76d93b")
```

## Response Style

- Be concise — summarize findings in 2-4 sentences
- Highlight the root cause if identified (e.g., "PostgreSQL connection failed")
- Include relevant trace IDs for reference
- Don't dump raw JSON unless explicitly requested
- If no errors found, say so clearly (e.g., "No errors in the last 10 minutes")

## Scoped Queries

Always prefer scoped queries to avoid noise:
- Use time ranges like `_time:10m` for recent issues
- Filter by service name when known
- Focus on `severity:ERROR` for failures

Example: Instead of "any errors?", ask "any LMS backend errors in the last 10 minutes?"
