#!/usr/bin/env python3
"""ToolForge sprint batch 2026-08-05 — head-exec _sprint_gen.py templates,
dict-based data, skips existing slugs, regenerates sitemap from disk."""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = '2026-08-05'

# ---- exec template head (everything before CONTENT DATA marker) ----
src = open(os.path.join(BASE, '_sprint_gen.py')).read()
head = src.split('# =================== CONTENT DATA ===================')[0]
g = {'TODAY': TODAY}
exec(head, g)
tool_html, compare_html, blog_html = g['tool_html'], g['compare_html'], g['blog_html']
DOMAIN = g['DOMAIN']
tool_slugs = {f[:-5] for f in os.listdir(os.path.join(BASE, 'tools')) if f.endswith('.html')}
blog_slugs = {f[:-5] for f in os.listdir(os.path.join(BASE, 'blog')) if f.endswith('.html')}
cmp_slugs  = {f[:-5] for f in os.listdir(os.path.join(BASE, 'compare')) if f.endswith('.html')}

TOOLS = [
 dict(slug="gemini-code-assist", name="Gemini Code Assist", tagline="Google's Gemini-powered coding assistant for VS Code and JetBrains — agent mode, repo-aware customization, and a genuinely free individual tier.", category="Coding",
   color1="#4285f4", color2="#3367d6", initials="GC", price="Free", price_label="Individual tier", price_num="0",
   free_tier="Free for individuals", rating="4.5/5", rating_num="4.5", users="1M+ developers", founded="2024",
   headline="Frontier coding help with a real free tier",
   intro="Gemini Code Assist is Google's answer to GitHub Copilot — inline completions, chat, and an agent mode inside VS Code and JetBrains IDEs. Its standout is pricing: the individual tier is free with generous monthly limits, and the enterprise tier adds code customization so suggestions match your private repos and conventions. Under the hood it runs Gemini 2.5-class models tuned for code.",
   who_for="Google Cloud shops, cost-sensitive developers priced out of Copilot, and enterprises that want suggestions tuned to their internal codebase.",
   features=[("🤖","Agent mode","Multi-step tasks: scaffold features, run tests, and edit across files from a single instruction."),
             ("🆓","Free individual tier","Tens of thousands of completions and chat requests per month at $0 — no card required."),
             ("🏢","Code customization","Enterprise tier grounds suggestions in your private repos and style guides."),
             ("☁️","Google Cloud native","Deep hooks into Cloud Shell, Android Studio, Workstations, and BigQuery.")],
   pros=["Best free tier among frontier coding assistants",
         "Enterprise code customization actually works",
         "Tight Google Cloud and Android integration",
         "Fast, low-latency completions"],
   cons=["Ecosystem smaller than Copilot's",
         "Best features gated behind enterprise plan",
         "Agent mode occasionally over-edits",
         "No JetBrains parity on every feature"],
   verdict="The default pick if you want frontier coding help for free, or if your org already lives on Google Cloud. Copilot still leads on ecosystem; Gemini Code Assist wins on price and Google integration.",
   cta_url="https://codeassist.google"),

 dict(slug="kokoro", name="Kokoro", tagline="The open-weight 82M-parameter TTS model that delivers studio-grade voices on a laptop CPU.", category="Audio",
   color1="#0f172a", color2="#334155", initials="Ko", price="Free", price_label="Apache-2.0", price_num="0",
   free_tier="Fully open source", rating="4.6/5", rating_num="4.6", users="500k+ downloads", founded="2025",
   headline="Big-studio voice quality from a pocket model",
   intro="Kokoro is the open-weight text-to-speech model that punched far above its size class when it dropped in early 2025. At just 82 million parameters it tops community TTS quality arenas, ships under Apache-2.0, and runs in real time on a laptop CPU — no GPU, no API key, no per-character bill. Builders reach for it when they need narration, agents, or audiobooks without cloud pricing.",
   who_for="Indie developers, accessibility builders, and anyone producing hours of narration who wants cloud-quality voices without cloud fees.",
   features=[("🪶","82M parameters","Tiny enough to run on CPU in real time — deploys anywhere."),
             ("🏆","Arena-topping quality","Rated alongside or above paid cloud TTS in blind listening tests."),
             ("🌍","Multi-language voices","American/British English plus Japanese, Chinese, French, and more."),
             ("⚡","Sub-second synthesis","Generate minutes of audio in seconds on commodity hardware.")],
   pros=["Completely free, Apache-2.0 license",
         "CPU-only realtime performance",
         "Consistent, broadcast-friendly default voices",
         "Thriving wrapper ecosystem (FastAPI, Gradio, ONNX)"],
   cons=["Fewer voices than ElevenLabs or Cartesia",
         "Emotion control is limited",
         "No official hosted API",
         "Long-form consistency still lags the top paid models"],
   verdict="The best free TTS you can self-host, full stop. For character work or cloned voices, ElevenLabs still leads — but for bulk narration on a budget, Kokoro is unbeatable.",
   cta_url="https://huggingface.co/hexgrad/Kokoro-82M"),

 dict(slug="cartesia-sonic-3", name="Cartesia Sonic 3", tagline="The real-time voice AI that laughs, sighs, and emotes — sub-100ms latency for live agents.", category="Voice",
   color1="#06b6d4", color2="#0284c7", initials="CS", price="$5", price_label="entry plan", price_num="5",
   free_tier="Free tier available", rating="4.6/5", rating_num="4.6", users="10k+ developers", founded="2023",
   headline="The voice that keeps pace with a phone call",
   intro="Cartesia's Sonic 3 is built on state-space models instead of transformers, which is how it achieves latency low enough for live phone and voice-agent work. Beyond speed, its signature trick is genuine non-verbal emotion — laughter, sighs, whispering — generated inline from your text. It's become the default voice layer for a large share of production voice agents.",
   who_for="Voice-agent developers, call-center builders, and interactive apps where round-trip latency decides whether the experience works at all.",
   features=[("😄","Real emotion","Inline laughter, breaths, and sighs — no audio editing needed."),
             ("⚡","Sub-100ms latency","Fast enough for natural back-and-forth on a live call."),
             ("🌍","40+ languages","One API for English, Spanish, Hindi, Japanese, and more."),
             ("🧬","Instant cloning","Clone a voice from a few seconds of reference audio.")],
   pros=["Fastest production TTS available",
         "Emotional range competitors can't match",
         "Stable at scale — built for agents",
         "Fair usage-based pricing"],
   cons=["Voice library smaller than ElevenLabs",
         "Studio narration workflows are thinner",
         "Best served via API — less friendly for non-devs"],
   verdict="The no-brainer choice for voice agents and interactive audio where latency is physics. For audiobook narration or a giant voice catalog, ElevenLabs still has the edge.",
   cta_url="https://cartesia.ai"),
]

