#!/usr/bin/env python3
import requests
import json
import os
import time
import sys

# URL for the API - using the port from docker-compose (8088)
API_URL = "http://localhost:8088/convert"

# Optional authentication token (set to match your AUTH_TOKEN environment variable if used)
# You can uncomment and set this if your server requires authentication
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "")

# Test cases with problematic characters that could cause YAML parsing issues
test_cases = [
    {
        "title": "Title with: colon",
        "author": "Author with Colon: Issue",
        "markdown": "# Test Document\n\nThis is a test document with special characters in metadata."
    },
    {
        "title": "Title with \"quotes\"",
        "author": "Author with 'quotes'",
        "markdown": "# Test Document\n\nThis is a test document with quote characters in metadata."
    },
    {
        "title": "Title with {braces} and [brackets]",
        "author": "Author with (parentheses)",
        "markdown": "# Test Document\n\nThis is a test document with bracket characters in metadata."
    },
    {
        "title": "Title with line\nbreak",
        "author": "Author with tab\tcharacter",
        "markdown": "# Test Document\n\nThis is a test document with control characters in metadata."
    },
    {
        "title": "Title with @ & % $ # * special chars",
        "author": "Author with ! ^ ~ ` | \\ special chars",
        "markdown": "# Test Document\n\nThis is a test document with special characters in metadata."
    }
]

def test_conversion(case_num, test_data):
    print(f"Testing case {case_num + 1}:")
    print(f"  Title: {test_data['title']}")
    print(f"  Author: {test_data['author']}")
    
    try:
        # Set up headers for authentication if needed
        headers = {}
        if AUTH_TOKEN:
            headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        
        # Make POST request to the API
        response = requests.post(API_URL, json=test_data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f"  Success! Conversion completed successfully.")
            
            # Save the EPUB file (optional)
            with open(f"test_case_{case_num + 1}.epub", "wb") as f:
                f.write(response.content)
            print(f"  EPUB file saved as test_case_{case_num + 1}.epub")
        else:
            print(f"  Error: HTTP {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  Exception: {str(e)}")
        return False

def main():
    print("Testing markdown-to-epub conversion with problematic metadata...")
    
    successes = 0
    failures = 0
    
    for i, test_case in enumerate(test_cases):
        print("\n" + "=" * 60)
        if test_conversion(i, test_case):
            successes += 1
        else:
            failures += 1
        print("=" * 60)
    
    print(f"\nTest Results: {successes} successes, {failures} failures")
    if failures == 0:
        print("All tests passed! The YAML metadata handling is now robust.")
        return 0
    else:
        print("Some tests failed. Further improvements may be needed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
