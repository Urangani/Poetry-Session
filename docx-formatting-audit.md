# Reality-a-colorful-illusion.docx — Formatting Audit

## Font/Size Issues

| Issue | Details |
|---|---|
| **Font face override** | Style base defines `Bookman Old Style 11pt`, but all runs are direct-formatted to `Times New Roman` |
| **7 font sizes in Normal** | 7.5pt (1 run), 8pt (235), 10pt (31), 12pt (59), 14pt (1), 20pt (7), 24pt (1) — likely from copy-paste |
| **8pt bloat** | 235 runs at 8pt — probably spacer/separator lines that should be standardized or removed |
| **Orphan sizes** | Single runs at 7.5pt and 14pt — typographic artifacts |
| **Largest sizes** | 20pt (7 runs) and 24pt (1 run — the title) used for headings via direct format instead of Heading style |

## Structural Issues

| Issue | Details |
|---|---|
| **Spacer paragraphs** | ~1500 empty Normal paragraphs used for vertical spacing instead of proper `spacing` or page breaks |
| **Heading2 spacing** | 6 Heading2 paragraphs use default style spacing; 2 use `before=0, after=0` — inconsistent |
| **TOC incomplete** | "Once Upon a Time" exists as a Heading2 but is missing from the Table of Contents |
| **TOC page numbers** | Hardcoded (e.g. "Jump5" with no space) instead of auto-generated TOC fields |
| **No section breaks** | Single continuous section — no separation between front matter, poems, or back matter |
| **Headers/footers empty** | Header/footer references exist in document.xml but their relationship IDs are null — no actual content |
| **BodyText unused** | 4 empty BodyText paragraphs near "Jump" poem — probably leftovers |

## Content Sync

| Issue | Details |
|---|---|
| **Poems in docx** | Only 6 poems (Jump, The dreamer, Urangani's reality, The moon is lonely tonight, Don't count the stars, Once Upon a Time) |
| **Poems in website** | 65 poems with metadata in `poems.json` — docx is far behind |

## Recommendations

1. Reapply the base Normal style (Bookman Old Style) and remove direct font/size overrides from all runs
2. Standardize body text to a single size (11pt or 12pt); use Heading styles for titles
3. Replace empty spacer paragraphs with proper paragraph spacing (`spaceAfter` or `spaceBefore`)
4. Rebuild TOC using Word's auto-generate feature (or remove and list manually)
5. Add section breaks between front matter, each poem section, and back matter
6. Set up running headers/footers (e.g. poem title on verso, author on recto)
7. Sync docx content with the 65 poems in the website markdown files
