from typing import Any, List, Optional

from box_ai_agents_toolkit import (
    box_ai_ask_file_multi,  # type: ignore
    box_ai_ask_file_single,  # type: ignore
    box_ai_ask_hub,  # type: ignore
    box_ai_extract_freeform,  # type: ignore
    box_ai_extract_structured_enhanced_using_fields,  # type: ignore
    box_ai_extract_structured_enhanced_using_template,  # type: ignore
    box_ai_extract_structured_using_fields,  # type: ignore
    box_ai_extract_structured_using_template,  # type: ignore
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_ai_ask_file_single_tool(
    ctx: Context, file_id: str, prompt: str, ai_agent_id: Optional[str] = None
) -> dict:
    """
    Ask Box AI about a single file.
    This tool allows users to query Box AI with a specific prompt, leveraging the content
    of a single file stored in Box. The AI processes the file and generates a response
    based on the provided prompt.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to be analyzed by the AI.
        prompt (str): The prompt or question to ask the AI.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for processing.
    """

    box_client = get_box_client(ctx)
    response = box_ai_ask_file_single(
        box_client, file_id, prompt=prompt, ai_agent_id=ai_agent_id
    )
    return response


async def box_ai_ask_file_multi_tool(
    ctx: Context, file_ids: List[str], prompt: str, ai_agent_id: Optional[str] = None
) -> dict:
    """
    Ask Box AI about multiple files.
    This tool allows users to query Box AI with a specific prompt, leveraging the content
    of multiple files stored in Box. The AI processes the files and generates a response
    based on the provided prompt.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): A list of IDs of the files to be analyzed by the AI.
        prompt (str): The prompt or question to ask the AI.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for processing.
    """
    box_client = get_box_client(ctx)
    response = box_ai_ask_file_multi(
        box_client, file_ids, prompt=prompt, ai_agent_id=ai_agent_id
    )
    return response


async def box_ai_ask_hub_tool(
    ctx: Context, hubs_id: str, prompt: str, ai_agent_id: Optional[str] = None
) -> dict:
    """
    Ask Box AI about a specific hub.
    This tool allows users to query Box AI with a specific prompt, leveraging the content
    of a hub in Box. The AI processes the hub and generates a response based on the provided prompt.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        hubs_id (str): The ID of the hub to be analyzed by the AI.
        prompt (str): The prompt or question to ask the AI.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for processing.
    Returns:
        dict: The response from the AI, containing the answer to the prompt.
    """
    if not isinstance(hubs_id, str):
        hubs_id = str(hubs_id)

    box_client = get_box_client(ctx)
    response = box_ai_ask_hub(
        box_client, hubs_id, prompt=prompt, ai_agent_id=ai_agent_id
    )
    return response


async def box_ai_extract_freeform_tool(
    ctx: Context,
    file_ids: List[str],
    prompt: str,
    ai_agent_id: Optional[str] = None,
) -> dict:
    """
    Extract data from files in Box using AI with a freeform prompt.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): The IDs of the files to read.
        prompt (str): The freeform prompt to guide the AI extraction.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for processing.
    Returns:
        dict: The extracted data in a json string format.
    """
    box_client = get_box_client(ctx)

    response = box_ai_extract_freeform(
        box_client, file_ids, prompt=prompt, ai_agent_id=ai_agent_id
    )
    return response


async def box_ai_extract_structured_using_fields_tool(
    ctx: Context,
    file_ids: List[str],
    fields: List[dict[str, Any]],
    ai_agent_id: Optional[str] = None,
) -> dict:
    """
    Extract structured data from files in Box using AI with specified fields.
    This tool allows users to extract structured data from files by specifying the fields
    they are interested in. The AI processes the files and extracts the relevant information
    based on the provided fields.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): The IDs of the files to read.
        fields (List[dict[str, Any]]): The fields to extract from the files.
            example:[
                                    {
                                        "type": "string",
                                        "key": "name",
                                        "displayName": "Name",
                                        "description": "Policyholder Name",
                                    },
                                    {
                                        "type": "string",
                                        "key": "number",
                                        "displayName": "Number",
                                        "description": "Policy Number",
                                    },
                                    {
                                        "type": "date",
                                        "key": "effectiveDate",
                                        "displayName": "Effective Date",
                                        "description": "Policy Effective Date",
                                    },
                                    {
                                        "type": "enum",
                                        "key": "paymentTerms",
                                        "displayName": "Payment Terms",
                                        "description": "Frequency of payment per year",
                                        "options": [
                                            {"key": "Monthly"},
                                            {"key": "Quarterly"},
                                            {"key": "Semiannual"},
                                            {"key": "Annually"},
                                        ],
                                    },
                                    {
                                        "type": "multiSelect",
                                        "key": "coverageTypes",
                                        "displayName": "Coverage Types",
                                        "description": "Types of coverage for the policy",
                                        "prompt": "Look in the coverage type table and include all listed types.",
                                        "options": [
                                            {"key": "Body Injury Liability"},
                                            {"key": "Property Damage Liability"},
                                            {"key": "Personal Damage Liability"},
                                            {"key": "Collision"},
                                            {"key": "Comprehensive"},
                                            {"key": "Uninsured Motorist"},
                                            {"key": "Something that does not exist"},
                                        ],
                                    },
                                ]

        ai_agent_id (Optional[str]): The ID of the AI agent to use for processing.
    Returns:
        dict: The extracted structured data in a json string format.
    """
    box_client = get_box_client(ctx)

    response = box_ai_extract_structured_using_fields(
        box_client, file_ids, fields, ai_agent_id=ai_agent_id
    )
    return response


async def box_ai_extract_structured_using_template_tool(
    ctx: Context,
    file_ids: List[str],
    template_key: str,
    ai_agent_id: Optional[str] = None,
) -> dict:
    """
    Extract structured data from files in Box using AI with a specified template.
    This tool allows users to extract structured data from files by using a predefined template.
    The AI processes the files and extracts the relevant information based on the provided template.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): The IDs of the files to read.
        template_key (str): The ID of the template to use for extraction.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for processing.
    Returns:
        dict: The extracted structured data in a json string format.
    """
    box_client = get_box_client(ctx)

    response = box_ai_extract_structured_using_template(
        box_client, file_ids, template_key, ai_agent_id=ai_agent_id
    )
    return response


async def box_ai_extract_structured_enhanced_using_fields_tool(
    ctx: Context,
    file_ids: List[str],
    fields: List[dict[str, Any]],
) -> dict:
    """
    Extract structured data from files in Box using AI with specified fields and enhanced processing.
    This tool allows users to extract structured data from files by specifying the fields
    they are interested in, with enhanced processing capabilities.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): The IDs of the files to read.
        fields (List[dict[str, Any]]): The fields to extract from the files.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for processing.
    Returns:
        dict: The extracted structured data in a json string format.
    """
    box_client = get_box_client(ctx)

    response = box_ai_extract_structured_enhanced_using_fields(
        box_client,
        file_ids,
        fields,
    )
    return response


async def box_ai_extract_structured_enhanced_using_template_tool(
    ctx: Context,
    file_ids: List[str],
    template_key: str,
) -> dict:
    """
    Extract structured data from files in Box using AI with a specified template and enhanced processing.
    This tool allows users to extract structured data from files by using a predefined template,
    with enhanced processing capabilities.
    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): The IDs of the files to read.
        template_key (str): The ID of the template to use for extraction.
    Returns:
        dict: The extracted structured data in a json string format.
    """
    box_client = get_box_client(ctx)

    response = box_ai_extract_structured_enhanced_using_template(
        box_client, file_ids, template_key
    )
    return response
