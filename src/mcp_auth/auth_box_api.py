import json
import os
import pathlib
from textwrap import dedent

from box_sdk_gen import (
    BoxCCGAuth,
    # Box Client
    BoxClient,
    BoxJWTAuth,
    BoxOAuth,
    # Box CCG
    CCGConfig,
    FileWithInMemoryCacheTokenStorage,
    # Box JWT
    JWTConfig,
    # Box OAuth
    OAuthConfig,
)
from dotenv import load_dotenv

load_dotenv()


def get_oauth_config() -> OAuthConfig:
    # Environment variables
    client_id = os.getenv("BOX_CLIENT_ID")
    client_secret = os.getenv("BOX_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            dedent("""
                To use OAUTH authentication, your .env file must contain the following variables:
                BOX_CLIENT_ID = 
                BOX_CLIENT_SECRET = 
                BOX_REDIRECT_URL = <redirect url as configured in the Box app settings. For MCP Server callback use http://localhost:8000/callback>
                """)
        )

    return OAuthConfig(
        client_id=client_id,
        client_secret=client_secret,
        token_storage=FileWithInMemoryCacheTokenStorage(".auth.oauth"),
    )


def get_oauth_client() -> BoxClient:
    conf = get_oauth_config()
    auth = BoxOAuth(conf)
    return add_extra_header_to_box_client(BoxClient(auth))


def get_ccg_config() -> CCGConfig:
    # Environment variables
    client_id = os.getenv("BOX_CLIENT_ID")
    client_secret = os.getenv("BOX_CLIENT_SECRET")
    subject_type = os.getenv("BOX_SUBJECT_TYPE")
    subject_id = os.getenv("BOX_SUBJECT_ID")

    if not client_id or not client_secret or not subject_type or not subject_id:
        raise ValueError(
            dedent("""
                To use CCG authentication, your .env file must contain the following variables:
                BOX_CLIENT_ID = 
                BOX_CLIENT_SECRET = 
                BOX_SUBJECT_TYPE = <enterprise or user>
                BOX_SUBJECT_ID = <enterprise id or user id>
                """)
        )

    if subject_type == "enterprise":
        enterprise_id = subject_id
        user_id = None
    else:
        enterprise_id = None
        user_id = subject_id

    return CCGConfig(
        client_id=client_id,
        client_secret=client_secret,
        enterprise_id=enterprise_id,
        user_id=user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(
            f".auth.ccg.{subject_type}.{subject_id}"
        ),
    )


def get_ccg_client() -> BoxClient:
    conf = get_ccg_config()
    auth = BoxCCGAuth(conf)
    return add_extra_header_to_box_client(BoxClient(auth))


def get_jwt_config() -> JWTConfig:
    """Get JWT configuration from environment variables or file."""
    if os.getenv("BOX_JWT_CONFIG_FILE"):
        return get_jwt_config_from_file()
    else:
        return get_jwt_config_from_env()


def get_jwt_config_from_env() -> JWTConfig:
    client_id = os.getenv("BOX_CLIENT_ID")
    client_secret = os.getenv("BOX_CLIENT_SECRET")
    jwt_key_id = os.getenv("BOX_PUBLIC_KEY_ID")
    private_key = os.getenv("BOX_PRIVATE_KEY")
    private_key_passphrase = os.getenv("BOX_PRIVATE_KEY_PASSPHRASE")
    subject_type = os.getenv("BOX_SUBJECT_TYPE")
    subject_id = os.getenv("BOX_SUBJECT_ID")

    # Validate required variables
    if (
        not client_id
        or not client_secret
        or not jwt_key_id
        or not private_key
        or not private_key_passphrase
        or not subject_type
        or not subject_id
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

    if subject_type == "user":
        enterprise_id = None
        user_id = subject_id
    else:
        enterprise_id = subject_id
        user_id = None

    return JWTConfig(
        client_id=client_id,
        client_secret=client_secret,
        jwt_key_id=jwt_key_id,
        private_key=private_key,
        private_key_passphrase=private_key_passphrase,
        enterprise_id=enterprise_id,
        user_id=user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(
            f".auth.jwt.{subject_type}.{subject_id}"
        ),
    )


def get_jwt_config_from_file() -> JWTConfig:
    file_location = os.getenv("BOX_JWT_CONFIG_FILE")
    subject_type = os.getenv("BOX_SUBJECT_TYPE")
    subject_id = os.getenv("BOX_SUBJECT_ID")

    if not file_location:
        raise ValueError(
            dedent("""
                To use JWT authentication from a config file, your .env file must contain the following variables:
                BOX_JWT_CONFIG_FILE = <path to config file>
                BOX_SUBJECT_TYPE = <enterprise or user>
                BOX_SUBJECT_ID = <enterprise id or user id>
                """)
        )

    file_location = pathlib.Path(file_location)
    if not file_location.is_file():
        raise ValueError(
            f"BOX_JWT_CONFIG_FILE path is not a valid file: {file_location}"
        )

    # Load json file
    with open(file_location, "r") as f:
        config = json.load(f)

    if not subject_type:
        subject_type = "enterprise"

    if not subject_id:
        subject_id = config.get("enterpriseID")

    jwt_config = JWTConfig.from_config_json_string(
        config_json_string=json.dumps(config),
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


def get_jwt_client() -> BoxClient:
    conf = get_jwt_config()
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
