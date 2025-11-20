# Box Tools AI

This document describes the tools available in the `box_tools_ai` module, which provide AI-powered capabilities for interacting with Box files and hubs. These tools leverage Box AI agents to answer questions, extract data, and process content from files and hubs stored in Box.

## Available Tools

### Question & Analysis Tools

#### 1. `box_ai_ask_file_single_tool`
Ask Box AI a question about a single file. Returns AI-generated response based on the file's content.
- **Arguments:**
  - `file_id` (str): ID of the Box file
  - `prompt` (str): Question or instruction for the AI
  - `ai_agent_id` (str, optional): Specific AI agent to use (defaults to default agent)
- **Returns:** dict with AI response
- **Use Case:** Get insights, summaries, or answers about a single document

#### 2. `box_ai_ask_file_multi_tool`
Ask Box AI a question about multiple files together. Returns a single AI-generated response analyzing all provided files.
- **Arguments:**
  - `file_ids` (list[str]): List of Box file IDs
  - `prompt` (str): Question or instruction for the AI
  - `ai_agent_id` (str, optional): Specific AI agent to use (defaults to default agent)
- **Returns:** dict with AI response analyzing all files
- **Use Case:** Compare documents, synthesize information across multiple files, or get comprehensive analysis

#### 3. `box_ai_ask_hub_tool`
Ask Box AI a question about a Box hub. Returns AI-generated response based on the hub's content.
- **Arguments:**
  - `hub_id` (str): ID of the Box hub
  - `prompt` (str): Question or instruction for the AI
  - `ai_agent_id` (str, optional): Specific AI agent to use (defaults to default agent)
- **Returns:** dict with AI response
- **Use Case:** Query knowledge across an entire hub or project workspace

---

### Data Extraction Tools

#### 4. `box_ai_extract_freeform_tool`
Extract or analyze information from files using natural language prompts. Returns unstructured data as a single comprehensive response.

**Best for:** Flexible, exploratory data extraction when you don't need strict structure.

- **Arguments:**
  - `file_ids` (list[str]): List of file IDs to analyze
  - `prompt` (str): Natural language question or extraction instruction
  - `ai_agent_id` (str, optional): Specific AI agent to use
- **Returns:** dict with extracted/analyzed information
- **Use Cases:**
  - "What are the key terms of this contract?"
  - "Compare the pricing across these three proposals and summarize differences"
  - "Based on these financial documents, what are the main risk factors?"
  - "Provide a 3-paragraph summary of the main points across these meeting notes"
- **Note:** Returns ONE comprehensive answer when multiple files provided. For analyzing each file separately, call the tool once per file.

#### 5. `box_ai_extract_structured_using_fields_tool`
Extract structured data from files by defining custom fields on-the-fly. Returns data as a single structured record.

**Best for:** Ad-hoc extraction with custom fields without needing pre-existing templates.

- **Arguments:**
  - `file_ids` (list[str]): IDs of files to read
  - `fields` (list[dict]): Custom field definitions
  - `ai_agent_id` (str, optional): Specific AI agent to use
- **Returns:** dict with structured extracted data
- **Field Types Supported:** string, date, enum, multiSelect, float, etc.
- **Example Field Definition:**
  ```json
  {
    "type": "string",
    "key": "contract_value",
    "displayName": "Contract Value",
    "description": "The total monetary value of the contract"
  }
  ```
- **Use Cases:**
  - Extract "contract_value" and "signing_date" from a contract
  - Combine data from a proposal and budget document into one record
  - Extract insurance policy details from multiple documents

#### 6. `box_ai_extract_structured_using_template_tool`
Extract structured data from files using a predefined Box metadata template. Returns data populating a single metadata instance.

**Best for:** Extraction using existing metadata templates defined in Box.

- **Arguments:**
  - `file_ids` (list[str]): IDs of files to read
  - `template_key` (str): Key of the metadata template to use
  - `ai_agent_id` (str, optional): Specific AI agent to use
- **Returns:** dict with structured extracted data
- **Use Cases:**
  - Extract invoice data using an "invoice" template
  - Extract customer info from multiple sources into one template instance

#### 7. `box_ai_extract_structured_enhanced_using_fields_tool`
Enhanced version of field-based extraction with improved accuracy and better handling of complex documents.

