"""Tool definitions for the observability MCP server."""

from __future__ import annotations

import json
from typing import Any

from mcp.types import TextContent, Tool
from pydantic import BaseModel

from mcp_obs.observability import ObsClient


class LogsSearchArgs(BaseModel):
    """Arguments for logs_search tool."""

    query: str
    limit: int = 20


class LogsErrorCountArgs(BaseModel):
    """Arguments for logs_error_count tool."""

    service: str | None = None
    minutes: int = 60


class TracesListArgs(BaseModel):
    """Arguments for traces_list tool."""

    service: str | None = None
    limit: int = 10


class TracesGetArgs(BaseModel):
    """Arguments for traces_get tool."""

    trace_id: str


class ToolSpec(BaseModel):
    """Specification for an MCP tool."""

    name: str
    description: str
    model: type[BaseModel]
    handler: Any

    def as_tool(self) -> Tool:
        """Convert to MCP Tool type."""
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.model.model_json_schema(),
        )


async def logs_search_handler(client: ObsClient, args: LogsSearchArgs) -> list[TextContent]:
    """Search logs by query."""
    entries = await client.logs_search(args.query, args.limit)
    result = []
    for entry in entries:
        result.append(entry.model_dump(mode="json", exclude_none=True))
    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def logs_error_count_handler(
    client: ObsClient, args: LogsErrorCountArgs
) -> list[TextContent]:
    """Count errors per service."""
    counts = await client.logs_error_count(args.service, args.minutes)
    return [TextContent(type="text", text=json.dumps(counts, indent=2))]


async def traces_list_handler(client: ObsClient, args: TracesListArgs) -> list[TextContent]:
    """List recent traces."""
    traces = await client.traces_list(args.service, args.limit)
    return [TextContent(type="text", text=json.dumps(traces, indent=2, ensure_ascii=False))]


async def traces_get_handler(client: ObsClient, args: TracesGetArgs) -> list[TextContent]:
    """Get a specific trace by ID."""
    trace = await client.traces_get(args.trace_id)
    if trace is None:
        return [TextContent(type="text", text=f"Trace {args.trace_id} not found")]

    result = {
        "trace_id": trace.trace_id,
        "service_name": trace.service_name,
        "spans_count": len(trace.spans or []),
        "spans": [],
    }

    for span in trace.spans or []:
        span_info = {
            "span_id": span.span_id,
            "operation_name": span.operation_name,
            "duration_ms": span.duration / 1000,
            "error": span.error,
        }
        if span.tags:
            error_msg = span.tags.get("error")
            if error_msg:
                span_info["error_message"] = str(error_msg)[:200]
        result["spans"].append(span_info)

    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


TOOL_SPECS = [
    ToolSpec(
        name="logs_search",
        description="Search logs in VictoriaLogs using LogsQL query. Use fields like service.name, severity, event, trace_id. Example: '_time:10m service.name:\"Learning Management Service\" severity:ERROR'",
        model=LogsSearchArgs,
        handler=logs_search_handler,
    ),
    ToolSpec(
        name="logs_error_count",
        description="Count errors per service over a time window (default: last 60 minutes). Optionally filter by service name.",
        model=LogsErrorCountArgs,
        handler=logs_error_count_handler,
    ),
    ToolSpec(
        name="traces_list",
        description="List recent traces for a service. Returns trace IDs and span counts.",
        model=TracesListArgs,
        handler=traces_list_handler,
    ),
    ToolSpec(
        name="traces_get",
        description="Fetch a specific trace by ID. Returns span hierarchy with durations and error status.",
        model=TracesGetArgs,
        handler=traces_get_handler,
    ),
]

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
