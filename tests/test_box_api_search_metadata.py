"""
Tests for Box API search functionality with metadata search capabilities.

These tests demonstrate how to search for files using different metadata fields
like description, tags, comments, and file content.
"""

import pytest
from typing import List

from box_ai_agents_toolkit import (
    BoxClient,
    File,
    SearchForContentContentTypes,
    box_search,
)


def test_box_search_by_description(box_client: BoxClient):
    """
    Test searching for files by description metadata.
    
    Note: This test requires files in your Box account to have descriptions.
    Update the search query to match descriptions in your test files.
    """
    # Search specifically in file descriptions
    search_results: List[File] = box_search(
        box_client, 
        "test",  # Update this to match descriptions in your Box files
        content_types=[SearchForContentContentTypes.DESCRIPTION]
    )
    
    # Verify we get results (if files with descriptions exist)
    # Note: This might return 0 results if no files have matching descriptions
    assert isinstance(search_results, list)
    
    # If results exist, verify they are files
    if search_results:
        assert all(file.type == "file" for file in search_results)


def test_box_search_by_file_content(box_client: BoxClient):
    """
    Test searching within file content.
    
    Note: This test requires files in your Box account with searchable content.
    Update the search query to match content in your test files.
    """
    # Search specifically within file content
    search_results: List[File] = box_search(
        box_client,
        "content",  # Update this to match content in your Box files  
        content_types=[SearchForContentContentTypes.FILE_CONTENT]
    )
    
    assert isinstance(search_results, list)
    
    if search_results:
        assert all(file.type == "file" for file in search_results)


def test_box_search_by_tags(box_client: BoxClient):
    """
    Test searching for files by tags.
    
    Note: This test requires files in your Box account to have tags.
    Update the search query to match tags on your test files.
    """
    # Search specifically in file tags
    search_results: List[File] = box_search(
        box_client,
        "important",  # Update this to match tags on your Box files
        content_types=[SearchForContentContentTypes.TAG]
    )
    
    assert isinstance(search_results, list)
    
    if search_results:
        assert all(file.type == "file" for file in search_results)


def test_box_search_by_comments(box_client: BoxClient):
    """
    Test searching for files by comments.
    
    Note: This test requires files in your Box account to have comments.
    Update the search query to match comments on your test files.
    """
    # Search specifically in file comments
    search_results: List[File] = box_search(
        box_client,
        "comment",  # Update this to match comments on your Box files
        content_types=[SearchForContentContentTypes.COMMENTS]
    )
    
    assert isinstance(search_results, list)
    
    if search_results:
        assert all(file.type == "file" for file in search_results)


def test_box_search_multiple_metadata_types(box_client: BoxClient):
    """
    Test searching across multiple metadata types simultaneously.
    
    This is the most comprehensive search that looks in name, description,
    content, comments, and tags.
    """
    # Search across all metadata types
    search_results: List[File] = box_search(
        box_client,
        "estate",  # Update this to match content in your Box account
        content_types=[
            SearchForContentContentTypes.NAME,
            SearchForContentContentTypes.DESCRIPTION,
            SearchForContentContentTypes.FILE_CONTENT,
            SearchForContentContentTypes.COMMENTS,
            SearchForContentContentTypes.TAG,
        ]
    )
    
    assert isinstance(search_results, list)
    
    if search_results:
        assert all(file.type == "file" for file in search_results)
        
        # Print results for debugging
        print(f"\n🔍 Found {len(search_results)} files:")
        for file in search_results[:5]:  # Limit to first 5 results
            print(f"  - {file.name} (ID: {file.id})")


def test_box_search_with_file_extensions(box_client: BoxClient):
    """
    Test searching with specific file extensions.
    
    This combines metadata search with file type filtering.
    """
    # Search for PDFs containing specific terms
    search_results: List[File] = box_search(
        box_client,
        "document",  # Update this to match your files
        file_extensions=["pdf", "doc", "docx"],
        content_types=[
            SearchForContentContentTypes.NAME,
            SearchForContentContentTypes.DESCRIPTION,
            SearchForContentContentTypes.FILE_CONTENT,
        ]
    )
    
    assert isinstance(search_results, list)
    
    if search_results:
        assert all(file.type == "file" for file in search_results)
        # Verify file extensions (if file name has extension)
        for file in search_results:
            if '.' in file.name:
                extension = file.name.split('.')[-1].lower()
                assert extension in ["pdf", "doc", "docx"], f"Unexpected file type: {extension}"


def test_box_search_estate_example(box_client: BoxClient):
    """
    Test case that matches the user's example: searching for estates with death certificates.
    
    This demonstrates a real-world search scenario.
    """
    # Search for estate-related files
    estate_results: List[File] = box_search(
        box_client,
        "estate death certificate",
        content_types=[
            SearchForContentContentTypes.NAME,
            SearchForContentContentTypes.DESCRIPTION,
            SearchForContentContentTypes.FILE_CONTENT,
            SearchForContentContentTypes.TAG,
        ]
    )
    
    assert isinstance(estate_results, list)
    
    # Print results for manual verification
    print(f"\n🏠 Estate search found {len(estate_results)} files:")
    for file in estate_results[:10]:  # Limit output
        print(f"  - {file.name} (ID: {file.id})")
        if hasattr(file, 'description') and file.description:
            print(f"    Description: {file.description}")


def test_box_search_patrick_estate_example(box_client: BoxClient):
    """
    Test case that matches the user's second example: find death certificate on patrick estate.
    
    This demonstrates a more specific search scenario.
    """
    # Search for Patrick estate death certificate
    patrick_results: List[File] = box_search(
        box_client,
        "patrick estate death certificate",
        content_types=[
            SearchForContentContentTypes.NAME,
            SearchForContentContentTypes.DESCRIPTION,
            SearchForContentContentTypes.FILE_CONTENT,
            SearchForContentContentTypes.TAG,
        ]
    )
    
    assert isinstance(patrick_results, list)
    
    # Print results for manual verification
    print(f"\n👤 Patrick estate search found {len(patrick_results)} files:")
    for file in patrick_results[:5]:  # Limit output
        print(f"  - {file.name} (ID: {file.id})")
        if hasattr(file, 'description') and file.description:
            print(f"    Description: {file.description}")


@pytest.mark.skip(reason="Enable this test only if you have specific test data")
def test_box_search_with_known_file_ids(box_client: BoxClient):
    """
    Template test for when you have specific files to test against.
    
    Update the file IDs and search terms to match your Box account.
    """
    # Example: Search for files that you know exist
    known_search_term = "HAB-1"  # Update to match your files
    
    search_results: List[File] = box_search(
        box_client,
        known_search_term,
        content_types=[SearchForContentContentTypes.NAME]
    )
    
    assert len(search_results) > 0, f"No files found for known term: {known_search_term}"
    
    # Verify specific file exists
    known_file_names = ["HAB-1-01.docx"]  # Update to match your files
    found_names = [file.name for file in search_results]
    
    for expected_name in known_file_names:
        assert any(expected_name in name for name in found_names), f"Expected file not found: {expected_name}" 