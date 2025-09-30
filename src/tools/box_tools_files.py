import base64
import os
from typing import Any

from box_ai_agents_toolkit import (
    DocumentFiles,
    ImageFiles,
    box_file_download,
    box_file_text_extract,
    box_upload_file,
)
from mcp.server.fastmcp import Context

from tools.box_tools_generic import get_box_client


async def box_read_tool(ctx: Context, file_id: str) -> dict[str, Any]:
    """
    Read the text content of a file in Box.

    Args:
        file_id (str): The ID of the file to read.
    return:
        str: The text content of the file.
    """
    # check if file id isn't a string and convert to a string
    if not isinstance(file_id, str):
        file_id = str(file_id)

    box_client = get_box_client(ctx)
    response = box_file_text_extract(box_client, file_id)
    return response


async def box_upload_file_from_path_tool(
    ctx: Context,
    file_path: str,
    folder_id: str = "0",
    new_file_name: str = "",
) -> str:
    """
    Upload a file to Box from a filesystem path.

    Args:
        file_path (str): Path on the *server* filesystem to the file to upload.
        folder_id (str): The ID of the destination folder. Defaults to root ("0").
        new_file_name (str): Optional new name to give the file in Box. If empty, uses the original filename.

    return:
        str: Information about the uploaded file (ID and name).
    """
    box_client = get_box_client(ctx)

    try:
        # Normalize the path and check if file exists
        file_path_expanded = os.path.expanduser(file_path)
        if not os.path.isfile(file_path_expanded):
            return f"Error: file '{file_path}' not found."

        # Determine the file name to use
        actual_file_name = new_file_name.strip() or os.path.basename(file_path_expanded)
        # Determine file extension to detect binary types
        _, ext = os.path.splitext(actual_file_name)
        binary_exts = {
            ".docx",
            ".pptx",
            ".xlsx",
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
        }
        # Read file content as bytes for binary types, else as text
        if ext.lower() in binary_exts:
            # Binary file: read raw bytes
            with open(file_path_expanded, "rb") as f:
                content = f.read()
        else:
            # Text file: read as UTF-8
            with open(file_path_expanded, "r", encoding="utf-8") as f:
                content = f.read()
        # Upload using toolkit (supports str or bytes)
        result = box_upload_file(box_client, content, actual_file_name, folder_id)
        return f"File uploaded successfully. File ID: {result['id']}, Name: {result['name']}"
    except Exception as e:
        return f"Error uploading file: {str(e)}"


async def box_upload_file_from_content_tool(
    ctx: Context,
    content: str | bytes,  # Accept both string and bytes
    file_name: str,
    folder_id: str = "0",
    is_base64: bool = False,  # New parameter to indicate if content is base64 encoded
) -> str:
    """
    Upload content as a file to Box using the toolkit.

    Args:
        content (str | bytes): The content to upload. Can be text or binary data.
        file_name (str): The name to give the file in Box.
        folder_id (str): The ID of the destination folder. Defaults to root ("0").
        is_base64 (bool): Whether the content is base64 encoded. Defaults to False.
    """
    box_client = get_box_client(ctx)

    try:
        # Handle base64 encoded content
        if is_base64 and isinstance(content, str):
            content = base64.b64decode(content)

        # Upload using toolkit
        result = box_upload_file(box_client, content, file_name, folder_id)
        return f"File uploaded successfully. File ID: {result['id']}, Name: {result['name']}"
    except Exception as e:
        return f"Error uploading file: {str(e)}"


async def box_download_file_tool(
    ctx: Context, file_id: str, save_file: bool = False, save_path: str | None = None
) -> str:
    """
    Download a file from Box and return its content as a string.
    Supports text files (returns content directly) and images (returns base64-encoded).
    Other file types will return an error message.
    Optionally saves the file locally.

    Args:
        file_id (str): The ID of the file to download.
        save_file (bool, optional): Whether to save the file locally. Defaults to False.
        save_path (str, optional): Path where to save the file. If not provided but save_file is True,
                                  uses a temporary directory. Defaults to None.

    return:
        str: For text files: content as string.
             For images: base64-encoded string with metadata.
             For unsupported files: error message.
             If save_file is True, includes the path where the file was saved.
    """
    box_client = get_box_client(ctx)

    # Convert file_id to string if it's not already
    if not isinstance(file_id, str):
        file_id = str(file_id)

    try:
        # Use the box_api function for downloading
        saved_path, file_content, mime_type = box_file_download(
            client=box_client, file_id=file_id, save_file=save_file, save_path=save_path
        )

        # Get file info to include name in response
        file_info = box_client.files.get_file_by_id(file_id)
        file_name = file_info.name
        file_extension = file_name.split(".")[-1].lower() if "." in file_name else ""

        # Prepare response based on content type
        response = ""
        if saved_path:
            response += f"File saved to: {saved_path}\n\n"

        # Check if file is a document (text-based file)
        is_document = (
            mime_type
            and mime_type.startswith("text/")
            or file_extension in [e.value for e in DocumentFiles]
        )

        # Check if file is an image
        is_image = (
            mime_type
            and mime_type.startswith("image/")
            or file_extension in [e.value for e in ImageFiles]
        )

        if is_document:
            # Text file - return content directly
            try:
                content_text = file_content.decode("utf-8")
                response += (
                    f"File downloaded successfully: {file_name}\n\n{content_text}"
                )
            except UnicodeDecodeError:
                # Handle case where file can't be decoded as UTF-8 despite being a "document"
                response += f"File {file_name} is a document but couldn't be decoded as text. It may be in a binary format."

        elif is_image:
            # Image file - return base64 encoded
            base64_data = base64.b64encode(file_content).decode("utf-8")
            response += f"Image downloaded successfully: {file_name}\nMIME type: {mime_type}\nBase64 encoded data:\n{base64_data}"

        else:
            # Unsupported file type for content display (but still saved if requested)
            if not saved_path:
                response += f"File {file_name} has unsupported type ({mime_type or 'unknown'}). Only text and image files are supported for content display."
            else:
                response += f"File {file_name} has unsupported type ({mime_type or 'unknown'}) for content display, but was saved successfully."

        return response

    except Exception as e:
        return f"Error downloading file: {str(e)}"
