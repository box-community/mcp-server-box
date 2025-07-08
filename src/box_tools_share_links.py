"""Box share link tools for MCP server."""
from typing import Optional
from mcp import Context
from box_tools_generic import get_box_client
from box_sdk_gen.schemas import FileFull, SharedLink
from box_sdk_gen.managers.shared_links_files import (
    UpdateFileSharedLinkSharedLink,
    UpdateFileSharedLinkSharedLinkAccessField,
    UpdateFileSharedLinkSharedLinkPermissionsField
)
from datetime import datetime
import json


async def box_create_share_link_tool(
    ctx: Context,
    file_id: str,
    access: str = "open",
    password: Optional[str] = None,
    unshared_at: Optional[str] = None,
    vanity_name: Optional[str] = None,
    can_download: bool = True
) -> str:
    """
    Create a shared link for a Box file.

    Args:
        ctx (Context): The MCP context.
        file_id (str): The ID of the file to share.
        access (str, optional): The level of access. Options: 'open', 'company', 'collaborators'. Defaults to "open".
        password (str, optional): Optional password to protect the link.
        unshared_at (str, optional): The date when the link should expire (ISO-8601 format).
        vanity_name (str, optional): Defines a custom vanity name for the shared link.
        can_download (bool, optional): Whether the file can be downloaded. Defaults to True.

    Returns:
        str: The shared link information as JSON string
    """
    try:
        box_client = get_box_client(ctx)
        
        # Parse access level
        access_map = {
            "open": UpdateFileSharedLinkSharedLinkAccessField.OPEN,
            "company": UpdateFileSharedLinkSharedLinkAccessField.COMPANY,
            "collaborators": UpdateFileSharedLinkSharedLinkAccessField.COLLABORATORS
        }
        access_field = access_map.get(access, UpdateFileSharedLinkSharedLinkAccessField.OPEN)
        
        # Create permissions object
        permissions = UpdateFileSharedLinkSharedLinkPermissionsField(
            can_download=can_download,
            can_preview=True,
            can_edit=False
        )
        
        # Create shared link configuration
        shared_link_config = UpdateFileSharedLinkSharedLink(
            access=access_field,
            password=password,
            permissions=permissions
        )
        
        if unshared_at:
            shared_link_config.unshared_at = datetime.fromisoformat(unshared_at.replace('Z', '+00:00'))
        
        if vanity_name:
            shared_link_config.vanity_name = vanity_name
        
        # Update file with shared link
        updated_file: FileFull = box_client.files.update_file_by_id(
            file_id=file_id,
            shared_link=shared_link_config
        )
        
        if updated_file.shared_link:
            result = {
                "url": updated_file.shared_link.url,
                "download_url": updated_file.shared_link.download_url,
                "vanity_url": updated_file.shared_link.vanity_url,
                "access": updated_file.shared_link.access,
                "effective_access": updated_file.shared_link.effective_access,
                "effective_permission": updated_file.shared_link.effective_permission,
                "is_password_enabled": updated_file.shared_link.is_password_enabled,
                "download_count": updated_file.shared_link.download_count,
                "preview_count": updated_file.shared_link.preview_count,
                "permissions": {
                    "can_download": updated_file.shared_link.permissions.can_download if updated_file.shared_link.permissions else None,
                    "can_preview": updated_file.shared_link.permissions.can_preview if updated_file.shared_link.permissions else None,
                    "can_edit": updated_file.shared_link.permissions.can_edit if updated_file.shared_link.permissions else None
                } if updated_file.shared_link.permissions else None
            }
            
            if updated_file.shared_link.unshared_at:
                result["unshared_at"] = updated_file.shared_link.unshared_at.isoformat()
                
            return json.dumps(result)
        else:
            return json.dumps({"error": "Failed to create shared link"})
            
    except Exception as e:
        return json.dumps({"error": str(e)})


async def box_get_shared_link_tool(ctx: Context, file_id: str) -> str:
    """
    Get an existing shared link for a Box file.

    Args:
        ctx (Context): The MCP context.
        file_id (str): The ID of the file.
        
    Returns:
        str: The shared link information or a message that no shared link exists.
    """
    try:
        box_client = get_box_client(ctx)
        
        # Get file information including shared link
        file: FileFull = box_client.files.get_file_by_id(
            file_id=file_id,
            fields=["shared_link"]
        )
        
        if file.shared_link:
            result = {
                "url": file.shared_link.url,
                "download_url": file.shared_link.download_url,
                "vanity_url": file.shared_link.vanity_url,
                "access": file.shared_link.access,
                "effective_access": file.shared_link.effective_access,
                "effective_permission": file.shared_link.effective_permission,
                "is_password_enabled": file.shared_link.is_password_enabled,
                "download_count": file.shared_link.download_count,
                "preview_count": file.shared_link.preview_count,
                "permissions": {
                    "can_download": file.shared_link.permissions.can_download if file.shared_link.permissions else None,
                    "can_preview": file.shared_link.permissions.can_preview if file.shared_link.permissions else None,
                    "can_edit": file.shared_link.permissions.can_edit if file.shared_link.permissions else None
                } if file.shared_link.permissions else None
            }
            
            if file.shared_link.unshared_at:
                result["unshared_at"] = file.shared_link.unshared_at.isoformat()
                
            return json.dumps(result)
        else:
            return json.dumps({"message": "No shared link exists for this file"})
            
    except Exception as e:
        return json.dumps({"error": str(e)})


async def box_remove_shared_link_tool(ctx: Context, file_id: str) -> str:
    """
    Remove a shared link from a Box file.

    Args:
        ctx (Context): The MCP context.
        file_id (str): The ID of the file.

    Returns:
        str: Confirmation message.
    """
    try:
        box_client = get_box_client(ctx)
        
        # Remove shared link by setting it to None
        box_client.files.update_file_by_id(
            file_id=file_id,
            shared_link={}  # Empty dict removes the shared link
        )
        
        return json.dumps({"message": "Shared link removed successfully"})
        
    except Exception as e:
        return json.dumps({"error": str(e)})