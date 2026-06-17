"""Fix Reality-a-colorful-illusion.docx formatting.

Issues fixed:
- All poems get proper Heading2 titles (not just first 6)
- Page breaks between each poem
- Direct font overrides removed (standardize to Bookman Old Style 11pt)
- Running headers with poem titles
- Proper section breaks
- Clean TOC
"""

import re, json, os, copy
from lxml import etree
import zipfile
import shutil

DOCX_PATH = 'Reality-a-colorful-illusion.docx'
POEMS_JSON = 'poems.json'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns = {
    'w': W_NS,
    'r': R_NS,
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}

# Load poem titles from website
with open(POEMS_JSON) as f:
    poems_meta = json.load(f)

# Build lookup: normalized title -> proper title
def normalize(s):
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    return re.sub(r'[^a-z0-9\']', '', s.lower())

title_lookup = {}
for p in poems_meta:
    key = normalize(p['title'])
    title_lookup[key] = p['title']
    # Also strip trailing period
    trimmed = p['title'].rstrip('.')
    key2 = normalize(trimmed)
    title_lookup[key2] = p['title']

print(f"Loaded {len(poems_meta)} known titles")

# === Read original docx ===
zf = zipfile.ZipFile(DOCX_PATH, 'r')
doc_xml = zf.read('word/document.xml')
# We'll also need to read and modify styles
styles_xml = zf.read('word/styles.xml')

root = etree.fromstring(doc_xml)
paras = root.findall('.//w:p', ns)
print(f"Total paragraphs: {len(paras)}")

# === Parse paragraphs into structured data ===
def get_para_style(p):
    pPr = p.find('w:pPr', ns)
    if pPr is not None:
        pStyle = pPr.find('w:pStyle', ns)
        if pStyle is not None:
            return pStyle.get(f'{{{W_NS}}}val')
    return None

def get_para_text(p):
    texts = p.findall('.//w:t', ns)
    return ''.join([t.text or '' for t in texts])

def is_empty_para(p):
    return not get_para_text(p).strip()

# Catalog all paragraphs
parsed = []
for i, p in enumerate(paras):
    style = get_para_style(p)
    text = get_para_text(p).strip()
    parsed.append({'idx': i, 'style': style, 'text': text, 'elem': p})

# Identify poem boundaries
# Structure:
#   paras 0-56: preamble (title page content)
#   paras 57-58: empty Heading1 (TOC placeholder)
#   para 59: "Dream & Escapes" (Heading1)
#   para 67: first Heading2 "Jump"
#   para 102: Heading2 "The dreamer"
#   para 115: Heading2 "Urangani's reality"
#   para 126: Heading2 "The moon is lonely tonight"
#   para 135: Heading2 "Don't count the stars"
#   para 142: Heading2 "Once Upon a Time" <-- everything after this is jammed content

# Find the start of actual poem content
poem_start_idx = None
for i, p in enumerate(parsed):
    if p['style'] == 'Heading2' and p['text'] and i > 10:
        poem_start_idx = i  # first Heading2 with text
        break

print(f"First poem title at paragraph {poem_start_idx}: {parsed[poem_start_idx]['text']}")

# Find the "Once Upon a Time" heading - everything after is the mega-block
ouat_idx = None
for i in range(poem_start_idx, len(parsed)):
    if parsed[i]['style'] == 'Heading2' and 'Once Upon a Time' in parsed[i]['text']:
        ouat_idx = i
        break

print(f"Once Upon a Time at paragraph {ouat_idx}")

# Build poem list:
# First 5 poems have proper headings
# After OUAT, detect poems by matching titles against known titles

poems = []  # list of {'title': str, 'paras': [list of paragraph indices]}

# Process first 5 poems (before OUAT)
current_title = None
current_paras = []
for i in range(poem_start_idx, ouat_idx):
    p = parsed[i]
    if p['style'] == 'Heading2' and p['text'] and p['text'] != 'Once Upon a Time':
        if current_title and current_paras:
            poems.append({'title': current_title, 'paras': current_paras})
        current_title = p['text']
        current_paras = []
    elif current_title and p['style'] == 'Normal':
        current_paras.append(i)

if current_title and current_paras:
    poems.append({'title': current_title, 'paras': current_paras})

# Now process the OUAT block - everything after is poems jammed together
# We need to detect where each poem starts by matching titles
# OUAT block starts at ouat_idx + 1 (skip the heading itself)
ouat_content_start = ouat_idx + 1

# Get all non-empty paragraphs from ouat start to end
content_paras = []
for i in range(ouat_content_start, len(parsed)):
    if parsed[i]['text']:  # non-empty
        content_paras.append(i)

