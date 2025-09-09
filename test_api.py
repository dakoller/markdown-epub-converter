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
import subprocess
import tempfile
import zipfile
from io import BytesIO

def test_health_check(base_url):
    """Test the health check endpoint."""
    url = f"{base_url}/status"
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

def verify_epub_structure(epub_file):
    """Verify that the EPUB file is a valid ZIP archive with the expected structure."""
    print(f"\n🔍 Verifying EPUB file structure: {epub_file}")
    
    if not os.path.exists(epub_file):
        print(f"❌ EPUB file not found: {epub_file}")
        return False
    
    if os.path.getsize(epub_file) == 0:
        print(f"❌ EPUB file is empty: {epub_file}")
        return False
    
    try:
        # Check if the file is a valid ZIP archive
        with zipfile.ZipFile(epub_file, 'r') as zip_ref:
            # Get the list of files in the EPUB
            file_list = zip_ref.namelist()
            
            if not file_list:
                print("❌ EPUB file is empty (no files in ZIP)")
                return False
            
            # Check for required EPUB files
            required_files = ['mimetype', 'META-INF/container.xml']
            missing_files = [f for f in required_files if f not in file_list]
            
            if missing_files:
                print(f"❌ EPUB missing required files: {', '.join(missing_files)}")
                return False
            
            # Check mimetype content (should be 'application/epub+zip')
            try:
                mimetype = zip_ref.read('mimetype').decode('utf-8').strip()
                if mimetype != 'application/epub+zip':
                    print(f"❌ Invalid mimetype: {mimetype}")
                    return False
                else:
                    print("✅ Valid mimetype found")
            except Exception as e:
                print(f"❌ Error reading mimetype: {str(e)}")
                return False
            
            # Print summary of files
            print(f"✅ EPUB contains {len(file_list)} files")
            print(f"   First 5 files: {', '.join(file_list[:5])}")
            
            return True
            
    except zipfile.BadZipFile as e:
        print(f"❌ EPUB file is not a valid ZIP archive: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error verifying EPUB structure: {str(e)}")
        return False

def verify_epub_metadata(epub_file, expected_title, expected_author):
    """Verify that the EPUB file contains the expected title and author."""
    print(f"\n🔍 Verifying metadata in EPUB file: {epub_file}")
    
    if not os.path.exists(epub_file):
        print(f"❌ EPUB file not found: {epub_file}")
        return False
    
    if os.path.getsize(epub_file) == 0:
        print(f"❌ EPUB file is empty: {epub_file}")
        return False
    
    try:
        # Create a temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use pandoc to convert EPUB to plain text for inspection
            cmd = [
                'pandoc',
                '--standalone',
                epub_file,
                '-t', 'plain',
                '--no-highlight',
                '-o', os.path.join(temp_dir, 'content.txt')
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"❌ Failed to extract content from EPUB: {result.stderr}")
                    return False
                
                # Read the extracted content
                with open(os.path.join(temp_dir, 'content.txt'), 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                # Check for title and author
                title_found = expected_title.lower() in content
                author_found = expected_author.lower() in content
                
                if title_found:
                    print(f"✅ Title found in EPUB: {expected_title}")
                else:
                    print(f"❌ Title not found in EPUB: {expected_title}")
                
                if author_found:
                    print(f"✅ Author found in EPUB: {expected_author}")
                else:
                    print(f"❌ Author not found in EPUB: {expected_author}")
                
                return title_found and author_found
                
            except Exception as e:
                print(f"❌ Error extracting content from EPUB: {str(e)}")
                
                # Fallback method: try to use strings command if available
                try:
                    strings_cmd = ['strings', epub_file]
                    strings_result = subprocess.run(strings_cmd, capture_output=True, text=True)
                    
                    if strings_result.returncode == 0:
                        content = strings_result.stdout.lower()
                        
                        title_found = expected_title.lower() in content
                        author_found = expected_author.lower() in content
                        
                        if title_found:
                            print(f"✅ Title found in EPUB (fallback method): {expected_title}")
                        else:
                            print(f"❌ Title not found in EPUB (fallback method): {expected_title}")
                        
                        if author_found:
                            print(f"✅ Author found in EPUB (fallback method): {expected_author}")
                        else:
                            print(f"❌ Author not found in EPUB (fallback method): {expected_author}")
                        
                        return title_found and author_found
                    
                except Exception:
                    pass
                
                return False
    
    except Exception as e:
        print(f"❌ Error verifying EPUB metadata: {str(e)}")
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
            
            # Verify EPUB structure
            structure_ok = verify_epub_structure(output_file)
            if not structure_ok:
                print("❌ Error: EPUB file structure is invalid")
                return False
            
            # Verify metadata
            metadata_ok = verify_epub_metadata(output_file, title, author)
            if not metadata_ok:
                print("⚠️ Warning: Metadata verification failed or incomplete")
                # Don't fail the test completely, just warn
            
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
    parser.add_argument('--input', default='testfile.md', help='Path to markdown file for testing')
    parser.add_argument('--output', default='test_output.epub', help='Output EPUB file path')
    parser.add_argument('--title', default='Should we revisit Extreme Programming in the age of AI?', help='Title for the EPUB')
    parser.add_argument('--author', default='Jacob Clark', help='Author for the EPUB')
    
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
        markdown_content = """Should we revisit Extreme Programming in the age of AI?
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
    print(f"Title: {args.title}")
    print(f"Author: {args.author}")
    
    if not (health_ok and conversion_ok):
        print("\n⚠️ Some tests failed. Check the logs for details.")
        sys.exit(1)
    else:
        print("\n🎉 All tests passed successfully!")

if __name__ == "__main__":
    main()
