import logging
import argparse

from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI

from server_context import box_lifespan
from box_tools_generic import box_who_am_i, box_authorize_app_tool
from box_tools_search import box_search_tool, box_search_folder_by_name_tool
import box_tools

# Disable all logging
logging.basicConfig(level=logging.CRITICAL)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# Override the logging call that's visible in the original code
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)


def get_mcp_server(
    server_name: str = "Box MCP Server",
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 8000,
) -> FastMCP:
    # Initialize FastMCP server

    if transport == "stdio":
        return FastMCP(server_name, lifespan=box_lifespan)
    else:
        return FastMCP(
            server_name,
            stateless_http=True,
            host=host,
            port=port,
            lifespan=box_lifespan,
        )


def register_tools(mcp: FastMCP):
    # Generic tools
    mcp.tool()(box_who_am_i)
    mcp.tool()(box_authorize_app_tool)

    # Search Tools
    mcp.tool()(box_search_tool)
    mcp.tool()(box_search_folder_by_name_tool)

    # Register all tools

    mcp.tool()(box_tools.box_read_tool)
    mcp.tool()(box_tools.box_ask_ai_tool)
    mcp.tool()(box_tools.box_ask_ai_tool_multi_file)
    mcp.tool()(box_tools.box_hubs_ask_ai_tool)

    mcp.tool()(box_tools.box_ai_extract_data)
    mcp.tool()(box_tools.box_list_folder_content_by_folder_id)
    mcp.tool()(box_tools.box_manage_folder_tool)
    mcp.tool()(box_tools.box_upload_file_from_path_tool)
    mcp.tool()(box_tools.box_upload_file_from_content_tool)
    mcp.tool()(box_tools.box_download_file_tool)
    mcp.tool()(box_tools.box_docgen_create_batch_tool)
    mcp.tool()(box_tools.box_docgen_get_job_tool)
    mcp.tool()(box_tools.box_docgen_list_jobs_tool)
    mcp.tool()(box_tools.box_docgen_list_jobs_by_batch_tool)
    mcp.tool()(box_tools.box_docgen_template_create_tool)
    mcp.tool()(box_tools.box_docgen_template_list_tool)
    mcp.tool()(box_tools.box_docgen_template_delete_tool)
    mcp.tool()(box_tools.box_docgen_template_get_by_id_tool)
    mcp.tool()(box_tools.box_docgen_template_list_tags_tool)
    mcp.tool()(box_tools.box_docgen_template_list_jobs_tool)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Box MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for SSE/HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE/HTTP transport (default: 8000)",
    )

    args = parser.parse_args()

    # Initialize FastMCP server
    mcp = get_mcp_server(
        server_name=f"Box MCP {args.transport.upper()} Server",
        transport=args.transport,
        host=args.host,
        port=args.port,
    )
    register_tools(mcp)

    @mcp.tool()
    def mcp_server_info():
        """Returns information about the MCP server."""
        if args.transport == "stdio":
            return {
                "server_name": mcp.name,
                "transport": args.transport,
                "host": "N/A",
                "port": "N/A",
            }

        return {
            "server_name": mcp.name,
            "transport": args.transport,
            "host": args.host,
            "port": args.port,
        }

    if args.transport == "sse":
        # Create FastAPI app and mount MCP SSE endpoint
        app = FastAPI()
        app.mount("/", mcp.sse_app())
        mcp.run(transport="sse")

    elif args.transport == "http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")
