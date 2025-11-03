"""Configuration for the Box MCP Server."""

import logging
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

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


@dataclass
class BoxApiConfig:
    """Configuration for Box API authentication."""

    # OAuth credentials
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    # CCG/JWT specific
    subject_type: Optional[str] = None  # "enterprise" or "user"
    subject_id: Optional[str] = None

    # JWT specific (from environment variables)
    public_key_id: Optional[str] = None
    private_key: Optional[str] = None
    private_key_passphrase: Optional[str] = None

    # JWT config file (alternative to env vars)
    jwt_config_file: Optional[str] = None




@dataclass
class McpAuthConfig:
    """Configuration for MCP server authentication."""

    # Token-based auth
    auth_token: Optional[str] = None

    # OAuth protected resource config file
    oauth_protected_resources_config_file: str = ".oauth-protected-resource.json"


@dataclass
class LoggingConfig:
    """Configuration for logging."""

    log_level: int = logging.INFO


@dataclass
class AppConfig:
    """Master application configuration containing all sub-configurations."""

    server: ServerConfig = field(default_factory=ServerConfig)
    box_api: BoxApiConfig = field(default_factory=BoxApiConfig)
    mcp_auth: McpAuthConfig = field(default_factory=McpAuthConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def from_env(cls) -> "AppConfig":
        """
        Create AppConfig from environment variables.
        Loads .env file and reads all configuration from environment.
        """
        # Load environment variables from .env file
        dotenv.load_dotenv()

        # Server configuration (defaults used, can be overridden at runtime)
        server_config = ServerConfig()

        # Box API configuration
        box_api_config = BoxApiConfig(
            client_id=os.getenv("BOX_CLIENT_ID"),
            client_secret=os.getenv("BOX_CLIENT_SECRET"),
            subject_type=os.getenv("BOX_SUBJECT_TYPE"),
            subject_id=os.getenv("BOX_SUBJECT_ID"),
            public_key_id=os.getenv("BOX_PUBLIC_KEY_ID"),
            private_key=os.getenv("BOX_PRIVATE_KEY"),
            private_key_passphrase=os.getenv("BOX_PRIVATE_KEY_PASSPHRASE"),
            jwt_config_file=os.getenv("BOX_JWT_CONFIG_FILE"),
        )

        # MCP Auth configuration
        mcp_auth_config = McpAuthConfig(
            auth_token=os.getenv("BOX_MCP_SERVER_AUTH_TOKEN"),
            oauth_protected_resources_config_file=os.getenv(
                "OAUTH_PROTECTED_RESOURCES_CONFIG_FILE",
                ".oauth-protected-resource.json"
            ),
        )

        # Logging configuration
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        logging_config = LoggingConfig(log_level=log_level)

        return cls(
            server=server_config,
            box_api=box_api_config,
            mcp_auth=mcp_auth_config,
            logging=logging_config,
        )


# Global instances (kept for backward compatibility during migration)
DEFAULT_CONFIG = ServerConfig()

# Load environment variables once at module level
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
