import argparse
import logging

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

from box_tools_ai import (
    box_ai_extract_tool,
    box_ask_ai_tool,
    box_ask_ai_tool_multi_file,
    box_hubs_ask_ai_tool,
)
from box_tools_docgen import (
    box_docgen_create_batch_tool,
    box_docgen_get_job_tool,
    box_docgen_list_jobs_by_batch_tool,
    box_docgen_list_jobs_tool,
    box_docgen_template_create_tool,
    box_docgen_template_delete_tool,
    box_docgen_template_get_by_id_tool,
    box_docgen_template_list_jobs_tool,
    box_docgen_template_list_tags_tool,
    box_docgen_template_list_tool,
)
from box_tools_files import (
    box_download_file_tool,
    box_read_tool,
    box_upload_file_from_content_tool,
    box_upload_file_from_path_tool,
)
from box_tools_folders import (
    box_list_folder_content_by_folder_id,
    box_manage_folder_tool,
)
from box_tools_generic import box_authorize_app_tool, box_who_am_i
from box_tools_search import box_search_folder_by_name_tool, box_search_tool
from box_tools_share_links import (
    box_create_share_link_tool,
    box_get_shared_link_tool,
    box_remove_shared_link_tool
)
from server_context import box_lifespan

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

    # AI Tools
    mcp.tool()(box_ask_ai_tool)
    mcp.tool()(box_ask_ai_tool_multi_file)
    mcp.tool()(box_hubs_ask_ai_tool)
    mcp.tool()(box_ai_extract_tool)

    # Document Generation Tools
    mcp.tool()(box_docgen_create_batch_tool)
    mcp.tool()(box_docgen_get_job_tool)
    mcp.tool()(box_docgen_list_jobs_tool)
    mcp.tool()(box_docgen_list_jobs_by_batch_tool)
    mcp.tool()(box_docgen_template_create_tool)
    mcp.tool()(box_docgen_template_list_tool)
    mcp.tool()(box_docgen_template_delete_tool)
    mcp.tool()(box_docgen_template_get_by_id_tool)
    mcp.tool()(box_docgen_template_list_tags_tool)
    mcp.tool()(box_docgen_template_list_jobs_tool)

    # File Tools
    mcp.tool()(box_read_tool)
    mcp.tool()(box_upload_file_from_path_tool)
    mcp.tool()(box_upload_file_from_content_tool)
    mcp.tool()(box_download_file_tool)

    # Folder Tools
    mcp.tool()(box_list_folder_content_by_folder_id)
    mcp.tool()(box_manage_folder_tool)
    
    # Share Link Tools
    mcp.tool()(box_create_share_link_tool)
    mcp.tool()(box_get_shared_link_tool)
    mcp.tool()(box_remove_shared_link_tool)


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
