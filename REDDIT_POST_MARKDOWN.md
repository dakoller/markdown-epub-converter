# Markdown to EPUB Converter: Extending the reach of your Markdown content

Hey r/markdown,

I wanted to share a tool I built that extends the usefulness of Markdown by converting it to EPUB format for e-readers via an API. This means the conversion to ePub can be integrated into automation workflows eg. with n8n or zapier. 

**Why Markdown → EPUB matters:**
As a Markdown enthusiast, I love its simplicity and portability. But when I want to read longer Markdown documents on my e-reader, the format becomes a limitation. EPUB provides better reading experience on dedicated devices with:
- Proper pagination
- Font size adjustment
- Table of contents navigation
- Consistent formatting across devices
- Better readability for long-form content

**What the converter does:**
- Preserves Markdown structure (headings, lists, links, emphasis)
- Converts to standard EPUB3 format
- Maintains metadata (title, author)
- Generates proper table of contents
- Handles images and formatting

**Markdown features supported:**
- Headers (all levels)
- Lists (ordered and unordered)
- Emphasis (bold, italic)
- Links and images
- Code blocks with syntax highlighting
- Tables
- Blockquotes
- Horizontal rules
- And more!

I've found this particularly useful for:
- Converting long-form Markdown articles for distraction-free reading
- Archiving Markdown documentation in a reader-friendly format
- Sharing Markdown content with non-technical readers
- Reading my Obsidian notes on my Kindle

The project is [available on GitHub](https://github.com/dakoller/markdown-epub-converter) with a simple web UI and API. It's built with Docker for easy deployment.

I'd love to hear from other Markdown users - how do you handle reading longer Markdown content? Do you convert to other formats for different reading contexts?
