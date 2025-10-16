# Markdown to EPUB Converter: A new tool for creating clean, standards-compliant EPUBs

Hey r/epub,

I wanted to share a tool I've built that creates clean, standards-compliant EPUB files from Markdown content.

**About the tool:**
I've created a Markdown to EPUB converter that focuses on producing high-quality EPUB3 files with proper structure and metadata. It's available as both a web UI and a REST API, making it flexible for different workflows.

**EPUB features:**
- Fully compliant with EPUB3 standards
- Clean HTML structure for optimal rendering
- Proper metadata handling (title, author, etc.)
- Automatically generated table of contents
- Responsive layout that works well on all e-readers
- Preservation of images and formatting
- Minimal CSS for consistent appearance

**Why I built this:**
As an e-reader enthusiast, I was frustrated with the inconsistent quality of EPUBs created by various converters. Many didn't handle the EPUB specification correctly, resulting in formatting issues or navigation problems on different devices. I wanted something that would create EPUBs that render beautifully on my Kindle, Kobo, and other e-readers.

**Use cases I've found valuable:**
- Converting web articles to EPUB for distraction-free reading
- Creating properly formatted e-books from my notes and writings
- Archiving documentation in a reader-friendly format
- Sharing content with friends who prefer reading on e-readers

**Technical details:**
- Built on Pandoc for reliable conversion
- Docker-based for easy deployment
- Optional authentication for public deployments
- Customizable metadata
- Handles a wide range of Markdown syntax

The project is [available on GitHub](https://github.com/dakoller/markdown-epub-converter) with documentation and examples.

I'd love to hear feedback from EPUB enthusiasts - what features do you look for in a good EPUB converter? Any particular pain points with existing tools that you'd like to see addressed?
