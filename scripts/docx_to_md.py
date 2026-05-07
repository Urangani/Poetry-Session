import os
import re
from docx import Document

# --- CONFIGURATION ---
INPUT_FILE = 'Reality-a-colorful-illusion.docx'
OUTPUT_FILE = 'Reality-a-colorful-illusion.md'
AUTHOR_NAME = "Urangani T.M"

def is_poem_number(text):
    """Matches '1.', '12', or '123' on its own line."""
    return bool(re.match(r'^\s*\d+\.?\s*$', text))

def convert_word_to_md():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '..', INPUT_FILE)
    output_path = os.path.join(script_dir, '..', OUTPUT_FILE)

    if not os.path.exists(input_path):
        print(f"❌ Error: Could not find '{input_path}'")
        return

    doc = Document(input_path)

    poems = []
    front_matter = []
    current_poem = None
    first_poem_found = False

    print(f"📖 Reading '{input_path}'...")

    for para in doc.paragraphs:
        text = para.text.strip()

        # 1. Detect Poem Number
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

        # 2. Collect Front Matter
        if not first_poem_found:
            if text or front_matter:
                front_matter.append(para.text)
            continue

        # 3. Process Poem Content
        if current_poem is not None:
            if text == AUTHOR_NAME:
                current_poem['has_author_sig'] = True
                continue

            if current_poem['title'] is None and text:
                current_poem['title'] = text

            current_poem['lines'].append(para.text)

    # Add last poem
    if current_poem:
        poems.append(current_poem)

    # --- WRITE SINGLE MARKDOWN FILE ---
    with open(output_path, 'w', encoding='utf-8') as f:
        # Front Matter
        if front_matter:
            f.write("# Front Matter\n\n")
            for line in front_matter:
                f.write(f"{line}  \n")
            f.write("\n\n")

        # Poems
        for poem in poems:
            if not any(line.strip() for line in poem['lines']):
                continue

            display_title = poem['title'] if poem['title'] else f"Poem {poem['number']}"

            # Metadata header
            f.write("---\n")
            f.write(f"title: \"{display_title}\"\n")
            f.write(f"author: \"{AUTHOR_NAME}\"\n")
            f.write(f"id: {poem['number']}\n")
            f.write("---\n\n")

            # Title
            f.write(f"# {display_title}\n\n")

            # Body
            for line in poem['lines']:
                if line.strip() == "":
                    f.write("\n")
                else:
                    f.write(f"{line}  \n")

            if poem['has_author_sig']:
                f.write(f"\n\n*{AUTHOR_NAME}*\n")

            f.write("\n\n")

    print(f"🎉 Finished! All poems saved into '{OUTPUT_FILE}'")

if __name__ == "__main__":
    convert_word_to_md()
