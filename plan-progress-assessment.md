# ProposedPlan.md — Progress Assessment

## Overview

`ProposedPlan.md` is a generic template for a poetry book + website project. The current project is significantly further along, making most of the plan's initial steps already complete or superseded.

## Status by Item

| Plan Item | Current Status | Notes |
|---|---|---|
| **Define core theme** | ✅ Complete | Theme established: "Reality, a colorful illusion" |
| **Group poems by theme** | ✅ Complete | Tags system active: nature, love, identity, darkness, time |
| **Select anchor poems** | ❌ Not done | No specific anchor/featured poems identified |
| **Format each poem** | ⚠️ Partial | Markdown poems consistent; docx has formatting issues (see audit) |
| **Write front matter** | ✅ Complete | `00_Front_Matter.md` exists with preface content |
| **Add closing matter** | ❌ Not done | No author's note, afterword, or commentary |
| **Proof and edit** | 🟡 Ongoing | Docx needs standardization pass |
| **Design homepage** | ✅ Complete | `index.html` with header, featured layout, poem display |
| **Build archive** | ✅ Complete | `poems.json` with 65 entries; category nav filtering works |
| **Format poem pages** | ✅ Complete | Markdown rendered via marked.js; consistent styling |
| **Add engagement layer** | ❌ Not done | No audio readings, commentary, or newsletter |
| **Create about page** | ❌ Not done | No dedicated about page; brief bio in footer only |
| **Set navigation flow** | ✅ Partial | Tag-based filtering exists; no prev/next poem navigation |
| **Test responsiveness** | ⚠️ Partial | CSS media queries now added for mobile |
| **Voice consistency** | ✅ Good | Consistent tone across both book and site |
| **Cross-integration (QR, etc.)** | ❌ Not done | Future idea only |

## What the Plan Misses

- **Poetry Studio editor** (`studio.html`) — a working CRUD interface for managing poems
- **Export features** — PDF and ZIP export endpoints exist in the Python backend
- **Docx ↔ Markdown sync** — the docx has 6 poems; the website has 65 — a gap that needs bridging
- **Version control / CI** — no mention of git workflow for content updates

## Priority Next Steps

1. **Sync docx with website** — bring the docx up to date with all 65 poems, or decide to use markdown as source of truth
2. **Closing matter** — add author's note / afterword to complete the book
3. **Anchor poems** — select and highlight 3–5 signature pieces on the homepage
4. **Engagement layer** — audio readings would add significant value for a poetry collection
5. **About page** — separate page with author bio and creative journey
