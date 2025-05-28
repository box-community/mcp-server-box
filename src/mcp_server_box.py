import base64
import json
import os

# from mcp.server import Server
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator, List, cast, Union


from box_ai_agents_toolkit import (
    BoxClient,
    DocumentFiles,
    File,
    Folder,
    ImageFiles,
    SearchForContentContentTypes,
    box_claude_ai_agent_ask,
    box_claude_ai_agent_extract,
    box_create_folder,
    box_delete_folder,
    box_file_ai_ask,
    box_hubs_ai_ask,
    box_multi_file_ai_ask,
    box_file_ai_extract,
    box_file_download,
    box_file_text_extract,
    box_folder_list_content,
    box_locate_folder_by_name,
    box_search,
    box_update_folder,
    box_upload_file,
    authorize_app,
    get_oauth_client,
    box_docgen_create_batch,
    box_docgen_get_job_by_id,
    box_docgen_list_jobs,
    box_docgen_list_jobs_by_batch,
    box_docgen_template_create,
    box_docgen_template_list,
    box_docgen_template_delete,
    box_docgen_template_get_by_id,
    box_docgen_template_list_tags,
    box_docgen_template_list_jobs,
    box_docgen_create_batch_from_user_input
)

from mcp.server.fastmcp import Context, FastMCP

# # Disable all logging
logging.basicConfig(level=logging.CRITICAL)
for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# Override the logging call that's visible in the original code
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)


@dataclass
class BoxContext:
    client: BoxClient = None


@asynccontextmanager
async def box_lifespan(server: FastMCP) -> AsyncIterator[BoxContext]:
    """Manage Box client lifecycle with OAuth handling"""
    try:
        client = get_oauth_client()
        yield BoxContext(client=client)
    # except Exception as e:
    #     logger.error(f"Error: {e}")
    finally:
        # Cleanup (if needed)
        pass


# Initialize FastMCP server
mcp = FastMCP("Box MCP Server", lifespan=box_lifespan)
# mcp = Server("Box MCP Server", lifespan=box_lifespan)


@mcp.tool()
async def box_who_am_i(ctx: Context) -> str:
    """
    Get the current user's information.
    This is also useful to check the connection status.

    return:
        str: The current user's information.
    """
    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    # Get the current user's information
    current_user = box_client.users.get_user_me()

    return f"Authenticated as: {current_user.name}"


@mcp.tool()
async def box_authorize_app_tool() -> str:
    """
    Authorize the Box application.
    Start the Box app authorization process

    return:
        str: Message
    """

    #logger.info("Authorizing Box application")
    result = authorize_app()
    if result:
        return "Box application authorized successfully"
    else:
        return "Box application not authorized"


@mcp.tool()
async def box_search_tool(
    ctx: Context,
    query: str,
    file_extensions: List[str] | None = None,
    where_to_look_for_query: List[str] | None = None,
    ancestor_folder_ids: List[str] | None = None,
) -> str:
    """
    Search for files in Box with the given query.

    Args:
        query (str): The query to search for.
        file_extensions (List[str]): The file extensions to search for, for example *.pdf
        content_types (List[SearchForContentContentTypes]): where to look for the information, possible values are:
            NAME
            DESCRIPTION,
            FILE_CONTENT,
            COMMENTS,
            TAG,
        ancestor_folder_ids (List[str]): The ancestor folder IDs to search in.
    return:
        str: The search results.
    """
    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    # Convert the where to look for query to content types
    content_types: List[SearchForContentContentTypes] = []
    if where_to_look_for_query:
        for content_type in where_to_look_for_query:
            content_types.append(SearchForContentContentTypes[content_type])

    # Search for files with the query
    search_results = box_search(
        box_client, query, file_extensions, content_types, ancestor_folder_ids
    )

    # Return the "id", "name", "description" of the search results
    search_results = [
        f"{file.name} (id:{file.id})"
        + (f" {file.description}" if file.description else "")
        for file in search_results
    ]

    return "\n".join(search_results)


