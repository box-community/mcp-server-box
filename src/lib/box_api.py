# Copyright (c) 2024 Airbyte, Inc., all rights reserved.

import json
import logging
import dotenv
import os
from dataclasses import dataclass
from typing import Iterable, List, Union

import requests
from box_sdk_gen import (
    AiExtractResponse,
    AiItemBase,
    AiItemBaseTypeField,
    BoxCCGAuth,
    BoxClient,
    BoxSDKError,
    CCGConfig,
    CreateAiAskMode,
    CreateAiExtractStructuredFields,
    CreateAiExtractStructuredFieldsOptionsField,
    File,
    Folder,
    FolderMini,
    SearchForContentContentTypes,
    SearchForContentType,
)


logger = logging.getLogger(__name__)


@dataclass
class BoxFileExtended:
    file: File
    text_representation: str


def get_box_ccg_client() -> BoxClient:
    dotenv.load_dotenv()
    client_id = os.getenv("BOX_CLIENT_ID")
    client_secret = os.getenv("BOX_CLIENT_SECRET")
    box_subject_type = os.getenv("BOX_SUBJECT_TYPE")
    box_subject_id = os.getenv("BOX_SUBJECT_ID")

    if box_subject_type == "enterprise":
        enterprise_id = box_subject_id
        user_id = None
    else:
        enterprise_id = None
        user_id = box_subject_id
    ccg_config = CCGConfig(
        client_id=client_id,
        client_secret=client_secret,
        enterprise_id=enterprise_id,
        user_id=user_id,
    )
    ccg_auth = BoxCCGAuth(ccg_config)
    return add_extra_header_to_box_client(BoxClient(ccg_auth))


def add_extra_header_to_box_client(box_client: BoxClient) -> BoxClient:
    """
    Add extra headers to the Box client.

    Args:
        box_client (BoxClient): A Box client object.
        header (Dict[str, str]): A dictionary of extra headers to add to the Box client.

    Returns:
        BoxClient: A Box client object with the extra headers added.
    """
    header = {"x-box-ai-library": "mcp-server-box"}
    return box_client.with_extra_headers(extra_headers=header)


def _do_request(box_client: BoxClient, url: str):
    """
    Performs a GET request to a Box API endpoint using the provided Box client.

    This is an internal helper function and should not be called directly.

    Args:
        box_client (BoxClient): An authenticated Box client object.
        url (str): The URL of the Box API endpoint to make the request to.

    Returns:
        bytes: The content of the response from the Box API.

    Raises:
        BoxSDKError: If an error occurs while retrieving the access token.
        requests.exceptions.RequestException: If the request fails (e.g., network error,
                                             4XX or 5XX status code).
    """
    try:
        access_token = box_client.auth.retrieve_token().access_token
    except BoxSDKError as e:
        raise e

    resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    resp.raise_for_status()
    return resp.content


def box_file_get_by_id(client: BoxClient, file_id: str) -> File:
    return client.files.get_file_by_id(file_id=file_id)


def box_file_text_extract(client: BoxClient, file_id: str) -> str:
    # Request the file with the "extracted_text" representation hint
    file_text_representation = client.files.get_file_by_id(
        file_id,
        x_rep_hints="[extracted_text]",
        fields=["name", "representations"],
    )
    # Check if any representations exist
    if not file_text_representation.representations.entries:
        logger.debug(f"No representation for file {file_text_representation.id}")
        return ""

    # Find the "extracted_text" representation
    extracted_text_entry = next(
        (
            entry
            for entry in file_text_representation.representations.entries
            if entry.representation == "extracted_text"
        ),
        None,
    )
    if not extracted_text_entry:
        return ""

    # Handle cases where the extracted text needs generation
    if extracted_text_entry.status.state == "none":
        _do_request(extracted_text_entry.info.url)  # Trigger text generation

    # Construct the download URL and sanitize filename
    url = extracted_text_entry.content.url_template.replace("{+asset_path}", "")

    # Download and truncate the raw content
    raw_content = _do_request(client, url)

    # check to see if rawcontent is bytes
    if isinstance(raw_content, bytes):
        return raw_content.decode("utf-8")
    else:
        return raw_content


def box_file_ai_ask(client: BoxClient, file_id: str, prompt: str) -> str:
    mode = CreateAiAskMode.SINGLE_ITEM_QA
    ai_item = AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE)
    response = client.ai.create_ai_ask(mode=mode, prompt=prompt, items=[ai_item])
    return response.answer


def box_file_ai_extract(client: BoxClient, file_id: str, prompt: str) -> dict:
    ai_item = AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE)
    response = client.ai.create_ai_extract(prompt=prompt, items=[ai_item])

    # Return a dictionary from the json answer
    return json.loads(response.answer)


def box_file_ai_extract_structured(
    client: BoxClient, file_id: str, fields_json_str: str
) -> str:
    ai_item = AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE)
    fields_list = json.loads(fields_json_str)
    ai_fields = []
    options = []
    for field in fields_list:
        field_options = field.get("options")
        if field_options is not None:
            for option in field.get("options"):
                options.append(
                    CreateAiExtractStructuredFieldsOptionsField(key=option.get("key"))
                )

        ai_fields.append(
            CreateAiExtractStructuredFields(
                key=field.get("key"),
                description=field.get("description"),
                display_name=field.get("display_name"),
                prompt=field.get("prompt"),
                type=field.get("type"),
                options=options if options is not None and len(options) > 0 else None,
            )
        )
    response: AiExtractResponse = client.ai.create_ai_extract_structured(
        items=[ai_item], fields=ai_fields
    )
    return json.dumps(response.to_dict(), indent=2)


