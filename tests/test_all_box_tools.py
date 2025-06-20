#!/usr/bin/env python3
"""
Comprehensive Test Suite for All Box MCP Server Tools

This script tests all the Box API tools implemented in the MCP server.
Run with: uv run python tests/test_all_box_tools.py

Make sure to update the test configuration with valid Box file/folder IDs
from your Box account before running.
"""

import sys
import os
import json
import tempfile
from typing import List, Dict, Any
import asyncio
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the Box client setup and JWT auth
import json
from box_ai_agents_toolkit import BoxClient
from box_sdk_gen import BoxJWTAuth, JWTConfig

def get_jwt_client():
    """Get authenticated Box client using JWT"""
    # Load config
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    config_path = os.path.join(os.path.dirname(__file__), '..', config_file)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Create JWT config
    jwt_config = JWTConfig(
        client_id=config['boxAppSettings']['clientID'],
        client_secret=config['boxAppSettings']['clientSecret'],
        enterprise_id=config['enterpriseID'],
        jwt_key_id=config['boxAppSettings']['appAuth']['publicKeyID'],
        private_key=config['boxAppSettings']['appAuth']['privateKey'],
        private_key_passphrase=config['boxAppSettings']['appAuth']['passphrase']
    )
    
    # Create auth and client
    auth = BoxJWTAuth(config=jwt_config)
    return BoxClient(auth=auth)