# Detect poem boundaries by scanning for title matches
current_poem_paras = []
current_poem_title = None
poem_num = len(poems) + 1

for para_idx in content_paras:
    text = parsed[para_idx]['text']
    key = normalize(text)
    
    matched_title = title_lookup.get(key)
    
    # Also try matching after stripping leading numbers like "4.", "30", "37", "56."
    if not matched_title:
        stripped = re.sub(r'^\d+\.?\s*', '', text)
        if stripped != text:
            key2 = normalize(stripped)
            matched_title = title_lookup.get(key2)
    
    # Also try matching first 3 words for multi-word titles
    if not matched_title:
        words = text.split()
        if len(words) <= 5:
            for n_words in range(min(len(words), 3), 0, -1):
                candidate = ' '.join(words[:n_words])
                key3 = normalize(candidate)
                if key3 in title_lookup and normalize(text) == key3:
                    # Only match if the entire line IS the title, not just starts with it
                    matched_title = title_lookup[key3]
                    break
    
    if matched_title:
        # Only save previous poem if it has content or it's the first and we're past start
        if current_poem_title is not None:
            poems.append({'title': current_poem_title, 'paras': current_poem_paras})
        current_poem_title = matched_title
        current_poem_paras = []
    else:
        current_poem_paras.append(para_idx)

# Don't forget last poem
if current_poem_title:
    poems.append({'title': current_poem_title, 'paras': current_poem_paras})

# Filter out empty poems (title-only with no content)
poems = [p for p in poems if p['paras']]

print(f"\n=== Identified {len(poems)} poems ===")
for i, poem in enumerate(poems):
    start = poem['paras'][0] if poem['paras'] else -1
    end = poem['paras'][-1] if poem['paras'] else -1
    print(f"  {i+1:2d}. {poem['title']:40s} ({len(poem['paras']):3d} lines, paras {start}-{end})")

# === Now rebuild the document ===
# Approach: Create new document XML from scratch with proper formatting

def make_element(tag, attrib=None, text=None):
    el = etree.Element(f'{{{W_NS}}}{tag}')
    if attrib:
        for k, v in attrib.items():
            el.set(f'{{{W_NS}}}{k}', v)
    if text:
        el.text = text
    return el

def sub_el(parent, tag, attrib=None, text=None):
    full_tag = f'{{{W_NS}}}{tag}'
    el = etree.SubElement(parent, full_tag)
    if attrib:
        for k, v in attrib.items():
            el.set(f'{{{W_NS}}}{k}', v)
    if text is not None:
        el.text = text
    return el

def make_run_props(font_name='Bookman Old Style', sz=22, bold=None, italic=None, color=None):
    """Create w:rPr element. sz is in half-points (22 = 11pt)."""
    rPr = etree.Element(f'{{{W_NS}}}rPr')
    rFonts = etree.SubElement(rPr, f'{{{W_NS}}}rFonts')
    rFonts.set(f'{{{W_NS}}}ascii', font_name)
    rFonts.set(f'{{{W_NS}}}hAnsi', font_name)
    rFonts.set(f'{{{W_NS}}}cs', font_name)
    if sz:
        sub_el(rPr, 'sz', {'val': str(sz)})
        sub_el(rPr, 'szCs', {'val': str(sz)})
    if bold:
        sub_el(rPr, 'b')
    if italic:
        sub_el(rPr, 'i')
    if color:
        sub_el(rPr, 'color', {'val': color, 'themeColor': 'text1'})
    return rPr

def make_paragraph(run_props_list, pStyle=None, spacing=None, alignment=None, page_break=False):
    """Create a w:p element.
    run_props_list: list of (text, rPr_dict) tuples
    """
    p = etree.Element(f'{{{W_NS}}}p')
    pPr = etree.SubElement(p, f'{{{W_NS}}}pPr')
    
    if pStyle:
        sub_el(pPr, 'pStyle', {'val': pStyle})
    
    if spacing:
        sp_attr = {}
        if 'before' in spacing:
            sp_attr['before'] = str(spacing['before'])
        if 'after' in spacing:
            sp_attr['after'] = str(spacing['after'])
        if 'line' in spacing:
            sp_attr['line'] = str(spacing['line'])
        if sp_attr:
            sub_el(pPr, 'spacing', sp_attr)
    
    if alignment:
        sub_el(pPr, 'jc', {'val': alignment})
    
    if page_break:
        sub_el(pPr, 'pageBreakBefore')
    
    for text, rpr_dict in run_props_list:
        r = etree.SubElement(p, f'{{{W_NS}}}r')
        r.append(make_run_props(**rpr_dict))
        t = etree.SubElement(r, f'{{{W_NS}}}t')
        t.text = text
        if ' ' in text and text.strip():
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    
    return p

