# Release Notes

## Version 0.1.0 (Initial Release) - September 2025

We're excited to announce the first release of the Markdown to EPUB Converter! This initial version provides a solid foundation for converting Markdown content to EPUB format through a simple REST API.

### Features

- **Markdown to EPUB Conversion**: Convert Markdown content to EPUB format using Pandoc
- **REST API**: Simple API for programmatic access
- **Web Interface**: User-friendly web UI for manual conversions
- **Optional Authentication**: Secure your API with token-based authentication
- **Docker Integration**: Easy deployment with Docker and Docker Compose
- **Configurable**: Customize behavior through environment variables

### API Endpoints

- `POST /convert`: Convert Markdown to EPUB
- `GET /status`: Check API health
- `GET /auth-status`: Check if authentication is required

### Security Features

- Optional token-based authentication
- Input validation for markdown content
- File system isolation within container
- Temporary file cleanup
- Resource limits to prevent DoS
- Warning displayed when authentication is not enabled

### Documentation

- Comprehensive README with usage examples
- API documentation with request/response formats
- Security considerations and best practices
- Configuration options and environment variables

### Known Limitations

- Maximum markdown input size: 10MB (configurable)
- Synchronous processing (blocking requests)
- Single-threaded Flask application
- Temporary files stored in container filesystem
- No persistent storage or caching

### Future Plans

- Add support for more input formats (HTML, RST, etc.)
- Implement asynchronous processing for large documents
- Add more customization options for EPUB output
- Improve error handling and reporting
- Add support for EPUB validation

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd markdown-epub-converter

# Build and start the service
docker-compose up -d
```

### Feedback and Contributions

We welcome feedback, bug reports, and contributions! Please open an issue or submit a pull request on GitHub.

---

Thank you for using Markdown to EPUB Converter!

Daniel Koller
- Twitter: [@dakoller](https://twitter.com/dakoller)
- Bluesky: [daniel.dakoller.net](https://bsky.app/profile/daniel.dakoller.net)
