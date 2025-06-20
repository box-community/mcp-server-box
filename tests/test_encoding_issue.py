#!/usr/bin/env python3
"""
Isolate the exact source of the encoding error
"""
import json
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

def test_step_by_step():
    """Test each step to isolate where the encoding error occurs"""
    
    print("🔍 ISOLATING ENCODING ERROR")
    print("=" * 50)
    
    # Load config
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print(f"📁 Config loaded from: {config_file}")
    
    try:
        from box_sdk_gen import BoxJWTAuth, JWTConfig, BoxClient
        print("✅ Box SDK imported")
        
        # Extract all values
        client_id = config['boxAppSettings']['clientID']
        client_secret = config['boxAppSettings']['clientSecret']
        enterprise_id = config['enterpriseID']
        jwt_key_id = config['boxAppSettings']['appAuth']['publicKeyID']
        private_key = config['boxAppSettings']['appAuth']['privateKey']
        passphrase = config['boxAppSettings']['appAuth']['passphrase']
        
        print("✅ Config values extracted")
        
        # Test each value for None
        values_to_check = {
            'client_id': client_id,
            'client_secret': client_secret,
            'enterprise_id': enterprise_id,
            'jwt_key_id': jwt_key_id,
            'private_key': private_key,
            'passphrase': passphrase
        }
        
        for name, value in values_to_check.items():
            if value is None:
                print(f"❌ {name} is None!")
                return False
            else:
                print(f"✅ {name}: {type(value)} (length: {len(str(value))})")
        
        # Step 1: Create JWT config
        print(f"\n🔧 Step 1: Creating JWT config...")
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
            traceback.print_exc()
            return False
        
        # Step 2: Create auth object
        print(f"\n🔧 Step 2: Creating auth object...")
        try:
            auth = BoxJWTAuth(config=jwt_config)
            print("✅ Auth object created successfully")
        except Exception as e:
            print(f"❌ Auth object creation failed: {e}")
            traceback.print_exc()
            return False
        
        # Step 3: Create client
        print(f"\n🔧 Step 3: Creating Box client...")
        try:
            client = BoxClient(auth=auth)
            print("✅ Box client created successfully")
        except Exception as e:
            print(f"❌ Box client creation failed: {e}")
            traceback.print_exc()
            return False
        
        # Step 4: Generate token (this is often where the error occurs)
        print(f"\n🔧 Step 4: Generating access token...")
        try:
            # Try to get a token without making an API call
            token = auth.retrieve_token()
            print("✅ Access token generated successfully")
            print(f"   Token type: {type(token)}")
            if hasattr(token, 'access_token'):
                print(f"   Token exists: {bool(token.access_token)}")
        except Exception as e:
            print(f"❌ Token generation failed: {e}")
            traceback.print_exc()
            
            # This is likely where our encoding error is happening
            if "'NoneType' object has no attribute 'encode'" in str(e):
                print(f"\n🚨 FOUND THE ISSUE: Token generation encoding error")
                print(f"This suggests a problem with the JWT signing process")
                return False
        
        # Step 5: Make API call
        print(f"\n🔧 Step 5: Making API call...")
        try:
            current_user = client.users.get_user_me()
            print("✅ API call successful!")
            print(f"   User: {current_user.name} ({current_user.login})")
            return True
        except Exception as e:
            print(f"❌ API call failed: {e}")
            traceback.print_exc()
            return False
            
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        return False

def try_regenerate_keypair():
    """Suggest regenerating the keypair"""
    
    print(f"\n🔧 SOLUTION: Try Regenerating the Keypair")
    print("=" * 50)
    
    print(f"The encoding error often happens when:")
    print(f"1. Private key format is corrupted")
    print(f"2. SDK version incompatibility") 
    print(f"3. Keypair was generated with different parameters")
    
    print(f"\n📝 Steps to regenerate:")
    print(f"1. Go to Box Developer Console")
    print(f"2. Navigate to your app → Configuration")
    print(f"3. In 'Public Key Management' section:")
    print(f"   - Click 'Generate a public/private keypair'") 
    print(f"   - Download the new config.json")
    print(f"   - Replace your current config files")
    print(f"4. Test again")
    
    print(f"\n⚠️  IMPORTANT: Save the new private key securely!")
    print(f"   Box doesn't store private keys, so you can't recover them.")

if __name__ == "__main__":
    success = test_step_by_step()
    
    if not success:
        try_regenerate_keypair()
        
        print(f"\n🔄 QUICK TEST: Let's also check Box SDK version...")
        try:
            import box_sdk_gen
            print(f"Box SDK version: {box_sdk_gen.__version__ if hasattr(box_sdk_gen, '__version__') else 'Unknown'}")
        except:
            print("Could not determine Box SDK version")
    else:
        print(f"\n🎉 SUCCESS: Authentication is working!")

