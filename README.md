# Poetry Session: Reality, A Colorful Illusion

A digital poetry collection by **Urangani T.M.** This project automatically converts a Word document (`.docx`) into a web-ready showcase of poems.

## How it Works

1.  **Source:** Write your poems in `Reality-a-colorful-illusion.docx`.
2.  **Conversion:** A Python script reads the Word file, splits it into individual Markdown files, and generates a `poems.json` manifest.
3.  **Display:** The `index.html` file fetches the manifest and renders the poems using `marked.js`.

## 🛠️ Project Structure

```text
Poetry-Session/
├── Reality-a-colorful-illusion.docx  # The source document
├── index.html                        # The web viewer
├── style.css                         # Styling for the poems
├── poems.json                        # Auto-generated list of poems
├── markdown_poems/                   # Generated Markdown files
├── scripts/
│   ├── convert-poems.py              # The conversion engine
│   └── requirements.txt              # Python dependencies
└── env/                              # Python virtual environment
```

## 📝 Usage

### 1. Update your poems
Edit the `Reality-a-colorful-illusion.docx` file. Ensure poems are numbered (e.g., `1.`, `2.`, etc.) for the script to recognize the split points.

### 2. Run the conversion script
To update the Markdown files and the website manifest, run:

```bash
# Activate the environment and run the script
./env/bin/python scripts/convert-poems.py
```

### 3. View the website
Open `index.html` in any web browser to see your updated collection.

## ⚙️ Technical Details

- **Python:** Uses `python-docx` to parse Word documents.
- **Frontend:** Pure HTML/CSS/JS.
- **Markdown Rendering:** Uses [marked.js](https://marked.js.org/) for fast, client-side rendering.
- **Metadata:** Each poem includes YAML front matter for easy integration with static site generators if needed in the future.
