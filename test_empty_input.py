#!/usr/bin/env python3
"""
Test script to verify empty markdown input handling.
"""

import requests
import json
import os

def test_empty_input():
    """Test that empty markdown input is handled correctly."""
    base_url = "http://localhost:8088"
    convert_url = f"{base_url}/convert"
    
    # Check if authentication is required
    auth_status_url = f"{base_url}/auth-status"
    try:
        auth_response = requests.get(auth_status_url)
        auth_required = auth_response.json().get('auth_required', False)
        print(f"Authentication required: {auth_required}")
    except Exception as e:
        print(f"Could not check auth status: {e}")
        auth_required = False
    
    # Set up headers if authentication is required
    headers = {'Content-Type': 'application/json'}
    if auth_required:
        auth_token = os.environ.get('AUTH_TOKEN', '')
        if auth_token:
            headers['Authorization'] = f'Bearer {auth_token}'
            print(f"Using authentication token from environment")
        else:
            print("WARNING: Authentication required but no AUTH_TOKEN in environment")
    
    # Test case 1: Empty string
    print("\nTesting empty string...")
    data = {
        "markdown": "",
        "title": "Empty Test",
        "author": "Test Author"
    }
    
    try:
        response = requests.post(convert_url, json=data, headers=headers)
        if response.status_code == 200:
            print("✓ Empty string handled successfully - EPUB created")
            # Save the file to verify
            with open('test_empty_string.epub', 'wb') as f:
                f.write(response.content)
            print(f"  File size: {len(response.content)} bytes")
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Test case 2: Whitespace only
    print("\nTesting whitespace only...")
    data = {
        "markdown": "   \n\n   \t   ",
        "title": "Whitespace Test",
        "author": "Test Author"
    }
    
    try:
        response = requests.post(convert_url, json=data, headers=headers)
        if response.status_code == 200:
            print("✓ Whitespace only handled successfully - EPUB created")
            # Save the file to verify
            with open('test_whitespace.epub', 'wb') as f:
                f.write(response.content)
            print(f"  File size: {len(response.content)} bytes")
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Test case 3: None value
    print("\nTesting None value...")
    data = {
        "markdown": None,
        "title": "None Test",
        "author": "Test Author"
    }
    
    try:
        response = requests.post(convert_url, json=data, headers=headers)
        if response.status_code == 200:
            print("✓ None value handled successfully - EPUB created")
            # Save the file to verify
            with open('test_none.epub', 'wb') as f:
                f.write(response.content)
            print(f"  File size: {len(response.content)} bytes")
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "="*50)
    print("Testing completed!")
    print("="*50)

if __name__ == '__main__':
    test_empty_input()
