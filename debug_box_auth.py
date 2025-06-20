#!/usr/bin/env python3
"""
Debug Box authentication issues step by step
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_auth_scenarios():
    """Test different authentication scenarios to identify the issue"""
    
    from box_sdk_gen import BoxJWTAuth, JWTConfig, BoxClient
    
    # Load config
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Extract values
    client_id = config['boxAppSettings']['clientID']
    client_secret = config['boxAppSettings']['clientSecret']
    enterprise_id = config['enterpriseID']
    jwt_key_id = config['boxAppSettings']['appAuth']['publicKeyID']
    private_key = config['boxAppSettings']['appAuth']['privateKey']
    passphrase = config['boxAppSettings']['appAuth']['passphrase']
    
    print("🔧 Testing different authentication approaches...")
    print("=" * 60)
    
    # Test 1: Basic JWT config creation
    print("\\n1️⃣ Testing JWT config creation...")
    try:
        jwt_config = JWTConfig(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
            jwt_key_id=jwt_key_id,
            private_key=private_key,
            private_key_passphrase=passphrase
        )
        print("✅ JWT config created successfully")
    except Exception as e:
        print(f"❌ JWT config creation failed: {e}")
        return
    
    # Test 2: JWT auth creation
    print("\\n2️⃣ Testing JWT auth creation...")
    try:
        auth = BoxJWTAuth(config=jwt_config)
        print("✅ JWT auth created successfully")
    except Exception as e:
        print(f"❌ JWT auth creation failed: {e}")
        return
    
    # Test 3: Box client creation
    print("\\n3️⃣ Testing Box client creation...")
    try:
        client = BoxClient(auth=auth)
        print("✅ Box client created successfully")
    except Exception as e:
        print(f"❌ Box client creation failed: {e}")
        return
    
    # Test 4: Service account authentication (this is what should work first)
    print("\\n4️⃣ Testing service account authentication...")
    try:
        # Try getting the service account user info
        current_user = client.users.get_user_me()
        print(f"✅ Service account auth successful!")
        print(f"   Service Account: {current_user.name} ({current_user.login})")
        print(f"   User ID: {current_user.id}")
    except Exception as e:
        print(f"❌ Service account auth failed: {e}")
        
        # This is the critical failure - the app is likely not authorized
        print("\\n🚨 DIAGNOSIS: App Authorization Issue")
        print("This error typically means:")
        print("1. Your Box app is not authorized in the Box Admin Console")
        print("2. The public key is not approved")
        print("3. The app settings are incorrect")
        return
    
    # Test 5: User impersonation (if service account works)
    user_id = os.getenv("BOX_USER_ID")
    if user_id:
        print(f"\\n5️⃣ Testing user impersonation for user {user_id}...")
        try:
            # Create a new auth instance for user impersonation
            user_auth = BoxJWTAuth(config=jwt_config, user_id=user_id)
            user_client = BoxClient(auth=user_auth)
            
            # Try to get the impersonated user's info
            impersonated_user = user_client.users.get_user_me()
            print(f"✅ User impersonation successful!")
            print(f"   Impersonated User: {impersonated_user.name} ({impersonated_user.login})")
            print(f"   User ID: {impersonated_user.id}")
            
        except Exception as e:
            print(f"❌ User impersonation failed: {e}")
            print("\\n💡 This might be expected if:")
            print("   - The user doesn't exist")
            print("   - The app doesn't have permission to impersonate this user")
            print("   - User impersonation is not enabled for your app")
    
    # Test 6: Try enterprise user listing
    print("\\n6️⃣ Testing enterprise user listing...")
    try:
        users = client.users.get_users(limit=5)
        print(f"✅ Enterprise user listing successful!")
        print(f"   Found {len(users.entries)} users (showing first 5)")
        for user in users.entries[:3]:
            print(f"     - {user.name} ({user.login}) ID: {user.id}")
    except Exception as e:
        print(f"❌ Enterprise user listing failed: {e}")

def print_setup_instructions():
    """Print instructions for setting up Box app properly"""
    
    print("\\n" + "=" * 60)
    print("📋 BOX APP SETUP CHECKLIST")
    print("=" * 60)
    
    print("\\n1️⃣ Box Developer Console (https://app.box.com/developers/console)")
    print("   ✓ Create a Custom App with 'Server Authentication (with JWT)'")
    print("   ✓ Generate a public/private keypair (download the config.json)")
    print("   ✓ Set app permissions (you need at least 'Read all files and folders')")
    print("   ✓ Note down your App ID for step 2")
    
    print("\\n2️⃣ Box Admin Console (https://app.box.com/master/settings/openbox)")
    print("   ✓ Go to Apps → Custom Apps")
    print("   ✓ Click '+ Authorize New App'")
    print("   ✓ Enter your App ID from step 1")
    print("   ✓ Click 'Next' and 'Authorize'")
    
    print("\\n3️⃣ Public Key Approval (in Box Developer Console)")
    print("   ✓ In your app settings, go to 'Configuration'")
    print("   ✓ Under 'Public Key Management', your key should show 'Approved'")
    print("   ✓ If it says 'Pending', contact your Box admin to approve it")
    
    print("\\n4️⃣ User Configuration")
    print("   ✓ In your .env file, set BOX_USER_ID to a valid Box user ID")
    print("   ✓ The user must exist in your Box enterprise")
    print("   ✓ The app must have permission to impersonate users (if needed)")

if __name__ == "__main__":
    print("🔐 Box Authentication Diagnostic Tool")
    print("=" * 60)
    
    try:
        test_auth_scenarios()
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
    
    print_setup_instructions()