@mcp.tool()
async def box_read_tool(ctx: Context, file_id: str) -> str:
    """
    Read the text content of a file in Box.

    Args:
        file_id (str): The ID of the file to read.
    return:
        str: The text content of the file.
    """
    # log parameters and its type
    # logging.info(f"file_id: {file_id}, type: {type(file_id)}")
    
    # check if file id isn't a string and convert to a string
    if not isinstance(file_id, str):
        file_id = str(file_id)

    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    response = box_file_text_extract(box_client, file_id)

    return response


@mcp.tool()
async def box_ask_ai_tool(ctx: Context, file_id: str, prompt: str) -> str:
    """
    Ask box ai about a file in Box.

    Args:
        file_id (str): The ID of the file to read.
        prompt (str): The prompt to ask the AI.
    return:
        str: The text content of the file.
    """
    # log parameters and its type
    # logging.info(f"file_id: {file_id}, type: {type(file_id)}")

    # check if file id isn't a string and convert to a string
    if not isinstance(file_id, str):
        file_id = str(file_id)

    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client
    #ai_agent = box_claude_ai_agent_ask()
    response = box_file_ai_ask(box_client, file_id, prompt=prompt)

    return response


@mcp.tool()
async def box_ask_ai_tool_multi_file(
    ctx: Context, file_ids: List[str], prompt: str
) -> str:
    """
    Use Box AI to analyze and respond to a prompt based on the content of multiple files.

    This tool allows users to query Box AI with a specific prompt, leveraging the content
    of multiple files stored in Box. The AI processes the files and generates a response
    based on the provided prompt.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): A list of file IDs to be analyzed by the AI.
        prompt (str): The prompt or question to ask the AI.

    Returns:
        str: The AI-generated response based on the content of the specified files.

    Raises:
        Exception: If there is an issue with the Box client, AI agent, or file processing.
    """

    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client
    # ai_agent = box_claude_ai_agent_ask()
    response = box_multi_file_ai_ask(
        box_client, file_ids, prompt=prompt
    )

    return response

@mcp.tool()
async def box_hubs_ask_ai_tool(ctx: Context, hubs_id: Any, prompt: str) -> str:
    """
    Ask box ai about a hub in Box. Currently there is no way to discover a hub 
    in Box, so you need to know the id of the hub. We will fix this in the future.

    Args:
        hubs_id (str): The ID of the hub to read.
        prompt (str): The prompt to ask the AI.
    return:
        str: The text content of the file.
    """
    # log parameters and its type
    logging.info(f"file_id: {hubs_id}, type: {type(hubs_id)}")

    # check if file id isn't a string and convert to a string
    if not isinstance(hubs_id, str):
        hubs_id = str(hubs_id)

    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client
    ai_agent = box_claude_ai_agent_ask()
    response = box_hubs_ai_ask(box_client, hubs_id, prompt=prompt, ai_agent=ai_agent)

    return response


@mcp.tool()
async def box_search_folder_by_name(ctx: Context, folder_name: str) -> str:
    """
    Locate a folder in Box by its name.

    Args:
        folder_name (str): The name of the folder to locate.
    return:
        str: The folder ID.
    """

    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    search_results = box_locate_folder_by_name(box_client, folder_name)

    # Return the "id", "name", "description" of the search results
    search_results = [f"{folder.name} (id:{folder.id})" for folder in search_results]

    return "\n".join(search_results)


@mcp.tool()
async def box_ai_extract_data(ctx: Context, file_id: str, fields: str) -> str:
    """ "
    Extract data from a single file in Box using AI.

    Args:
        file_id (str): The ID of the file to read.
        fields (str): The fields to extract from the file.
    return:
        str: The extracted data in a json string format.
    """
    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    # check if file id isn't a string and convert to a string
    if not isinstance(file_id, str):
        file_id = str(file_id)

    # ai_agent = box_claude_ai_agent_extract()
    response = box_file_ai_extract(box_client, file_id, fields)

    return json.dumps(response)


