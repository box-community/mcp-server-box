import logging
from typing import Optional

from fastapi import status
from starlette.responses import JSONResponse

from config import McpAuthConfig

logger = logging.getLogger(__name__)


def auth_validate_token(scope, config: "McpAuthConfig") -> Optional[JSONResponse]:
    """
    Validate if the auth token is properly configured.

    Args:
        scope: ASGI scope containing request information
        config: McpAuthConfig containing the expected auth token

    Returns:
        Optional[JSONResponse]: Error response if validation fails, None if successful
    """

    path = scope["path"]
    logger.debug(f"Token validation processing: {scope['method']} {path}")

    expected_token = config.auth_token

    # Extract authorization header
    headers = dict(scope.get("headers", []))
    auth_header = headers.get(b"authorization", b"").decode("utf-8")

    # Validate authentication
    response = None

    if not expected_token:
        logger.error("BOX_MCP_SERVER_AUTH_TOKEN not configured")
        response = JSONResponse(
            content={
                "error": "invalid_token",
                "error_description": "Server authentication not properly configured",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    elif not auth_header:
        logger.warning(
            f"[Token] Missing authorization header for {scope['method']} {path}"
        )
        response = JSONResponse(
            content={
                "error": "invalid_request",
                "error_description": "Missing Authorization header",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    elif not auth_header.startswith("Bearer "):
        logger.warning("[Token] Invalid authorization header format")
        response = JSONResponse(
            content={
                "error": "invalid_request",
                "error_description": "Authorization header must use Bearer scheme",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        token = auth_header.replace("Bearer ", "")
        if token != expected_token:
            logger.warning(f"[Token] Invalid token for {scope['method']} {path}")
            response = JSONResponse(
                content={
                    "error": "invalid_token",
                    "error_description": "The access token is invalid or expired",
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            logger.debug(
                f"[Token] Token authentication successful for {scope['method']} {path}"
            )
            return None

    return response
