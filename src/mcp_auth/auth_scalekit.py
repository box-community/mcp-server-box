import logging
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import status
from scalekit import ScalekitClient
from scalekit.common.scalekit import TokenValidationOptions
from starlette.requests import Request
from starlette.responses import JSONResponse

load_dotenv(dotenv_path=".env.scalekit")
logger = logging.getLogger(__name__)


class ScaleKitConfig:
    """Server configuration class with environment variable defaults."""

    # Server identification
    SERVER_NAME = "Python MCP Server"
    SERVER_VERSION = "1.0.0"

    # Server settings
    PORT = int(os.getenv("PORT", 3003))  # Default port for MCP server
    LOG_LEVEL = os.getenv(
        "LOG_LEVEL", "info"
    )  # Logging level (debug, info, warning, error)

    # ScaleKit OAuth 2.1 configuration
    SK_ENV_URL = os.getenv("SK_ENV_URL", "")  # ScaleKit environment URL
    SK_CLIENT_ID = os.getenv("SK_CLIENT_ID", "")  # ScaleKit client ID
    SK_CLIENT_SECRET = os.getenv("SK_CLIENT_SECRET", "")  # ScaleKit client secret

    # MCP server configuration
    MCP_SERVER_ID = os.getenv("MCP_SERVER_ID", "")  # Unique MCP server identifier

    # OAuth 2.1 protected resource metadata (optional - will use defaults if not provided)
    PROTECTED_RESOURCE_METADATA = os.getenv("PROTECTED_RESOURCE_METADATA", "")

    EXPECTED_AUDIENCE = os.getenv(
        "EXPECTED_AUDIENCE", ""
    )  # Expected audience for token validation


def get_scalekit_client() -> Optional[ScalekitClient]:
    """
    Returns an instance of ScalekitClient.
    """
    config = ScaleKitConfig()
    # Initialize ScaleKit client for token validation
    try:
        scalekit_client = ScalekitClient(
            env_url=config.SK_ENV_URL,
            client_id=config.SK_CLIENT_ID,
            client_secret=config.SK_CLIENT_SECRET,
        )
        logger.info("ScaleKit client initialized successfully")
        return scalekit_client
    except Exception as e:
        logger.warning(f"ScaleKit SDK not available: {e}")
        scalekit_client = None
        return scalekit_client


async def auth_validate_token_scalekit(
    # request: Request, call_next
    scope,
) -> Optional[JSONResponse]:
    """
    Validates the Bearer token from the Authorization header using ScaleKitClient.
    Returns None if the token is valid, otherwise returns a JSONResponse with an error.
    """
    path = scope["path"]
    logger.debug(f"[Scalekit] Token validation processing: {scope['method']} {path}")

    # Initialize ScaleKit client
    config = ScaleKitConfig()
    scalekit_client = get_scalekit_client()

    if not scalekit_client:
        logger.error("[Scalekit] ScaleKit client is not initialized")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "server_error",
                "error_description": "ScaleKit client is not initialized",
            },
        )

    # Extract authorization header
    headers = dict(scope.get("headers", []))
    auth_header = headers.get(b"authorization", b"").decode("utf-8")

    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("[Scalekit] Missing or invalid Authorization header")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "invalid_request",
                "error_description": "Missing or invalid Authorization header",
            },
        )

    token = auth_header.split(" ")[1]

    try:
        options = TokenValidationOptions(
            issuer=config.SK_ENV_URL, audience=[config.EXPECTED_AUDIENCE]
        )

        is_valid = scalekit_client.validate_access_token(token, options=options)
        logger.info(f"[Scalekit] Token validation result: {is_valid}")

        if not is_valid:
            logger.warning(f"Token validation failed for {scope['method']} {path}")
            return JSONResponse(
                content='{"error": "Invalid token"}',
                media_type="application/json",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        logger.info(
            f"[Scalekit] Authentication successful for for {scope['method']} {path}"
        )
        return None

    except Exception as e:
        logger.warning(f"Token validation failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "invalid_token",
                "error_description": "The access token is invalid or has expired",
            },
        )
