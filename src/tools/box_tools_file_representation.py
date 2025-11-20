from typing import Any

from box_ai_agents_toolkit import box_file_text_extract
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_file_text_extract_tool(
    ctx: Context,
    file_id: str,
) -> dict[str, Any]:
    """
    Extract text from a file in Box.

    The result can be markdown or plain text. If a markdown representation
    is available, it will be preferred.

    Args:
        file_id (str): The ID of the file to extract text from.

    Returns:
        dict[str, Any]: The extracted text (markdown or plain text).
    """
    box_client = get_box_client(ctx)
    return box_file_text_extract(box_client, file_id)
