import os
import re

POEMS_DIR = 'markdown_poems'

def standardize():
    files = [f for f in os.listdir(POEMS_DIR) if f.endswith('.md')]
    
    for filename in files:
        filepath = os.path.join(POEMS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if YAML exists
        if content.startswith('---'):
            # Already has YAML, we need to inject new fields if missing
            parts = content.split('---')
            if len(parts) >= 3:
                yaml_content = parts[1]
                body = '---'.join(parts[2:])
                
                # Default type
                if 'type:' not in yaml_content:
                    yaml_content += "type: poem\n"
                if 'status:' not in yaml_content:
                    yaml_content += "status: published\n"
                if 'tags:' not in yaml_content:
                    yaml_content += "tags: []\n"
                
                new_content = f"---{yaml_content}---{body}"
            else:
                new_content = content # Shouldn't happen
        else:
            # No YAML, create it
            title = filename.split('_', 1)[-1].replace('.md', '').replace('_', ' ')
            if filename == '00_Front_Matter.md':
                yaml = "---\ntitle: \"Front Matter\"\ntype: intro\nstatus: published\n---\n\n"
            else:
                yaml = f"---\ntitle: \"{title}\"\ntype: poem\nstatus: published\ntags: []\n---\n\n"
            new_content = yaml + content
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Standardized: {filename}")

if __name__ == "__main__":
    standardize()
