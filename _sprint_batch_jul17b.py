#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sprint batch driver (2026-07-17, cycle 2). Creates genuinely-missing
high-SEO tool / compare / blog pages using the live _tpl engine, regenerates
the sitemap from disk, pings IndexNow, and logs results. Non-destructive.
"""
import os, sys, datetime

BASE = os.path.expanduser('~/projects/toolforge')
sys.path.insert(0, BASE)
TODAY = "2026-07-17"
DOMAIN = "https://toolforge.io"
INDEXNOW_KEY = "9a8b7c6d"

import _tpl
_tpl.TODAY = TODAY
_tpl.DOMAIN = DOMAIN
tool_html, compare_html, blog_html = _tpl.tool_html, _tpl.compare_html, _tpl.blog_html

def existing(sub):
    d = os.path.join(BASE, sub)
    return {f[:-5] for f in os.listdir(d) if f.endswith('.html')} if os.path.isdir(d) else set()

tool_slugs = existing('tools')
cmp_slugs = existing('compare')
blog_slugs = existing('blog')

new_urls = []
created = {"tools": 0, "compare": 0, "blog": 0}

# ============================================================
# NEW TOOL PAGES (only genuinely missing, notable models/tools)
# ============================================================
TOOLS = [
 dict(slug="claude-3-opus", name="Claude 3 Opus", tagline="Anthropic's most capable 2024 flagship — top-tier reasoning, coding, and long-context understanding.",
   category="Coding", color1="#d97706", color2="#b45309", initials="O3", price="$20/mo", price_label="Claude Pro", price_num="20",
   free_tier="Limited free tier", rating="4.9/5", rating_num="4.9", users="Millions", founded="2024",
   headline="The thinking model",
   intro="Claude 3 Opus was Anthropic's most powerful model when it launched in March 2024, and it remains a benchmark-setter for nuanced reasoning, careful coding, and 200K-token context. It led many eval leaderboards on first release and is the model teams reach for when the task is hard and the stakes are high. Opus is slower and pricier than Sonnet or Haiku, but when quality matters it still earns its keep.",
   who_for="Researchers, analysts, and engineers who need the strongest reasoning and the longest context window for complex documents and codebases.",
   features=[("🧠","Top-tier reasoning","Led early 2024 benchmarks on math, coding, and graduate-level questions."),
             ("📚","200K context","Ingest entire books, codebases, or contract sets in one prompt."),
             ("💻","Coding strength","Writes clean, well-structured code across many languages."),
             ("🛡️","Constitutional AI","Strong safety and refusal behavior tuned for reliability.")],
   pros=["Best-in-class reasoning at launch","Huge 200K context window","Excellent code and writing","Strong safety posture"],
   cons=["Slower than Sonnet/Haiku","Higher price per token","Superseded by newer flagships for some tasks","No native real-time browsing"],
   verdict="Claude 3 Opus is the model to pick when correctness beats speed. For day-to-day work, Claude Sonnet is the better value — but Opus still wins the hardest problems.",
   cta_url="https://claude.ai/?via=toolforge"),

 dict(slug="llama-3-1", name="Llama 3.1", tagline="Meta's open-weight 405B flagship — near-frontier quality you can self-host and fine-tune.",
   category="Coding", color1="#0668E1", color2="#0a58c9", initials="L3", price="Free", price_label="open weight", price_num="0",
   free_tier="Open weights (free)", rating="4.6/5", rating_num="4.6", users="Millions of devs", founded="2024",
   headline="Frontier quality, open weights",
   intro="Llama 3.1 (405B) was Meta's breakthrough open model — the first openly licensed model to match closed frontier systems on many benchmarks. With 8B, 70B, and 405B sizes, it gives teams a self-hostable option for everything from chatbots to RAG pipelines. Because the weights are open, you can run it privately, fine-tune it, and avoid per-token API bills.",
   who_for="Teams that need frontier-grade quality with data control, self-hosting, or custom fine-tuning — and don't want vendor lock-in.",
   features=[("🔓","Open weights","Download, self-host, and modify under Meta's community license."),
             ("🌐","128K context","Long enough for most documents and multi-turn agents."),
             ("⚖️","Multiple sizes","8B for edge, 70B for servers, 405B for frontier tasks."),
             ("🛠️","Fine-tunable","LoRA / full fine-tunes on your own data.")],
   pros=["Frontier-ish quality, no API cost","True data privacy via self-host","Huge ecosystem and tooling","Multilingual out of the box"],
   cons=["Needs GPU infra for 405B","Trails top closed models on some evals","License has usage caps","Setup heavier than an API call"],
   verdict="Llama 3.1 is the default open model for teams that want control. If you can run it, you get near-frontier quality without sending data to a third party.",
   cta_url="https://www.llama.com/?via=toolforge"),

 dict(slug="llama-3-2", name="Llama 3.2", tagline="Meta's efficient 1B/3B and vision-capable 11B/90B open models for edge and multimodal use.",
   category="Productivity", color1="#0668E1", color2="#0a58c9", initials="L2", price="Free", price_label="open weight", price_num="0",
   free_tier="Open weights (free)", rating="4.4/5", rating_num="4.4", users="Millions of devs", founded="2024",
   headline="Small, fast, multimodal",
   intro="Llama 3.2 extended the family with tiny 1B and 3B text models that run on phones and laptops, plus 11B and 90B vision-language models that can read images. It's the practical choice when you need on-device inference or cheap multimodal understanding without a cloud bill.",
   who_for="Mobile and edge developers, and teams needing cheap vision understanding on private infrastructure.",
   features=[("📱","On-device 1B/3B","Runs offline on phones and consumer hardware."),
             ("👁️","Vision models","11B/90B variants understand images and charts."),
             ("🔓","Open weights","Self-host or fine-tune freely."),
             ("⚡","Low latency","Tiny sizes mean instant local responses.")],
   pros=["Runs on-device with no cloud","Vision + text in open weights","Free to deploy","Great for privacy-first apps"],
   cons=["Smaller models weaker on hard tasks","Vision trails dedicated VLMs","Needs ML infra knowledge","Less polished than GPT-4o-class"],
   verdict="Llama 3.2 is the smart pick for edge and private multimodal apps. Use the 90B vision model when you need image understanding without a vendor API.",
   cta_url="https://www.llama.com/?via=toolforge"),

 dict(slug="mistral-7b", name="Mistral 7B", tagline="The open 7B model that proved small can be mighty — fast, cheap, and self-hostable.",
   category="Coding", color1="#fa520f", color2="#e0410a", initials="M7", price="Free", price_label="open weight", price_num="0",
   free_tier="Open weights (free)", rating="4.3/5", rating_num="4.3", users="Millions of devs", founded="2023",
   headline="Small model, big impact",
   intro="Mistral 7B was the 2023 release that reset expectations for small open models — beating models 3x its size on many benchmarks while running on a single GPU. It remains a workhorse for self-hosted chatbots, classification, and RAG where latency and cost matter more than peak quality.",
   who_for="Teams building cost-sensitive or on-prem AI features that don't need frontier reasoning.",
   features=[("⚡","Tiny & fast","Runs on consumer GPUs and even laptops."),
             ("💸","Cheap to serve","Low VRAM means pennies per million tokens."),
             ("🔓","Open weights","Apache 2.0 — use commercially, no strings."),
             ("🔧","Easy fine-tune","Small size makes LoRA training quick.")],
   pros=["Runs anywhere, cheaply","Permissive Apache license","Strong for its size","Huge fine-tune community"],
   cons=["Not frontier-quality","Weak on hard reasoning","Needs infra to deploy","Superseded by larger Mistrals"],
   verdict="Mistral 7B is the pragmatic default for lightweight, self-hosted workloads. When you need more, step up to Mixtral or Mistral Large.",
   cta_url="https://mistral.ai/?via=toolforge"),

 dict(slug="mistral-nemo", name="Mistral NeMo", tagline="The 12B open model built with NVIDIA — 128K context, multilingual, fine-tune friendly.",
   category="Productivity", color1="#fa520f", color2="#e0410a", initials="Nm", price="Free", price_label="open weight", price_num="0",
   free_tier="Open weights (free)", rating="4.4/5", rating_num="4.4", users="Growing", founded="2024",
   headline="Compact but capable",
   intro="Mistral NeMo is a 12B model co-developed with NVIDIA, pairing Mistral's efficient architecture with a roomy 128K context window. It's designed to be a drop-in upgrade from 7B-class models — small enough to serve cheaply, capable enough for real multilingual workloads and easy fine-tuning.",
   who_for="Teams wanting a step up from 7B without the cost of 70B+, especially for multilingual and long-context tasks.",
   features=[("🧠","128K context","Handles long documents and multi-turn sessions."),
             ("🌍","Multilingual","Strong across European and many other languages."),
             ("🔧","Fine-tune ready","Built for easy adaptation to your domain."),
             ("🔓","Open weights","Apache 2.0 for commercial use.")],
   pros=["Big context in a small model","Multilingual strength","Cheap to serve","Friendly license"],
   cons=["Not frontier-level reasoning","Needs GPU to deploy","Less known than Llama","Vision not included"],
   verdict="Mistral NeMo is the sweet spot for multilingual, long-context, self-hosted apps that don't need a 70B model. A strong 12B pick.",
   cta_url="https://mistral.ai/?via=toolforge"),

 dict(slug="stable-diffusion-xl", name="Stable Diffusion XL", tagline="The open image model that set the standard for self-hosted, customizable AI art.",
   category="Image", color1="#ff4d4d", color2="#e03131", initials="SX", price="Free", price_label="open weight", price_num="0",
   free_tier="Open weights (free)", rating="4.5/5", rating_num="4.5", users="Millions of creators", founded="2023",
   headline="Open image generation, refined",
   intro="Stable Diffusion XL (SDXL) was Stability AI's major leap in open image quality — sharper details, better prompt adherence, and native 1024px output. Because the weights are open, artists run it locally, train custom LoRAs, and build commercial pipelines without per-image fees. It remains the backbone of most open image tooling.",
   who_for="Artists, indie developers, and businesses that want full control over image generation and no usage caps.",
   features=[("🎨","High-quality output","1024px native, strong composition and detail."),
             ("🔓","Open weights","Self-host, fine-tune, and commercialize freely."),
             ("🧩","LoRA & embeddings","Train tiny style adapters on your art."),
             ("🖥️","Local or cloud","Run on a gaming GPU or a rented instance.")],
   pros=["Full ownership and privacy","No per-image cost","Massive ecosystem (Auto1111, ComfyUI)","Commercial-friendly license"],
   cons=["Setup is technical","Needs a decent GPU","Prompting is finicky","Trails Midjourney on aesthetics"],
   verdict="SDXL is the open-image workhorse. If you want control, privacy, and zero per-image cost, it's unbeatable — pair it with ComfyUI for pro workflows.",
   cta_url="https://stability.ai/?via=toolforge"),

 dict(slug="sd3", name="Stable Diffusion 3", tagline="Stability's MMDiT model with dramatically better text rendering and prompt adherence.",
   category="Image", color1="#ff4d4d", color2="#e03131", initials="S3", price="Free", price_label="open weight", price_num="0",
   free_tier="Open weights (free)", rating="4.4/5", rating_num="4.4", users="Growing", founded="2024",
   headline="Text that actually renders",
   intro="Stable Diffusion 3 introduced a new MMDiT architecture that finally solved AI image generation's oldest embarrassment: legible text in images. It also improved prompt adherence and multi-subject composition. The smaller SD3 Medium is open-weight, making it a strong choice for designs that need real words on screen.",
   who_for="Designers and developers who need accurate text, logos, and typography inside generated images.",
   features=[("🔤","Legible text","Renders words and short phrases far better than prior SD."),
             ("🎯","Prompt adherence","Follows complex, multi-subject prompts."),
             ("🧩","MMDiT architecture","More stable training and composition."),
             ("🔓","Open Medium","SD3 Medium weights available openly.")],
   pros=["Best-in-class in-image text","Strong composition","Open Medium weights","Good resource efficiency"],
   cons=["Largest sizes not open","Setup still technical","Ecosystem younger than SDXL","Trails Midjourney on artistry"],
   verdict="SD3 is the one to reach for when your image needs real text — signs, logos, UI mockups. For pure art, Midjourney still leads.",
   cta_url="https://stability.ai/?via=toolforge"),

 dict(slug="flux-1-1", name="FLUX.1", tagline="Black Forest Labs' open image model family — razor-sharp realism and prompt accuracy.",
   category="Image", color1="#10b981", color2="#059669", initials="Fx", price="Free", price_label="open weight", price_num="0",
   free_tier="Open weights (free)", rating="4.7/5", rating_num="4.7", users="Millions of creators", founded="2024",
   headline="The new open-image king",
   intro="FLUX.1, from the original Stable Diffusion team at Black Forest Labs, raised the bar for open image generation in 2024. The [dev] variant is open-weight and delivers photographic realism, precise hands, and excellent prompt following that rivals or beats Midjourney on many prompts — without usage caps.",
   who_for="Creators and developers who want Midjourney-grade quality with open weights and full control.",
   features=[("📸","Photoreal output","Sharp, natural images with correct anatomy."),
             ("🎯","Prompt precision","Follows detailed, specific instructions."),
             ("🔓","Open [dev] weights","Self-host and commercialize."),
             ("⚡","Fast variants","[schnell] for real-time generation.")],
   pros=["Near-frontier image quality","Open dev weights","Better hands/anatomy than SDXL","Active community"],
   cons=["Needs a capable GPU","Younger ecosystem than SDXL","Commercial terms vary by variant","Not quite Midjourney on style"],
   verdict="FLUX.1 is the open-image model to beat in 2024-2025. If you want control AND quality, it's the best open option available.",
   cta_url="https://blackforestlabs.ai/?via=toolforge"),

 dict(slug="gemini-2-5-flash-lite", name="Gemini 2.5 Flash-Lite", tagline="Google's cheapest, fastest model — built for high-volume, latency-sensitive tasks.",
   category="Productivity", color1="#4285f4", color2="#3367d6", initials="Gf", price="$0.10/M tok", price_label="input", price_num="0",
   free_tier="Free tier", rating="4.4/5", rating_num="4.4", users="Millions", founded="2025",
   headline="Speed at scale, low cost",
   intro="Gemini 2.5 Flash-Lite is Google's answer to 'I need a million classifications a day.' It trades a little quality for the lowest price and latency in the Gemini lineup, making it ideal for summarization, tagging, routing, and other high-throughput jobs where cost-per-token dominates.",
   who_for="Engineering and product teams running massive volumes of simple AI tasks on a budget.",
   features=[("💸","Lowest cost","Among the cheapest capable models per token."),
             ("⚡","High throughput","Low latency for real-time pipelines."),
             ("📚","Long context","Inherited million-token window for big inputs."),
             ("🌐","Multimodal","Text, image, and more in one model.")],
   pros=["Extremely cheap at scale","Fast response times","Long context window","Multimodal input"],
   cons=["Lower quality than Flash/Pro","Not for hard reasoning","Needs Google Cloud/AI Studio","Less known than GPT"],
   verdict="Flash-Lite is the right call when you're processing huge volumes and every fraction of a cent matters. For quality-sensitive work, step up to Gemini Flash or Pro.",
   cta_url="https://ai.google.dev/?via=toolforge"),

 dict(slug="claude-3-5-haiku", name="Claude 3.5 Haiku", tagline="Anthropic's fastest, cheapest model — near-Sonnet quality at lightning speed.",
   category="Productivity", color1="#d97706", color2="#b45309", initials="H3", price="$0.80/M tok", price_label="input", price_num="0",
   free_tier="Free tier", rating="4.6/5", rating_num="4.6", users="Millions", founded="2024",
   headline="Cheap speed, real quality",
   intro="Claude 3.5 Haiku is Anthropic's smallest, fastest model — and unusually, it punches close to much larger models on many tasks. It's the go-to for classification, extraction, chat routing, and any workload where latency and cost dominate but you still want Claude's instruction-following.",
   who_for="Teams needing fast, affordable, high-volume text processing with Claude's reliability.",
   features=[("⚡","Blazing speed","Lowest-latency Claude for real-time apps."),
             ("💸","Low cost","Fraction of Opus/Sonnet price per token."),
             ("🎯","Strong instruction-following","Better than expected for its size."),
             ("📚","Long context","200K window for big inputs.")],
   pros=["Near-Sonnet quality, far cheaper","Very low latency","Great for routing/classification","200K context"],
   cons=["Not for hardest reasoning","Weaker than Opus on nuance","Closed API (no self-host)","No vision in base form"],
   verdict="Claude 3.5 Haiku is the smart default for high-volume, latency-sensitive tasks. Use it for the 80% of work that doesn't need Opus.",
   cta_url="https://claude.ai/?via=toolforge"),
]

# ============================================================
# NEW COMPARE PAGES
# ============================================================
COMPARES = [
 dict(slug="claude-3-vs-gpt-4o", name_a="Claude 3", name_b="GPT-4o",
   color_a="#d97706", color_b="#10a37f", initials_a="C3", initials_b="G4",
   desc_a="Anthropic's 2024 family — strong reasoning and long context.",
   desc_b="OpenAI's omni model — fast, multimodal, and widely integrated.",
   price_a="$20/mo", price_b="$20/mo", best_a="Reasoning, writing, long docs", best_b="Speed, multimodal, ecosystem",
   url_a="https://claude.ai/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   verdict="GPT-4o wins on multimodal breadth and speed; Claude 3 (especially Opus/Sonnet) wins on careful reasoning and long-context writing. Most users are fine with either — pick by which app you prefer.",
   winner="Tie — depends on use"),

 dict(slug="dall-e-3-vs-midjourney", name_a="DALL·E 3", name_b="Midjourney",
   color_a="#10a37f", color_b="#ff4d4d", initials_a="D3", initials_b="Mj",
   desc_a="OpenAI's prompt-following image model, built into ChatGPT.",
   desc_b="The art-first image model known for striking, stylized output.",
   price_a="$20/mo", price_b="$10/mo", best_a="Prompt accuracy, integration", best_b="Aesthetic quality, style",
   url_a="https://openai.com/dall-e/?via=toolforge", url_b="https://www.midjourney.com/?via=toolforge",
   verdict="DALL·E 3 follows your prompt more literally and lives inside ChatGPT; Midjourney produces more beautiful, art-directed images but is harder to control. Choose DALL·E for precision, Midjourney for beauty.",
   winner="Tie — precision vs beauty"),

 dict(slug="copilot-vs-chatgpt", name_a="Microsoft Copilot", name_b="ChatGPT",
   color_a="#0a72ef", color_b="#10a37f", initials_a="Mc", initials_b="Cg",
   desc_a="Microsoft's AI assistant woven into Office and Windows.",
   desc_b="OpenAI's general-purpose chatbot and app ecosystem.",
   price_a="$20/mo", price_b="$20/mo", best_a="Office/Windows workflows", best_b="General tasks, plugins, coding",
   url_a="https://copilot.microsoft.com/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   verdict="Copilot is the better pick if you live in Word, Excel, and Teams; ChatGPT is the more capable generalist with a bigger ecosystem. Power users will want ChatGPT regardless.",
   winner="ChatGPT (general) / Copilot (Office)"),
]

# ============================================================
# NEW BLOG POSTS (long-tail SEO)
# ============================================================
def card(name, color, initial, badge, desc, url):
    return dict(name=name, color=color, initial=initial, badge=badge, desc=desc, url=url)

BLOGS = [
 dict(slug="best-ai-tools-for-teachers", title="The 10 Best AI Tools for Teachers in 2026",
   meta="Save hours every week on lesson plans, grading, and differentiation. The AI stack teachers actually use.",
   category="Teachers", read="3", lead="Teachers are among the biggest winners of the AI wave — not because AI replaces them, but because it deletes the busywork. The 2026 stack handles lesson planning, worksheet generation, and even first-pass feedback so educators can spend time on what only humans can do.",
   verdict="Use ChatGPT or Claude for planning, MagicSchool for teacher-specific tasks, Quizizz for assessments, and Canva for materials. Most of this is free, which matters on a school budget.",
   tools=[
     card("ChatGPT","#10a37f","Cg","Free","Lesson plans + ideas","https://chat.openai.com/?via=toolforge"),
     card("Claude","#d97706","Cl","Free","Long-form + feedback","https://claude.ai/?via=toolforge"),
     card("MagicSchool","#7c3aed","Ms","Free","Teacher-built AI","https://magicschool.ai/?via=toolforge"),
     card("Quizizz","#7c3aed","Qz","Free","AI quizzes + assessments","https://quizizz.com/?via=toolforge"),
     card("Diffit","#0a72ef","Df","Free","Differentiated texts","https://diffit.me/?via=toolforge"),
     card("Canva","#00c4cc","Cn","Free","Worksheets + visuals","https://www.canva.com/?via=toolforge"),
     card("Eduaide","#1db954","Ed","Free","Resource generator","https://eduaide.ai/?via=toolforge"),
     card("Slidesgo","#ff7a00","Sg","Free","AI slide decks","https://slidesgo.com/?via=toolforge"),
     card("Grammarly","#15c39a","Gr","Free","Writing feedback","https://www.grammarly.com/?via=toolforge"),
     card("NotebookLM","#4285f4","NL","Free","Study guides from docs","https://notebooklm.google.com/?via=toolforge"),
   ]),
]

# ============================================================
# WRITE MISSING PAGES
# ============================================================
for t in TOOLS:
    if t['slug'] in tool_slugs:
        print("  SKIP tool", t['slug']); continue
    with open(os.path.join(BASE, 'tools', t['slug'] + '.html'), 'w') as f:
        f.write(tool_html(t))
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html")
    created['tools'] += 1
    print("  + tools/" + t['slug'] + ".html")

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print("  SKIP compare", c['slug']); continue
    with open(os.path.join(BASE, 'compare', c['slug'] + '.html'), 'w') as f:
        f.write(compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    created['compare'] += 1
    print("  + compare/" + c['slug'] + ".html")

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print("  SKIP blog", b['slug']); continue
    with open(os.path.join(BASE, 'blog', b['slug'] + '.html'), 'w') as f:
        f.write(blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    created['blog'] += 1
    print("  + blog/" + b['slug'] + ".html")

# ---------- regenerate sitemap from disk ----------
def priority(rel):
    if rel == 'index.html' or '/' not in rel:
        return '1.0'
    if rel.startswith('category/'): return '0.6'
    if rel.startswith('tools/'): return '0.8'
    if rel.startswith('blog/'): return '0.7'
    if rel.startswith('compare/'): return '0.7'
    return '0.8'

files = []
for root, dirs, fnames in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fn in fnames:
        if fn.startswith('.') or not fn.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(root, fn), BASE).replace(os.sep, '/')
        files.append(rel)
files.sort()

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for rel in files:
    lines += ['  <url>', f'    <loc>{DOMAIN}/{rel}</loc>',
              f'    <lastmod>{TODAY}</lastmod>', '    <changefreq>weekly</changefreq>',
              f'    <priority>{priority(rel)}</priority>', '  </url>']
lines.append('</urlset>')
with open(os.path.join(BASE, 'sitemap.xml'), 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f"\nSitemap regenerated: {len(files)} URLs")

with open('/tmp/toolforge_new_urls.txt', 'w') as f:
    f.write('\n'.join(new_urls) + '\n')

# ---------- IndexNow ping ----------
def ping_indexnow(urls):
    import json, urllib.request, urllib.error
    if not urls:
        return "no new urls"
    payload = json.dumps({"host": "toolforge.io", "key": INDEXNOW_KEY, "urlList": urls}).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        return f"HTTP {resp.status}: {resp.read().decode()[:200]}"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:300]}"
    except Exception as e:
        return f"ERROR: {e}"

idx = ping_indexnow(new_urls)
print("IndexNow:", idx)

# ---------- log ----------
logpath = '/tmp/toolforge_sprint_log.md'
entry = f"\n## {TODAY} — Sprint batch (cron, cycle 2)\n"
entry += f"- Tools created: {created['tools']} | Compares: {created['compare']} | Blogs: {created['blog']}\n"
entry += f"- Total new URLs: {len(new_urls)}\n"
entry += f"- Sitemap URLs after regen: {len(files)}\n"
entry += f"- IndexNow: {idx}\n"
if new_urls:
    entry += "- New slugs: " + ", ".join(u.split('/')[-1] for u in new_urls) + "\n"
with open(logpath, 'a') as f:
    f.write(entry)

print(f"\nCREATED: {created}")
print(f"TOTAL NEW URLS: {len(new_urls)}")
