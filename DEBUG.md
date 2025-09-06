# Debugging Guide for Markdown to EPUB Converter

This guide provides instructions for debugging the Markdown to EPUB converter, particularly focusing on the zero byte output issue.

## Understanding the Zero Byte Output Issue

If you're experiencing a zero byte output from the converter, it means that the EPUB file is being created but has no content. This could be caused by several issues:

1. **Pandoc installation issues**: The container might not have pandoc properly installed or accessible.
2. **Permission problems**: The non-root user might not have proper permissions to write files.
3. **Temporary directory issues**: Problems with the temporary directory creation or access.
4. **Conversion process errors**: Pandoc might be failing during the conversion process.
5. **File handling issues**: Problems with reading input or writing output files.

## Enhanced Logging

The application has been updated with comprehensive logging to help diagnose issues:

1. **Application logs**: Detailed logs for each step of the conversion process.
2. **Pandoc output capture**: Both stdout and stderr from pandoc are captured and logged.
3. **File verification**: Checks for file existence and size at critical points.
4. **Error details**: More detailed error messages with exception information.

## Using the Test Script

A test script (`test_api.py`) has been provided to help diagnose issues:

### Basic Usage

```bash
# Make the script executable
chmod +x test_api.py

# Run with default settings (uses a sample markdown document)
./test_api.py

# Specify a custom URL if not running on localhost:5000
./test_api.py --url http://localhost:8088

# Use a specific markdown file as input
./test_api.py --input your_markdown_file.md

# Specify output file name
./test_api.py --output your_output.epub

# Set custom title and author
./test_api.py --title "Your Title" --author "Your Name"
```

### Interpreting Test Results

The test script will:

1. Check if the API is running (health check)
2. Send a test conversion request
3. Save the output EPUB file
4. Verify the file has content
5. Provide a summary of the tests

If any test fails, detailed error information will be displayed.

## Debugging Steps

If you're still experiencing the zero byte output issue, follow these steps:

### 1. Check Container Logs

```bash
# View logs from the container
docker-compose logs markdown-epub-api

# Follow logs in real-time
docker-compose logs -f markdown-epub-api
```

Look for error messages, particularly related to pandoc execution or file operations.

### 2. Verify Pandoc Installation

```bash
# Enter the container
docker-compose exec markdown-epub-api sh

# Check if pandoc is installed and working
pandoc --version

# Try a simple conversion manually
echo "# Test" > test.md
pandoc test.md -o test.epub
ls -la test.epub
```

### 3. Check Permissions

```bash
# Inside the container
ls -la /app
ls -la /app/tmp
```

Ensure the appuser has write permissions to the necessary directories.

### 4. Test with Different Input

Try converting a very simple markdown file to rule out issues with the input content:

```markdown
# Simple Test

This is a simple test document.
```

### 5. Check Resource Usage

```bash
# Check container resource usage
docker stats markdown-epub-api
```

Ensure the container isn't running out of memory or CPU resources.

### 6. Inspect Network Issues

If you're accessing the API remotely, check for network-related issues:

```bash
# Inside the container
wget --spider http://localhost:5000/
```

## Common Solutions

1. **Rebuild the container**: `docker-compose build --no-cache markdown-epub-api`
2. **Update pandoc**: Try using a different version of pandoc in the Dockerfile
3. **Increase memory limits**: Adjust the memory limits in docker-compose.yml
4. **Check disk space**: Ensure there's enough disk space for temporary files
5. **Simplify the conversion**: Try with minimal markdown content and options

## Additional Debugging Tools

The Docker image has been updated with additional debugging tools:

- `curl`: For testing HTTP endpoints
- `wget`: For downloading files and testing connectivity
- `procps`: For process monitoring (ps, top)
- `htop`: For interactive process viewer

You can use these tools inside the container to help diagnose issues.

## Getting Help

If you're still experiencing issues after following these debugging steps, please provide:

1. The complete container logs
2. The output from the test script
3. Details about your environment (OS, Docker version, etc.)
4. Any modifications you've made to the Dockerfile or application code

This information will help diagnose and resolve the issue more effectively.
