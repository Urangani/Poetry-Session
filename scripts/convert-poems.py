import os
import re
import json
from docx import Document

# --- CONFIGURATION ---
INPUT_FILE = 'Reality-a-colorful-illusion.docx'
OUTPUT_FOLDER = 'markdown_poems'
MANIFEST_FILE = '../poems.json'  # Path relative to the script's directory
AUTHOR_NAME = "Urangani T.M"

def sanitize_filename(title):
    """Creates a filesystem-safe filename."""
    if not title:
        return "Untitled"
    # Remove invalid characters and replace spaces with underscores
    safe = re.sub(r'[<>:"/\\|?*]', '', str(title))
    safe = safe.strip().replace(' ', '_')
    return safe[:50]

def is_poem_number(text):
    """
    Matches '1.', '12', or '  123  '. 
    Uses regex to ensure it's just a number (with optional dot) on its own line.
    """
    return bool(re.match(r'^\s*\d+\.?\s*$', text))

def convert_word_to_md():
    # Adjust paths if running from script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '..', INPUT_FILE)
    output_dir = os.path.join(script_dir, '..', OUTPUT_FOLDER)
    manifest_path = os.path.join(script_dir, MANIFEST_FILE)

    if not os.path.exists(input_path):
        print(f"❌ Error: Could not find '{input_path}'")
        return

    os.makedirs(output_dir, exist_ok=True)
    doc = Document(input_path)

    poems = []
    front_matter = []
    current_poem = None
    first_poem_found = False

    print(f"📖 Reading '{input_path}'...")

    for para in doc.paragraphs:
        text = para.text.strip()

        # 1. Detect Poem Number (The Split Point)
        if is_poem_number(text):
            if current_poem:
                poems.append(current_poem)

            first_poem_found = True
            num = re.search(r'\d+', text).group()
            current_poem = {
                'number': num,
                'title': None,
                'lines': [],
                'has_author_sig': False
            }
            continue

        # 2. Collect Front Matter (Everything before Poem #1)
        if not first_poem_found:
            if text or front_matter: # Capture text and existing breaks
                front_matter.append(para.text)
            continue

        # 3. Process Poem Content
        if current_poem is not None:
            # Check for Author Signature
            if text == AUTHOR_NAME:
                current_poem['has_author_sig'] = True
                continue # Skip adding it to 'lines' to handle it via formatting later

            # Identify the first non-empty line as the Title (for the filename)
            if current_poem['title'] is None and text:
                current_poem['title'] = text

            # Add line to poem body (Preserving original paragraph text for indentation)
            current_poem['lines'].append(para.text)

    # Add the last poem in the document
    if current_poem:
        poems.append(current_poem)

    # --- WRITING FILES ---

    manifest_data = []

    # Save Front Matter (00_Front_Matter.md)
    if front_matter:
        fm_filename = "00_Front_Matter.md"
        fm_path = os.path.join(output_dir, fm_filename)
        with open(fm_path, 'w', encoding='utf-8') as f:
            f.write("# Front Matter\n\n")
            for line in front_matter:
                f.write(f"{line}  \n")
        print(f"✓ Saved: {fm_filename}")
        manifest_data.append({"title": "Front Matter", "file": f"{OUTPUT_FOLDER}/{fm_filename}"})

    # Save Individual Poems
    saved_count = 0
    for poem in poems:
        # Skip empty entries
        if not any(line.strip() for line in poem['lines']):
            continue

        clean_title = sanitize_filename(poem['title'])
        # Padding number with zeros (e.g., 001) keeps files sorted numerically
        filename = f"{poem['number'].zfill(3)}_{clean_title}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            # Write Metadata Header (YAML)
            f.write("---\n")
            f.write(f"title: \"{poem['title'] if poem['title'] else 'Untitled'}\"\n")
            f.write(f"author: \"{AUTHOR_NAME}\"\n")
            f.write(f"id: {poem['number']}\n")
            f.write("---\n\n")

            # Write H1 Title
            display_title = poem['title'] if poem['title'] else f"Poem {poem['number']}"
            f.write(f"# {display_title}\n\n")

            # Write Poem Body
            for line in poem['lines']:
                if line.strip() == "":
                    f.write("\n") # Stanza break
                else:
                    f.write(f"{line}  \n") # Double space for markdown line break

            # Append Author Signature at the end if it was found
            if poem['has_author_sig']:
                f.write(f"\n\n*{AUTHOR_NAME}*")

        print(f"✓ Saved: {filename}")
        manifest_data.append({
            "title": poem['title'] if poem['title'] else f"Poem {poem['number']}",
            "file": f"{OUTPUT_FOLDER}/{filename}"
        })
        saved_count += 1

    # Save JSON Manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=2)
    print(f"✓ Generated: poems.json")

    print(f"\n🎉 Finished! Processed {saved_count} poems into '{OUTPUT_FOLDER}/'")

if __name__ == "__main__":
    convert_word_to_md()