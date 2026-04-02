"""Settings for the observability MCP server."""

import os
from functools import lru_cache

from pydantic import BaseModel


class ObsSettings(BaseModel):
    """Settings for connecting to VictoriaLogs and VictoriaTraces."""

    victorialogs_url: str = "http://victorialogs:9428"
    victoriatraces_url: str = "http://victoriatraces:10428"


@lru_cache
def get_settings() -> ObsSettings:
    """Get settings from environment or defaults."""
    return ObsSettings(
        victorialogs_url=os.environ.get(
            "NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"
        ),
        victoriatraces_url=os.environ.get(
            "NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428"
        ),
    )
