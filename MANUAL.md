# User Manual: The Unified Poetry Ecosystem

Welcome to your complete poetry management system. This guide will help you master the workflow from initial draft to professional publication.

---

## 🚀 Quick Start: Launching the Studio

To manage your poems, you must first start the "Backstage Engine":

1.  Open your terminal in the project folder.
2.  Run the following command:
    ```bash
    python3 scripts/poetry_core.py studio
    ```
3.  Open `studio.html` in your browser (or click the hidden link in the website footer).

---

## 🖋️ Managing Your Poetry

### 1. Adding a New Poem
- In the **Poetry Studio**, click the **+ New Poem** button.
- Enter a title. A new draft will be created instantly.
- Type your poem in the large text area.
- Set its status to `published` when you're ready for the world to see it.

### 2. Editing & Tagging
- Click any poem in the left-hand list to load it.
- **Title/Status/Type**: Use the top fields to change metadata.
- **Tags**: Enter tags separated by commas (e.g., `nature, love, hope`). These will appear as navigation buttons on your website.
- **Save Changes**: Always click "Save Changes" to sync your work to the website and PDF generator.

### 3. Importing from Word
If you have drafted several poems in your `.docx` file, you can import them all at once:
```bash
python3 scripts/poetry_core.py import
```
*Note: This will add them as drafts so you can refine them in the Studio.*

---

## 📦 Extracting & Exporting

### 1. Generating a Professional PDF
- In the Studio, click **Export PDF**.
- A beautifully styled book (`Reality_A_Colorful_Illusion.pdf`) will be generated with one poem per page, perfectly centered.

### 2. Exporting Markdown (Backup/ZIP)
- Click **Export Markdown ZIP** to get a compressed file of all your raw poem files. This is perfect for backups or sending to other editors.

---

## 🌐 The Reader's Gallery (`index.html`)

This is your public-facing site. It automatically:
- Filters out `drafts` (only shows `published` poems).
- Excludes `intro` and `outro` content (keeping the focus on poetry).
- Creates navigation buttons based on the tags you've used in the Studio.

---

## 🛠️ Troubleshooting & Maintenance

- **Website not updating?** Make sure you clicked "Save Changes" in the Studio.
- **Studio won't load?** Ensure the Python script (`poetry_core.py studio`) is running in your terminal.
- **Spacing issues?** The system uses Markdown. Use a double space at the end of a line for a line break, or a double "Enter" for a new stanza.

&copy; 2026 Reality, a colorful illusion • Built for Urangani T.M.
