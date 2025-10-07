"""OAuth 2.1 discovery endpoints for MCP server."""

import json
import logging
import os
from pathlib import Path

from fastapi import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def load_protected_resource_metadata() -> dict:
    """Load OAuth Protected Resource Metadata from configuration file."""
    config_file = os.getenv(
        "OAUTH_PROTECTED_RESOURCES_CONFIG_FILE", ".oauth-protected-resource.json"
    )
    config_path = Path(config_file)

    if not config_path.exists():
        logger.error(
            f"OAuth Protected Resource config file not found: {config_path.absolute()}"
        )
        return {}

    try:
        with open(config_path, "r") as f:
            metadata = json.load(f)
            logger.info(f"Loaded OAuth Protected Resource metadata from {config_path}")
            return metadata
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in OAuth config file {config_path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading OAuth config file {config_path}: {e}")
        return {}


async def oauth_protected_resource_handler(request: Request) -> JSONResponse:
    """
    RFC 9728: OAuth 2.0 Protected Resource Metadata endpoint.

    This is the PRIMARY endpoint that MCP clients use to discover:
    - Which authorization server protects this resource
    - What scopes are supported
    - How to send bearer tokens
    """
    # Handle OPTIONS preflight request
    if request.method == "OPTIONS":
        return JSONResponse(
            status_code=200,
            content={},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )

    metadata = load_protected_resource_metadata()

    if not metadata:
        return JSONResponse(
            status_code=500,
            content={
                "error": "server_error",
                "error_description": "OAuth Protected Resource metadata not configured",
            },
            headers={
                "Access-Control-Allow-Origin": "*",
            },
        )

    return JSONResponse(
        status_code=200,
        content=metadata,
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            "Access-Control-Allow-Origin": "*",
        },
    )


async def oauth_protected_resource_mcp_handler(request: Request) -> JSONResponse:
    """
    MCP-specific variant of the OAuth Protected Resource endpoint.
    Returns the same metadata as the standard endpoint.
    """
    return await oauth_protected_resource_handler(request)


async def oauth_authorization_server_handler(request: Request) -> JSONResponse:
    """
    Informational endpoint for OAuth Authorization Server metadata.

    This server is a PROTECTED RESOURCE, not an authorization server.
    Clients should use the protected resource endpoint instead.
    """
    # Handle OPTIONS preflight request
    if request.method == "OPTIONS":
        return JSONResponse(
            status_code=200,
            content={},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )

    metadata = load_protected_resource_metadata()
    auth_servers = metadata.get("authorization_servers", [])

    if auth_servers:
        message = (
            f"This MCP server is an OAuth 2.0 Protected Resource, not an authorization server. "
            f"For authorization server metadata, please query: {auth_servers[0]}/.well-known/oauth-authorization-server"
        )
    else:
        message = (
            "This MCP server is an OAuth 2.0 Protected Resource, not an authorization server. "
            "Use /.well-known/oauth-protected-resource to discover authorization requirements."
        )

    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "error_description": message,
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        },
    )


async def openid_configuration_handler(request: Request) -> JSONResponse:
    """
    Informational endpoint for OpenID Connect configuration.

    This server does NOT implement OpenID Connect.
    It uses OAuth 2.1 Bearer tokens only.
    """
    # Handle OPTIONS preflight request
    if request.method == "OPTIONS":
        return JSONResponse(
            status_code=200,
            content={},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )

    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "error_description": (
                "This MCP server does not implement OpenID Connect. "
                "It uses OAuth 2.1 Bearer token authentication. "
                "Use /.well-known/oauth-protected-resource to discover authorization requirements."
            ),
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        },
    )


def add_oauth_endpoints(app) -> None:
    """Add OAuth discovery endpoints to the FastAPI/Starlette app."""
    from starlette.routing import Route

    # Add OAuth discovery routes (support both GET and OPTIONS for CORS)
    oauth_routes = [
        Route(
            "/.well-known/oauth-protected-resource",
            oauth_protected_resource_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-protected-resource/mcp",
            oauth_protected_resource_mcp_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-authorization-server",
            oauth_authorization_server_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/openid-configuration",
            openid_configuration_handler,
            methods=["GET", "OPTIONS"],
        ),
    ]

    # Add routes to the app's router (insert at beginning for priority matching)
    for route in oauth_routes:
        app.router.routes.insert(0, route)

    logger.info(f"Added {len(oauth_routes)} OAuth discovery endpoints")
