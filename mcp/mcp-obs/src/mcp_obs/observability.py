"""Observability client for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import json
from typing import Any

import httpx
from pydantic import BaseModel

from mcp_obs.settings import ObsSettings


class LogEntry(BaseModel):
    """A single log entry from VictoriaLogs."""

    msg: str | None = None
    time: str | None = None
    severity: str | None = None
    service_name: str | None = None
    event: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    error: str | None = None
    raw: dict[str, Any] | None = None


class TraceSpan(BaseModel):
    """A single span from a trace."""

    span_id: str
    operation_name: str
    start_time: int
    duration: int
    error: bool = False
    tags: dict[str, Any] | None = None


class Trace(BaseModel):
    """A complete trace with spans."""

    trace_id: str
    service_name: str | None = None
    spans: list[TraceSpan] | None = None
    raw: dict[str, Any] | None = None


class ObsClient:
    """Client for querying VictoriaLogs and VictoriaTraces."""

    def __init__(self, settings: ObsSettings) -> None:
        self.settings = settings
        self._http_client: httpx.AsyncClient | None = None

    @property
    def http_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(timeout=30.0)
        return self._http_client

    async def close(self) -> None:
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    async def logs_search(
        self, query: str, limit: int = 20
    ) -> list[LogEntry]:
        """Search logs in VictoriaLogs using LogsQL."""
        url = f"{self.settings.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": limit}

        try:
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            
            # VictoriaLogs returns newline-delimited JSON (NDJSON)
            entries = []
            for line in response.text.strip().split("\n"):
                if not line.strip():
                    continue
                try:
                    hit = json.loads(line)
                    entry = LogEntry(
                        msg=hit.get("_msg"),
                        time=hit.get("_time"),
                        severity=hit.get("severity"),
                        service_name=hit.get("service.name"),
                        event=hit.get("event"),
                        trace_id=hit.get("trace_id"),
                        span_id=hit.get("span_id"),
                        error=hit.get("error"),
                        raw=hit,
                    )
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue

            return entries
        except httpx.HTTPError as e:
            return [
                LogEntry(
                    msg=f"Error querying VictoriaLogs: {type(e).__name__}: {e}",
                    severity="ERROR",
                )
            ]

    async def logs_error_count(
        self, service: str | None = None, minutes: int = 60
    ) -> dict[str, int]:
        """Count errors per service over a time window."""
        time_range = f"_time:{minutes}m"
        if service:
            query = f'{time_range} service.name:"{service}" severity:ERROR'
        else:
            query = f"{time_range} severity:ERROR"

        entries = await self.logs_search(query, limit=1000)

        counts: dict[str, int] = {}
        for entry in entries:
            svc = entry.service_name or "unknown"
            counts[svc] = counts.get(svc, 0) + 1

        return counts

    async def traces_list(
        self, service: str | None = None, limit: int = 10
    ) -> list[dict[str, Any]]:
        """List recent traces for a service."""
        url = f"{self.settings.victoriatraces_url}/select/jaeger/api/traces"
        params = {"limit": limit}
        if service:
            params["service"] = service

        try:
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            traces_data = data.get("data", [])
            result = []
            for trace in traces_data:
                trace_info = {
                    "trace_id": trace.get("traceID"),
                    "spans_count": len(trace.get("spans", [])),
                    "service_name": None,
                }

                processes = trace.get("processes", {})
                for proc in processes.values():
                    if proc.get("serviceName"):
                        trace_info["service_name"] = proc["serviceName"]
                        break

                result.append(trace_info)

            return result
        except httpx.HTTPError as e:
            return [{"error": f"Error querying VictoriaTraces: {type(e).__name__}: {e}"}]

    async def traces_get(self, trace_id: str) -> Trace | None:
        """Fetch a specific trace by ID."""
        url = f"{self.settings.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"

        try:
            response = await self.http_client.get(url)
            response.raise_for_status()
            data = response.json()

            traces_data = data.get("data", [])
            if not traces_data:
                return None

            trace_data = traces_data[0]
            spans_data = trace_data.get("spans", [])

            spans = []
            for span in spans_data:
                tags = {}
                for tag in span.get("tags", []):
                    tags[tag.get("key", "")] = tag.get("value")

                is_error = tags.get("error") is not None or tags.get(
                    "otel.status_description"
                )

                spans.append(
                    TraceSpan(
                        span_id=span.get("spanID", ""),
                        operation_name=span.get("operationName", ""),
                        start_time=span.get("startTime", 0),
                        duration=span.get("duration", 0),
                        error=bool(is_error),
                        tags=tags,
                    )
                )

            service_name = None
            processes = trace_data.get("processes", {})
            for proc in processes.values():
                if proc.get("serviceName"):
                    service_name = proc["serviceName"]
                    break

            return Trace(
                trace_id=trace_data.get("traceID", ""),
                service_name=service_name,
                spans=spans,
                raw=trace_data,
            )
        except httpx.HTTPError as e:
            return Trace(
                trace_id=trace_id,
                service_name="error",
                spans=[],
                raw={"error": f"Error querying VictoriaTraces: {type(e).__name__}: {e}"},
            )
