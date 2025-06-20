#!/usr/bin/env python3
"""
Test App Only authentication specifically
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_app_only_auth():
    """Test authentication for App Only access"""
    
    print("🔍 APP ONLY AUTHENTICATION TEST")
    print("=" * 50)
    
    # Load config
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print(f"📁 Using config: {config_file}")
    print(f"🆔 Client ID: {config['boxAppSettings']['clientID']}")
    print(f"🏢 Enterprise ID: {config['enterpriseID']}")
    
    try:
        from box_sdk_gen import BoxJWTAuth, JWTConfig, BoxClient
        
        # Create JWT config
        jwt_config = JWTConfig(
            client_id=config['boxAppSettings']['clientID'],
            client_secret=config['boxAppSettings']['clientSecret'],
            enterprise_id=config['enterpriseID'],
            jwt_key_id=config['boxAppSettings']['appAuth']['publicKeyID'],
            private_key=config['boxAppSettings']['appAuth']['privateKey'],
            private_key_passphrase=config['boxAppSettings']['appAuth']['passphrase']
        )
        
        print(f"\n🔧 Testing App Only authentication...")
        
        # For App Only access, do NOT specify a user_id - let it use the service account
        auth = BoxJWTAuth(config=jwt_config)
        client = BoxClient(auth=auth)
        
        # Test 1: Try to get current user (service account)
        try:
            print(f"\n1️⃣ Testing service account access...")
            current_user = client.users.get_user_me()
            print(f"✅ Service account authenticated successfully!")
            print(f"   Name: {current_user.name}")
            print(f"   Login: {current_user.login}")  
            print(f"   ID: {current_user.id}")
            print(f"   Type: {current_user.type}")
            
            service_account_id = current_user.id
            
        except Exception as e:
            print(f"❌ Service account test failed: {e}")
            
            # Check if it's a permissions issue
            if "insufficient_access" in str(e).lower():
                print(f"\n🚨 ISSUE: Insufficient Permissions")
                print(f"Your app may need additional scopes.")
                print(f"Current scope: 'Read all files and folders'")
                print(f"You might need: 'Read and write all files and folders'")
                
            elif "'NoneType' object has no attribute 'encode'" in str(e):
                print(f"\n🚨 ISSUE: Still getting encoding error")
                print(f"This might be a public key approval issue.")
                
            return False
        
        # Test 2: Try to access root folder
        try:
            print(f"\n2️⃣ Testing folder access...")
            root_folder = client.folders.get_folder_by_id('0')
            print(f"✅ Root folder access successful!")
            print(f"   Folder name: {root_folder.name}")
            print(f"   Folder ID: {root_folder.id}")
            
        except Exception as e:
            print(f"❌ Folder access failed: {e}")
            
        # Test 3: Try to list some content
        try:
            print(f"\n3️⃣ Testing content listing...")
            items = client.folders.get_folder_items('0', limit=5)
            print(f"✅ Content listing successful!")
            print(f"   Found {len(items.entries)} items in root folder")
            
            for item in items.entries[:3]:
                print(f"     - {item.name} (ID: {item.id}, Type: {item.type})")
                
        except Exception as e:
            print(f"❌ Content listing failed: {e}")
            
        # Test 4: Check if we can search (this is what you ultimately want)
        try:
            print(f"\n4️⃣ Testing search capability...")
            # Use the search endpoint directly
            search_results = client.search.search_for_content("test", limit=5)
            print(f"✅ Search capability confirmed!")
            print(f"   Search returned {len(search_results.entries)} results")
            
        except Exception as e:
            print(f"❌ Search test failed: {e}")
            if "insufficient_access" in str(e).lower():
                print(f"   This might require additional permissions")
            
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def check_app_only_requirements():
    """Check specific requirements for App Only access"""
    
    print(f"\n📋 APP ONLY REQUIREMENTS")
    print("=" * 50)
    
    requirements = [
        "✅ App is authorized (confirmed from your screenshot)",
        "✅ App access is set to 'App Only' (confirmed)",
        "✅ Authentication type is JWT (confirmed)",
        "❓ Public key is approved in Developer Console",
        "❓ App has sufficient permissions for search",
        "❓ Enterprise has content to search"
    ]
    
    for req in requirements:
        print(f"{req}")
    
    print(f"\n💡 IMPORTANT FOR APP ONLY ACCESS:")
    print(f"   - Don't try to impersonate users")
    print(f"   - The app acts as a service account")
    print(f"   - It can only access content the service account can see")
    print(f"   - Search will only return content accessible to the service account")

if __name__ == "__main__":
    success = test_app_only_auth()
    check_app_only_requirements()
    
    if success:
        print(f"\n🎉 App Only authentication is working!")
    else:
        print(f"\n❌ App Only authentication still failing")
        print(f"\nNext step: Check public key approval in Box Developer Console")
        print(f"Go to: https://app.box.com/developers/console")
        print(f"→ Your app → Configuration → Public Key Management")

