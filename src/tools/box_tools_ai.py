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

from tools.box_tools_generic import get_box_client


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
    Extract or analyze information from one or more files using a natural language prompt and return a SINGLE response.

    This tool provides maximum flexibility for data extraction and analysis. Instead of defining
    structured fields, you simply ask Box AI a question or give it instructions in natural language.
    When multiple files are provided, Box AI analyzes ALL files together to provide ONE comprehensive answer.

    This is the most flexible extraction tool but provides unstructured results. Use structured
    extraction tools (template-based or field-based) when you need consistent, machine-readable output.

    Use cases:
    - Single file analysis: "What are the key terms of this contract?"
    - Multiple files analysis: "Compare the pricing across these three proposals and summarize differences"
    - Complex questions: "Based on these financial documents, what are the main risk factors?"
    - Summarization: "Provide a 3-paragraph summary of the main points across these meeting notes"

    NOT for batch processing: If you need to ask the same question about multiple files
    separately (e.g., "summarize each report individually"), call this tool once per file in a loop.


    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_ids (List[str]): A list of file IDs to extract information from, example: ["1234567890", "0987654321"].
        prompt (str): The fields to extract.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for the extraction. If None, the default AI agent will be used.
    Returns:
        dict: The AI response containing the extracted information.
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
    Extract structured data from one or more files using custom fields and return a SINGLE data instance.

    This tool analyzes the provided file(s) and extracts information based on custom field
    definitions you provide. When multiple files are provided, Box AI combines information
    from ALL files to create ONE complete data record.

    Unlike template-based extraction, this tool allows you to define fields on-the-fly without
    creating a metadata template in Box first. This is useful for ad-hoc data extraction or
    when you need fields that don't match any existing template.

    Use cases:
    - Single file: Extract custom fields from one document (e.g., extract "contract_value"
      and "signing_date" from a contract)
    - Multiple files: Combine data from multiple sources into one data instance
      (e.g., extract "total_project_cost" from both a proposal and budget document)

    NOT for batch processing: If you need to extract data from multiple files as
    separate instances, call this tool once per file in a loop.

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
    Extract structured data from one or more files and return a SINGLE metadata instance.

    This tool analyzes the provided file(s) and extracts information to populate a single
    metadata instance based on the specified template. When multiple files are provided,
    Box AI combines information from ALL files to create ONE complete metadata record.

    Use cases:
    - Single file: Extract metadata from one receipt, invoice, or document
    - Multiple files: Combine data from multiple sources into one metadata instance
      (e.g., extract customer info from both a contract PDF and a supporting letter)

    NOT for batch processing: If you need to extract metadata from multiple files as
    separate instances, call this tool once per file in a loop.

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
    Extract structured data from one or more files using custom fields and return a SINGLE data instance (Enhanced version).

    This enhanced tool analyzes the provided file(s) and extracts information based on custom
    field definitions you provide. When multiple files are provided, Box AI combines information
    from ALL files to create ONE complete data record.

    Enhanced features:
    - Uses advanced AI models (e.g., Google Gemini) for improved accuracy
    - Better handling of complex document layouts and image quality
    - More robust extraction for handwritten or low-quality scans
    - Improved understanding of complex field relationships

    Unlike template-based extraction, this tool allows you to define fields on-the-fly without
    creating a metadata template in Box first. This is useful for ad-hoc data extraction or
    when you need fields that don't match any existing template.

    Use cases:
    - Single file: Extract custom fields from one document
    - Multiple files: Combine data from multiple sources into one data instance
      (e.g., extract patient info from medical records, lab results, and prescription images)

    NOT for batch processing: If you need to extract data from multiple files as
    separate instances, call this tool once per file in a loop.

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
    Extract structured data from one or more files and return a SINGLE metadata instance (Enhanced version).

    This enhanced tool analyzes the provided file(s) and extracts information to populate a
    single metadata instance based on the specified template. When multiple files are provided,
    Box AI combines information from ALL files to create ONE complete metadata record.

    Enhanced features:
    - Uses advanced AI models (e.g., Google Gemini) for improved accuracy
    - Better handling of complex document layouts and image quality
    - More robust extraction for handwritten or low-quality scans

    Use cases:
    - Single file: Extract metadata from one receipt, invoice, or document
    - Multiple files: Combine data from multiple sources into one metadata instance
      (e.g., extract project info from a proposal PDF, budget spreadsheet, and timeline image)

    NOT for batch processing: If you need to extract metadata from multiple files as
    separate instances, call this tool once per file in a loop.

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
