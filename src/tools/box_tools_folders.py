from typing import List, Union

from box_ai_agents_toolkit import (
    File,
    Folder,
    box_create_folder,
    box_delete_folder,
    box_folder_list_content,
    box_update_folder,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_list_folder_content_by_folder_id(
    ctx: Context,
    folder_id: str,
    is_recursive: bool = False,
) -> dict:
    """
    List the content of a folder in Box by its ID.

    Args:
        folder_id (str): The ID of the folder to list the content of.
        is_recursive (bool): Whether to list the content recursively.

    return:
        dict: The content of the folder in a json string format, including the "id", "name", "type", and "description".
    """
    box_client = get_box_client(ctx)

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
    return response
    # return json.dumps(response)


async def box_manage_folder_tool(
    ctx: Context,
    action: str,
    folder_id: str = "",  # Required for delete and update; empty means not provided
    name: str = "",  # Required for create; empty means not provided
    parent_id: str = "",  # Optional for create; empty means root
    description: str = "",  # Optional for update
    recursive: bool = False,  # Optional for delete
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
    box_client = get_box_client(ctx)

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
