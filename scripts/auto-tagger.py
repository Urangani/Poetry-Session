import os
import re

POEMS_DIR = 'markdown_poems'

# Keywords for auto-tagging
TAG_MAP = {
    'nature': ['tree', 'flower', 'rain', 'moon', 'stars', 'lake', 'sun', 'sky', 'earth'],
    'love': ['love', 'heart', 'kiss', 'dear', 'princess', 'sister', 'her', 'she'],
    'darkness': ['hell', 'misery', 'deadly', 'karma', 'damned', 'suffer', 'pains'],
    'identity': ['who am i', 'reality', 'illusion', 'mind', 'dreamer', 'fool'],
    'time': ['eternity', 'beyond', 'new year', 'once upon a time', 'gone', 'forever']
}

def get_tags(title, content):
    found_tags = set()
    text = (title + " " + content).lower()
    for tag, keywords in TAG_MAP.items():
        if any(kw in text for kw in keywords):
            found_tags.add(tag)
    return list(found_tags)

def update_poems():
    files = [f for f in os.listdir(POEMS_DIR) if f.endswith('.md')]
    
    for filename in files:
        filepath = os.path.join(POEMS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            parts = content.split('---')
            if len(parts) >= 3:
                yaml_content = parts[1]
                body = '---'.join(parts[2:])
                
                # Check for existing tags
                tag_match = re.search(r'tags: \[(.*?)\]', yaml_content)
                current_tags = []
                if tag_match:
                    current_tags = [t.strip().strip('"').strip("'") for t in tag_match.group(1).split(',') if t.strip()]
                
                # Only auto-tag if empty
                if not current_tags:
                    new_tags = get_tags(filename, body)
                    if new_tags:
                        yaml_content = re.sub(r'tags: \[.*?\]', f"tags: {str(new_tags)}", yaml_content)
                
                new_content = f"---{yaml_content}---{body}"
                
                # Optimization: Only write if changed
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"🏷️ Tagged: {filename}")

if __name__ == "__main__":
    update_poems()
