#!/usr/bin/env python3
"""
Test script for the Markdown to EPUB converter API.
This script sends a test request to the API and helps diagnose issues.
"""

import requests
import argparse
import json
import os
import sys

def test_health_check(base_url):
    """Test the health check endpoint."""
    url = f"{base_url}/"
    print(f"\n🔍 Testing health check endpoint: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Health check successful")
            return True
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Error connecting to server: {str(e)}")
        return False

def test_conversion(base_url, markdown_content, title="Test Title", author="Test Author", output_file="test_output.epub"):
    """Test the conversion endpoint with the provided markdown content."""
    url = f"{base_url}/convert"
    print(f"\n🔍 Testing conversion endpoint: {url}")
    
    payload = {
        "markdown": markdown_content,
        "title": title,
        "author": author
    }
    
    print(f"Sending request with:")
    print(f"  - Title: {title}")
    print(f"  - Author: {author}")
    print(f"  - Markdown content length: {len(markdown_content)} characters")
    
    try:
        # Send the request with a longer timeout
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"Status code: {response.status_code}")
        
        # Check if the response is JSON (error) or binary (EPUB file)
        content_type = response.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            print(f"Error response: {response.text}")
            return False
        
        elif 'application/epub+zip' in content_type:
            # Save the EPUB file
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            # Check if the file has content
            file_size = os.path.getsize(output_file)
            print(f"✅ EPUB file saved to {output_file} ({file_size} bytes)")
            
            if file_size == 0:
                print("❌ Warning: Output file has zero bytes!")
                return False
            
            return True
        
        else:
            print(f"Unexpected content type: {content_type}")
            print(f"Response preview: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error during conversion request: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test the Markdown to EPUB converter API')
    parser.add_argument('--url', default='http://localhost:5000', help='Base URL of the API')
    parser.add_argument('--input', help='Path to markdown file for testing')
    parser.add_argument('--output', default='test_output.epub', help='Output EPUB file path')
    parser.add_argument('--title', default='Test Title', help='Title for the EPUB')
    parser.add_argument('--author', default='Test Author', help='Author for the EPUB')
    
    args = parser.parse_args()
    
    # Test health check
    health_ok = test_health_check(args.url)
    
    # Test conversion
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except Exception as e:
            print(f"❌ Error reading input file: {str(e)}")
            sys.exit(1)
    else:
        # Use a simple markdown sample if no input file is provided
        markdown_content = """# Sample Markdown

This is a test document to verify the Markdown to EPUB conversion.

## Features

- Lists
- **Bold text**
- *Italic text*

> Blockquotes are also supported.

```python
# And code blocks
print("Hello, World!")
```
"""
    
    conversion_ok = test_conversion(
        args.url, 
        markdown_content, 
        args.title, 
        args.author, 
        args.output
    )
    
    # Print summary
    print("\n📋 Test Summary:")
    print(f"Health Check: {'✅ Passed' if health_ok else '❌ Failed'}")
    print(f"Conversion: {'✅ Passed' if conversion_ok else '❌ Failed'}")
    
    if not (health_ok and conversion_ok):
        print("\n⚠️ Some tests failed. Check the logs for details.")
        sys.exit(1)
    else:
        print("\n🎉 All tests passed successfully!")

if __name__ == "__main__":
    main()
