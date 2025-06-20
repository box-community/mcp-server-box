#!/usr/bin/env python3
"""
Basic Box JWT authentication test using only the core SDK
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_basic_jwt_auth():
    """Test JWT authentication with the basic Box SDK"""
    
    try:
        # Try importing the Box SDK directly
        from box_sdk_gen import BoxJWTAuth, JWTConfig, BoxClient
        print("✅ Box SDK imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Box SDK: {e}")
        return False
    
    # Load config
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    print(f"📁 Loading config from: {config_file}")
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Extract values
    client_id = config['boxAppSettings']['clientID']
    client_secret = config['boxAppSettings']['clientSecret']
    enterprise_id = config['enterpriseID']
    jwt_key_id = config['boxAppSettings']['appAuth']['publicKeyID']
    private_key = config['boxAppSettings']['appAuth']['privateKey']
    passphrase = config['boxAppSettings']['appAuth']['passphrase']
    
    print("🔍 Configuration values:")
    print(f"   Client ID: {client_id[:10]}...")
    print(f"   Enterprise ID: {enterprise_id}")
    print(f"   JWT Key ID: {jwt_key_id}")
    print(f"   Private Key length: {len(private_key)}")
    print(f"   Passphrase: {'(set)' if passphrase else '(empty)'}")
    
    try:
        print("\n🔧 Creating JWT config...")
        
        # Create JWT config step by step with error handling
        jwt_config = JWTConfig(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
            jwt_key_id=jwt_key_id,
            private_key=private_key,
            private_key_passphrase=passphrase
        )
        print("✅ JWT config created successfully")
        
        print("🔧 Creating JWT auth...")
        auth = BoxJWTAuth(config=jwt_config)
        print("✅ JWT auth created successfully")
        
        print("🔧 Creating Box client...")
        client = BoxClient(auth=auth)
        print("✅ Box client created successfully")
        
        print("🔧 Testing connection...")
        # Try a simple API call
        current_user = client.users.get_user_me()
        print(f"✅ Successfully authenticated as: {current_user.name} ({current_user.login})")
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print(f"Error type: {type(e)}")
        
        # Check if it's the encoding error
        if "'NoneType' object has no attribute 'encode'" in str(e):
            print("\n🔍 This is the encoding error. Let's debug further...")
            
            # Print all the values to see which one might be None
            print("Debug values:")
            print(f"  client_id: {repr(client_id)}")
            print(f"  client_secret: {repr(client_secret)}")
            print(f"  enterprise_id: {repr(enterprise_id)}")
            print(f"  jwt_key_id: {repr(jwt_key_id)}")
            print(f"  private_key (first 100 chars): {repr(private_key[:100])}")
            print(f"  passphrase: {repr(passphrase)}")
            
        return False

if __name__ == "__main__":
    print("🔑 Basic Box JWT Authentication Test")
    print("=" * 50)
    
    success = test_basic_jwt_auth()
    
    if success:
        print("\n✅ JWT authentication is working correctly!")
    else:
        print("\n❌ JWT authentication failed")
        print("\nNext steps:")
        print("1. Check that your Box app is properly configured")
        print("2. Ensure the public key is approved in Box Dev Console")
        print("3. Verify the app is authorized in Box Admin Console")

