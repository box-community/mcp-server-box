#!/usr/bin/env python3
"""
Test script to validate private key format and fix encoding issues
"""
import json
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

def test_private_key():
    """Test if the private key in config.json is valid"""
    
    # Load config
    config_file = 'config_fixed.json' if os.path.exists('config_fixed.json') else 'config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    private_key_str = config['boxAppSettings']['appAuth']['privateKey']
    passphrase = config['boxAppSettings']['appAuth']['passphrase']
    
    print("🔍 Testing private key format...")
    print(f"Private key length: {len(private_key_str)}")
    print(f"Passphrase: {'(set)' if passphrase else '(empty)'}")
    
    # Check if key starts/ends correctly
    if not private_key_str.startswith('-----BEGIN ENCRYPTED PRIVATE KEY-----'):
        print("❌ Private key doesn't start with correct header")
        return False
        
    if not private_key_str.endswith('-----END ENCRYPTED PRIVATE KEY-----'):
        print("❌ Private key doesn't end with correct footer")
        return False
    
    print("✅ Private key headers look correct")
    
    # Try to load the private key
    try:
        private_key_bytes = private_key_str.encode('utf-8')
        passphrase_bytes = passphrase.encode('utf-8') if passphrase else None
        
        # Try to load with cryptography library
        from cryptography.hazmat.primitives import serialization
        
        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=passphrase_bytes,
        )
        print("✅ Private key loads successfully with cryptography library")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load private key: {e}")
        return False

def fix_private_key_format():
    """Fix private key format by ensuring proper line endings"""
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    private_key = config['boxAppSettings']['appAuth']['privateKey']
    
    # Replace \\n with actual newlines
    fixed_key = private_key.replace('\\n', '\n')
    
    # Update config
    config['boxAppSettings']['appAuth']['privateKey'] = fixed_key
    
    # Save fixed config
    with open('config_fixed.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created config_fixed.json with proper line endings")
    return True

if __name__ == "__main__":
    print("🔑 Box Private Key Validator")
    print("=" * 40)
    
    if test_private_key():
        print("\n✅ Private key format appears to be correct")
    else:
        print("\n🔧 Attempting to fix private key format...")
        fix_private_key_format()
        print("📝 Try using config_fixed.json instead of config.json")

