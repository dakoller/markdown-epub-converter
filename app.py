import os
import tempfile
import subprocess
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required markdown field
    if not data or 'markdown' not in data:
        return jsonify({"error": "Missing required field: markdown"}), 400
    
    markdown_content = data['markdown']
    title = data.get('title', 'Untitled')
    author = data.get('author', 'Unknown Author')
    
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create input markdown file
            input_path = os.path.join(temp_dir, 'input.md')
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Set output path for EPUB file
            output_path = os.path.join(temp_dir, 'output.epub')
            
            # Build pandoc command
            cmd = [
                'pandoc',
                input_path,
                '-o', output_path,
                '--metadata', f'title={title}',
                '--metadata', f'author={author}'
            ]
            
            # Execute pandoc command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Check if conversion was successful
            if result.returncode != 0:
                return jsonify({"error": f"Conversion failed: {result.stderr}"}), 500
            
            # Return the EPUB file
            return send_file(
                output_path,
                mimetype='application/epub+zip',
                as_attachment=True,
                download_name='book.epub'
            )
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
