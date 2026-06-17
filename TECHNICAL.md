# Technical Implementation Details

This project uses a "Single Source of Truth" workflow to manage the poetry collection.

## 🛠️ Architecture

- **Source Content**: Markdown files in `markdown_poems/` containing YAML front matter.
- **Workflow**: 
  - Word files are imported using `scripts/convert-poems.py`.
  - Metadata is standardized using `scripts/standardize-metadata.py`.
  - The website manifest (`poems.json`) is generated via `scripts/publish.py`.
- **Frontend**: 
  - Pure HTML/JS/CSS located in `index.html` and the `assets/` directory.
  - Uses `marked.js` for client-side markdown rendering.

## 🚀 Common Commands

### 1. Import from Word
If you have new drafts in the `.docx` file:
```bash
python3 scripts/convert-poems.py
```

### 2. Standardize Metadata
To ensure all poems have the correct tags and status:
```bash
python3 scripts/standardize-metadata.py
```

### 3. Publish to Web
To update the `poems.json` manifest used by the website:
```bash
python3 scripts/publish.py
```

## 📋 Metadata Schema
Every poem file should have the following header:
```yaml
---
title: "Poem Title"
type: poem        # Options: poem, intro, outro
status: published # Options: draft, review, published
tags: [tag1, tag2]
---
```
