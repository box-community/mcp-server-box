import json
import pathlib
from textwrap import dedent

from box_sdk_gen import (
    BoxCCGAuth,
    BoxClient,
    BoxJWTAuth,
    BoxOAuth,
    CCGConfig,
    FileWithInMemoryCacheTokenStorage,
    JWTConfig,
    OAuthConfig,
)

from config import BoxApiConfig


def get_oauth_config(config: "BoxApiConfig") -> OAuthConfig:
    """
    Get OAuth configuration from the provided config object.

    Args:
        config: BoxApiConfig containing client_id and client_secret

    Returns:
        OAuthConfig: Configured OAuth settings

    Raises:
        ValueError: If required credentials are missing
    """
    if not config.client_id or not config.client_secret:
        raise ValueError(
            dedent("""
                To use OAUTH authentication, your .env file must contain the following variables:
                BOX_CLIENT_ID =
                BOX_CLIENT_SECRET =
                BOX_REDIRECT_URL = <redirect url as configured in the Box app settings. For MCP Server callback use http://localhost:8000/callback>
                """)
        )

    return OAuthConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        token_storage=FileWithInMemoryCacheTokenStorage(".auth.oauth"),
    )


def get_oauth_client(config: "BoxApiConfig") -> BoxClient:
    """
    Get OAuth authenticated Box client.

    Args:
        config: BoxApiConfig containing OAuth credentials

    Returns:
        BoxClient: Authenticated Box client
    """
    conf = get_oauth_config(config)
    auth = BoxOAuth(conf)
    return add_extra_header_to_box_client(BoxClient(auth))


def get_ccg_config(config: "BoxApiConfig") -> CCGConfig:
    """
    Get CCG (Client Credentials Grant) configuration from the provided config object.

    Args:
        config: BoxApiConfig containing CCG credentials

    Returns:
        CCGConfig: Configured CCG settings

    Raises:
        ValueError: If required credentials are missing
    """
    if not config.client_id or not config.client_secret or not config.subject_type or not config.subject_id:
        raise ValueError(
            dedent("""
                To use CCG authentication, your .env file must contain the following variables:
                BOX_CLIENT_ID =
                BOX_CLIENT_SECRET =
                BOX_SUBJECT_TYPE = <enterprise or user>
                BOX_SUBJECT_ID = <enterprise id or user id>
                """)
        )

    if config.subject_type == "enterprise":
        enterprise_id = config.subject_id
        user_id = None
    else:
        enterprise_id = None
        user_id = config.subject_id

    return CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=enterprise_id,
        user_id=user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(
            f".auth.ccg.{config.subject_type}.{config.subject_id}"
        ),
    )


def get_ccg_client(config: "BoxApiConfig") -> BoxClient:
    """
    Get CCG authenticated Box client.

    Args:
        config: BoxApiConfig containing CCG credentials

    Returns:
        BoxClient: Authenticated Box client
    """
    conf = get_ccg_config(config)
    auth = BoxCCGAuth(conf)
    return add_extra_header_to_box_client(BoxClient(auth))


def get_jwt_config(config: "BoxApiConfig") -> JWTConfig:
    """
    Get JWT configuration from config object.
    Uses file-based config if jwt_config_file is set, otherwise uses environment variables.

    Args:
        config: BoxApiConfig containing JWT credentials

    Returns:
        JWTConfig: Configured JWT settings

    Raises:
        ValueError: If required credentials are missing
    """
    if config.jwt_config_file:
        return get_jwt_config_from_file(config)
    else:
        return get_jwt_config_from_env(config)


