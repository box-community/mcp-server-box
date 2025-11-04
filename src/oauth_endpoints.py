"""OAuth 2.1 discovery endpoints for MCP server."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Request
from httpx import AsyncClient
from starlette.responses import JSONResponse

from config import AppConfig

logger = logging.getLogger(__name__)


def load_protected_resource_metadata(config_file: str) -> dict:
    """
    Load OAuth Protected Resource Metadata from configuration file.

    Args:
        config_file: Path to the OAuth protected resource config file

    Returns:
        dict: OAuth Protected Resource metadata
    """
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


def create_oauth_protected_resource_handler(app_config: AppConfig):
    """Create handler with app_config closure."""
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

        metadata = load_protected_resource_metadata(
            app_config.mcp_auth.oauth_protected_resources_config_file
        )

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

    return oauth_protected_resource_handler


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


def create_oauth_authorization_server_handler(app_config: AppConfig):
    """Create handler with app_config closure."""
    async def oauth_authorization_server_handler(request: Request) -> JSONResponse:
        """
        This end point provides works around the Box API not having dynamic client registration
        It first gets the Box's metadata from https://account.box.com/.well-known/oauth-authorization-server
        and if the returned json it does not contain the "registration_endpoint" field, it adds it to the response.
        This "registration_endpoint" field is required for dynamic client registration, and will point to another endpoint
        in this server that will handle client registration.
        """
        # Get Box's OAuth Authorization Server metadata

        async with AsyncClient() as client:
            box_response = await client.get(
                "https://account.box.com/.well-known/oauth-authorization-server"
            )
        box_metadata = box_response.json()
        metadata = load_protected_resource_metadata(
            app_config.mcp_auth.oauth_protected_resources_config_file
        )

        # logger.debug(f"Box OAuth Authorization Server metadata: {request}")

        # Add registration_endpoint if missing
        if "registration_endpoint" not in box_metadata:
            box_metadata["registration_endpoint"] = (
                f"{metadata.get('resource', '').rstrip('/mcp').rstrip('/sse').rstrip('/')}/oauth/register"
            )

        # Add scopes_supported from protected resource metadata if not included in the box_metadata
        if "scopes_supported" not in box_metadata and "scopes_supported" in metadata:
            box_metadata["scopes_supported"] = metadata["scopes_supported"]

        return JSONResponse(
            status_code=200,
            content=box_metadata,
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
                "Access-Control-Allow-Origin": "*",
            },
        )

    return oauth_authorization_server_handler


async def oauth_register_handler(request: Request, app_config: AppConfig) -> JSONResponse:
    """
    Handle dynamic client registration requests.

    This is a stub implementation that accepts registration requests
    and returns a fixed client_id and client_secret.
    """
    # Get the registration request body
    registration_request = await request.json()

    # Extract fields sent by the client
    redirect_uris = registration_request.get("redirect_uris", [])
    grant_types = registration_request.get(
        "grant_types", ["authorization_code", "refresh_token"]
    )
    response_types = registration_request.get("response_types", ["code"])
    token_endpoint_auth_method = registration_request.get(
        "token_endpoint_auth_method", "client_secret_post"
    )

    # Optional: Log what the client sent
    logger.debug(f"Registration request: {registration_request}")

    
    registration_response = {
        "client_id": app_config.box_api.client_id,
        "client_secret": app_config.box_api.client_secret,
        "client_id_issued_at": int(datetime.now(timezone.utc).timestamp()),
        "client_secret_expires_at": 0,  # Never expires
        "redirect_uris": redirect_uris,  # Echo back what client sent
        "grant_types": grant_types,
        "response_types": response_types,
        "token_endpoint_auth_method": token_endpoint_auth_method,
    }

    return JSONResponse(
        status_code=201,
        content=registration_response,
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-store",
            "Access-Control-Allow-Origin": "*",
        },
    )


def add_oauth_endpoints(app, app_config: AppConfig) -> None:
    """
    Add OAuth discovery endpoints to the FastAPI/Starlette app.

    Args:
        app: FastAPI/Starlette application
        app_config: Complete application configuration
    """
    from starlette.routing import Route

    # Create handlers with config closure
    protected_resource_handler = create_oauth_protected_resource_handler(app_config)
    authorization_server_handler = create_oauth_authorization_server_handler(app_config)

    async def oauth_register_handler_with_config(request: Request) -> JSONResponse:
        return await oauth_register_handler(request, app_config)

    # Add OAuth discovery routes (support both GET and OPTIONS for CORS)
    oauth_routes = [
        Route(
            "/.well-known/oauth-protected-resource",
            protected_resource_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-protected-resource/mcp",
            protected_resource_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-protected-resource/sse",
            protected_resource_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-authorization-server",
            authorization_server_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-authorization-server/mcp",
            authorization_server_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-authorization-server/sse",
            authorization_server_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/oauth/register",
            oauth_register_handler_with_config,
            methods=["POST", "GET"],
        ),
    ]

    # Add routes to the app's router (insert at beginning for priority matching)
    for route in oauth_routes:
        app.router.routes.insert(0, route)

    logger.info(f"Added {len(oauth_routes)} OAuth discovery endpoints")