COMPARES = [
 dict(slug="cursor-2-vs-windsurf", name_a="Cursor 2", name_b="Windsurf", color_a="#000000", color_b="#0a72ef",
   initials_a="Cu", initials_b="Ws", url_a="https://www.cursor.com/?via=toolforge", url_b="https://windsurf.com",
   desc_a="The AI-first editor with the Composer model and multi-agent workflows", desc_b="The agentic IDE built around Cascade flows",
   price_a="$20/mo Pro", price_b="$15/mo Pro", best_a="big refactors, multi-file edits, mature ecosystem", best_b="fluid agent flows, lower price, lighter feel",
   verdict="Use <strong>Cursor 2</strong> if you want the most mature AI editor — its in-house Composer model makes multi-file edits fast and cheap, and the extension ecosystem is largest. Use <strong>Windsurf</strong> if you prefer Cascade's flow-based agent UX and a slightly lower price. Both are excellent in 2026; Cursor leads on ecosystem depth, Windsurf on agentic elegance.",
   winner="Cursor 2 — slightly, on maturity"),

 dict(slug="seedream-4-vs-nano-banana", name_a="Seedream 4", name_b="Nano Banana", color_a="#f97316", color_b="#d97706",
   initials_a="Sd", initials_b="Nb", url_a="https://seed.bytedance.com/en/", url_b="https://gemini.google.com",
   desc_a="ByteDance's 4K native image model with sharp text rendering", desc_b="Google's Gemini 2.5 Flash Image — the viral editing king",
   price_a="~$0.03/image API", price_b="Free in Gemini app", best_a="4K output, posters, legible typography, batch API", best_b="photo editing, character consistency, free access",
   verdict="Use <strong>Seedream 4</strong> when you need native 4K generation, crisp in-image text, and high-volume API pricing — it's the production workhorse. Use <strong>Nano Banana</strong> when you're editing real photos or need character consistency across a series, all for free inside Gemini. Creators increasingly use both: Nano Banana to edit, Seedream to scale.",
   winner="Tie — Seedream for generation, Nano Banana for editing"),

 dict(slug="glm-5-vs-kimi-k2", name_a="GLM-5", name_b="Kimi K2", color_a="#7c3aed", color_b="#111827",
   initials_a="GL", initials_b="Kk", url_a="https://chat.z.ai", url_b="https://www.kimi.com",
   desc_a="Zhipu's flagship open-weight model with strong multilingual chops", desc_b="Moonshot's agentic MoE that topped open-source coding benchmarks",
   price_a="Free chat / cheap API", price_b="Free chat / cheap API", best_a="multilingual tasks, reasoning, enterprise deployment in China", best_b="agentic coding, tool use, long autonomous runs",
   verdict="Use <strong>GLM-5</strong> for multilingual workloads and general reasoning with enterprise-grade Chinese-market support. Use <strong>Kimi K2</strong> when the job is agentic coding or long tool-use chains — its MoE architecture was tuned specifically for autonomous task execution. Both are open-weight and radically cheaper than US frontier APIs.",
   winner="Kimi K2 — narrowly, on agentic coding"),
]

