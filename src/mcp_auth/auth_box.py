import logging
from typing import Optional

from fastapi import status
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def box_auth_validate_token(scope) -> Optional[JSONResponse]:
    """Validate if the auth token is properly configured."""

    path = scope["path"]
    logger.debug(f"Token validation processing: {scope['method']} {path}")

    # Extract authorization header
    headers = dict(scope.get("headers", []))
    auth_header = headers.get(b"authorization", b"").decode("utf-8")

    # Validate authentication
    response = None

    if not auth_header:
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

        logger.debug(f"Token is present for {scope['method']} {path}")
        logger.debug("A box client will be created using the provided token.")
        # Store the OAuth token in the scope for use in request handlers
        scope["oauth_token"] = token
        return None

    return response