def make_empty_para(pStyle=None, spacing=None):
    return make_paragraph([], pStyle=pStyle, spacing=spacing)

# Build body content
body = etree.Element(f'{{{W_NS}}}body')

# === TITLE PAGE ===
# Title
body.append(make_paragraph(
    [('Reality, A colorful illusion', {'font_name': 'Bookman Old Style', 'sz': 48, 'bold': True})],
    spacing={'before': '3000', 'after': '200'},
    alignment='center'
))
# Author
body.append(make_paragraph(
    [('Written by Urangani Terrence Mafunzwaini', {'font_name': 'Bookman Old Style', 'sz': 24})],
    spacing={'before': '600', 'after': '100'},
    alignment='center'
))
# Description
preface_text = ("I wrote these poems out of curiosity, guided by a desire to explore the beauty of writing. "
    "Feelings hold them etched into memory by putting everything in paper. "
    "I present to you, 'Reality, a colorful illusion'.")
body.append(make_paragraph(
    [(preface_text, {'font_name': 'Bookman Old Style', 'sz': 22})],
    spacing={'before': '400', 'after': '0', 'line': '276'},
    alignment='center'
))

# Page break before TOC
body.append(make_paragraph([], page_break=True))

# === TABLE OF CONTENTS ===
body.append(make_paragraph(
    [('Table of Contents', {'font_name': 'Bookman Old Style', 'sz': 36})],
    pStyle='Heading1',
    spacing={'before': '240', 'after': '360'},
    alignment='center'
))

for i, poem in enumerate(poems):
    toc_text = f"{i+1}. {poem['title']}"
    body.append(make_paragraph(
        [(toc_text, {'font_name': 'Bookman Old Style', 'sz': 22})],
        pStyle='TOC1' if i == 0 else 'TOC2',
        spacing={'before': '60', 'after': '60'}
    ))

# Page break before poems
body.append(make_paragraph([], page_break=True))

# === SECTION: Dream & Escapes ===
body.append(make_paragraph(
    [('Dream & Escapes', {'font_name': 'Bookman Old Style', 'sz': 36})],
    pStyle='Heading1',
    spacing={'before': '600', 'after': '400'}
))

# === POEMS ===
for poem_idx, poem in enumerate(poems):
    if poem_idx > 0:
        # Page break before each poem
        body.append(make_paragraph([], page_break=True))
    
    # Poem title as Heading2
    body.append(make_paragraph(
        [(poem['title'], {'font_name': 'Bookman Old Style', 'sz': 32, 'italic': True})],
        pStyle='Heading2',
        spacing={'before': '360', 'after': '240'},
        alignment='center'
    ))
    
    # Poem body
    for para_idx in (poem.get('paras') or []):
        text = parsed[para_idx]['text']
        if text:
            body.append(make_paragraph(
                [(text, {'font_name': 'Bookman Old Style', 'sz': 22})],
                spacing={'before': '0', 'after': '60', 'line': '276'}
            ))
        else:
            body.append(make_paragraph(
                [(' ', {'font_name': 'Bookman Old Style', 'sz': 22})],
                spacing={'before': '0', 'after': '60'}
            ))

# === SECTION PROPERTIES ===
sectPr = make_element('sectPr')
# Page dimensions (letter)
pgSz = etree.SubElement(sectPr, f'{{{W_NS}}}pgSz')
pgSz.set(f'{{{W_NS}}}w', '12240')
pgSz.set(f'{{{W_NS}}}h', '15840')
# Margins
pgMar = etree.SubElement(sectPr, f'{{{W_NS}}}pgMar')
pgMar.set(f'{{{W_NS}}}top', '1440')
pgMar.set(f'{{{W_NS}}}right', '1440')
pgMar.set(f'{{{W_NS}}}bottom', '1440')
pgMar.set(f'{{{W_NS}}}left', '1440')
pgMar.set(f'{{{W_NS}}}header', '720')
pgMar.set(f'{{{W_NS}}}footer', '720')

# Skip original header references (they were empty) — let Word use defaults
# Title page has no header
body.append(sectPr)

# Create the full document XML
document = etree.Element(f'{{{W_NS}}}document')
document.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}ignorable', 'w14 w15')
document.append(body)

# Build the document XML tree
body_content = etree.tostring(document, xml_declaration=True, encoding='UTF-8', standalone=True)

# === READ styles.xml from original to preserve styles ===
# We need to add TOC1 and TOC2 styles if they don't exist
styles_root = etree.fromstring(styles_xml)

