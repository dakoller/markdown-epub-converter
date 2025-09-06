# Markdown to EPUB Converter

A containerized web service that converts Markdown content to EPUB format using Pandoc, exposing a simple REST API for easy integration.

## Features

- Convert Markdown to EPUB format
- Simple REST API
- Containerized with Docker
- Configurable via environment variables

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

### Endpoint

```
POST /convert
Content-Type: application/json
```

### Request Format

```json
{
  "markdown": "# Chapter 1\n\nThis is the content...",
  "title": "My Book Title",
  "author": "Author Name"
}
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

## Usage Examples

### cURL Example
```bash
curl -X POST http://localhost:8080/convert \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# My Book\n\nThis is chapter one...",
    "title": "My First Book",
    "author": "John Doe"
  }' \
  --output book.epub
```

### Python Example
```python
import requests

response = requests.post('http://localhost:8080/convert', json={
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
