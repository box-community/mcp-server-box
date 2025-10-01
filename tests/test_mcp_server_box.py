from src.mcp_server_box import create_server_info_tool, get_mcp_server


class DummyArgs:
    def __init__(self, transport="stdio", host="127.0.0.1", port=8000, auth="oauth"):
        self.transport = transport
        self.host = host
        self.port = port
        self.auth = auth


def test_get_mcp_server_stdio():
    server = get_mcp_server(transport="stdio", auth="oauth")
    assert server.name == "Box MCP Server"
    assert hasattr(server, "run")


def test_get_mcp_server_http():
    server = get_mcp_server(transport="sse", host="1.2.3.4", port=1234, auth="ccg")
    assert server.name == "Box MCP Server"
    # FastMCP may not expose host/port attributes directly; just check stateless_http is True
    stateless_http = server.settings.stateless_http
    assert stateless_http is True


def test_create_server_info_tool():
    # Minimal mock for FastMCP to test tool registration
    from typing import Any

    class MCPMock:
        def __init__(self):
            self.name = "TestServer"
            self.tools = {}

        def tool(self):
            def decorator(fn):
                self.tools[fn.__name__] = fn
                return fn

            return decorator

    mcp: Any = MCPMock()  # type: ignore
    args = DummyArgs(transport="sse", host="localhost", port=9000, auth="ccg")
    create_server_info_tool(mcp, args)
    assert "mcp_server_info" in mcp.tools
    info = mcp.tools["mcp_server_info"]()
    assert info["server_name"] == "TestServer"
    assert info["transport"] == "sse"
    assert info["auth"] == "ccg"
    assert info["host"] == "localhost"
    assert info["port"] == 9000
