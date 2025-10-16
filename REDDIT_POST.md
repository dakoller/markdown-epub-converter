# [Self-Hosted] Markdown to EPUB Converter - Bridge the gap in your knowledge workflow

Hey r/selfhosted,

I wanted to share a small but useful tool I built to solve a specific problem in my knowledge management workflow: converting Markdown files to EPUB format for my e-reader.

**What it does:**
- Converts Markdown content to properly formatted EPUB files
- Provides both a REST API and a simple web UI
- Includes optional token-based authentication
- Runs in Docker for easy deployment

**Why I built it:**
I use an RSS reader to discover content, save notes in Obsidian (Markdown), and read longer articles on my e-reader (EPUB). This tool bridges that gap, letting me easily convert my Markdown notes/articles to a format suitable for distraction-free reading.

**Self-hosting benefits:**
- Complete control over your data
- No file size limitations
- Integrate with your existing tools
- Optional authentication for public-facing deployments
- Easy deployment with Docker and Docker Compose

I'm hosting it on my home server using Dokploy, but it's lightweight enough to run on a Raspberry Pi or any system with Docker.

The project is [available on GitHub](https://github.com/dakoller/markdown-epub-converter) with comprehensive documentation. I'd love to hear your feedback or suggestions for improvements!

*What tools do you use in your knowledge management workflow?*
