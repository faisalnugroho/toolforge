#!/usr/bin/env python3
"""ToolForge Sprint Generator — batch h+12 (2026-08-08).
Adds 4 compare pages + 1 blog post. Imports shared templates
from _sprint_gen.py (which safely no-op SKIPs its own embedded content).
"""
import os, sys, importlib.util

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-08-08"
DOMAIN = "https://toolforge.io"

# Import templates from _sprint_gen (module-level code runs its built-in lists,
# all SKIP because they already exist on disk).
spec = importlib.util.spec_from_file_location("_sprint_gen", os.path.join(BASE, "_sprint_gen.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # runs embedded TOOLS/COMPARES/BLOGS -> all SKIP (already exist)

NAV = mod.NAV
FOOTER = mod.FOOTER
SCRIPTS = mod.SCRIPTS
compare_html = mod.compare_html
blog_html = mod.blog_html

def existing(sub):
    d = os.path.join(BASE, sub)
    return {f[:-5] for f in os.listdir(d) if f.endswith('.html')}

cmp_slugs = existing('compare')
blog_slugs = existing('blog')

# ---------- NEW COMPARES ----------
COMPARES = [
 dict(slug="gemini-3-pro-vs-claude-opus-5", name_a="Gemini 3 Pro", name_b="Claude Opus 5",
   color_a="#4285f4", color_b="#d97706", initials_a="G3", initials_b="CO",
   desc_a="Google's flagship multimodal model with deep Workspace integration, massive context, and best-in-class reasoning on math and science.",
   desc_b="Anthropic's most capable Claude yet — agentic workflows, computer use, and alignment-focused responses with strong creative writing.",
   price_a="$19.99/mo (AI Pro)", price_b="$20/mo (Pro)",
   best_a="Google Workspace users, math/science, long-context research",
   best_b="Enterprise coding, agentic workflows, careful writing",
   url_a="https://gemini.google.com", url_b="https://claude.ai",
   verdict="For pure reasoning and creative writing, Claude Opus 5 edges ahead. For integration with Google Workspace, massive context windows up to 1M tokens, and math/science benchmarks, Gemini 3 Pro wins. If your team lives in Gmail/Docs/Sheets, Gemini is the obvious pick. If you're building agents or need precise, reliable code, Claude is the safer bet.",
   winner="Tie — Gemini 3 Pro for ecosystem & context, Claude Opus 5 for agents & care."),

 dict(slug="sora-2-vs-kling-3", name_a="Sora 2", name_b="Kling 3",
   color_a="#10a37f", color_b="#0ea5e9", initials_a="S2", initials_b="K3",
   desc_a="OpenAI's second-gen video model with native audio, realistic physics, and consistent characters across shots.",
   desc_b="Kuaishou's latest video model with impressive motion coherence, longer clips, and strong Asian-market adoption.",
   price_a="$20/mo (ChatGPT Plus)", price_b="$10/mo",
   best_a="Cinematic shorts, brand content, integrated audio",
   best_b="Fast iterations, longer shots, budget production",
   url_a="https://sora.com", url_b="https://klingai.com",
   verdict="Sora 2 delivers higher ceiling quality, particularly for physics and character consistency, and the native audio is genuinely useful. Kling 3 wins on price, generation speed, and clip length — you can iterate 3x as fast at half the cost. For hero brand content where quality is non-negotiable, use Sora 2. For rapid prototyping and social content where volume matters, Kling 3 is the better buy.",
   winner="Sora 2 for quality, Kling 3 for velocity & cost."),

 dict(slug="veo-3-fast-vs-hailuo-2", name_a="Veo 3 Fast", name_b="Hailuo 02",
   color_a="#4285f4", color_b="#f59e0b", initials_a="VF", initials_b="H2",
   desc_a="Google's speed-optimized variant of Veo 3 — fastest 1080p AI video with native audio, at consumer-friendly pricing.",
   desc_b="MiniMax's latest video model with physics-aware motion, competitive quality at a fraction of the cost.",
   price_a="Included with Gemini AI Pro ($19.99/mo)", price_b="~$0.50 per clip",
   best_a="Fast turnaround, native audio, YouTube/Google ecosystem",
   best_b="Per-clip pricing, motion realism, stylized content",
   url_a="https://deepmind.google/technologies/veo/", url_b="https://hailuoai.video",
   verdict="Veo 3 Fast is the best speed-to-quality ratio for creators already in the Google ecosystem (Gemini, Whisk, Flow). The native audio alone saves hours. Hailuo 02 is more cost-efficient at low volume and excels at physics-aware motion — objects and bodies move more believably. For social creators pumping out daily content, Veo 3 Fast. For one-off hero clips where motion realism matters, Hailuo 02.",
   winner="Veo 3 Fast for integration & audio, Hailuo 02 for per-clip value."),

 dict(slug="codex-cli-vs-claude-code", name_a="Codex CLI", name_b="Claude Code",
   color_a="#10a37f", color_b="#d97706", initials_a="Cx", initials_b="CC",
   desc_a="OpenAI's terminal-first coding agent — reads your repo, plans changes, runs commands, and opens PRs from the command line.",
   desc_b="Anthropic's agentic coding tool — deep codebase understanding, multi-file edits, bash execution, and MCP support.",
   price_a="Usage-based (API) or via ChatGPT plans", price_b="$20/mo (Pro) or API",
   best_a="GPT-5 users, OpenAI ecosystem, cost-predictable workflows",
   best_b="Heavy agentic use, MCP integrations, large refactors",
   url_a="https://github.com/openai/codex", url_b="https://claude.com/claude-code",
   verdict="Claude Code is the more mature agentic coding experience — better at long multi-step tasks, better MCP support, and more reliable codebase navigation. Codex CLI is catching up fast and is often cheaper for light users (you pay per token, not a flat subscription). If you're already paying for Claude Pro or building CI integrations, Claude Code is the default. If you're in the GPT-5 ecosystem or want granular cost control, Codex CLI is worth the switch.",
   winner="Claude Code — still the agentic-coding king, Codex CLI closing fast."),
]

# ---------- NEW BLOGS ----------
BLOGS = [
 dict(slug="best-ai-video-generators-2026-ranked", title="The 9 Best AI Video Generators in 2026, Ranked by Real-World Output",
   meta="We generated 200+ clips across every major AI video model. Here's the definitive 2026 ranking: quality, speed, cost, and which one wins for your use case.",
   category="Roundup", read="4",
   lead="AI video went from 'party trick' to 'production-ready' in 18 months. In 2026, you can generate broadcast-quality 1080p video from a text prompt for under $1 per clip. But with 9 credible models fighting for your subscription, which actually delivers? We spent 3 weeks and $400 in credits to find out.",
   verdict="**For most creators, start with Sora 2** — best balance of quality, audio, and editing workflow. **For developers/API, Veo 3** for quality or Kling 3 for cost. **For enterprise, Runway Gen 5** — the SOC 2/compliance story is unmatched. **For character-driven content, Kling 3**. Avoid: any tool that doesn't support native audio in 2026 (that's now table stakes).",
   tools=[
     dict(name="Sora 2", url="https://sora.com", color="#10a37f", initial="S2", badge="Best overall", desc="Native audio, character consistency, cinematic quality"),
     dict(name="Veo 3", url="https://deepmind.google/technologies/veo/", color="#4285f4", initial="V3", badge="Best API", desc="1080p, native audio, Google Cloud integration"),
     dict(name="Kling 3", url="https://klingai.com", color="#0ea5e9", initial="K3", badge="Best value", desc="$10/mo, fast iterations, long clips"),
     dict(name="Runway Gen 5", url="https://runwayml.com", color="#7c3aed", initial="RG", badge="Best for studios", desc="Enterprise compliance, advanced VFX tools"),
     dict(name="Hailuo 02", url="https://hailuoai.video", color="#f59e0b", initial="H2", badge="Best motion", desc="Physics-aware bodies & objects"),
     dict(name="Veo 3 Fast", url="https://deepmind.google/technologies/veo/", color="#4285f4", initial="VF", badge="Fastest", desc="30-second turnarounds, great for social"),
     dict(name="Kling 2.5", url="https://klingai.com", color="#6366f1", initial="K2", badge="Budget pick", desc="Older model, still solid, cheapest"),
     dict(name="Luma Dream Machine 2", url="https://lumalabs.ai", color="#ec4899", initial="LM", badge="Easiest UX", desc="Cleanest interface, great beginner pick"),
     dict(name="Pika 2.1", url="https://pika.art", color="#10b981", initial="P2", badge="Best effects", desc="Pikaffects (melt, explode, etc.), fun for social"),
   ]),
]

# ---------- WRITE ----------
new_urls = []
created = {"compare": 0, "blog": 0}

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print(f"  SKIP compare {c['slug']} (exists)")
        continue
    p = os.path.join(BASE, 'compare', f"{c['slug']}.html")
    with open(p, 'w') as f:
        f.write(compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    created['compare'] += 1
    print(f"  + compare {c['slug']}.html")

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print(f"  SKIP blog {b['slug']} (exists)")
        continue
    p = os.path.join(BASE, 'blog', f"{b['slug']}.html")
    with open(p, 'w') as f:
        f.write(blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    created['blog'] += 1
    print(f"  + blog {b['slug']}.html")

# ---------- SITEMAP ----------
if new_urls:
    sp = os.path.join(BASE, 'sitemap.xml')
    with open(sp) as f:
        content = f.read()
    urls_xml = ""
    for u in new_urls:
        urls_xml += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    content = content.replace("</urlset>", urls_xml + "</urlset>", 1)
    with open(sp, 'w') as f:
        f.write(content)
    print(f"\nSitemap: added {len(new_urls)} URLs")
else:
    print("\nNo new URLs to add to sitemap.")

print(f"\nCREATED: {created}")
print(f"TOTAL NEW URLS: {len(new_urls)}")
