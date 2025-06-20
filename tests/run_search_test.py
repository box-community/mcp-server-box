#!/usr/bin/env python3
"""
Standalone Box Search Test Script

Usage: python run_search_test.py "search query"
Example: python run_search_test.py "find me estates with death certificates"
"""

import sys
import os
import json
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add the src directory to the path so we can import the Box functionality
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from box_ai_agents_toolkit import (
    BoxClient,
    SearchForContentContentTypes,
    box_search,
)
# Use the core SDK for authentication
from box_sdk_gen import BoxJWTAuth, JWTConfig

load_dotenv()


class BoxSearchTester:
    def __init__(self):
        """Initialize the Box client using JWT authentication from a config file"""
        config_path = "config_fixed.json"
        if not os.path.exists(config_path):
            print(f"❌ JWT config file not found at: {config_path}")
            print("Please go to your Box App's Developer Console, generate a keypair,")
            print("and save the downloaded file as 'config.json' in the project root.")
            sys.exit(1)

        try:
            print("🔐 Authenticating with Box using JWT config file...")
            
            # Manually load the config.json file
            with open(config_path, 'r') as f:
                config_data = json.load(f)

            # Get the user to act on behalf of from the .env file
            user_id_to_act_as = os.getenv("BOX_USER_ID")
            if not user_id_to_act_as:
                print("❌ BOX_USER_ID not found in your .env file.")
                print("   Please add 'BOX_USER_ID=your_user_id' to your .env file.")
                sys.exit(1)

            # Extract JWT settings from the JSON data using the correct keywords for this SDK version
            # Validate all required fields
            client_id = config_data['boxAppSettings']['clientID']
            client_secret = config_data['boxAppSettings']['clientSecret']
            enterprise_id = config_data['enterpriseID']
            jwt_key_id = config_data['boxAppSettings']['appAuth']['publicKeyID']
            private_key = config_data['boxAppSettings']['appAuth']['privateKey']
            passphrase = config_data['boxAppSettings']['appAuth']['passphrase']
            
            # Check for None values
            if client_id is None:
                print("❌ client_id is None in config.json")
                sys.exit(1)
            if client_secret is None:
                print("❌ client_secret is None in config.json")
                sys.exit(1)
            if enterprise_id is None:
                print("❌ enterprise_id is None in config.json")
                sys.exit(1)
            if jwt_key_id is None:
                print("❌ jwt_key_id is None in config.json")
                sys.exit(1)
            if private_key is None:
                print("❌ private_key is None in config.json")
                sys.exit(1)
                
            # Handle passphrase (can be None)
            if passphrase is None:
                passphrase = ''
                
            print(f"🔍 Debug: All values loaded successfully")
            print(f"   Client ID: {client_id[:10]}...")
            print(f"   Client Secret: {client_secret[:5] if client_secret else 'None'}...")
            print(f"   Enterprise ID: {enterprise_id}")
            print(f"   JWT Key ID: {jwt_key_id}")
            print(f"   Private Key length: {len(private_key) if private_key else 0}")
            print(f"   Passphrase: {'(empty)' if not passphrase else '(set)'}")
            
            # Additional validation
            print(f"🔍 Debug: Type validation:")
            print(f"   client_id type: {type(client_id)}")
            print(f"   client_secret type: {type(client_secret)}")
            print(f"   private_key type: {type(private_key)}")
            print(f"   passphrase type: {type(passphrase)}")
                
            print("🔍 Creating JWTConfig...")
            jwt_config = JWTConfig(
                client_id=client_id,
                client_secret=client_secret,
                enterprise_id=enterprise_id,
                jwt_key_id=jwt_key_id,
                private_key=private_key,
                private_key_passphrase=passphrase
            )
            
            print("🔍 Creating BoxJWTAuth...")
            auth = BoxJWTAuth(config=jwt_config)
            
            print("🔍 Creating BoxClient...")
            # Create a client (user impersonation handled by JWT config)
            self.client = BoxClient(auth=auth)
            
            print("🔍 Testing connection...")
            print(f"🔍 Debug: user_id_to_act_as = '{user_id_to_act_as}'")
            
            # Test connection using the service account (JWT auth gives us a service account)
            try:
                current_user = self.client.users.get_user_me()
                print(f"✅ Authenticated successfully as service account: {current_user.name} ({current_user.login})")
            except Exception as e:
                print(f"⚠️  get_user_me() failed: {e}")
                print("🔍 Trying alternative approach...")
                # Try getting enterprise users to test connection
                try:
                    users = self.client.users.get_users(limit=1)
                    print(f"✅ Authentication successful! Enterprise connection working.")
                except Exception as e2:
                    print(f"❌ Enterprise users call also failed: {e2}")
                    raise e

        except Exception as e:
            print(f"❌ Failed to connect to Box with JWT: {e}")
            print("\nTroubleshooting:")
            print("1. Ensure 'config.json' is the correct file from the Box Dev Console.")
            print("2. Ensure the public key has been approved in the Box Dev Console.")
            print("3. Ensure the App is authorized in your Box Admin Console (under 'Apps').")
            sys.exit(1)

    def parse_search_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into search parameters
        
        Args:
            query: Natural language search query
            
        Returns:
            Dictionary with search parameters
        """
        query_lower = query.lower()
        
        # Extract key terms and determine search strategy
        search_params = {
            'query': query,
            'file_extensions': None,
            'where_to_look_for_query': ['NAME', 'DESCRIPTION', 'FILE_CONTENT', 'COMMENTS', 'TAG'],
            'ancestor_folder_ids': None
        }
        
        # Look for specific file types
        file_type_patterns = {
            r'\b(pdf|document|doc|docx)\b': ['pdf', 'doc', 'docx'],
            r'\b(certificate|cert)\b': ['pdf', 'doc', 'docx', 'jpg', 'png'],
            r'\b(image|photo|picture)\b': ['jpg', 'jpeg', 'png', 'gif', 'tiff'],
            r'\b(spreadsheet|excel|csv)\b': ['xlsx', 'xls', 'csv'],
        }
        
        for pattern, extensions in file_type_patterns.items():
            if re.search(pattern, query_lower):
                search_params['file_extensions'] = extensions
                break
        
        # Extract main search terms (remove common words)
        stop_words = {'find', 'me', 'a', 'an', 'the', 'with', 'on', 'in', 'for', 'of', 'and', 'or'}
        words = re.findall(r'\b\w+\b', query_lower)
        key_terms = [word for word in words if word not in stop_words and len(word) > 2]
        
        if key_terms:
            # Use the most important terms for the actual search
            search_params['query'] = ' '.join(key_terms[:5])  # Limit to 5 most relevant terms
        
        return search_params

    def perform_search(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Perform the Box search with given parameters
        
        Args:
            search_params: Dictionary containing search parameters
            
        Returns:
            List of search results
        """
        try:
            # Convert where_to_look_for_query to SearchForContentContentTypes
            content_types = []
            if search_params.get('where_to_look_for_query'):
                for content_type in search_params['where_to_look_for_query']:
                    try:
                        content_types.append(SearchForContentContentTypes[content_type])
                    except KeyError:
                        print(f"⚠️  Unknown content type: {content_type}")
            
            print(f"🔍 Searching for: '{search_params['query']}'")
            if search_params.get('file_extensions'):
                print(f"📁 File types: {search_params['file_extensions']}")
            print(f"🎯 Searching in: {search_params['where_to_look_for_query']}")
            print("---")
            
            # Perform the search
            results = box_search(
                self.client,
                search_params['query'],
                file_extensions=search_params.get('file_extensions'),
                content_types=content_types,
                ancestor_folder_ids=search_params.get('ancestor_folder_ids')
            )
            
            # Convert results to dictionaries for easier handling
            formatted_results = []
            for file in results:
                result = {
                    'id': file.id,
                    'name': file.name,
                    'type': file.type,
                    'description': getattr(file, 'description', None),
                    'size': getattr(file, 'size', None),
                    'modified_at': getattr(file, 'modified_at', None),
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []

    def display_results(self, results: List[Dict[str, Any]], original_query: str):
        """
        Display search results in a user-friendly format
        
        Args:
            results: List of search result dictionaries
            original_query: The original search query
        """
        if not results:
            print("🚫 No results found.")
            print("\n💡 Tips:")
            print("  - Try different keywords")
            print("  - Check if files exist in your Box account")
            print("  - Make sure files have descriptions, tags, or comments")
            return
        
        print(f"📊 Found {len(results)} result(s) for: '{original_query}'")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['name']}")
            print(f"   ID: {result['id']}")
            print(f"   Type: {result['type']}")
            
            if result.get('description'):
                print(f"   Description: {result['description']}")
            
            if result.get('size'):
                # Convert bytes to human readable format
                size_mb = result['size'] / (1024 * 1024)
                if size_mb > 1:
                    print(f"   Size: {size_mb:.2f} MB")
                else:
                    size_kb = result['size'] / 1024
                    print(f"   Size: {size_kb:.2f} KB")
            
            if result.get('modified_at'):
                print(f"   Modified: {result['modified_at']}")
        
        print("\n" + "=" * 60)

    def run_interactive_search(self, query: str):
        """
        Run the complete search process
        
        Args:
            query: Search query string
        """
        print(f"🚀 Box Search Test - Query: '{query}'")
        print("=" * 60)
        
        # Parse the query
        search_params = self.parse_search_query(query)
        
        # Perform search
        results = self.perform_search(search_params)
        
        # Display results
        self.display_results(results, query)
        
        # Offer additional actions
        if results:
            print(f"\n🔧 You can now use these file IDs with other Box tools:")
            print(f"   - Read file: box_read_tool(file_id)")
            print(f"   - Ask AI: box_ask_ai_tool(file_id, 'your question')")
            print(f"   - Extract data: box_ai_extract_data(file_id, 'fields')")


def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) != 2:
        print("Usage: python run_search_test.py \"search query\"")
        print("Example: python run_search_test.py \"find me estates with death certificates\"")
        print("Example: python run_search_test.py \"find me the death certificate on the patrick estate\"")
        sys.exit(1)
    
    query = sys.argv[1]
    
    # Initialize and run the search
    try:
        tester = BoxSearchTester()
        tester.run_interactive_search(query)
    except KeyboardInterrupt:
        print("\n\n👋 Search cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 