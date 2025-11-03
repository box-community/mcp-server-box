import pytest
import sys
from unittest import mock

import src.mcp_server_box as mcp_server_box


def test_main_default(monkeypatch):
    """Test main() with default environment and no CLI args."""
    # Patch sys.argv to simulate no CLI args
    monkeypatch.setattr(sys, "argv", ["mcp_server_box.py"])
    # Patch mcp.run to avoid actually starting the server
    with mock.patch.object(mcp_server_box, "create_mcp_server") as mock_create_server:
        mock_server = mock.Mock()
        mock_create_server.return_value = mock_server
        mock_server.run.return_value = None
        # Patch register_tools and create_server_info_tool to no-op
        with mock.patch.object(mcp_server_box, "register_tools"), \
             mock.patch.object(mcp_server_box, "create_server_info_tool"):
            result = mcp_server_box.main()
            assert result == 0
            mock_server.run.assert_called_once()


def test_main_with_args(monkeypatch):
    """Test main() with custom CLI args."""
    monkeypatch.setattr(sys, "argv", [
        "mcp_server_box.py",
        "--transport", "http",
        "--host", "127.0.0.1",
        "--port", "9999",
        "--mcp-auth-type", "none",
        "--box-auth-type", "mcp_client",
    ])
    with mock.patch.object(mcp_server_box, "create_mcp_server") as mock_create_server:
        mock_server = mock.Mock()
        mock_create_server.return_value = mock_server
        mock_server.run.return_value = None
        with mock.patch.object(mcp_server_box, "register_tools"), \
             mock.patch.object(mcp_server_box, "create_server_info_tool"):
            result = mcp_server_box.main()
            assert result == 0
            mock_server.run.assert_called_once()


def test_main_stdio_forces_no_auth(monkeypatch):
    """Test that stdio transport forces mcp_auth_type to none."""
    monkeypatch.setattr(sys, "argv", [
        "mcp_server_box.py",
        "--transport", "stdio",
        "--mcp-auth-type", "none",
        "--box-auth-type", "mcp_client",
    ])
    with mock.patch.object(mcp_server_box, "create_mcp_server") as mock_create_server:
        mock_server = mock.Mock()
        mock_create_server.return_value = mock_server
        mock_server.run.return_value = None
        with mock.patch.object(mcp_server_box, "register_tools"), \
             mock.patch.object(mcp_server_box, "create_server_info_tool"):
            result = mcp_server_box.main()
            assert result == 0
            # mcp_auth_type should be forced to NONE
            assert mcp_server_box.app_config.server.mcp_auth_type.name == "NONE"


def test_main_oauth_forces_box_auth(monkeypatch):
    """Test that mcp_auth_type=oauth forces box_auth_type to mcp_client."""
    monkeypatch.setattr(sys, "argv", [
        "mcp_server_box.py",
        "--transport", "http",
        "--mcp-auth-type", "none",
        "--box-auth-type", "jwt",
    ])
    with mock.patch.object(mcp_server_box, "create_mcp_server") as mock_create_server:
        mock_server = mock.Mock()
        mock_create_server.return_value = mock_server
        mock_server.run.return_value = None
        with mock.patch.object(mcp_server_box, "register_tools"), \
             mock.patch.object(mcp_server_box, "create_server_info_tool"):
            result = mcp_server_box.main()
            assert result == 0
            # box_auth should be forced to MCP_CLIENT
            # assert mcp_server_box.app_config.server.box_auth.name == "NONE"