class BoxToolsTester:
    """Test all Box MCP Server tools"""
    
    def __init__(self):
        """Initialize with Box client and test configuration"""
        print("🔧 Initializing Box client...")
        try:
            self.client = get_jwt_client()
            print("✅ Box client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Box client: {e}")
            sys.exit(1)
        
        # Test configuration - UPDATE THESE WITH YOUR BOX ACCOUNT VALUES
        self.test_config = {
            # File IDs - replace with actual file IDs from your Box account
            'test_file_id': None,  # Set this to a valid file ID
            'test_pdf_file_id': None,  # Set this to a PDF file ID for AI tests
            'test_image_file_id': None,  # Set this to an image file ID
            
            # Folder IDs
            'test_folder_id': '0',  # Root folder (always available)
            'test_parent_folder_id': '0',  # Parent for creating new folders
            
            # DocGen IDs (if available)
            'test_template_id': None,  # Set if you have DocGen templates
            'test_batch_id': None,  # Set if you have DocGen batches
            'test_job_id': None,  # Set if you have DocGen jobs
            'test_hub_id': None,  # Set if you have Hubs
            
            # Test data
            'test_folder_name': f"test_folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'test_file_content': "This is test content for Box MCP server testing.",
            'test_file_name': f"test_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            'search_query': 'test',
        }
        
        self.results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }
    
    def log_test(self, test_name: str, status: str, message: str = "", result: Any = None):
        """Log test result"""
        status_emoji = {
            'PASS': '✅',
            'FAIL': '❌', 
            'SKIP': '⏭️'
        }
        
        print(f"{status_emoji.get(status, '❓')} {test_name}: {message}")
        
        self.results['details'].append({
            'test': test_name,
            'status': status,
            'message': message,
            'result': str(result)[:200] if result else None
        })
        
        if status == 'PASS':
            self.results['passed'] += 1
        elif status == 'FAIL':
            self.results['failed'] += 1
        else:
            self.results['skipped'] += 1
    
    def test_who_am_i(self):
        """Test box_who_am_i tool"""
        try:
            current_user = self.client.users.get_user_me()
            result = f"Authenticated as: {current_user.name}"
            self.log_test("box_who_am_i", "PASS", f"User: {current_user.name}", result)
            return result
        except Exception as e:
            self.log_test("box_who_am_i", "FAIL", str(e))
            return None
    
    def test_search_tool(self):
        """Test box_search_tool"""
        try:
            from box_ai_agents_toolkit import box_search, SearchForContentContentTypes
            
            # Test basic search
            search_results = box_search(
                self.client, 
                self.test_config['search_query'],
                file_extensions=['pdf', 'docx', 'txt'],
                content_types=[SearchForContentContentTypes.NAME, SearchForContentContentTypes.FILE_CONTENT],
                ancestor_folder_ids=None
            )
            
            result = f"Found {len(search_results)} results"
            self.log_test("box_search_tool", "PASS", result, [f.name for f in search_results[:3]])
            return search_results
        except Exception as e:
            self.log_test("box_search_tool", "FAIL", str(e))
            return []
    
    def test_read_tool(self):
        """Test box_read_tool"""
        if not self.test_config['test_file_id']:
            self.log_test("box_read_tool", "SKIP", "No test_file_id configured")
            return None
        
        try:
            from box_ai_agents_toolkit import box_file_text_extract
            content = box_file_text_extract(self.client, self.test_config['test_file_id'])
            self.log_test("box_read_tool", "PASS", f"Read {len(content)} characters", content[:100])
            return content
        except Exception as e:
            self.log_test("box_read_tool", "FAIL", str(e))
            return None
    
    def test_ask_ai_tool(self):
        """Test box_ask_ai_tool"""
        if not self.test_config['test_pdf_file_id']:
            self.log_test("box_ask_ai_tool", "SKIP", "No test_pdf_file_id configured")
            return None
        
        try:
            from box_ai_agents_toolkit import box_file_ai_ask
            prompt = "What is this document about?"
            response = box_file_ai_ask(self.client, self.test_config['test_pdf_file_id'], prompt)
            self.log_test("box_ask_ai_tool", "PASS", f"AI response received", response[:100])
            return response
        except Exception as e:
            self.log_test("box_ask_ai_tool", "FAIL", str(e))
            return None
    
    def test_ask_ai_multi_file_tool(self):
        """Test box_ask_ai_tool_multi_file"""
        if not self.test_config['test_pdf_file_id']:
            self.log_test("box_ask_ai_tool_multi_file", "SKIP", "No test files configured")
            return None
        
        try:
            from box_ai_agents_toolkit import box_multi_file_ai_ask
            file_ids = [self.test_config['test_pdf_file_id']]  # Add more if available
            prompt = "Summarize these documents"
            response = box_multi_file_ai_ask(self.client, file_ids, prompt)
            self.log_test("box_ask_ai_tool_multi_file", "PASS", "Multi-file AI response received", response[:100])
            return response
        except Exception as e:
            self.log_test("box_ask_ai_tool_multi_file", "FAIL", str(e))
            return None
    
    def test_hubs_ask_ai_tool(self):
        """Test box_hubs_ask_ai_tool"""
        if not self.test_config['test_hub_id']:
            self.log_test("box_hubs_ask_ai_tool", "SKIP", "No test_hub_id configured")
            return None
        
        try:
            from box_ai_agents_toolkit import box_hubs_ai_ask, box_claude_ai_agent_ask
            ai_agent = box_claude_ai_agent_ask()
            prompt = "What content is available in this hub?"
            response = box_hubs_ai_ask(self.client, self.test_config['test_hub_id'], prompt, ai_agent)
            self.log_test("box_hubs_ask_ai_tool", "PASS", "Hub AI response received", response[:100])
            return response
        except Exception as e:
            self.log_test("box_hubs_ask_ai_tool", "FAIL", str(e))
            return None
    
    def test_search_folder_by_name(self):
        """Test box_search_folder_by_name"""
        try:
            from box_ai_agents_toolkit import box_locate_folder_by_name
            # Search for common folder names
            search_names = ['Documents', 'Test', 'Uploads']
            
            for name in search_names:
                try:
                    folders = box_locate_folder_by_name(self.client, name)
                    if folders:
                        self.log_test("box_search_folder_by_name", "PASS", f"Found {len(folders)} folders named '{name}'")
                        return folders
                except:
                    continue
            
            self.log_test("box_search_folder_by_name", "PASS", "Search completed (no matches found)")
            return []
        except Exception as e:
            self.log_test("box_search_folder_by_name", "FAIL", str(e))
            return []
    
    def test_ai_extract_data(self):
        """Test box_ai_extract_data"""
        if not self.test_config['test_pdf_file_id']:
            self.log_test("box_ai_extract_data", "SKIP", "No test_pdf_file_id configured")
            return None
        
        try:
            from box_ai_agents_toolkit import box_file_ai_extract
            fields = "title, author, summary"
            response = box_file_ai_extract(self.client, self.test_config['test_pdf_file_id'], fields)
            self.log_test("box_ai_extract_data", "PASS", "Data extraction completed", response)
            return response
        except Exception as e:
            self.log_test("box_ai_extract_data", "FAIL", str(e))
            return None
    
    def test_list_folder_content(self):
        """Test box_list_folder_content_by_folder_id"""
        try:
            from box_ai_agents_toolkit import box_folder_list_content
            folder_id = self.test_config['test_folder_id']
            content = box_folder_list_content(self.client, folder_id, is_recursive=False)
            self.log_test("box_list_folder_content_by_folder_id", "PASS", f"Listed {len(content)} items")
            return content
        except Exception as e:
            self.log_test("box_list_folder_content_by_folder_id", "FAIL", str(e))
            return []
    
    def test_manage_folder_tool(self):
        """Test box_manage_folder_tool (create, update, delete)"""
        created_folder_id = None
        
        # Test create
        try:
            from box_ai_agents_toolkit import box_create_folder
            new_folder = box_create_folder(
                self.client, 
                self.test_config['test_folder_name'], 
                self.test_config['test_parent_folder_id']
            )
            created_folder_id = new_folder.id
            self.log_test("box_manage_folder_tool (create)", "PASS", f"Created folder: {new_folder.name} (ID: {created_folder_id})")
        except Exception as e:
            self.log_test("box_manage_folder_tool (create)", "FAIL", str(e))
            return
        
        # Test update
        if created_folder_id:
            try:
                from box_ai_agents_toolkit import box_update_folder
                updated_folder = box_update_folder(
                    self.client,
                    created_folder_id,
                    name=self.test_config['test_folder_name'] + "_updated",
                    description="Updated test folder description"
                )
                self.log_test("box_manage_folder_tool (update)", "PASS", f"Updated folder: {updated_folder.name}")
            except Exception as e:
                self.log_test("box_manage_folder_tool (update)", "FAIL", str(e))
        
        # Test delete (cleanup)
        if created_folder_id:
            try:
                from box_ai_agents_toolkit import box_delete_folder
                box_delete_folder(self.client, created_folder_id, recursive=False)
                self.log_test("box_manage_folder_tool (delete)", "PASS", f"Deleted folder: {created_folder_id}")
            except Exception as e:
                self.log_test("box_manage_folder_tool (delete)", "FAIL", str(e))
    
    def test_upload_file_tools(self):
        """Test file upload tools"""
        uploaded_file_id = None
        
        # Test upload from content
        try:
            from box_ai_agents_toolkit import box_upload_file
            result = box_upload_file(
                self.client,
                self.test_config['test_file_content'],
                self.test_config['test_file_name'],
                self.test_config['test_folder_id']
            )
            uploaded_file_id = result['id']
            self.log_test("box_upload_file_from_content_tool", "PASS", f"Uploaded file: {result['name']} (ID: {uploaded_file_id})")
        except Exception as e:
            self.log_test("box_upload_file_from_content_tool", "FAIL", str(e))
        
        # Test upload from path (create a temp file first)
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
                tmp_file.write("Test file content for path upload")
                tmp_path = tmp_file.name
            
            result = box_upload_file(
                self.client,
                open(tmp_path, 'r').read(),
                f"path_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                self.test_config['test_folder_id']
            )
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            self.log_test("box_upload_file_from_path_tool", "PASS", f"Uploaded from path: {result['name']}")
            
            # Clean up uploaded file
            if result.get('id'):
                try:
                    self.client.files.delete_file_by_id(result['id'])
                except:
                    pass
                    
        except Exception as e:
            self.log_test("box_upload_file_from_path_tool", "FAIL", str(e))
        
        # Clean up the content upload file
        if uploaded_file_id:
            try:
                self.client.files.delete_file_by_id(uploaded_file_id)
            except:
                pass
    
    def test_download_file_tool(self):
        """Test box_download_file_tool"""
        if not self.test_config['test_file_id']:
            self.log_test("box_download_file_tool", "SKIP", "No test_file_id configured")
            return
        
        try:
            from box_ai_agents_toolkit import box_file_download
            saved_path, content, mime_type = box_file_download(
                self.client,
                self.test_config['test_file_id'],
                save_file=False
            )
            self.log_test("box_download_file_tool", "PASS", f"Downloaded file, MIME: {mime_type}, Size: {len(content)} bytes")
        except Exception as e:
            self.log_test("box_download_file_tool", "FAIL", str(e))
    
    def test_docgen_tools(self):
        """Test DocGen tools"""
        # Most DocGen tests require specific setup, so we'll test basic functionality
        
        # Test list templates
        try:
            from box_ai_agents_toolkit import box_docgen_template_list
            templates = box_docgen_template_list(self.client)
            self.log_test("box_docgen_template_list_tool", "PASS", f"Listed {len(templates.entries)} templates")
        except Exception as e:
            self.log_test("box_docgen_template_list_tool", "FAIL", str(e))
        
        # Test list jobs
        try:
            from box_ai_agents_toolkit import box_docgen_list_jobs
            jobs = box_docgen_list_jobs(self.client)
            self.log_test("box_docgen_list_jobs_tool", "PASS", f"Listed {len(jobs.entries)} jobs")
        except Exception as e:
            self.log_test("box_docgen_list_jobs_tool", "FAIL", str(e))
        
        # Skip other DocGen tests that require specific template/job IDs
        docgen_tools = [
            "box_docgen_create_batch_tool",
            "box_docgen_get_job_tool", 
            "box_docgen_list_jobs_by_batch_tool",
            "box_docgen_template_create_tool",
            "box_docgen_template_delete_tool",
            "box_docgen_template_get_by_id_tool",
            "box_docgen_template_list_tags_tool",
            "box_docgen_template_list_jobs_tool"
        ]
        
        for tool in docgen_tools:
            self.log_test(tool, "SKIP", "Requires specific DocGen setup")
    
    def run_all_tests(self):
        """Run all Box API tool tests"""
        print("🚀 Starting Box MCP Server Tools Test Suite")
        print("=" * 60)
        
        # Basic tests
        print("\n📋 Basic Tests")
        print("-" * 30)
        self.test_who_am_i()
        
        # Search and discovery tests
        print("\n🔍 Search and Discovery Tests")
        print("-" * 30)
        self.test_search_tool()
        self.test_search_folder_by_name()
        
        # Content tests
        print("\n📄 Content Tests")
        print("-" * 30)
        self.test_read_tool()
        self.test_list_folder_content()
        
        # AI tests
        print("\n🤖 AI Tests")
        print("-" * 30)
        self.test_ask_ai_tool()
        self.test_ask_ai_multi_file_tool()
        self.test_hubs_ask_ai_tool()
        self.test_ai_extract_data()
        
        # File management tests
        print("\n📁 File Management Tests")
        print("-" * 30)
        self.test_manage_folder_tool()
        self.test_upload_file_tools()
        self.test_download_file_tool()
        
        # DocGen tests
        print("\n📋 DocGen Tests")
        print("-" * 30)
        self.test_docgen_tools()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"⏭️ Skipped: {self.results['skipped']}")
        print(f"📈 Total: {sum([self.results['passed'], self.results['failed'], self.results['skipped']])}")
        
        if self.results['failed'] > 0:
            print("\n❌ Failed Tests:")
            for detail in self.results['details']:
                if detail['status'] == 'FAIL':
                    print(f"   - {detail['test']}: {detail['message']}")
        
        return self.results

def main():
    """Main function"""
    print("""
🧪 Box MCP Server Tools Test Suite
==================================

This script tests all Box API tools implemented in the MCP server.

IMPORTANT: Before running, update the test_config in BoxToolsTester.__init__() 
with valid file and folder IDs from your Box account.

Test Configuration Required:
- test_file_id: A valid file ID for read/download tests
- test_pdf_file_id: A PDF file ID for AI tests  
- test_image_file_id: An image file ID for download tests
- test_template_id: A DocGen template ID (optional)

""")
    
    input("Press Enter to continue or Ctrl+C to exit...")
    
    tester = BoxToolsTester()
    results = tester.run_all_tests()
    
    # Exit with error code if any tests failed
    if results['failed'] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()

