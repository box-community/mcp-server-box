"""Configuration for the Box MCP Server."""

import logging
import os
import sys
from dataclasses import dataclass
from enum import Enum

import colorlog
import dotenv


class TransportType(str, Enum):
    """Available transport types for the MCP server."""

    STDIO = "stdio"
    SSE = "sse"
    STREAMABLE_HTTP = "http"


class BoxAuthType(str, Enum):
    """Available authentication types for Box API."""

    OAUTH = "oauth"
    CCG = "ccg"
    JWT = "jwt"
    MCP_CLIENT = "mcp_client"


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
    port: int = 8005
    box_auth: BoxAuthType = BoxAuthType.OAUTH
    mcp_auth_type: McpAuthType = McpAuthType.TOKEN
    server_name: str = "Box Community MCP"


# Global instance
DEFAULT_CONFIG = ServerConfig()

dotenv.load_dotenv()
LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)


def setup_logging(level: int = LOG_LEVEL) -> None:
    """Configure colored logging for the application."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)s%(reset)s:     %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )

    logging.basicConfig(level=level, handlers=[handler], force=True)

    # Set log level for all existing loggers
    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).setLevel(level)
