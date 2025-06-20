#!/usr/bin/env python3
"""
Test server authentication specifically and provide detailed diagnosis
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

def diagnose_server_auth():
    """Diagnose server authentication setup"""
    
    print("🔍 SERVER AUTHENTICATION DIAGNOSIS")
    print("=" * 50)
    
    # Check config file
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    print(f"📁 Using config: {config_file}")
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Extract key info
    client_id = config['boxAppSettings']['clientID']
    enterprise_id = config['enterpriseID']
    
    print(f"🆔 App Client ID: {client_id}")
    print(f"🏢 Enterprise ID: {enterprise_id}")
    
    # Check what type of authentication this config supports
    has_jwt_auth = 'appAuth' in config['boxAppSettings']
    has_oauth = 'clientSecret' in config['boxAppSettings']
    
    print(f"\n🔐 Authentication Types Available:")
    print(f"   JWT (Server Auth): {'✅ Yes' if has_jwt_auth else '❌ No'}")
    print(f"   OAuth (User Auth): {'✅ Yes' if has_oauth else '❌ No'}")
    
    if not has_jwt_auth:
        print("\n❌ PROBLEM: No JWT authentication configured!")
        print("Your app needs to be configured for 'Server Authentication (with JWT)'")
        return False
    
    # Try the authentication
    try:
        from box_sdk_gen import BoxJWTAuth, JWTConfig, BoxClient
        
        jwt_config = JWTConfig(
            client_id=config['boxAppSettings']['clientID'],
            client_secret=config['boxAppSettings']['clientSecret'],
            enterprise_id=config['enterpriseID'],
            jwt_key_id=config['boxAppSettings']['appAuth']['publicKeyID'],
            private_key=config['boxAppSettings']['appAuth']['privateKey'],
            private_key_passphrase=config['boxAppSettings']['appAuth']['passphrase']
        )
        
        # Create service account auth (no user impersonation)
        service_auth = BoxJWTAuth(config=jwt_config)
        service_client = BoxClient(auth=service_auth)
        
        print(f"\n🔧 Testing service account access...")
        
        # Test service account
        try:
            current_user = service_client.users.get_user_me()
            print(f"✅ Service account works!")
            print(f"   Name: {current_user.name}")
            print(f"   Login: {current_user.login}")
            print(f"   ID: {current_user.id}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Service account failed: {error_msg}")
            
            # Provide specific diagnosis based on error
            if "'NoneType' object has no attribute 'encode'" in error_msg:
                print(f"\n🚨 DIAGNOSIS: Authorization Required")
                print(f"Your server app needs to be authorized by a Box admin.")
                print(f"\nTo fix this:")
                print(f"1. Go to Box Admin Console: https://app.box.com/master/settings/openbox")
                print(f"2. Navigate to 'Apps' → 'Custom Apps'") 
                print(f"3. Click '+ Authorize New App'")
                print(f"4. Enter your Client ID: {client_id}")
                print(f"5. Click 'Authorize'")
                
            elif "invalid_client" in error_msg:
                print(f"\n🚨 DIAGNOSIS: Invalid App Configuration")
                print(f"Check that your config.json file is correct and up-to-date.")
                
            elif "unauthorized" in error_msg:
                print(f"\n🚨 DIAGNOSIS: Public Key Not Approved")
                print(f"Your public key needs approval in the Box Developer Console.")
                
            return False
            
    except ImportError as e:
        print(f"❌ Cannot import Box SDK: {e}")
        return False
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def check_app_requirements():
    """Check if all requirements for server auth are met"""
    
    print(f"\n📋 SERVER APP REQUIREMENTS CHECKLIST")
    print("=" * 50)
    
    # Get app details from config
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    client_id = config['boxAppSettings']['clientID']
    
    requirements = [
        {
            'name': 'App Type is Server Authentication (JWT)',
            'check': 'appAuth' in config['boxAppSettings'],
            'help': 'Recreate app with Server Authentication (with JWT) option'
        },
        {
            'name': 'Public/Private Key Pair Generated', 
            'check': config['boxAppSettings']['appAuth']['privateKey'].startswith('-----BEGIN'),
            'help': 'Generate new key pair in Box Developer Console'
        },
        {
            'name': 'App Authorized in Admin Console',
            'check': None,  # Can't check programmatically
            'help': f'Go to Box Admin Console and authorize Client ID: {client_id}'
        },
        {
            'name': 'Public Key Approved',
            'check': None,  # Can't check programmatically  
            'help': 'Check Box Developer Console → Configuration → Public Key Management'
        },
        {
            'name': 'Sufficient App Permissions',
            'check': None,  # Can't check programmatically
            'help': 'Ensure app has "Read and write all files and folders" permission'
        }
    ]
    
    for req in requirements:
        status = "✅" if req['check'] is True else "❓" if req['check'] is None else "❌"
        print(f"\n{status} {req['name']}")
        if req['check'] is False or req['check'] is None:
            print(f"   Action: {req['help']}")

if __name__ == "__main__":
    success = diagnose_server_auth()
    check_app_requirements()
    
    if not success:
        print(f"\n💡 TIP: Server authentication requires admin approval.")
        print(f"   The person who created the Box enterprise account")
        print(f"   needs to authorize your app in the Admin Console.")