**Best for:** Complex documents, handwritten content, or low-quality scans where standard extraction may struggle.

- **Arguments:**
  - `file_ids` (list[str]): IDs of files to read
  - `fields` (list[dict]): Custom field definitions
- **Returns:** dict with structured extracted data
- **Enhanced Features:**
  - Uses advanced AI models (e.g., Google Gemini)
  - Better handling of complex document layouts
  - More robust extraction for handwritten or low-quality scans
  - Improved understanding of complex field relationships

#### 8. `box_ai_extract_structured_enhanced_using_template_tool`
Enhanced version of template-based extraction with improved accuracy for complex documents.

**Best for:** Complex documents with existing metadata templates.

- **Arguments:**
  - `file_ids` (list[str]): IDs of files to read
  - `template_key` (str): Key of the metadata template to use
- **Returns:** dict with structured extracted data
- **Enhanced Features:**
  - Uses advanced AI models for improved accuracy
  - Better handling of complex document layouts
  - More robust extraction for handwritten or low-quality scans

---

### AI Agent Management Tools

#### 9. `box_ai_agent_info_by_id_tool`
Get detailed information about a specific AI agent by its ID.
- **Arguments:**
  - `ai_agent_id` (str): ID of the AI agent
- **Returns:** dict with agent information
- **Use Case:** Retrieve configuration and details about a specific AI agent

#### 10. `box_ai_agents_list_tool`
List all available AI agents in your Box environment.
- **Arguments:**
  - `limit` (int, optional): Maximum number of agents to return (default: 1000)
- **Returns:** dict with list of available AI agents
- **Use Case:** Discover available agents before specifying agent_id in other tools

#### 11. `box_ai_agents_search_by_name_tool`
Search for AI agents by name in your Box environment.
- **Arguments:**
  - `name` (str): Name filter to search for agents
  - `limit` (int, optional): Maximum results (default: 1000)
- **Returns:** dict with matching AI agents
- **Use Case:** Find a specific agent without knowing its exact ID

---

## Extraction Tools Comparison

| Tool | Input Type | Output Type | Best For | Multiple Files |
|------|-----------|-----------|----------|----------------|
| `freeform` | Natural language | Unstructured text | Flexible analysis | Combined answer |
| `structured_fields` | Custom fields | Structured JSON | Ad-hoc extraction | Single record |
| `structured_template` | Metadata template | Structured JSON | Template-based | Single record |
| `enhanced_fields` | Custom fields | Structured JSON | Complex documents | Single record |
| `enhanced_template` | Metadata template | Structured JSON | Complex documents | Single record |

## Usage Notes

- All tools require a valid Box client context.
- AI agent selection is optional; if omitted, the default agent is used.
- **Multiple Files Behavior:**
  - Extraction tools (both freeform and structured) analyze ALL provided files together and return ONE complete answer/record
  - If you need separate results for each file, call the tool once per file
- **Enhanced Extraction:**
  - Enhanced tools provide better accuracy for difficult documents
  - May take longer to process than standard extraction
  - Recommended for handwritten content, low-quality scans, or complex layouts

## Examples

### Example 1: Analyze a Single Contract
```
Tool: box_ai_ask_file_single_tool
file_id: "12345"
prompt: "What is the contract duration and renewal date?"
```

### Example 2: Compare Multiple Proposals
```
Tool: box_ai_ask_file_multi_tool
file_ids: ["proposal1", "proposal2", "proposal3"]
prompt: "Compare the pricing, timeline, and deliverables across these proposals"
```

### Example 3: Extract Insurance Policy Data
```
Tool: box_ai_extract_structured_using_fields_tool
file_ids: ["policy_doc"]
fields: [
  {"type": "string", "key": "policy_number", "displayName": "Policy Number"},
  {"type": "date", "key": "effective_date", "displayName": "Effective Date"},
  {"type": "enum", "key": "coverage_type", "displayName": "Coverage Type", "options": [{"key": "Basic"}, {"key": "Premium"}]}
]
```

### Example 4: Extract Using Existing Template
```
Tool: box_ai_extract_structured_using_template_tool
file_ids: ["invoice_pdf"]
template_key: "invoice_template"
```

Refer to [src/tools/box_tools_ai.py](src/tools/box_tools_ai.py) for implementation details.
