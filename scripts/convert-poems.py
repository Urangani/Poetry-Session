import os
import re
from docx import Document

# --- CONFIGURATION ---
INPUT_FILE = 'Reality-a-colorful-illusion.docx'
OUTPUT_FOLDER = 'markdown_poems'
AUTHOR_NAME = "Urangani T.M"

def sanitize_filename(title):
    """Creates a filesystem-safe filename."""
    if not title:
        return "Untitled"
    safe = re.sub(r'[<>:"/\\|?*]', '', str(title))
    safe = safe.strip().replace(' ', '_')
    return safe[:50]

def is_poem_number(text):
    """Matches poem split points."""
    return bool(re.match(r'^\s*\d+\.?\s*$', text))

def convert_word_to_md():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '..', INPUT_FILE)
    output_dir = os.path.join(script_dir, '..', OUTPUT_FOLDER)

    if not os.path.exists(input_path):
        print(f"❌ Error: Could not find '{input_path}'")
        return

    os.makedirs(output_dir, exist_ok=True)
    doc = Document(input_path)

    poems = []
    front_matter = []
    current_poem = None
    first_poem_found = False

    print(f"📖 Importing from '{INPUT_FILE}'...")

    for para in doc.paragraphs:
        text = para.text.strip()

        if is_poem_number(text):
            if current_poem:
                poems.append(current_poem)
            first_poem_found = True
            num = re.search(r'\d+', text).group()
            current_poem = {'number': num, 'title': None, 'lines': [], 'has_author_sig': False}
            continue

        if not first_poem_found:
            if text or front_matter:
                front_matter.append(para.text)
            continue

        if current_poem is not None:
            if text == AUTHOR_NAME:
                current_poem['has_author_sig'] = True
                continue
            if current_poem['title'] is None and text:
                current_poem['title'] = text
            current_poem['lines'].append(para.text)

    if current_poem:
        poems.append(current_poem)

    # Save Individual Poems (Skipping if exists to preserve manual edits)
    new_count = 0
    skipped_count = 0
    for poem in poems:
        if not any(line.strip() for line in poem['lines']):
            continue

        clean_title = sanitize_filename(poem['title'])
        filename = f"{poem['number'].zfill(3)}_{clean_title}.md"
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath):
            skipped_count += 1
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f"title: \"{poem['title'] if poem['title'] else 'Untitled'}\"\n")
            f.write(f"author: \"{AUTHOR_NAME}\"\n")
            f.write(f"id: {poem['number']}\n")
            f.write("type: poem\n")
            f.write("status: draft\n")
            f.write("tags: []\n")
            f.write("---\n\n")

            display_title = poem['title'] if poem['title'] else f"Poem {poem['number']}"
            f.write(f"# {display_title}\n\n")

            for line in poem['lines']:
                if line.strip() == "":
                    f.write("\n")
                else:
                    f.write(f"{line}  \n")

            if poem['has_author_sig']:
                f.write(f"\n\n*{AUTHOR_NAME}*")

        print(f"✓ Created: {filename}")
        new_count += 1

    print(f"\n✨ Import complete!")
    print(f"   - {new_count} new poems added as drafts.")
    print(f"   - {skipped_count} existing poems preserved.")
    print(f"   - Run 'python3 scripts/publish.py' to update the website.")

if __name__ == "__main__":
    convert_word_to_md()
