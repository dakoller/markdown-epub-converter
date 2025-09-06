import os
import tempfile
import subprocess
import logging
import sys
from flask import Flask, request, send_file, jsonify

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
    title = data.get('title', 'Untitled')
    author = data.get('author', 'Unknown Author')
    
    logger.info(f"Processing conversion request - Title: {title}, Author: {author}")
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
            
            # Build pandoc command
            cmd = [
                'pandoc',
                input_path,
                '-o', output_path,
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
            
            # Return the EPUB file
            logger.info("Sending EPUB file to client")
            try:
                return send_file(
                    output_path,
                    mimetype='application/epub+zip',
                    as_attachment=True,
                    download_name='book.epub'
                )
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
