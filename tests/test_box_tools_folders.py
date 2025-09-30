import pytest

from tools.box_tools_folders import (
    box_list_folder_content_by_folder_id,
    box_manage_folder_tool,
)


@pytest.mark.asyncio
async def test_box_api_list_content_folders(ctx):
    # This folder only has folders
    items: dict = await box_list_folder_content_by_folder_id(ctx, "298939523710")

    assert len(items) > 0
    # check if items are files or folder in their type
    assert all(item.get("type") in ["file", "folder"] for item in items)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_box_api_list_content_files(ctx):
    # This filter only has files
    items = await box_list_folder_content_by_folder_id(ctx, "298939487242")

    assert len(items) > 0
    assert all(item.get("type") in ["file", "folder"] for item in items)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_box_manage_folder_create(ctx):
    # Create a folder in the root directory
    response = await box_manage_folder_tool(
        ctx,
        action="create",
        name="Test Folder",
        parent_id="0",  # Root folder
    )

    assert response is not None
    assert isinstance(response, str)
    assert "Test Folder" in response


@pytest.mark.skip
@pytest.mark.asyncio
async def test_box_manage_folder_update(ctx):
    # Create a folder first to update it
    create_response = await box_manage_folder_tool(
        ctx,
        action="create",
        name="Folder to Update",
        parent_id="0",  # Root folder
    )

    assert create_response is not None
    assert isinstance(create_response, str)

    # Extract folder ID from the response
    folder_id = create_response.split(" ")[-1]

    # Update the folder
    update_response = await box_manage_folder_tool(
        ctx,
        action="update",
        folder_id=folder_id,
        name="Updated Folder Name",
    )

    assert update_response is not None
    assert isinstance(update_response, str)
    assert "Updated Folder Name" in update_response


@pytest.mark.skip
@pytest.mark.asyncio
async def test_box_manage_folder_delete(ctx):
    # Create a folder first to delete it
    create_response = await box_manage_folder_tool(
        ctx,
        action="create",
        name="Folder to Delete",
        parent_id="0",  # Root folder
    )

    assert create_response is not None
    assert isinstance(create_response, str)

    # Extract folder ID from the response
    folder_id = create_response.split(" ")[-1]

    # Delete the folder
    delete_response = await box_manage_folder_tool(
        ctx,
        action="delete",
        folder_id=folder_id,
        recursive=True,  # Ensure all contents are deleted
    )

    assert delete_response is not None
    assert isinstance(delete_response, str)
    assert "deleted" in delete_response.lower()
