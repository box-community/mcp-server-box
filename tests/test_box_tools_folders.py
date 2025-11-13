from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from tools.box_tools_folders import (
    box_folder_copy_tool,
    box_folder_create_tool,
    box_folder_delete_tool,
    box_folder_favorites_add_tool,
    box_folder_favorites_remove_tool,
    box_folder_info_tool,
    box_folder_items_list_tool,
    box_folder_list_tags_tool,
    box_folder_move_tool,
    box_folder_rename_tool,
    box_folder_set_collaboration_tool,
    box_folder_set_description_tool,
    box_folder_set_sync_tool,
    box_folder_set_upload_email_tool,
    box_folder_tag_add_tool,
    box_folder_tag_remove_tool,
)


@pytest.mark.asyncio
async def test_box_folder_copy_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    destination_parent_folder_id = "67890"
    with (
        patch("tools.box_tools_folders.box_folder_copy") as mock_copy,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_copy.return_value = {"id": "999", "name": "Copied Folder"}
        result = await box_folder_copy_tool(ctx, folder_id, destination_parent_folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "999"
        mock_copy.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            destination_parent_folder_id=destination_parent_folder_id,
            name=None,
        )


@pytest.mark.asyncio
async def test_box_folder_copy_tool_with_name():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    destination_parent_folder_id = "67890"
    new_name = "New Folder Name"
    with (
        patch("tools.box_tools_folders.box_folder_copy") as mock_copy,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_copy.return_value = {"id": "999", "name": new_name}
        result = await box_folder_copy_tool(
            ctx, folder_id, destination_parent_folder_id, new_name
        )
        assert isinstance(result, dict)
        assert result["name"] == new_name
        mock_copy.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            destination_parent_folder_id=destination_parent_folder_id,
            name=new_name,
        )


@pytest.mark.asyncio
async def test_box_folder_create_tool():
    ctx = MagicMock(spec=Context)
    folder_name = "Test Folder"
    with (
        patch("tools.box_tools_folders.box_folder_create") as mock_create,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "123", "name": folder_name}
        result = await box_folder_create_tool(ctx, folder_name)
        assert isinstance(result, dict)
        assert result["name"] == folder_name
        mock_create.assert_called_once_with(
            client="client", name=folder_name, parent_folder_id="0"
        )


@pytest.mark.asyncio
async def test_box_folder_create_tool_with_parent():
    ctx = MagicMock(spec=Context)
    folder_name = "Test Folder"
    parent_folder_id = "456"
    with (
        patch("tools.box_tools_folders.box_folder_create") as mock_create,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_create.return_value = {"id": "123", "name": folder_name}
        result = await box_folder_create_tool(ctx, folder_name, parent_folder_id)
        assert isinstance(result, dict)
        mock_create.assert_called_once_with(
            client="client", name=folder_name, parent_folder_id=parent_folder_id
        )


@pytest.mark.asyncio
async def test_box_folder_delete_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_delete") as mock_delete,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_delete.return_value = {"message": "Folder deleted"}
        result = await box_folder_delete_tool(ctx, folder_id)
        assert isinstance(result, dict)
        mock_delete.assert_called_once_with(
            client="client", folder_id=folder_id, recursive=False
        )


@pytest.mark.asyncio
async def test_box_folder_delete_tool_recursive():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_delete") as mock_delete,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_delete.return_value = {"message": "Folder deleted recursively"}
        result = await box_folder_delete_tool(ctx, folder_id, recursive=True)
        assert isinstance(result, dict)
        mock_delete.assert_called_once_with(
            client="client", folder_id=folder_id, recursive=True
        )


@pytest.mark.asyncio
async def test_box_folder_favorites_add_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_favorites_add") as mock_add,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_add.return_value = {"id": "12345", "is_favorite": True}
        result = await box_folder_favorites_add_tool(ctx, folder_id)
        assert isinstance(result, dict)
        assert result["is_favorite"] is True
        mock_add.assert_called_once_with(client="client", folder_id=folder_id)


@pytest.mark.asyncio
async def test_box_folder_favorites_remove_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_favorites_remove") as mock_remove,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_remove.return_value = {"id": "12345", "is_favorite": False}
        result = await box_folder_favorites_remove_tool(ctx, folder_id)
        assert isinstance(result, dict)
        assert result["is_favorite"] is False
        mock_remove.assert_called_once_with(client="client", folder_id=folder_id)


@pytest.mark.asyncio
async def test_box_folder_info_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_info") as mock_info,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_info.return_value = {"id": "12345", "name": "Test Folder"}
        result = await box_folder_info_tool(ctx, folder_id)
        assert isinstance(result, dict)
        assert result["id"] == "12345"
        mock_info.assert_called_once_with(client="client", folder_id=folder_id)


@pytest.mark.asyncio
async def test_box_folder_items_list_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_items_list") as mock_list,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = {"entries": []}
        result = await box_folder_items_list_tool(ctx, folder_id)
        assert isinstance(result, dict)
        mock_list.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            is_recursive=False,
            limit=1000,
        )


@pytest.mark.asyncio
async def test_box_folder_items_list_tool_recursive():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_items_list") as mock_list,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list.return_value = {"entries": []}
        result = await box_folder_items_list_tool(
            ctx, folder_id, is_recursive=True, limit=500
        )
        assert isinstance(result, dict)
        mock_list.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            is_recursive=True,
            limit=500,
        )