@mcp.tool()
async def box_list_folder_content_by_folder_id(
    ctx: Context,
    folder_id: str,
    is_recursive: bool = False,
) -> str:
    """
    List the content of a folder in Box by its ID.

    Args:
        folder_id (str): The ID of the folder to list the content of.
        is_recursive (bool): Whether to list the content recursively.

    return:
        str: The content of the folder in a json string format, including the "id", "name", "type", and "description".
    """
    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    # check if file id isn't a string and convert to a string
    if not isinstance(folder_id, str):
        folder_id = str(folder_id)

    response: List[Union[File, Folder]] = box_folder_list_content(
        box_client, folder_id, is_recursive
    )

    # Convert the response to a json string

    response = [
        {
            "id": item.id,
            "name": item.name,
            "type": item.type,
            "description": item.description if hasattr(item, "description") else None,
        }
        for item in response
    ]
    return json.dumps(response)


@mcp.tool()
async def box_manage_folder_tool(
    ctx: Context,
    action: str,
    folder_id: str = "",       # Required for delete and update; empty means not provided
    name: str = "",            # Required for create; empty means not provided
    parent_id: str = "",       # Optional for create; empty means root
    description: str = "",     # Optional for update
    recursive: bool = False,     # Optional for delete
) -> str:
    """
    Manage Box folders - create, delete, or update.

    Args:
        action (str): The action to perform: "create", "delete", or "update"
        folder_id (str | None): The ID of the folder (required for delete and update)
        name (str | None): The name for the folder (required for create, optional for update)
        parent_id (str | None): The ID of the parent folder (required for create, optional for update)
                       Root folder is "0" or 0.
        description (str): Description for the folder (optional for update)
        recursive (bool): Whether to delete recursively (optional for delete)

    return:
        str: Result of the operation
    """
    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    # Validate and normalize inputs
    if action.lower() not in ["create", "delete", "update"]:
        return f"Invalid action: {action}. Must be one of: create, delete, update."

    action = action.lower()

    # Convert IDs to strings if needed
    if folder_id is not None and not isinstance(folder_id, str):
        folder_id = str(folder_id)

    if parent_id is not None and not isinstance(parent_id, str):
        parent_id = str(parent_id)

    # Handle create action
    if action == "create":
        if not name:
            return "Error: name is required for create action"

        try:
            # Default to root folder ("0") if no parent_id provided
            parent_id_str = parent_id or "0"

            new_folder = box_create_folder(
                client=box_client, name=name, parent_id=parent_id_str
            )
            return f"Folder created successfully. Folder ID: {new_folder.id}, Name: {new_folder.name}"
        except Exception as e:
            return f"Error creating folder: {str(e)}"

    # Handle delete action
    elif action == "delete":
        if not folder_id:
            return "Error: folder_id is required for delete action"

        try:
            box_delete_folder(
                client=box_client, folder_id=folder_id, recursive=recursive
            )
            return f"Folder with ID {folder_id} deleted successfully"
        except Exception as e:
            return f"Error deleting folder: {str(e)}"

    # Handle update action
    elif action == "update":
        if not folder_id:
            return "Error: folder_id is required for update action"

        try:
            updated_folder = box_update_folder(
                client=box_client,
                folder_id=folder_id,
                name=name,
                description=description,
                parent_id=parent_id,
            )
            return f"Folder updated successfully. Folder ID: {updated_folder.id}, Name: {updated_folder.name}"
        except Exception as e:
            return f"Error updating folder: {str(e)}"


