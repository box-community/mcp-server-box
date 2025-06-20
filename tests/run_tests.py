#!/usr/bin/env python3
"""
Master test runner for Box MCP Server tools

This script provides easy commands to test all Box API functionality.

Usage: uv run python tests/run_tests.py [command]

Quick Commands:
  basic           - Test basic tools (auth, search, list)
  upload          - Test file upload functionality  
  comprehensive   - Run comprehensive test suite
  auth            - Test authentication only
  help            - Show detailed help

Examples:
  uv run python tests/run_tests.py basic
  uv run python tests/run_tests.py upload
  uv run python tests/run_tests.py comprehensive
"""

import sys
import os
import subprocess
from typing import List

def run_command(cmd: List[str], description: str):
    """Run a command and handle output"""
    print(f"\n🚀 {description}")
    print("=" * 60)
    
    try:
        # Use uv run to ensure proper environment
        full_cmd = ['uv', 'run'] + cmd
        # Run from the parent directory (project root) not the tests directory
        project_root = os.path.dirname(os.path.dirname(__file__))
        result = subprocess.run(full_cmd, cwd=project_root, capture_output=False)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def test_basic():
    """Run basic Box tools tests"""
    print("🧪 Running Basic Box Tools Tests")
    
    success = run_command(
        ['python', 'tests/test_basic_tools.py', 'all'],
        "Basic Tools Test (auth, search, list, folders)"
    )
    
    return success

def test_upload():
    """Test file upload functionality"""
    print("🧪 Testing File Upload Functionality")
    
    # Test temp upload (with cleanup)
    success1 = run_command(
        ['python', 'tests/test_file_ops.py', 'upload_temp'],
        "File Upload Test (temp file with cleanup)"
    )
    
    # Test folder creation
    success2 = run_command(
        ['python', 'tests/test_file_ops.py', 'create_folder'],
        "Folder Creation Test"
    )
    
    return success1 and success2

def test_auth_only():
    """Test authentication only"""
    print("🧪 Testing Authentication")
    
    success = run_command(
        ['python', 'tests/test_basic_tools.py', 'who_am_i'],
        "Authentication Test"
    )
    
    return success

def test_comprehensive():
    """Run the comprehensive test suite"""
    print("🧪 Running Comprehensive Test Suite")
    
    success = run_command(
        ['python', 'tests/test_all_box_tools.py'],
        "Comprehensive Box Tools Test Suite"
    )
    
    return success

def show_help():
    """Show detailed help"""
    print("""
🧪 Box MCP Server Test Suite
============================

This test runner helps you test all Box API functionality implemented in the MCP server.

COMMANDS:
  basic           - Test basic functionality (auth, search, list folders)
                   Safe to run, doesn't modify your Box account
                   
  upload          - Test file upload/folder creation with automatic cleanup
                   Creates and deletes test files/folders
                   
  auth            - Test authentication only
                   Quick check if your Box connection is working
                   
  comprehensive   - Run full test suite for all tools
                   Requires configuration of test file IDs
                   
  help            - Show this help message

EXAMPLES:
  # Quick check if everything is working
  uv run python tests/run_tests.py auth
  
  # Test basic read-only functionality  
  uv run python tests/run_tests.py basic
  
  # Test file operations (creates/deletes test files)
  uv run python tests/run_tests.py upload
  
  # Run all tests (requires setup)
  uv run python tests/run_tests.py comprehensive

INDIVIDUAL TEST SCRIPTS:
  
  You can also run individual test scripts directly:
  
  # Basic tools
  uv run python tests/test_basic_tools.py [who_am_i|search|list|folders|all]
  
  # File operations  
  uv run python tests/test_file_ops.py [read|download|upload|upload_temp|create_folder] [FILE_ID]
  
  # Authentication troubleshooting
  uv run python tests/test_server_auth.py
  uv run python tests/test_encoding_issue.py

CONFIGURATION:
  
  For comprehensive testing, edit tests/test_all_box_tools.py and update the test_config
  with valid file IDs from your Box account:
  
  - test_file_id: Any readable file for read/download tests
  - test_pdf_file_id: A PDF file for AI tests
  - test_image_file_id: An image file for download tests

TROUBLESHOOTING:
  
  If tests fail:
  1. Check authentication: uv run python tests/run_tests.py auth
  2. Check existing test files in tests/ directory
  3. Review error messages for specific issues
  4. Ensure your Box app has proper permissions

""")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("""
🧪 Box MCP Server Test Runner

Usage: uv run python tests/run_tests.py [command]

Quick Commands:
  basic           - Test basic tools (auth, search, list)
  upload          - Test file upload functionality  
  auth            - Test authentication only
  comprehensive   - Run comprehensive test suite
  help            - Show detailed help

Examples:
  uv run python tests/run_tests.py basic
  uv run python tests/run_tests.py auth
  uv run python tests/run_tests.py help
""")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'help':
        show_help()
        return
    
    print("🚀 Box MCP Server Test Runner")
    print("=" * 50)
    
    success = False
    
    if command == 'basic':
        success = test_basic()
        
    elif command == 'upload':
        success = test_upload()
        
    elif command == 'auth':
        success = test_auth_only()
        
    elif command == 'comprehensive':
        success = test_comprehensive()
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'uv run python tests/run_tests.py help' for available commands")
        sys.exit(1)
    
    # Final summary
    print("\\n" + "=" * 50)
    if success:
        print("🎉 All tests completed successfully!")
        print("\\n💡 Next steps:")
        print("   - Your Box MCP server is working correctly")
        print("   - You can now use it with Claude or other MCP clients")
        print("   - Check the README.md for integration instructions")
    else:
        print("❌ Some tests failed")
        print("\\n🔧 Troubleshooting:")
        print("   - Check your Box API credentials in .env file")
        print("   - Verify your Box app is authorized in Box Admin Console")
        print("   - Run 'uv run python tests/run_tests.py help' for more info")
        sys.exit(1)

if __name__ == "__main__":
    main()