def get_jwt_config_from_env(config: "BoxApiConfig") -> JWTConfig:
    """
    Get JWT configuration from environment variables via config object.

    Args:
        config: BoxApiConfig containing JWT credentials from environment

    Returns:
        JWTConfig: Configured JWT settings

    Raises:
        ValueError: If required credentials are missing
    """
    # Validate required variables
    if (
        not config.client_id
        or not config.client_secret
        or not config.public_key_id
        or not config.private_key
        or not config.private_key_passphrase
        or not config.subject_type
        or not config.subject_id
    ):
        raise ValueError(
            dedent("""
                To use JWT authentication, your .env file must contain the following variables:
                BOX_CLIENT_ID =
                BOX_CLIENT_SECRET =
                BOX_PUBLIC_KEY_ID =
                BOX_PRIVATE_KEY =
                BOX_PRIVATE_KEY_PASSPHRASE =
                BOX_SUBJECT_TYPE = <enterprise or user>
                BOX_SUBJECT_ID = <enterprise id or user id>
                """)
        )

    if config.subject_type == "user":
        enterprise_id = None
        user_id = config.subject_id
    else:
        enterprise_id = config.subject_id
        user_id = None

    return JWTConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        jwt_key_id=config.public_key_id,
        private_key=config.private_key,
        private_key_passphrase=config.private_key_passphrase,
        enterprise_id=enterprise_id,
        user_id=user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(
            f".auth.jwt.{config.subject_type}.{config.subject_id}"
        ),
    )


def get_jwt_config_from_file(config: "BoxApiConfig") -> JWTConfig:
    """
    Get JWT configuration from a config file.

    Args:
        config: BoxApiConfig containing jwt_config_file path and optional subject settings

    Returns:
        JWTConfig: Configured JWT settings

    Raises:
        ValueError: If config file is missing or invalid
    """
    if not config.jwt_config_file:
        raise ValueError(
            dedent("""
                To use JWT authentication from a config file, your .env file must contain the following variables:
                BOX_JWT_CONFIG_FILE = <path to config file>
                BOX_SUBJECT_TYPE = <enterprise or user>
                BOX_SUBJECT_ID = <enterprise id or user id>
                """)
        )

    file_location = pathlib.Path(config.jwt_config_file)
    if not file_location.is_file():
        raise ValueError(
            f"BOX_JWT_CONFIG_FILE path is not a valid file: {file_location}"
        )

    # Load json file
    with open(file_location, "r") as f:
        jwt_file_config = json.load(f)

    # Use provided subject_type or default to "enterprise"
    subject_type = config.subject_type if config.subject_type else "enterprise"

    # Use provided subject_id or get from config file
    subject_id = config.subject_id if config.subject_id else jwt_file_config.get("enterpriseID")

    jwt_config = JWTConfig.from_config_json_string(
        config_json_string=json.dumps(jwt_file_config),
        token_storage=FileWithInMemoryCacheTokenStorage(
            f".auth.jwt.{subject_type}.{subject_id}"
        ),
    )

    # check if we have user_id or enterprise_id set
    if subject_type == "user":
        jwt_config.user_id = subject_id
        jwt_config.enterprise_id = None
    else:
        jwt_config.enterprise_id = subject_id
        jwt_config.user_id = None

    return jwt_config


def get_jwt_client(config: "BoxApiConfig") -> BoxClient:
    """
    Get JWT authenticated Box client.

    Args:
        config: BoxApiConfig containing JWT credentials

    Returns:
        BoxClient: Authenticated Box client
    """
    conf = get_jwt_config(config)
    auth = BoxJWTAuth(conf)

    # Box API does not seem to recognize the JWT client with user vs enterprise set
    # refreshing the token seems to fix this issue
    auth.refresh_token()

    return add_extra_header_to_box_client(BoxClient(auth))


def add_extra_header_to_box_client(box_client: BoxClient) -> BoxClient:
    """
    Add extra headers to the Box client.

    Args:
        box_client (BoxClient): A Box client object.
        header (Dict[str, str]): A dictionary of extra headers to add to the Box client.

    Returns:
        BoxClient: A Box client object with the extra headers added.
    """
    header = {"x-box-ai-library": "mcp-server-box"}
    return box_client.with_extra_headers(extra_headers=header)
