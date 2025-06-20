#!/usr/bin/env python3
"""
Test commands for Box file operations

Usage: uv run python tests/test_file_ops.py [command] [file_id]

Commands:
  read FILE_ID      - Read text content from a file
  download FILE_ID  - Download a file 
  upload            - Upload a test file
  upload_temp       - Upload a temporary file and clean up
  create_folder     - Create a test folder
  all FILE_ID       - Run all file tests (requires valid file ID)
"""

import sys
import os
import tempfile
import json
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from box_ai_agents_toolkit import (
    box_file_text_extract,
    box_file_download,
    box_upload_file,
    box_create_folder,
    box_delete_folder
)

# Use the JWT authentication we set up
from box_sdk_gen import BoxJWTAuth, JWTConfig, BoxClient

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

def test_read_file(file_id: str):
    """Test box_read_tool"""
    print(f"🔍 Testing box_read_tool with file ID: {file_id}")
    
    client = get_jwt_client()
    
    try:
        content = box_file_text_extract(client, file_id)
        print(f"✅ Success: Read {len(content)} characters")
        print(f"   First 200 chars: {content[:200]}...")
        
        if len(content) > 200:
            print(f"   [Content truncated - showing first 200 of {len(content)} characters]")
            
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def test_download_file(file_id: str):
    """Test box_download_file_tool"""
    print(f"🔍 Testing box_download_file_tool with file ID: {file_id}")
    
    client = get_jwt_client()
    
    try:
        # Download without saving
        saved_path, content, mime_type = box_file_download(
            client, file_id, save_file=False
        )
        
        print(f"✅ Success: Downloaded file")
        print(f"   MIME type: {mime_type}")
        print(f"   Content size: {len(content)} bytes")
        
        # Get file info
        file_info = client.files.get_file_by_id(file_id)
        print(f"   File name: {file_info.name}")
        
    except Exception as e:
        print(f"❌ Error downloading file: {e}")

def test_upload_file():
    """Test box_upload_file_from_content_tool"""
    print("🔍 Testing box_upload_file_from_content_tool")
    
    client = get_jwt_client()
    
    test_content = f"""Test file content created at {datetime.now()}

This is a test file uploaded via the Box MCP Server.

Contents:
- Test data
- Timestamp: {datetime.now().isoformat()}
- Random data: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
"""
    
    file_name = f"test_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        result = box_upload_file(client, test_content, file_name, '0')
        
        print(f"✅ Success: Uploaded file")
        print(f"   File ID: {result['id']}")
        print(f"   File name: {result['name']}")
        
        # Verify by reading it back
        print(f"\n🔍 Verifying upload by reading back...")
        try:
            read_content = box_file_text_extract(client, result['id'])
            if test_content.strip() == read_content.strip():
                print(f"✅ Verification successful: Content matches")
            else:
                print(f"⚠️ Verification warning: Content doesn't match exactly")
                
        except Exception as e:
            print(f"⚠️ Verification failed: {e}")
        
        return result['id']
        
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return None

def test_upload_temp_file():
    """Test box_upload_file_from_path_tool with cleanup"""
    print("🔍 Testing box_upload_file_from_path_tool (with cleanup)")
    
    client = get_jwt_client()
    uploaded_file_id = None
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(f"Temporary file content created at {datetime.now()}")
            tmp_path = tmp_file.name
        
        print(f"   Created temp file: {tmp_path}")
        
        # Read and upload the content
        with open(tmp_path, 'r') as f:
            content = f.read()
            
        file_name = f"temp_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        result = box_upload_file(client, content, file_name, '0')
        uploaded_file_id = result['id']
        
        print(f"✅ Success: Uploaded temp file")
        print(f"   File ID: {result['id']}")
        print(f"   File name: {result['name']}")
        
        # Clean up local temp file
        os.unlink(tmp_path)
        print(f"   Cleaned up local temp file")
        
        # Clean up uploaded file
        try:
            client.files.delete_file_by_id(uploaded_file_id)
            print(f"   Cleaned up uploaded file from Box")
        except Exception as e:
            print(f"   ⚠️ Warning: Could not clean up uploaded file: {e}")
            
    except Exception as e:
        print(f"❌ Error in temp file test: {e}")
        
        # Try to clean up if something went wrong
        if uploaded_file_id:
            try:
                client.files.delete_file_by_id(uploaded_file_id)
            except:
                pass

def test_create_folder():
    """Test box_manage_folder_tool"""
    print("🔍 Testing box_manage_folder_tool (create/delete)")
    
    client = get_jwt_client()
    
    folder_name = f"test_folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    created_folder_id = None
    
    try:
        # Create folder
        new_folder = box_create_folder(client, folder_name, '0')
        created_folder_id = new_folder.id
        
        print(f"✅ Success: Created folder")
        print(f"   Folder ID: {new_folder.id}")
        print(f"   Folder name: {new_folder.name}")
        
        # Clean up - delete the folder
        try:
            box_delete_folder(client, created_folder_id, recursive=False)
            print(f"   Cleaned up: Deleted test folder")
        except Exception as e:
            print(f"   ⚠️ Warning: Could not clean up folder: {e}")
            
    except Exception as e:
        print(f"❌ Error creating folder: {e}")
        
        # Try to clean up if something went wrong
        if created_folder_id:
            try:
                box_delete_folder(client, created_folder_id, recursive=False)
            except:
                pass

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("""
🧪 Box File Operations Test Commands

Usage: uv run python tests/test_file_ops.py [command] [file_id]

Available commands:
  read FILE_ID      - Read text content from a file
  download FILE_ID  - Download a file and show info
  upload            - Upload a test file (leaves file in Box)
  upload_temp       - Upload a temp file and clean up
  create_folder     - Create and delete a test folder
  all FILE_ID       - Run all file tests

Examples:
  uv run python tests/test_file_ops.py read 1234567890
  uv run python tests/test_file_ops.py upload
  uv run python tests/test_file_ops.py all 1234567890

Note: For read/download/all commands, you need a valid file ID from your Box account.
You can get file IDs by running: uv run python tests/test_basic_tools.py list
""")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    print("🚀 Box File Operations Test")
    print("=" * 40)
    
    try:
        if command == 'read':
            if len(sys.argv) < 3:
                print("❌ Error: read command requires file_id")
                print("Usage: uv run python tests/test_file_ops.py read FILE_ID")
                sys.exit(1)
            test_read_file(sys.argv[2])
            
        elif command == 'download':
            if len(sys.argv) < 3:
                print("❌ Error: download command requires file_id")
                print("Usage: uv run python tests/test_file_ops.py download FILE_ID")
                sys.exit(1)
            test_download_file(sys.argv[2])
            
        elif command == 'upload':
            uploaded_id = test_upload_file()
            if uploaded_id:
                print(f"\n💡 Note: Test file left in Box with ID: {uploaded_id}")
                print(f"   You can clean it up manually or use it for other tests")
                
        elif command == 'upload_temp':
            test_upload_temp_file()
            
        elif command == 'create_folder':
            test_create_folder()
            
        elif command == 'all':
            if len(sys.argv) < 3:
                print("❌ Error: all command requires file_id for read/download tests")
                print("Usage: uv run python tests/test_file_ops.py all FILE_ID")
                sys.exit(1)
                
            file_id = sys.argv[2]
            
            test_read_file(file_id)
            print("\\n" + "-" * 40)
            test_download_file(file_id)
            print("\\n" + "-" * 40)
            test_upload_temp_file()
            print("\\n" + "-" * 40)
            test_create_folder()
            
        else:
            print(f"❌ Unknown command: {command}")
            sys.exit(1)
            
        print("\\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