@mcp.tool()
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

    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

    try:
        # Normalize the path and check if file exists
        file_path_expanded = os.path.expanduser(file_path)
        if not os.path.isfile(file_path_expanded):
            return f"Error: file '{file_path}' not found."

        # Determine the file name to use
        actual_file_name = new_file_name.strip() or os.path.basename(file_path_expanded)
        # Determine file extension to detect binary types
        _, ext = os.path.splitext(actual_file_name)
        binary_exts = {".docx", ".pptx", ".xlsx", ".pdf", ".jpg", ".jpeg", ".png", ".gif"}
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


@mcp.tool()
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
    # Get the Box client
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client

    try:
        # Handle base64 encoded content
        if is_base64 and isinstance(content, str):
            content = base64.b64decode(content)
        
        # Upload using toolkit
        result = box_upload_file(box_client, content, file_name, folder_id)
        return f"File uploaded successfully. File ID: {result['id']}, Name: {result['name']}"
    except Exception as e:
        return f"Error uploading file: {str(e)}"


@mcp.tool()
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
    # Get the Box client
    box_client: BoxClient = cast(
        BoxContext, ctx.request_context.lifespan_context
    ).client

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
    
@mcp.tool()
async def box_docgen_create_batch_tool(
    ctx: Context,
    file_id: str,
    destination_folder_id: str,
    user_input_file_path: str,
    output_type: str = "pdf",
) -> str:
    """
    Generate documents from a Box Doc Gen template using a local JSON file.

    Args:
        file_id (str): ID of the template file in Box.
        destination_folder_id (str): Where to save the generated documents.
        user_input_file_path (str): Path to a local JSON file containing
            either a single dict or a list of dicts for document generation.
        output_type (str): Output format (e.g. 'pdf'). Defaults to 'pdf'.

    Returns:
        str: JSON-serialized response from Box, or an error message.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    try:
        path = os.path.expanduser(user_input_file_path)
        if not os.path.isfile(path):
            return f"Error: user_input_file_path '{user_input_file_path}' not found"
        with open(path, 'r', encoding='utf-8') as f:
            raw_input = json.load(f)

        # If no explicit generated_file_name, use any override provided in JSON
        if 'file_name' in raw_input and isinstance(raw_input, dict):
            generated_file_name = raw_input.pop('file_name')
        else:
            generated_file_name = "Test_Name"


        batch = box_docgen_create_batch_from_user_input(
            client=box_client,
            file_id=file_id,
            destination_folder_id=destination_folder_id,
            user_input=raw_input,
            generated_file_name=generated_file_name,
            output_type=output_type,
        )
        # Return the serialized batch result as pretty JSON
        return json.dumps(_serialize(batch), indent=2)
    except Exception as e:
        return f"Error generating document batch: {str(e)}"

@mcp.tool()
async def box_docgen_get_job_tool(ctx: Context, job_id: str) -> str:
    """
    Fetch a single DocGen job by its ID.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    response = box_docgen_get_job_by_id(box_client, job_id)
    # Serialize SDK object to JSON-safe structures
    return json.dumps(_serialize(response), indent=2)

