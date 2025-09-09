# Markdown to EPUB Converter

A containerized web service that converts Markdown content to EPUB format using Pandoc, exposing a simple REST API for easy integration.

## Features

- Convert Markdown to EPUB format
- Simple REST API
- Containerized with Docker
- Configurable via environment variables
- Optional authentication for API access
- Web UI for easy conversion

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd markdown-epub-converter
   ```

2. Build and start the service:
   ```bash
   docker-compose up -d
   ```

3. The API will be available at `http://localhost:8080/convert`

## API Usage

### Endpoints

#### Convert Markdown to EPUB
```
POST /convert
Content-Type: application/json
```

#### Check API Health
```
GET /status
```

#### Check Authentication Status
```
GET /auth-status
```

### Request Format

```json
{
  "markdown": "# Chapter 1\n\nThis is the content...",
  "title": "My Book Title",
  "author": "Author Name"
}
```

### Authentication

When authentication is enabled, include one of the following headers with your request:

```
Authorization: Bearer your_token_here
```

or

```
X-Auth-Token: your_token_here
```

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `markdown` | string | Yes | - | The markdown content to convert |
| `title` | string | No | "Untitled" | The book title for metadata |
| `author` | string | No | "Unknown Author" | The author name for metadata |

### Response

**Success (200 OK)**
```
Content-Type: application/epub+zip
Content-Disposition: attachment; filename="book.epub"
[Binary EPUB file data]
```

**Error (400 Bad Request)**
```json
{
  "error": "Missing required field: markdown"
}
```

**Error (500 Internal Server Error)**
```json
{
  "error": "Conversion failed: [error details]"
}
```

**Error (401 Unauthorized)**
```json
{
  "error": "Authentication required"
}
```

## Usage Examples

### cURL Example

#### Without Authentication
```bash
curl -X POST http://localhost:8088/convert \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# My Book\n\nThis is chapter one...",
    "title": "My First Book",
    "author": "John Doe"
  }' \
  --output book.epub
```

#### With Authentication
```bash
curl -X POST http://localhost:8088/convert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token_here" \
  -d '{
    "markdown": "# My Book\n\nThis is chapter one...",
    "title": "My First Book",
    "author": "John Doe"
  }' \
  --output book.epub
```

### Python Example

#### Without Authentication
```python
import requests

response = requests.post('http://localhost:8088/convert', json={
    'markdown': '# Hello World\n\nThis is my book content.',
    'title': 'Hello World Book',
    'author': 'Jane Smith'
})

if response.status_code == 200:
    with open('book.epub', 'wb') as f:
        f.write(response.content)
```

#### With Authentication
```python
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer your_token_here'
}

response = requests.post('http://localhost:8088/convert', 
                        headers=headers,
                        json={
                            'markdown': '# Hello World\n\nThis is my book content.',
                            'title': 'Hello World Book',
                            'author': 'Jane Smith'
                        })

if response.status_code == 200:
    with open('book.epub', 'wb') as f:
        f.write(response.content)
```

## Configuration

The service can be configured using environment variables in the `docker-compose.yml` file:

- `PORT`: API server port (default: 5000)
- `HOST`: API server host (default: 0.0.0.0)
- `DEBUG`: Enable debug mode (default: False)
- `AUTH_TOKEN`: Set this to enable authentication with the specified token

### Enabling Authentication

To enable authentication:

1. Edit the `docker-compose.yml` file and uncomment the AUTH_TOKEN line:
   ```yaml
   # Authentication (uncomment and set a secure token to enable authentication)
   - AUTH_TOKEN=your_secure_token_here
   ```

2. Replace `your_secure_token_here` with a strong, unique token

3. Rebuild and restart the container:
   ```bash
   docker-compose down && docker-compose build && docker-compose up -d
   ```

4. To disable authentication, either comment out the AUTH_TOKEN line or set it to an empty string, then rebuild and restart the container

### Web Interface

The service includes a web interface accessible at the root URL (e.g., `http://localhost:8088/`). The web interface:

- Automatically detects if authentication is required
- Shows a warning when authentication is not enabled
- Provides a simple form for converting Markdown to EPUB

## Limitations

- Maximum markdown input size: 10MB (configurable)
- Synchronous processing (blocking requests)
- Single-threaded Flask application
- Temporary files stored in container filesystem
- No persistent storage or caching

## Security Considerations

- Input validation for markdown content
- File system isolation within container
- Temporary file cleanup
- Resource limits to prevent DoS
- No shell injection vulnerabilities in pandoc execution
- Optional authentication for API access
- Warning displayed when authentication is not enabled

## Testing

The project includes a test script that can be used to verify the API functionality:

```bash
# Test without authentication
python test_api.py --url http://localhost:8088

# Test with authentication
python test_api.py --url http://localhost:8088 --token your_token_here
```

## Author

Daniel Koller
- Twitter: [@dakoller](https://twitter.com/dakoller)
- Bluesky: [daniel.dakoller.net](https://bsky.app/profile/daniel.dakoller.net)
