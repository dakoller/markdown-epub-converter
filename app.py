import os
import tempfile
import subprocess
import logging
import sys
from flask import Flask, request, send_file, jsonify, send_from_directory

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint for container health monitoring."""
    logger.info("Health check endpoint called")
    return jsonify({"status": "healthy"}), 200

@app.route('/openapi.yaml', methods=['GET'])
def openapi_spec():
    """Serve the OpenAPI specification file."""
    logger.info("OpenAPI specification endpoint called")
    return send_file('openapi.yaml', mimetype='text/yaml')

@app.route('/convert', methods=['POST'])
def convert():
    logger.info("Convert endpoint called")
    
    # Get JSON data from request
    data = request.get_json()
    logger.debug(f"Request data: {data}")
    
    # Validate required markdown field
    if not data or 'markdown' not in data:
        logger.error("Missing required field: markdown")
        return jsonify({"error": "Missing required field: markdown"}), 400
    
    markdown_content = data['markdown']
    
    # Get title and author with validation
    title = data.get('title', 'Untitled')
    if not title or not isinstance(title, str):
        logger.warning("Invalid or missing title, using default")
        title = 'Untitled'
    
    author = data.get('author', 'Unknown Author')
    if not author or not isinstance(author, str):
        logger.warning("Invalid or missing author, using default")
        author = 'Unknown Author'
    
    logger.info(f"Processing conversion request - Title: '{title}', Author: '{author}'")
    logger.debug(f"Markdown content length: {len(markdown_content)} characters")
    
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.debug(f"Created temporary directory: {temp_dir}")
            
            # Create input markdown file
            input_path = os.path.join(temp_dir, 'input.md')
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Verify input file was created correctly
            if not os.path.exists(input_path):
                logger.error(f"Failed to create input file at {input_path}")
                return jsonify({"error": "Failed to create input file"}), 500
                
            input_size = os.path.getsize(input_path)
            logger.debug(f"Input file created at {input_path} with size {input_size} bytes")
            
            # Set output path for EPUB file
            output_path = os.path.join(temp_dir, 'output.epub')
            logger.debug(f"Output path set to {output_path}")
            
            # Create metadata file for better control
            metadata_path = os.path.join(temp_dir, 'metadata.yaml')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                f.write(f"""---
title: "{title}"
author: "{author}"
date: "{os.environ.get('EPUB_DATE', '')}"
language: "{os.environ.get('EPUB_LANGUAGE', 'en-US')}"
rights: "{os.environ.get('EPUB_RIGHTS', '')}"
publisher: "{os.environ.get('EPUB_PUBLISHER', '')}"
---
""")
            logger.debug(f"Created metadata file at {metadata_path}")
            
            # Build pandoc command with metadata file and explicit EPUB format
            cmd = [
                'pandoc',
                '--standalone',
                '--metadata-file=' + metadata_path,
                input_path,
                '-o', output_path,
                # Explicitly specify EPUB format
                '-t', 'epub',
                # Add EPUB version
                '--epub-version=3',
                # Still include direct metadata for backwards compatibility
                '--metadata', f'title={title}',
                '--metadata', f'author={author}'
            ]
            logger.info(f"Executing pandoc command: {' '.join(cmd)}")
            
            # Execute pandoc command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Log pandoc output
            logger.debug(f"Pandoc stdout: {result.stdout}")
            logger.debug(f"Pandoc stderr: {result.stderr}")
            logger.debug(f"Pandoc return code: {result.returncode}")
            
            # Check if conversion was successful
            if result.returncode != 0:
                logger.error(f"Pandoc conversion failed with return code {result.returncode}")
                logger.error(f"Pandoc error: {result.stderr}")
                return jsonify({"error": f"Conversion failed: {result.stderr}"}), 500
                
            # Verify output file exists and has content
            if not os.path.exists(output_path):
                logger.error(f"Output file not found at {output_path}")
                return jsonify({"error": "Output file not created by pandoc"}), 500
                
            output_size = os.path.getsize(output_path)
            logger.info(f"Output file created at {output_path} with size {output_size} bytes")
            
            if output_size == 0:
                logger.error("Output file has zero bytes")
                return jsonify({"error": "Generated EPUB file is empty"}), 500
                
            # Verify metadata was included (basic check)
            logger.info("Verifying metadata in EPUB file")
            verify_cmd = [
                'pandoc',
                '--standalone',
                output_path,
                '-t', 'plain',
                '--no-highlight'
            ]
            try:
                verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
                if verify_result.returncode == 0:
                    content = verify_result.stdout.lower()
                    if title.lower() in content:
                        logger.info("Title verified in EPUB content")
                    else:
                        logger.warning(f"Title '{title}' not found in EPUB content")
                    
                    if author.lower() in content:
                        logger.info("Author verified in EPUB content")
                    else:
                        logger.warning(f"Author '{author}' not found in EPUB content")
                else:
                    logger.warning("Could not verify metadata in EPUB file")
            except Exception as e:
                logger.warning(f"Error verifying metadata: {str(e)}")
            
            # Verify the EPUB file is a valid ZIP archive
            logger.info("Verifying EPUB file integrity")
            try:
                import zipfile
                with zipfile.ZipFile(output_path, 'r') as zip_ref:
                    # Try to get the list of files to verify the ZIP structure
                    file_list = zip_ref.namelist()
                    logger.info(f"EPUB contains {len(file_list)} files: {', '.join(file_list[:5])}{'...' if len(file_list) > 5 else ''}")
            except zipfile.BadZipFile as e:
                logger.error(f"EPUB file is not a valid ZIP archive: {str(e)}")
                return jsonify({"error": f"Generated EPUB is corrupted: {str(e)}"}), 500
            except Exception as e:
                logger.error(f"Error verifying EPUB ZIP structure: {str(e)}")
                # Continue anyway, as this is just a verification step
            
            # Copy the file to a more permanent location to avoid temp file issues
            permanent_output_path = os.path.join(os.path.dirname(output_path), 'final_output.epub')
            try:
                import shutil
                shutil.copy2(output_path, permanent_output_path)
                logger.info(f"Copied EPUB to {permanent_output_path}")
                
                # Double check the copied file
                if os.path.getsize(permanent_output_path) != os.path.getsize(output_path):
                    logger.error("File size mismatch after copying")
                    return jsonify({"error": "File corruption during copying"}), 500
            except Exception as e:
                logger.error(f"Error copying EPUB file: {str(e)}")
                # Continue with the original file if copying fails
                permanent_output_path = output_path
            
            # Return the EPUB file
            logger.info("Sending EPUB file to client")
            try:
                # Read the file into memory to avoid temp file issues
                with open(permanent_output_path, 'rb') as f:
                    file_data = f.read()
                
                from io import BytesIO
                mem_file = BytesIO(file_data)
                
                # Send from memory instead of from disk
                response = send_file(
                    mem_file,
                    mimetype='application/epub+zip',
                    as_attachment=True,
                    download_name='book.epub'
                )
                
                # Add headers to prevent caching issues
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                
                return response
            except Exception as e:
                logger.error(f"Error sending file: {str(e)}")
                return jsonify({"error": f"Error sending file: {str(e)}"}), 500
    
    except Exception as e:
        logger.exception(f"Exception during conversion process: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting application on {host}:{port} (debug={debug})")
    
    # Check if pandoc is installed and working
    try:
        version_result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        logger.info(f"Pandoc version: {version_result.stdout.splitlines()[0]}")
    except Exception as e:
        logger.error(f"Error checking pandoc installation: {str(e)}")
    
    app.run(host=host, port=port, debug=debug)