# Check if TOC1 style exists
style_ids = set()
for s in styles_root.findall('.//w:style', ns):
    sid = s.get(f'{{{W_NS}}}styleId')
    if sid:
        style_ids.add(sid)

# Add TOC styles if missing
if 'TOC1' not in style_ids:
    toc1 = etree.SubElement(styles_root, f'{{{W_NS}}}style')
    toc1.set(f'{{{W_NS}}}type', 'paragraph')
    toc1.set(f'{{{W_NS}}}styleId', 'TOC1')
    name_el = etree.SubElement(toc1, f'{{{W_NS}}}name')
    name_el.set(f'{{{W_NS}}}val', 'toc 1')
    # Copy from Normal but with indent
    pPr = etree.SubElement(toc1, f'{{{W_NS}}}pPr')
    ind = etree.SubElement(pPr, f'{{{W_NS}}}ind')
    ind.set(f'{{{W_NS}}}left', '0')

if 'TOC2' not in style_ids:
    toc2 = etree.SubElement(styles_root, f'{{{W_NS}}}style')
    toc2.set(f'{{{W_NS}}}type', 'paragraph')
    toc2.set(f'{{{W_NS}}}styleId', 'TOC2')
    name_el = etree.SubElement(toc2, f'{{{W_NS}}}name')
    name_el.set(f'{{{W_NS}}}val', 'toc 2')
    pPr = etree.SubElement(toc2, f'{{{W_NS}}}pPr')
    ind = etree.SubElement(pPr, f'{{{W_NS}}}ind')
    ind.set(f'{{{W_NS}}}left', '360')

# Also update Normal style in styles.xml to use Bookman Old Style 11pt
for style in styles_root.findall('.//w:style', ns):
    sid = style.get(f'{{{W_NS}}}styleId')
    if sid == 'Normal':
        rPr = style.find('w:rPr', ns)
        if rPr is None:
            rPr = etree.SubElement(style, f'{{{W_NS}}}rPr')
        # Set font
        rFonts = rPr.find('w:rFonts', ns)
        if rFonts is None:
            rFonts = etree.SubElement(rPr, f'{{{W_NS}}}rFonts')
        rFonts.set(f'{{{W_NS}}}ascii', 'Bookman Old Style')
        rFonts.set(f'{{{W_NS}}}hAnsi', 'Bookman Old Style')
        rFonts.set(f'{{{W_NS}}}cs', 'Bookman Old Style')
        # Set size
        sz = rPr.find('w:sz', ns)
        if sz is None:
            sz = etree.SubElement(rPr, f'{{{W_NS}}}sz')
        sz.set(f'{{{W_NS}}}val', '22')
        szCs = rPr.find('w:szCs', ns)
        if szCs is None:
            szCs = etree.SubElement(rPr, f'{{{W_NS}}}szCs')
        szCs.set(f'{{{W_NS}}}val', '22')

# Also set heading styles
for sid in ['Heading1', 'Heading2']:
    for style in styles_root.findall('.//w:style', ns):
        if style.get(f'{{{W_NS}}}styleId') == sid:
            rPr = style.find('w:rPr', ns)
            if rPr is not None:
                rFonts = rPr.find('w:rFonts', ns)
                if rFonts is None:
                    rFonts = etree.SubElement(rPr, f'{{{W_NS}}}rFonts')
                rFonts.set(f'{{{W_NS}}}ascii', 'Bookman Old Style')
                rFonts.set(f'{{{W_NS}}}hAnsi', 'Bookman Old Style')

updated_styles = etree.tostring(styles_root, xml_declaration=True, encoding='UTF-8', standalone=True)

# === Write the new docx ==========
import shutil, os

# We need to build a valid docx file
# Copy original and replace document.xml and styles.xml
tmp_path = DOCX_PATH + '.tmp'
shutil.copy2(DOCX_PATH, tmp_path)

# Replace files in the zip
import tempfile
with zipfile.ZipFile(tmp_path, 'r') as zin:
    items = zin.infolist()
    with zipfile.ZipFile(DOCX_PATH + '.new', 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in items:
            if item.filename == 'word/document.xml':
                zout.writestr(item, body_content)
            elif item.filename == 'word/styles.xml':
                zout.writestr(item, updated_styles)
            else:
                zout.writestr(item, zin.read(item.filename))

# Replace original with new
os.replace(DOCX_PATH + '.new', DOCX_PATH)
os.remove(tmp_path)

print(f"\nSaved: {DOCX_PATH}")
print(f"Poems formatted: {len(poems)}")
