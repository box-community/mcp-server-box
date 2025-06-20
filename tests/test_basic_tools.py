#!/usr/bin/env python3
"""
Quick test commands for basic Box tools

Usage: uv run python tests/test_basic_tools.py [command]

Commands:
  who_am_i    - Test authentication and get current user
  search      - Test search functionality  
  list        - List contents of root folder
  folders     - Search for folders by name
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from box_ai_agents_toolkit import (
    box_search, 
    SearchForContentContentTypes,
    box_folder_list_content,
    box_locate_folder_by_name
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

def test_who_am_i():
    """Test box_who_am_i tool"""
    print("🔍 Testing box_who_am_i...")
    
    client = get_jwt_client()
    current_user = client.users.get_user_me()
    
    print(f"✅ Success: Authenticated as {current_user.name} ({current_user.login})")
    print(f"   User ID: {current_user.id}")
    print(f"   User Type: {current_user.type}")

def test_search():
    """Test box_search_tool"""
    print("🔍 Testing box_search_tool...")
    
    client = get_jwt_client()
    
    # Test with different queries
    queries = ['test', 'document', 'pdf']
    
    for query in queries:
        print(f"\n🔍 Searching for '{query}'...")
        try:
            results = box_search(
                client,
                query,
                file_extensions=['pdf', 'docx', 'txt'],
                content_types=[SearchForContentContentTypes.NAME, SearchForContentContentTypes.FILE_CONTENT]
            )
            
            print(f"   Found {len(results)} results")
            for i, file in enumerate(results[:3]):
                print(f"   {i+1}. {file.name} (ID: {file.id})")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_list_folder():
    """Test box_list_folder_content_by_folder_id"""
    print("🔍 Testing box_list_folder_content_by_folder_id...")
    
    client = get_jwt_client()
    
    try:
        # List root folder contents
        content = box_folder_list_content(client, '0', is_recursive=False)
        
        print(f"✅ Success: Found {len(content)} items in root folder")
        for i, item in enumerate(content[:5]):
            print(f"   {i+1}. {item.name} (ID: {item.id}, Type: {item.type})")
            
        if len(content) > 5:
            print(f"   ... and {len(content) - 5} more items")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_search_folders():
    """Test box_search_folder_by_name"""
    print("🔍 Testing box_search_folder_by_name...")
    
    client = get_jwt_client()
    
    # Common folder names to search for
    folder_names = ['Documents', 'Pictures', 'Downloads', 'Test', 'Uploads']
    
    for name in folder_names:
        print(f"\n🔍 Searching for folders named '{name}'...")
        try:
            folders = box_locate_folder_by_name(client, name)
            
            if folders:
                print(f"   Found {len(folders)} folders")
                for folder in folders[:3]:
                    print(f"   - {folder.name} (ID: {folder.id})")
            else:
                print(f"   No folders found with name '{name}'")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("""
🧪 Box Basic Tools Test Commands

Usage: uv run python tests/test_basic_tools.py [command]

Available commands:
  who_am_i    - Test authentication and get current user info
  search      - Test search functionality with various queries
  list        - List contents of root folder  
  folders     - Search for folders by common names
  all         - Run all basic tests

Examples:
  uv run python tests/test_basic_tools.py who_am_i
  uv run python tests/test_basic_tools.py search
  uv run python tests/test_basic_tools.py all
""")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    print("🚀 Box Basic Tools Test")
    print("=" * 40)
    
    try:
        if command == 'who_am_i':
            test_who_am_i()
        elif command == 'search':
            test_search()
        elif command == 'list':
            test_list_folder()
        elif command == 'folders':
            test_search_folders()
        elif command == 'all':
            test_who_am_i()
            print("\n" + "-" * 40)
            test_search()
            print("\n" + "-" * 40)
            test_list_folder()
            print("\n" + "-" * 40)
            test_search_folders()
        else:
            print(f"❌ Unknown command: {command}")
            sys.exit(1)
            
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

