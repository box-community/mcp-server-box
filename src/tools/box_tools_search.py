from typing import List

from box_ai_agents_toolkit import (
    SearchForContentContentTypes,
    box_locate_folder_by_name,
    box_search,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_search_tool(
    ctx: Context,
    query: str,
    file_extensions: List[str] | None = None,
    where_to_look_for_query: List[str] | None = None,
    ancestor_folder_ids: List[str] | None = None,
) -> List[dict]:
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
        List[dict]: The search results.
    """
    box_client = get_box_client(ctx)

    # Convert the where to look for query to content types
    content_types: List[SearchForContentContentTypes] = []
    if where_to_look_for_query:
        for content_type in where_to_look_for_query:
            content_types.append(SearchForContentContentTypes[content_type])

    # Search for files with the query
    search_results = box_search(
        box_client, query, file_extensions, content_types, ancestor_folder_ids
    )

    return [search_result.to_dict() for search_result in search_results]


async def box_search_folder_by_name_tool(ctx: Context, folder_name: str) -> List[dict]:
    """
    Locate a folder in Box by its name.

    Args:
        folder_name (str): The name of the folder to locate.
    return:
        List[dict]: The folder ID.
    """
    box_client = get_box_client(ctx)
    search_results = box_locate_folder_by_name(box_client, folder_name)
    return [search_result.to_dict() for search_result in search_results]