def box_folder_text_representation(
    client: BoxClient,
    folder_id: str,
    is_recursive: bool = False,
    by_pass_text_extraction: bool = False,
) -> Iterable[BoxFileExtended]:
    # folder items iterator
    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "file":
            file = box_file_get_by_id(client=client, file_id=item.id)
            if not by_pass_text_extraction:
                text_representation = box_file_text_extract(
                    client=client, file_id=item.id
                )
            else:
                text_representation = ""
            yield BoxFileExtended(file=file, text_representation=text_representation)
        elif item.type == "folder" and is_recursive:
            yield from box_folder_text_representation(
                client=client,
                folder_id=item.id,
                is_recursive=is_recursive,
                by_pass_text_extraction=by_pass_text_extraction,
            )


def box_folder_ai_ask(
    client: BoxClient,
    folder_id: str,
    prompt: str,
    is_recursive: bool = False,
    by_pass_text_extraction: bool = False,
) -> Iterable[BoxFileExtended]:
    # folder items iterator
    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "file":
            file = box_file_get_by_id(client=client, file_id=item.id)
            if not by_pass_text_extraction:
                text_representation = box_file_ai_ask(
                    client=client, file_id=item.id, prompt=prompt
                )
            else:
                text_representation = ""
            yield BoxFileExtended(file=file, text_representation=text_representation)
        elif item.type == "folder" and is_recursive:
            yield from box_folder_ai_ask(
                client=client,
                folder_id=item.id,
                prompt=prompt,
                is_recursive=is_recursive,
                by_pass_text_extraction=by_pass_text_extraction,
            )


def box_folder_ai_extract(
    client: BoxClient,
    folder_id: str,
    prompt: str,
    is_recursive: bool = False,
    by_pass_text_extraction: bool = False,
) -> Iterable[BoxFileExtended]:
    # folder items iterator
    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "file":
            file = box_file_get_by_id(client=client, file_id=item.id)
            if not by_pass_text_extraction:
                text_representation = box_file_ai_extract(
                    client=client, file_id=item.id, prompt=prompt
                )
            else:
                text_representation = ""
            yield BoxFileExtended(file=file, text_representation=text_representation)
        elif item.type == "folder" and is_recursive:
            yield from box_folder_ai_extract(
                client=client,
                folder_id=item.id,
                prompt=prompt,
                is_recursive=is_recursive,
                by_pass_text_extraction=by_pass_text_extraction,
            )


def box_folder_ai_extract_structured(
    client: BoxClient,
    folder_id: str,
    fields_json_str: str,
    is_recursive: bool = False,
    by_pass_text_extraction: bool = False,
) -> Iterable[BoxFileExtended]:
    # folder items iterator
    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "file":
            file = box_file_get_by_id(client=client, file_id=item.id)
            if not by_pass_text_extraction:
                text_representation = box_file_ai_extract_structured(
                    client=client, file_id=item.id, fields_json_str=fields_json_str
                )
            else:
                text_representation = ""
            yield BoxFileExtended(file=file, text_representation=text_representation)
        elif item.type == "folder" and is_recursive:
            yield from box_folder_ai_extract_structured(
                client=client,
                folder_id=item.id,
                fields_json_str=fields_json_str,
                is_recursive=is_recursive,
                by_pass_text_extraction=by_pass_text_extraction,
            )


def box_search(
    client: BoxClient,
    query: str,
    file_extensions: List[str] | None = None,
    content_types: List[SearchForContentContentTypes] | None = None,
    ancestor_folder_ids: List[str] | None = None,
) -> List[File]:
    # content_types: List[SearchForContentContentTypes] = [
    #     SearchForContentContentTypes.NAME,
    #     SearchForContentContentTypes.DESCRIPTION,
    #     # SearchForContentContentTypes.FILE_CONTENT,
    #     SearchForContentContentTypes.COMMENTS,
    #     SearchForContentContentTypes.TAG,
    # ]
    type = [
        SearchForContentType.FILE,
    ]
    fields: List[str] = ["id", "name", "type", "size", "description"]

    search_results = client.search.search_for_content(
        query=query,
        file_extensions=file_extensions,
        ancestor_folder_ids=ancestor_folder_ids,
        content_types=content_types,
        type=type,
        fields=fields,
    )
    return search_results.entries


def box_locate_folder_by_name(
    client: BoxClient, folder_name: str, parent_folder_id: str = "0"
) -> List[Folder]:
    type = [
        SearchForContentType.FOLDER,
    ]
    fields: List[str] = ["id", "name", "type"]

    content_types: List[SearchForContentContentTypes] = [
        SearchForContentContentTypes.NAME,
    ]

    search_results = client.search.search_for_content(
        query=folder_name,
        # file_extensions=file_extensions,
        ancestor_folder_ids=parent_folder_id,
        content_types=content_types,
        type=type,
        fields=fields,
    )
    return search_results.entries


def box_folder_list_content(
    client: BoxClient, folder_id: str, is_recursive: bool = False
) -> List[Union[File, Folder]]:
    # fields = "id,name,type"
    result: List[Union[File, FolderMini]] = []

    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "web_link":
            continue
        if item.type == "folder" and is_recursive:
            result.extend(box_folder_list_content(client, item.id, is_recursive))
        result.append(item)

    return result