@mcp.tool()
async def box_docgen_list_jobs_tool(
    ctx: Context,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all DocGen jobs for the current user (paginated).
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    response = box_docgen_list_jobs(box_client, marker=marker, limit=limit)
    # Serialize SDK object to JSON-safe structures
    return json.dumps(_serialize(response), indent=2)

@mcp.tool()
async def box_docgen_list_jobs_by_batch_tool(
    ctx: Context,
    batch_id: str,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all DocGen jobs that belong to a particular batch.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    try:
        response = box_docgen_list_jobs_by_batch(
            box_client, batch_id=batch_id, marker=marker, limit=limit
        )
        
        # Log the response type and structure for debugging
        logger.info(f"Response type: {type(response)}")
        logger.info(f"Response dir: {dir(response)}")
        
        # Create a simple dictionary with basic information
        result = {
            "batch_id": batch_id,
            "response_type": str(type(response)),
            "available_attributes": dir(response)
        }
        
        # Try to access some common attributes safely
        if hasattr(response, "total_count"):
            result["total_count"] = response.total_count
        
        if hasattr(response, "entries"):
            result["job_count"] = len(response.entries)
            result["jobs"] = []
            for job in response.entries:
                try:
                    job_info = {
                        "type": str(type(job)),
                        "attributes": dir(job)
                    }
                    # Try to safely get some common job attributes
                    for attr in ["id", "status", "created_at", "modified_at"]:
                        if hasattr(job, attr):
                            job_info[attr] = str(getattr(job, attr))
                    result["jobs"].append(job_info)
                except Exception as job_error:
                    logger.error(f"Error processing job: {str(job_error)}")
                    result["jobs"].append({"error": str(job_error)})
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error in box_docgen_list_jobs_by_batch_tool: {str(e)}")
        # Return a formatted error JSON
        return json.dumps({
            "error": str(e),
            "batch_id": batch_id,
            "details": "Error occurred while processing the response"
        }, indent=2)

@mcp.tool()
async def box_docgen_template_create_tool(ctx: Context, file_id: str) -> str:
    """
    Mark a file as a Box Doc Gen template.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    response = box_docgen_template_create(box_client, file_id)
    # The SDK returns a DocGenTemplateBase object which isn't directly JSON‑serialisable.
    # Use the common _serialize helper (defined later in this module) to convert it
    # into plain dict/list primitives before dumping to JSON.
    return json.dumps(_serialize(response))


@mcp.tool()
async def box_docgen_template_list_tool(
    ctx: Context,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all Box Doc Gen templates accessible to the user.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    templates = box_docgen_template_list(box_client, marker=marker, limit=limit)

    return json.dumps(_serialize(templates))


@mcp.tool()
async def box_docgen_template_delete_tool(ctx: Context, template_id: str) -> str:
    """
    Unmark a file as a Box Doc Gen template.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    box_docgen_template_delete(box_client, template_id)
    return json.dumps({"deleted_template": template_id})


@mcp.tool()
async def box_docgen_template_get_by_id_tool(ctx: Context, template_id: str) -> str:
    """
    Retrieve details of a specific Box Doc Gen template.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    template = box_docgen_template_get_by_id(box_client, template_id)
    return json.dumps(_serialize(template))


@mcp.tool()
async def box_docgen_template_list_tags_tool(
    ctx: Context,
    template_id: str,
    template_version_id: str | None = None,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all tags on a Box Doc Gen template.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    tags = box_docgen_template_list_tags(
        box_client,
        template_id,
        template_version_id=template_version_id,
        marker=marker,
        limit=limit,
    )
    return json.dumps(_serialize(tags))


@mcp.tool()
async def box_docgen_template_list_jobs_tool(
    ctx: Context,
    template_id: str,
    marker: str | None = None,
    limit: int | None = None,
) -> str:
    """
    List all Doc Gen jobs that used a specific template.
    """
    box_client: BoxClient = cast(BoxContext, ctx.request_context.lifespan_context).client
    jobs = box_docgen_template_list_jobs(
        box_client, template_id=template_id, marker=marker, limit=limit
    )
    return json.dumps(_serialize(jobs))

# Helper to make Box SDK objects JSON‑serialisable
def _serialize(obj):
    """Recursively convert Box SDK objects (which expose __dict__) into
    plain dict / list structures so they can be json.dumps‑ed."""

    if isinstance(obj, list):
        return [_serialize(i) for i in obj]

    # Primitive types are fine
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj

    # Handle dictionary-like objects
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}

    # SDK models generally have __dict__ with public attributes
    try:
        if hasattr(obj, "__dict__"):
            return {k: _serialize(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
        
        # Try to get all public attributes if __dict__ is not available
        return {k: _serialize(getattr(obj, k)) for k in dir(obj) 
                if not k.startswith("_") and not callable(getattr(obj, k))}
    except Exception:
        # If all else fails, convert to string
        return str(obj)


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