BLOGS = [
 dict(slug="ai-tools-for-manga-artists-2026",
   title="AI Tools for Manga Artists in 2026: What Actually Helps (and What to Skip)",
   meta="The AI tools manga artists actually use in 2026 — concept references, style-consistent characters, screentone shortcuts, and translation — without losing your line work.",
   category="AI Tools for Creators", read=9,
   lead="Manga is a deadline sport. The artists winning with AI in 2026 aren't letting it draw pages — they're using it for reference, ideation, and the grind around the art, keeping the line work unmistakably theirs.",
   verdict="Start with <strong>Niji Journey</strong> for style-true anime references and <strong>Clip Studio Paint</strong> as your canvas. Add <strong>Scenario</strong> if you publish serialized work and need the same character on-model for 200 chapters. Everything else on this list is optional acceleration — your pen is still the product.",
   tools=[
     dict(name="Niji Journey", url="https://nijijourney.com", color="#db2777", initial="Ni", badge="$10/mo", desc="The anime-specialized Midjourney collab — the most style-accurate manga references available"),
     dict(name="Midjourney", url="https://www.midjourney.com", color="#1f2937", initial="Mj", badge="$10/mo", desc="Niji mode 6 nails shonen/shojo aesthetics; use --niji for panel concept art"),
     dict(name="Scenario", url="https://www.scenario.com", color="#7c3aed", initial="Sc", badge="$29/mo", desc="Train a LoRA on YOUR characters — same face, same outfit, chapter after chapter"),
     dict(name="Clip Studio Paint", url="https://www.clipstudio.net/en/", color="#0ea5e9", initial="CP", badge="$4.50/mo", desc="The industry canvas; its AI-adjacent tools (auto-tone, pose scanner) save real hours"),
     dict(name="Leonardo AI", url="https://leonardo.ai/?via=toolforge", color="#f97316", initial="Le", badge="Free tier", desc="Fast background and environment concepts when Chapter 12 needs a new city"),
     dict(name="Krea", url="https://www.krea.ai", color="#111827", initial="Kr", badge="Free tier", desc="Real-time canvas — sketch a layout, watch render options appear live"),
     dict(name="Stable Diffusion", url="https://stability.ai", color="#6366f1", initial="SD", badge="Free (open)", desc="Self-host with manga LoRAs and ControlNet for pose-locked reference boards"),
     dict(name="ElevenLabs", url="https://elevenlabs.io/?via=toolforge", color="#06b6d4", initial="El", badge="$5/mo", desc="Voice your characters for promo reels and drama-CD style shorts"),
   ]),

 dict(slug="ai-tools-for-fantasy-authors-2026",
   title="AI Tools for Fantasy Authors in 2026: Worldbuilding, Drafting, and Covers",
   meta="The AI stack working fantasy authors actually run in 2026 — worldbuilding bibles, scene drafting, continuity checks, and covers that don't look AI-made.",
   category="AI Tools for Writers", read=10,
   lead="Fantasy is the genre with the most to lose from generic AI prose — and the most to gain from AI continuity. A 300k-word epic has more moving parts than any human memory; 2026's tools finally track them all.",
   verdict="Anchor on <strong>Sudowrite</strong> for drafting and <strong>Notion</strong> for your worldbuilding bible. Add <strong>Claude</strong> as your continuity editor (paste chapters, ask for inconsistencies). Only touch AI covers if your budget is truly zero — readers can smell stock fantasy art, and a $150 human cover still outsells a $0 AI one.",
   tools=[
     dict(name="Sudowrite", url="https://www.sudowrite.com", color="#7c3aed", initial="Su", badge="$19/mo", desc="Built by sci-fi authors — Story Engine maps outline to chapters without flattening your voice"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="$20/mo", desc="The continuity editor — 200k context means it reads your whole Book 1 while you draft Book 2"),
     dict(name="NovelAI", url="https://novelai.net", color="#0f766e", initial="NA", badge="$10/mo", desc="Anime-styled illustration + lorebook; beloved in the LitRPG and progression-fantasy scene"),
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="$20/mo", desc="Brainstorm partner for magic-system rules, naming conventions, and faction politics"),
     dict(name="Notion", url="https://www.notion.so", color="#111827", initial="No", badge="Free", desc="The worldbuilding bible — linked databases for characters, maps, timelines, and gods"),
     dict(name="Obsidian", url="https://obsidian.md", color="#5b21b6", initial="Ob", badge="Free", desc="Offline-first worldbuilding wiki with graph view — see your plot connect visually"),
     dict(name="Midjourney", url="https://www.midjourney.com", color="#1f2937", initial="Mj", badge="$10/mo", desc="Character mood boards and map references for your cartographer — not your final cover"),
     dict(name="ElevenLabs", url="https://elevenlabs.io/?via=toolforge", color="#06b6d4", initial="El", badge="$5/mo", desc="Hear your dialogue read aloud — catches stiff phrasing your eyes skip over"),
   ]),
]

