# ToolForge

AI Tools Directory — a curated, honest review site for the best AI tools of 2026.

## Stack
- Pure static HTML/CSS/JS — no build step, no framework
- Vercel/Netlify-ready (or any static host)
- ~12 pages, < 100KB total

## Structure
```
toolforge/
├── index.html              # Home (hero, categories, featured tools)
├── tools.html              # Browse all 12 tools (filterable)
├── about.html              # Methodology + team + disclosure
├── contact.html            # Contact form
├── tools/                  # 8 tool detail pages
│   ├── cursor.html
│   ├── elevenlabs.html
│   ├── jasper.html
│   ├── midjourney.html
│   ├── perplexity.html
│   ├── runway.html
│   ├── copy-ai.html
│   └── notion-ai.html
├── css/
│   └── style.css           # Design system (Vercel-clean + dark mode)
├── js/
│   └── main.js             # Theme toggle, category filter, newsletter
├── assets/                 # (empty — to be filled)
├── robots.txt
└── sitemap.xml
```

## Local Development
```bash
cd ~/projects/toolforge
python3 -m http.server 8000
# Open http://localhost:8000
```

## Deploy
See `static-site-hosting` skill for Netlify/Vercel deploy.

## Monetization
- **Phase 1 (now):** Affiliate links. Sign up for programs at Jasper, ElevenLabs, Copy.ai, Midjourney, Cursor, Notion, Perplexity, Runway. Replace placeholder `#` links with real affiliate URLs.
- **Phase 2 (1-3 months):** SEO content. Target "best AI tool for X" keywords. Add 2-3 new tool reviews per week.
- **Phase 3 (3+ months):** Apply for Google AdSense (need 1000+ daily visitors).
- **Phase 4 (6+ months):** Sponsored newsletter slots. Sponsored listings (clearly marked).

## Customization
- Brand color: change `--accent` in `css/style.css`
- Add a new tool: copy any `tools/<name>.html`, update content
- Add new category: add card to `index.html` categories section + add filter button in `tools.html`