@pytest.mark.asyncio
async def test_box_folder_list_tags_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_list_tags") as mock_list_tags,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_list_tags.return_value = [{"id": "1", "tag": "important"}]
        result = await box_folder_list_tags_tool(ctx, folder_id)
        assert isinstance(result, list)
        mock_list_tags.assert_called_once_with(client="client", folder_id=folder_id)


@pytest.mark.asyncio
async def test_box_folder_move_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    destination_parent_folder_id = "67890"
    with (
        patch("tools.box_tools_folders.box_folder_move") as mock_move,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_move.return_value = {"id": "12345", "parent": {"id": "67890"}}
        result = await box_folder_move_tool(ctx, folder_id, destination_parent_folder_id)
        assert isinstance(result, dict)
        mock_move.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            destination_parent_folder_id=destination_parent_folder_id,
        )


@pytest.mark.asyncio
async def test_box_folder_rename_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    new_name = "Renamed Folder"
    with (
        patch("tools.box_tools_folders.box_folder_rename") as mock_rename,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_rename.return_value = {"id": "12345", "name": new_name}
        result = await box_folder_rename_tool(ctx, folder_id, new_name)
        assert isinstance(result, dict)
        assert result["name"] == new_name
        mock_rename.assert_called_once_with(
            client="client", folder_id=folder_id, new_name=new_name
        )


@pytest.mark.asyncio
async def test_box_folder_set_collaboration_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_set_collaboration") as mock_collab,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_collab.return_value = {"id": "12345", "type": "folder"}
        result = await box_folder_set_collaboration_tool(
            ctx, folder_id, False, False, True
        )
        assert isinstance(result, dict)
        mock_collab.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            can_non_owners_invite=False,
            can_non_owners_view_collaborators=False,
            is_collaboration_restricted_to_enterprise=True,
        )


@pytest.mark.asyncio
async def test_box_folder_set_description_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    description = "Test description"
    with (
        patch("tools.box_tools_folders.box_folder_set_description") as mock_desc,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_desc.return_value = {"id": "12345", "description": description}
        result = await box_folder_set_description_tool(ctx, folder_id, description)
        assert isinstance(result, dict)
        assert result["description"] == description
        mock_desc.assert_called_once_with(
            client="client", folder_id=folder_id, description=description
        )


@pytest.mark.asyncio
async def test_box_folder_set_sync_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    sync_state = "synced"
    with (
        patch("tools.box_tools_folders.box_folder_set_sync") as mock_sync,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_sync.return_value = {"id": "12345", "sync_state": sync_state}
        result = await box_folder_set_sync_tool(ctx, folder_id, sync_state)
        assert isinstance(result, dict)
        assert result["sync_state"] == sync_state
        mock_sync.assert_called_once_with(
            client="client", folder_id=folder_id, sync_state=sync_state
        )


@pytest.mark.asyncio
async def test_box_folder_set_upload_email_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    with (
        patch("tools.box_tools_folders.box_folder_set_upload_email") as mock_email,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_email.return_value = {"id": "12345", "upload_email_access": "collaborators"}
        result = await box_folder_set_upload_email_tool(ctx, folder_id)
        assert isinstance(result, dict)
        mock_email.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            folder_upload_email_access="collaborators",
        )


@pytest.mark.asyncio
async def test_box_folder_set_upload_email_tool_custom_access():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    access_level = "open"
    with (
        patch("tools.box_tools_folders.box_folder_set_upload_email") as mock_email,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_email.return_value = {"id": "12345", "upload_email_access": access_level}
        result = await box_folder_set_upload_email_tool(ctx, folder_id, access_level)
        assert isinstance(result, dict)
        mock_email.assert_called_once_with(
            client="client",
            folder_id=folder_id,
            folder_upload_email_access=access_level,
        )


@pytest.mark.asyncio
async def test_box_folder_tag_add_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    tag = "important"
    with (
        patch("tools.box_tools_folders.box_folder_tag_add") as mock_tag_add,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_tag_add.return_value = {"id": "12345", "tags": ["important"]}
        result = await box_folder_tag_add_tool(ctx, folder_id, tag)
        assert isinstance(result, dict)
        mock_tag_add.assert_called_once_with(
            client="client", folder_id=folder_id, tag=tag
        )


@pytest.mark.asyncio
async def test_box_folder_tag_remove_tool():
    ctx = MagicMock(spec=Context)
    folder_id = "12345"
    tag = "important"
    with (
        patch("tools.box_tools_folders.box_folder_tag_remove") as mock_tag_remove,
        patch("tools.box_tools_folders.get_box_client") as mock_get_client,
    ):
        mock_get_client.return_value = "client"
        mock_tag_remove.return_value = {"id": "12345", "tags": []}
        result = await box_folder_tag_remove_tool(ctx, folder_id, tag)
        assert isinstance(result, dict)
        mock_tag_remove.assert_called_once_with(
            client="client", folder_id=folder_id, tag=tag
        )
