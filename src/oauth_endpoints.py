"""OAuth 2.1 discovery endpoints for MCP server."""

import json
import logging
import os
from pathlib import Path
from datetime import datetime
from httpx import AsyncClient

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


# async def oauth_authorization_server_handler(request: Request) -> JSONResponse:
#     """
#     Informational endpoint for OAuth Authorization Server metadata.

#     This server is a PROTECTED RESOURCE, not an authorization server.
#     Clients should use the protected resource endpoint instead.
#     """
#     # Handle OPTIONS preflight request
#     if request.method == "OPTIONS":
#         return JSONResponse(
#             status_code=200,
#             content={},
#             headers={
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Methods": "GET, OPTIONS",
#                 "Access-Control-Allow-Headers": "*",
#             },
#         )

#     metadata = load_protected_resource_metadata()
#     auth_servers = metadata.get("authorization_servers", [])

#     if auth_servers:
#         message = (
#             f"This MCP server is an OAuth 2.0 Protected Resource, not an authorization server. "
#             f"For authorization server metadata, please query: {auth_servers[0]}/.well-known/oauth-authorization-server"
#         )
#     else:
#         message = (
#             "This MCP server is an OAuth 2.0 Protected Resource, not an authorization server. "
#             "Use /.well-known/oauth-protected-resource to discover authorization requirements."
#         )

#     return JSONResponse(
#         status_code=404,
#         content={
#             "error": "not_found",
#             "error_description": message,
#         },
#         headers={
#             "Access-Control-Allow-Origin": "*",
#         },
#     )


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
    metadata = load_protected_resource_metadata()

    # logger.debug(f"Box OAuth Authorization Server metadata: {request}")

    # Add registration_endpoint if missing
    if "registration_endpoint" not in box_metadata:
        box_metadata["registration_endpoint"] = (
            f"{metadata.get('resource', '').rstrip('/mcp').rstrip('/sse').rstrip('/')}/oauth/register"
        )

        # str(
        #     request.url.replace(path="/oauth/register")
        # )
    return JSONResponse(
        status_code=200,
        content=box_metadata,
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            "Access-Control-Allow-Origin": "*",
        },
    )


async def oauth_register_handler(request: Request) -> JSONResponse:
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
    print(f"Registration request: {registration_request}")

    # Fetch Box metadata if needed
    async with AsyncClient() as client:
        box_response = await client.get(
            "https://account.box.com/.well-known/oauth-authorization-server"
        )
    box_metadata = box_response.json()

    # Build response using client's requested values
    registration_response = {
        "client_id": "utcn9zsvobqtby3e7za0qzwtebb6qbty",
        "client_secret": "v5DKn0mkV4q4IZZafjYn6kfuUnwtdVeb",
        "client_id_issued_at": int(datetime.utcnow().timestamp()),
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
            "/.well-known/oauth-protected-resource/sse",
            oauth_protected_resource_mcp_handler,
            methods=["GET", "OPTIONS"],
        ),
        # Route(
        #     "/.well-known/oauth-authorization-server",
        #     # oauth_authorization_server_handler,
        #     oauth_protected_resource_handler,
        #     methods=["GET", "OPTIONS"],
        # ),
        Route(
            "/.well-known/oauth-authorization-server/mcp",
            # oauth_authorization_server_handler,
            oauth_protected_resource_mcp_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/openid-configuration",
            openid_configuration_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/.well-known/oauth-authorization-server",
            oauth_authorization_server_handler,
            methods=["GET", "OPTIONS"],
        ),
        Route(
            "/oauth/register",
            oauth_register_handler,
            methods=["POST", "GET"],
        ),
    ]

    # Add routes to the app's router (insert at beginning for priority matching)
    for route in oauth_routes:
        app.router.routes.insert(0, route)

    logger.info(f"Added {len(oauth_routes)} OAuth discovery endpoints")