# ---- pre-flight: blog tool URLs must be full https (pitfall from 2026-08-03) ----
for b in BLOGS:
    for t in b['tools']:
        assert t['url'].startswith('https://'), (b['slug'], t['name'])

new_urls = []
created = {"tools": 0, "compare": 0, "blog": 0}
for t in TOOLS:
    if t['slug'] in tool_slugs:
        print("SKIP tool", t['slug']); continue
    with open(os.path.join(BASE, 'tools', t['slug'] + '.html'), 'w') as f:
        f.write(tool_html(t))
    new_urls.append(DOMAIN + '/tools/' + t['slug'] + '.html'); created['tools'] += 1
    print("+ tool", t['slug'])

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print("SKIP compare", c['slug']); continue
    with open(os.path.join(BASE, 'compare', c['slug'] + '.html'), 'w') as f:
        f.write(compare_html(c))
    new_urls.append(DOMAIN + '/compare/' + c['slug'] + '.html'); created['compare'] += 1
    print("+ compare", c['slug'])

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print("SKIP blog", b['slug']); continue
    html = blog_html(b)
    # post-process hardcoded date literals (blog template bakes 2026-07-11 + June byline)
    html = html.replace('2026-07-11', TODAY).replace('2026-07-10', TODAY)
    html = html.replace('Published June 2026', 'Published August 2026')
    with open(os.path.join(BASE, 'blog', b['slug'] + '.html'), 'w') as f:
        f.write(html)
    new_urls.append(DOMAIN + '/blog/' + b['slug'] + '.html'); created['blog'] += 1
    print("+ blog", b['slug'])

# ---- full sitemap regen from disk (idempotent; avoids append-dup races) ----
urls = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
    for fn in files:
        if not fn.endswith('.html') or fn == '404.html':
            continue
        rel = os.path.relpath(os.path.join(root, fn), BASE).replace(os.sep, '/')
        if rel == 'index.html':
            u = ''
            pr = '1.0'
        elif rel.endswith('/index.html'):
            u = rel[:-10]
            pr = '0.8'
        else:
            u = rel
            pr = '0.8'
        urls.append((u, pr))
urls.sort()
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, pr in urls:
    xml.append('  <url>')
    xml.append('    <loc>https://toolforge.io/' + u + '</loc>')
    xml.append('    <lastmod>' + TODAY + '</lastmod>')
    xml.append('    <changefreq>weekly</changefreq>')
    xml.append('    <priority>' + pr + '</priority>')
    xml.append('  </url>')
xml.append('</urlset>')
with open(os.path.join(BASE, 'sitemap.xml'), 'w') as f:
    f.write('\n'.join(xml) + '\n')

print('SITEMAP URLS:', len(urls))
print('CREATED:', created)
print('NEW URLS:')
for u in new_urls:
    print(' ', u)
print('EXIT_OK')
