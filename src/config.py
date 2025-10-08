"""Configuration for the Box MCP Server."""

from dataclasses import dataclass
from enum import Enum


class TransportType(str, Enum):
    """Available transport types for the MCP server."""

    STDIO = "stdio"
    SSE = "sse"
    STREAMABLE_HTTP = "http"


class BoxAuthType(str, Enum):
    """Available authentication types for Box API."""

    OAUTH = "oauth"
    CCG = "ccg"


class McpAuthType(str, Enum):
    """Available authentication types for MCP server."""

    OAUTH = "oauth"
    TOKEN = "token"
    NONE = "none"


@dataclass
class ServerConfig:
    """Default configuration values for the MCP server."""

    transport: TransportType = TransportType.STDIO
    host: str = "localhost"
    port: int = 8001
    box_auth: BoxAuthType = BoxAuthType.OAUTH
    mcp_auth_type: McpAuthType = McpAuthType.TOKEN
    server_name: str = "Box Community MCP"


# Global instance
DEFAULT_CONFIG = ServerConfig()
