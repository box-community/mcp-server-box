import base64
import os
from typing import Any, Optional

from box_ai_agents_toolkit import (
    box_file_download,
    box_file_upload,
)
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_file_download_tool(
    ctx: Context,
    file_id: str,
    save_file: bool = False,
    save_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Download a file from Box and optionally save it locally.

    Args:
        file_id (str): The ID of the file to download.
        save_file (bool, optional): Whether to save the file locally. Defaults to False.
        save_path (str, optional): Path where to save the file. If not provided but save_file is True,
                                  uses a temporary directory. Defaults to None.

    Returns:
        dict[str, Any]: For text files: content as string.
                       For images: base64-encoded string with metadata.
                       For unsupported files: error message.
                       If save_file is True, includes the path where the file was saved.
    """
    box_client = get_box_client(ctx)
    path_saved, file_content, mime_type = box_file_download(
        box_client, file_id, save_file, save_path
    )

    result: dict[str, Any] = {}

    if path_saved:
        result["path_saved"] = path_saved

    if mime_type:
        result["mime_type"] = mime_type

    # Handle different file types
    if mime_type and mime_type.startswith("image/"):
        # For images, return base64-encoded content
        if file_content:
            result["content"] = base64.b64encode(file_content).decode()
    elif mime_type and mime_type.startswith("text/"):
        # For text files, return decoded content
        if file_content:
            result["content"] = file_content.decode("utf-8", errors="replace")
    else:
        # For other types, return base64-encoded content
        if file_content:
            result["content"] = base64.b64encode(file_content).decode()

    return result


async def box_file_upload_tool(
    ctx: Context,
    content: str | bytes,
    file_name: str,
    parent_folder_id: str,
) -> dict[str, Any]:
    """
    Upload content as a file to Box.

    Args:
        content (str | bytes): The content to upload. Can be text or binary data.
        file_name (str): The name to give the file in Box.
        parent_folder_id (str): The ID of the destination folder. Defaults to root ("0").

    Returns:
        dict[str, Any]: Information about the uploaded file including id and name.
    """
    box_client = get_box_client(ctx)
    return box_file_upload(box_client, content, file_name, parent_folder_id)


async def box_file_upload_from_path_tool(
    ctx: Context,
    file_path: str,
    parent_folder_id: str,
    file_name: Optional[str] = None,
) -> dict[str, Any]:
    """
    Upload a local file to Box by specifying its file path.
    Supports any file type including binary files like .pptx, .xlsx, .pdf, .zip, etc.

    Args:
        file_path (str): The absolute path to the local file to upload.
        parent_folder_id (str): The ID of the destination folder in Box. Use "0" for root folder.
        file_name (str, optional): The name to give the file in Box. If not provided, uses the original file name.

    Returns:
        dict[str, Any]: Information about the uploaded file including id, name, and type.
    """
    if not os.path.isabs(file_path):
        return {"error": f"Please provide an absolute file path. Received: {file_path}"}

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    if not os.path.isfile(file_path):
        return {"error": f"Path is not a file: {file_path}"}

    upload_name = file_name or os.path.basename(file_path)

    with open(file_path, "rb") as f:
        content = f.read()

    box_client = get_box_client(ctx)
    return box_file_upload(box_client, content, upload_name, parent_folder_id)
