#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config at runtime, then launches nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config() -> Path:
    """Read config.json, inject env var values, write config.resolved.json."""
    config_dir = Path(__file__).parent
    config_file = config_dir / "config.json"
    resolved_file = Path("/tmp/config.resolved.json")
    
    # Load base config
    with open(config_file) as f:
        config = json.load(f)
    
    # Override provider API key and base URL from env vars
    llm_api_key = os.environ.get("LLM_API_KEY", "")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL", "")
    llm_api_model = os.environ.get("LLM_API_MODEL", "")
    
    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base_url:
        config["providers"]["custom"]["apiBase"] = llm_api_base_url
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model
    
    # Override gateway host/port from env vars
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "")
    
    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)
    
    # Override MCP server env vars
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY", "")
    
    if "mcpServers" in config.get("tools", {}):
        if "lms" in config["tools"]["mcpServers"]["lms"]:
            if "env" not in config["tools"]["mcpServers"]["lms"]:
                config["tools"]["mcpServers"]["lms"]["env"] = {}
            if lms_backend_url:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
            if lms_api_key:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key
    
    # Override webchat channel settings
    webchat_enabled = os.environ.get("NANOBOT_WEBCHAT_ENABLED", "true").lower() == "true"
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "18791")
    
    if "channels" not in config:
        config["channels"] = {}
    
    config["channels"]["webchat"] = {
        "enabled": webchat_enabled,
        "host": webchat_host,
        "port": webchat_port,
        "allowFrom": ["*"]
    }
    
    # Add mcp_webchat MCP server if env vars are set
    webchat_relay_url = os.environ.get("NANOBOT_WEBSOCKET_RELAY_URL", "")
    webchat_token = os.environ.get("NANOBOT_WEBSOCKET_TOKEN", "")
    
    if webchat_relay_url and webchat_token:
        if "mcpServers" not in config.get("tools", {}):
            config["tools"]["mcpServers"] = {}
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "NANOBOT_WEBSOCKET_RELAY_URL": webchat_relay_url,
                "NANOBOT_WEBSOCKET_TOKEN": webchat_token
            }
        }
    
    # Write resolved config
    with open(resolved_file, "w") as f:
        json.dump(config, f, indent=2)
    
    return resolved_file


def main():
    """Resolve config and exec into nanobot gateway."""
    config_dir = Path(__file__).parent
    workspace_dir = config_dir / "workspace"
    
    resolved_config = resolve_config()
    
    print(f"Using config: {resolved_config}", file=sys.stderr)
    print(f"Workspace: {workspace_dir}", file=sys.stderr)
    
    # Exec into nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_config),
            "--workspace",
            str(workspace_dir),
        ]
    )


if __name__ == "__main__":
    main()
