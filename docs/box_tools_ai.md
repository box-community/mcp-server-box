# Box Tools AI

This document describes the tools available in the `box_tools_ai` module, which provide AI-powered capabilities for interacting with Box files and hubs. These tools leverage Box AI agents to answer questions, extract data, and process content from files and hubs stored in Box.

## Available Tools

### 1. `box_ai_ask_file_single_tool`
Ask Box AI about a single file using a prompt. Returns AI-generated response based on the file's content.
- **Arguments:**
  - `ctx`: Request context
  - `file_id`: ID of the Box file
  - `prompt`: Question or instruction for the AI
  - `ai_agent_id` (optional): Specific AI agent to use

### 2. `box_ai_ask_file_multi_tool`
Ask Box AI about multiple files using a prompt. Returns AI-generated response based on the content of multiple files.
- **Arguments:**
  - `ctx`: Request context
  - `file_ids`: List of Box file IDs
  - `prompt`: Question or instruction for the AI
  - `ai_agent_id` (optional): Specific AI agent to use

### 3. `box_ai_ask_hub_tool`
Ask Box AI about a specific hub using a prompt. Returns AI-generated response based on the hub's content.
- **Arguments:**
  - `ctx`: Request context
  - `hubs_id`: ID of the Box hub
  - `prompt`: Question or instruction for the AI
  - `ai_agent_id` (optional): Specific AI agent to use

### 4. `box_ai_extract_freeform_tool`
Extract data from Box files using a freeform prompt. Returns extracted data in JSON format.
- **Arguments:**
  - `ctx`: Request context
  - `file_ids`: List of Box file IDs
  - `prompt`: Freeform extraction prompt
  - `ai_agent_id` (optional): Specific AI agent to use

### 5. `box_ai_extract_structured_using_fields_tool`
Extract structured data from Box files by specifying fields. Returns extracted structured data in JSON format.
- **Arguments:**
  - `ctx`: Request context
  - `file_ids`: List of Box file IDs
  - `fields`: List of field definitions (see example below)
  - `ai_agent_id` (optional): Specific AI agent to use

**Field Example:**
```json
[
  {"type": "string", "key": "name", "displayName": "Name", "description": "Policyholder Name"},
  {"type": "date", "key": "effectiveDate", "displayName": "Effective Date", "description": "Policy Effective Date"}
]
```

### 6. `box_ai_extract_structured_using_template_tool`
Extract structured data from Box files using a predefined template. Returns extracted structured data in JSON format.
- **Arguments:**
  - `ctx`: Request context
  - `file_ids`: List of Box file IDs
  - `template_key`: Template ID for extraction
  - `ai_agent_id` (optional): Specific AI agent to use

### 7. `box_ai_extract_structured_enhanced_using_fields_tool`
Extract structured data from Box files by specifying fields, with enhanced processing. Returns extracted structured data in JSON format.
- **Arguments:**
  - `ctx`: Request context
  - `file_ids`: List of Box file IDs
  - `fields`: List of field definitions

### 8. `box_ai_extract_structured_enhanced_using_template_tool`
Extract structured data from Box files using a predefined template, with enhanced processing. Returns extracted structured data in JSON format.
- **Arguments:**
  - `ctx`: Request context
  - `file_ids`: List of Box file IDs
  - `template_key`: Template ID for extraction

---

## Usage Notes
- All tools require a valid Box client context (`ctx`).
- AI agent selection is optional for most tools; if omitted, the default agent is used.
- Structured extraction tools support both field-based and template-based extraction.
- Enhanced extraction tools provide improved accuracy and processing capabilities.

Refer to the source code in `src/tools/box_tools_ai.py` for implementation details and argument structures.
