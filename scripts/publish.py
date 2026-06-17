import os
import json
import re

POEMS_DIR = 'markdown_poems'
MANIFEST_PATH = 'poems.json'

def parse_yaml(content):
    """Simple YAML parser for basic key-value pairs."""
    metadata = {}
    if content.startswith('---'):
        parts = content.split('---')
        if len(parts) >= 3:
            yaml_block = parts[1]
            lines = yaml_block.strip().split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    # Basic list parsing for tags
                    if value.startswith('[') and value.endswith(']'):
                        value = [t.strip().strip('"').strip("'") for t in value[1:-1].split(',') if t.strip()]
                    
                    metadata[key] = value
    return metadata

def publish():
    print("🚀 Starting publishing process...")
    
    files = sorted([f for f in os.listdir(POEMS_DIR) if f.endswith('.md')])
    poems_manifest = []
    book_order = []

    for filename in files:
        filepath = os.path.join(POEMS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = parse_yaml(content)
        
        # 1. Filter for Web Gallery
        if metadata.get('type') == 'poem' and metadata.get('status') == 'published':
            poems_manifest.append({
                "title": metadata.get('title', 'Untitled'),
                "file": f"{POEMS_DIR}/{filename}",
                "tags": metadata.get('tags', []),
                "id": metadata.get('id')
            })
            print(f"  + Added to Web: {filename}")

        # 2. Track for Book Order (including intros/outros)
        if metadata.get('status') == 'published':
            book_order.append({
                "title": metadata.get('title'),
                "type": metadata.get('type'),
                "file": filepath
            })

    # Save manifest for Web
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(poems_manifest, f, indent=2)
    
    print(f"✅ Generated {MANIFEST_PATH} with {len(poems_manifest)} poems.")
    print("📖 Book generation ready (Order saved in memory).")

if __name__ == "__main__":
    publish()
