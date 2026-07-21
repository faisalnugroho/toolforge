#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sprint batch driver (2026-07-17, cron cycle 2h).
Creates genuinely-missing high-SEO tool / compare / blog pages using the
live _tpl engine, regenerates the sitemap from disk, pings IndexNow, and
logs results. Non-destructive and idempotent (skips existing slugs).
"""
import os, sys, datetime

BASE = os.path.expanduser('~/projects/toolforge')
sys.path.insert(0, BASE)
TODAY = "2026-07-17"
DOMAIN = "https://toolforge.io"
INDEXNOW_KEY = "9a8b7c6d5e4f3a2b1c0d"

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
# NEW TOOL PAGES (only genuinely missing, notable tools)
# ============================================================
TOOLS = [
 dict(slug="deepseek-chat", name="DeepSeek Chat", tagline="DeepSeek's flagship conversational model — open-weights quality that rivals frontier models at a fraction of the cost.",
   category="Chat", color1="#4d6bfe", color2="#3a52d6", initials="DS", price="Free", price_label="API from $0.07/M tok", price_num="0",
   free_tier="Free web chat", rating="4.7/5", rating_num="4.7", users="100M+ users", founded="2023",
   headline="Frontier quality, open weights",
   intro="DeepSeek Chat is the conversational face of DeepSeek, the Chinese AI lab that shocked the industry in 2025 with open-weight models matching GPT-4-class quality. The chat product gives you long context, strong reasoning, and coding help for free in the browser, while the API is among the cheapest frontier-grade options available. For developers who want to self-host or avoid US-provider lock-in, DeepSeek is the default alternative.",
   who_for="Cost-conscious developers, researchers who want open weights, and teams building outside the US cloud ecosystem.",
   features=[("💬","Free web chat","Full reasoning and coding help at no cost in the browser."),
             ("🔓","Open weights","Models you can download and run privately on your own hardware."),
             ("⚡","Cheap API","Frontier-class tokens starting around $0.07 per million — a fraction of Big Tech pricing."),
             ("🧠","Strong reasoning","DeepSeek-R1 style chain-of-thought on math, code, and logic.")],
   pros=["Best price-to-performance in the market","Open weights = data sovereignty","Strong coding and math","Fast-moving lab, frequent releases"],
   cons=["Censorship on some China-policy topics","Smaller ecosystem than OpenAI","Web UI less polished","Rate limits during hype spikes"],
   verdict="If you want GPT-4-class quality without the bill, DeepSeek Chat is the obvious first stop. Self-hosters and budget dev teams should standardize on it.",
   cta_url="https://chat.deepseek.com/?via=toolforge"),

 dict(slug="qwen-chat", name="Qwen Chat", tagline="Alibaba's Qwen family — a full open-weight stack from 0.5B to 110B+ with vision, coding, and agent modes.",
   category="Chat", color1="#615ced", color2="#4a44c0", initials="Qw", price="Free", price_label="API pay-as-go", price_num="0",
   free_tier="Free web + open weights", rating="4.6/5", rating_num="4.6", users="Tens of millions", founded="2023",
   headline="Alibaba's open multimodal stack",
   intro="Qwen (通义千问) is Alibaba's flagship model family and one of the strongest open-weight contenders globally. The Qwen Chat product bundles chat, vision, code, and long-context modes in one interface, while the underlying models — from a 0.5B edge model to 110B+ MoE — are downloadable and commercially usable under permissive licenses. For teams in APAC or anyone building multilingual products, Qwen is the regional default.",
   who_for="Multilingual teams, APAC businesses, and engineers who want a full open model family with vision and agent support.",
   features=[("🌏","Multilingual","Strong in Chinese, English, and 20+ languages out of the box."),
             ("👁️","Vision + code","Qwen-VL for images and Qwen-Coder for repositories."),
             ("📦","Full size range","From 0.5B edge models to 110B+ MoE — one family, every use case."),
             ("🔓","Commercial open weights","Download and ship in production under permissive terms.")],
   pros=["Excellent multilingual coverage","Complete open model family","Vision and coding variants","Free to start"],
   cons=["Less third-party tooling than OpenAI","Censorship on some topics","Enterprise support less mature outside China","UI iterations can be rough"],
   verdict="For multilingual and open-weight needs, Qwen is the most complete family after DeepSeek. Use it when you need vision, code, and chat from one downloadable stack.",
   cta_url="https://chat.qwen.ai/?via=toolforge"),

 dict(slug="gpt-4o-mini", name="GPT-4o mini", tagline="OpenAI's cheap, fast, multimodal workhorse — the default model for high-volume and real-time apps.",
   category="Chat", color1="#10a37f", color2="#0e8c6e", initials="4m", price="$0.15/M", price_label="input tokens", price_num="0",
   free_tier="Free in ChatGPT", rating="4.6/5", rating_num="4.6", users="Billions of calls/mo", founded="2024",
   headline="The default fast model",
   intro="GPT-4o mini is OpenAI's small, fast, and absurdly cheap multimodal model. It handles text and images, supports a 128K context, and costs roughly 60x less than GPT-4o while beating the old GPT-3.5 on most benchmarks. It's the model most developers actually ship behind production features — search, classification, extraction, chatbots — where latency and cost matter more than max reasoning.",
   who_for="Production engineers, startups, and anyone routing high-volume or latency-sensitive traffic that doesn't need the flagship.",
   features=[("⚡","Fast + cheap","Sub-second latency at ~$0.15/M input tokens — built for scale."),
             ("👁️","Multimodal","Text and image input in one model."),
             ("📏","128K context","Long documents and conversations without truncation."),
             ("🔌","Drop-in API","OpenAI SDK compatible, easy to swap with GPT-4o.")],
   pros=["Best price/performance for production","Multimodal","Huge context window","Backed by OpenAI reliability"],
   cons=["Not the smartest model","No long-chain reasoning like o-series","Tied to OpenAI pricing changes","No open weights"],
   verdict="If you're shipping at scale, GPT-4o mini is the model you route 80% of traffic to. Save the flagship for the hard 20%.",
   cta_url="https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/?via=toolforge"),

 dict(slug="llama-3-70b", name="Llama 3 70B", tagline="Meta's open-weight 70B model — the self-hosting standard for private, customizable inference.",
   category="Chat", color1="#0668E1", color2="#0650b0", initials="L3", price="Free", price_label="self-host / cheap API", price_num="0",
   free_tier="Open weights (free)", rating="4.6/5", rating_num="4.6", users="Millions self-hosted", founded="2024",
   headline="The self-host standard",
   intro="Llama 3 70B is Meta's workhorse open-weight model and the backbone of the open inference ecosystem. With 8B, 70B, and 405B sizes, it lets companies run frontier-grade chat fully on their own hardware — no per-call API bills, no data leaving the building. Paired with Ollama, vLLM, or Groq, it powers private assistants, RAG pipelines, and on-prem copilots across regulated industries.",
   who_for="Enterprises with data-residency needs, indie devs running local models, and anyone building on open inference.",
   features=[("🔓","Open weights","Download and run anywhere — laptop to datacenter."),
             ("🏠","Private by default","No data leaves your infrastructure."),
             ("🛠️","Fine-tunable","LoRA, full FT, and蒸馏 all supported."),
             ("🌐","Huge ecosystem","Ollama, vLLM, LM Studio, Groq — every tool supports it.")],
   pros=["True data sovereignty","No per-call cost at scale","Massive tooling ecosystem","Strong base for fine-tunes"],
   cons=["You run the infra","70B needs serious GPUs to serve fast","Not as strong as frontier closed models","Quality varies by quantization"],
   verdict="For private, customizable AI, Llama 3 70B is the open standard. Run it locally or on Groq and you get GPT-3.5-class quality with zero vendor lock-in.",
   cta_url="https://www.llama.com/?via=toolforge"),

 dict(slug="claude-3-haiku", name="Claude 3 Haiku", tagline="Anthropic's fastest, cheapest model — near-instant responses with strong instruction-following.",
   category="Chat", color1="#d97706", color2="#b45309", initials="Hk", price="$0.25/M", price_label="input tokens", price_num="0",
   free_tier="Free in Claude.ai", rating="4.5/5", rating_num="4.5", users="Widely used", founded="2024",
   headline="Speed without the bill",
   intro="Claude 3 Haiku is Anthropic's smallest, fastest model — built for instant responses and high-volume tasks where you'd otherwise reach for a tiny model. It punches above its weight on instruction-following and structured output, making it ideal for classification, extraction, and customer-facing chat where latency is king. It's the model you pair with Opus or Sonnet in a routing setup.",
   who_for="Teams needing instant, cheap, reliable responses — support bots, classifiers, and preprocessing before a bigger model.",
   features=[("⚡","Near-instant","Lowest latency in the Claude family."),
             ("✅","Reliable structure","Great at JSON, extraction, and following exact formats."),
             ("💲","Cheap","~$0.25/M input — production-friendly."),
             ("🤝","Pairs with Opus","Use Haiku for triage, Opus for the hard cases.")],
   pros=["Excellent speed-to-cost","Strong instruction following","Good structured output","Anthropic safety defaults"],
   cons=["Less capable than Sonnet/Opus","No long-chain reasoning","No open weights","Smaller context than siblings"],
   verdict="Claude 3 Haiku is the right call when you need Anthropic quality at chatbot speed and price. Route the easy 90% here, escalate the rest.",
   cta_url="https://www.anthropic.com/claude/haiku?via=toolforge"),

 dict(slug="claude-3-5-sonnet", name="Claude 3.5 Sonnet", tagline="Anthropic's balanced workhorse — top coding and agentic skills at roughly half the cost of Opus.",
   category="Chat", color1="#d97706", color2="#b45309", initials="S5", price="$3/M", price_label="input tokens", price_num="3",
   free_tier="Free tier available", rating="4.8/5", rating_num="4.8", users="Millions of devs", founded="2024",
   headline="The dev favorite",
   intro="Claude 3.5 Sonnet became the default coding model for a generation of developers — beating far larger models on SWE-bench and agentic tasks while costing a fraction of Opus. Its artifact feature turned Claude.ai into a mini IDE, and its balance of speed, cost, and capability made it the backbone of Cursor, Cline, and countless coding agents. For most real work, Sonnet is the sweet spot.",
   who_for="Software engineers, builders, and agent builders who want frontier capability at sustainable cost.",
   features=[("💻","Best-in-class coding","Top SWE-bench scores; the model most coding agents default to."),
             ("🎨","Artifacts","Live code/HTML/doc preview inside the chat."),
             ("⚡","Fast + affordable","Half the price of Opus with most of the skill."),
             ("🤖","Agentic","Strong tool-use and multi-step planning.")],
   pros=["Elite coding and agentic skills","Great value vs Opus","Artifacts are genuinely useful","Strong safety profile"],
   cons=["Not quite Opus on deepest reasoning","No open weights","Rate limits on free tier","Costs add up at scale"],
   verdict="For 90% of coding and agentic work, Claude 3.5 Sonnet is the smartest buy. Keep Opus for the genuinely hard problems.",
   cta_url="https://www.anthropic.com/claude/sonnet?via=toolforge"),

 dict(slug="google-gemini", name="Google Gemini", tagline="Google's multimodal flagship — native text, image, audio, and video understanding with 1M+ token context.",
   category="Chat", color1="#4285f4", color2="#3367d6", initials="Gm", price="$1.50/M", price_label="input tokens (Pro)", price_num="0",
   free_tier="Free tier (Flash)", rating="4.7/5", rating_num="4.7", users="Billions via Workspace", founded="2023",
   headline="Multimodal by design",
   intro="Gemini is Google's natively multimodal model family, built from the ground up to understand text, images, audio, and video together. The Pro tier competes with GPT-4o and Claude on reasoning, while Flash is a cheap, fast workhorse, and the 1M+ token context window lets you drop in entire codebases or books. Deeply integrated into Workspace, Android, and Search, Gemini is the default AI for the Google ecosystem.",
   who_for="Google Workspace shops, multimodal app builders, and anyone needing enormous context windows.",
   features=[("🎬","Native multimodal","Text, image, audio, and video in one model."),
             ("📚","1M+ context","Paste entire repos, PDFs, or videos."),
             ("⚡","Flash tier","Cheap, fast default for production."),
             ("🔗","Workspace-native","Built into Docs, Gmail, Android.")],
   pros=["Best-in-class context length","True multimodal","Tight Google integration","Strong free tier"],
   cons=["Pro pricing adds up","Less third-party tooling than OpenAI","Occasional honesty hiccups","US-policy constraints"],
   verdict="For multimodal and long-context work inside the Google world, Gemini is unmatched. Flash is the cheap default; Pro handles the heavy lifting.",
   cta_url="https://gemini.google.com/?via=toolforge"),

 dict(slug="runway-gen-3", name="Runway Gen-3", tagline="Runway's third-gen video model — crisp text-to-video and image-to-video with strong motion coherence.",
   category="Video", color1="#00c2a8", color2="#009e88", initials="R3", price="$12/mo", price_label="Standard", price_num="12",
   free_tier="Limited free credits", rating="4.5/5", rating_num="4.5", users="Millions of creators", founded="2023",
   headline="Filmmaker-grade generation",
   intro="Gen-3 is Runway's leap into production-quality AI video. It generates coherent, high-fidelity clips from text or images, with fine control over motion, camera, and style. Combined with Runway's editing suite (rotoscoping, inpainting, motion brush), it's the tool filmmakers and agencies reach for when they need controllable, on-brand video without a camera. Gen-3 Alpha Turbo made it fast and affordable enough for real workflows.",
   who_for="Filmmakers, agencies, and marketers who need controllable, brand-safe AI video.",
   features=[("🎥","Text & image to video","Prompt or upload a frame; get coherent motion."),
             ("🎚️","Motion control","Direct camera moves and subject motion precisely."),
             ("🪄","Editing suite","Rotoscoping, inpaint, and motion brush in one app."),
             ("⚡","Turbo mode","Faster, cheaper generations for iteration.")],
   pros=["Strong motion coherence","Deep editing toolkit","Turbo is fast/cheap","Industry-adopted"],
   cons=["Credit limits bite fast","Not photoreal at long durations","Steeper learning curve","Watermarks on free tier"],
   verdict="For controllable, editor-friendly AI video, Runway Gen-3 is the professional pick. Pair it with Kling or Veo for variety.",
   cta_url="https://runwayml.com/?via=toolforge"),
]

# ============================================================
# NEW COMPARE PAGES (high search volume, verified missing)
# ============================================================
COMPARES = [
 dict(slug="gpt-4o-vs-gpt-4", name_a="GPT-4o", name_b="GPT-4",
   color_a="#10a37f", color_b="#1a7f64", initials_a="4o", initials_b="G4",
   desc_a="OpenAI's fast multimodal flagship with voice and vision.",
   desc_b="OpenAI's 2023 text-only powerhouse that started the boom.",
   price_a="$20/mo", price_b="$20/mo",
   best_a="Multimodal, real-time voice, speed", best_b="Legacy baseline, some long-context tasks",
   url_a="https://openai.com/gpt-4o?via=toolforge", url_b="https://openai.com/index/gpt-4/?via=toolforge",
   verdict="GPT-4o beats GPT-4 on speed, price, and multimodal almost everywhere. There's little reason to use legacy GPT-4 in 2026 unless a specific integration requires it.",
   winner="GPT-4o — faster, cheaper, multimodal"),

 dict(slug="gemini-vs-gpt-4o", name_a="Gemini", name_b="GPT-4o",
   color_a="#4285f4", color_b="#10a37f", initials_a="Gm", initials_b="4o",
   desc_a="Google's native multimodal model with 1M+ token context.",
   desc_b="OpenAI's fast multimodal flagship with voice and vision.",
   price_a="$1.50/M (Pro)", price_b="$2.50/M (input)",
   best_a="Long context, video understanding, Google Workspace", best_b="Ecosystem, tooling, real-time voice",
   url_a="https://gemini.google.com/?via=toolforge", url_b="https://openai.com/gpt-4o?via=toolforge",
   verdict="Gemini wins on context length and native video; GPT-4o wins on ecosystem and third-party tooling. Pick Gemini for long-document and multimodal Google work, GPT-4o for the broadest integration support.",
   winner="Tie — depends on context length vs ecosystem"),

 dict(slug="claude-3-5-sonnet-vs-gpt-4o", name_a="Claude 3.5 Sonnet", name_b="GPT-4o",
   color_a="#d97706", color_b="#10a37f", initials_a="S5", initials_b="4o",
   desc_a="Anthropic's coding-focused workhorse with artifacts.",
   desc_b="OpenAI's multimodal flagship with voice and vision.",
   price_a="$3/M (input)", price_b="$2.50/M (input)",
   best_a="Coding, agentic tasks, long-form writing", best_b="Multimodal, voice, ecosystem",
   url_a="https://www.anthropic.com/claude/sonnet?via=toolforge", url_b="https://openai.com/gpt-4o?via=toolforge",
   verdict="Claude 3.5 Sonnet is the developer favorite for coding and agentic work; GPT-4o is the safer all-rounder with voice and a bigger tool ecosystem. Most builders run both.",
   winner="Tie — Sonnet for code, GPT-4o for all-round"),

 dict(slug="deepseek-vs-claude", name_a="DeepSeek", name_b="Claude",
   color_a="#4d6bfe", color_b="#d97706", initials_a="DS", initials_b="Cl",
   desc_a="Open-weight, ultra-cheap frontier-class models from China.",
   desc_b="Anthropic's thoughtful, safety-first assistant.",
   price_a="Free / $0.07/M", price_b="$3/M (Sonnet input)",
   best_a="Cost, open weights, self-hosting", best_b="Writing, coding, safety, enterprise trust",
   url_a="https://chat.deepseek.com/?via=toolforge", url_b="https://www.anthropic.com/claude?via=toolforge",
   verdict="DeepSeek wins on price and sovereignty; Claude wins on writing quality, coding, and enterprise trust. Use DeepSeek for cost-sensitive volume, Claude where output quality is the product.",
   winner="Tie — DeepSeek for cost, Claude for quality"),

 dict(slug="qwen-vs-deepseek", name_a="Qwen", name_b="DeepSeek",
   color_a="#615ced", color_b="#4d6bfe", initials_a="Qw", initials_b="DS",
   desc_a="Alibaba's full open multimodal model family.",
   desc_b="DeepSeek's open reasoning and chat models.",
   price_a="Free / pay-as-go", price_b="Free / $0.07/M",
   best_a="Multilingual, vision, complete family", best_b="Reasoning, cheapest API",
   url_a="https://chat.qwen.ai/?via=toolforge", url_b="https://chat.deepseek.com/?via=toolforge",
   verdict="Both are top open-weight labs. Qwen is stronger for multilingual and vision use cases; DeepSeek leads on raw reasoning and API price. Pick by language and modality needs.",
   winner="Tie — Qwen for multilingual/vision, DeepSeek for reasoning"),
]

# ============================================================
# NEW BLOG POSTS (fresh long-tail SEO, verified missing)
# ============================================================
def card(name, color, initial, badge, desc, url):
    return dict(name=name, color=color, initial=initial, badge=badge, desc=desc, url=url)

BLOGS = [
 dict(slug="best-ai-tools-for-pastors", title="The 7 Best AI Tools for Pastors in 2026 (Reclaim 10 Hours/Week)",
   meta="Sermon prep, newsletters, and admin — the AI stack that lets pastors focus on people instead of paperwork.",
   category="Faith Leaders", read="3",
   lead="Pastors wear every hat: preacher, writer, counselor, and administrator. AI in 2026 takes the admin off your plate so you can spend that time with your congregation. Here are the tools worth your attention.",
   verdict="Use ChatGPT or Claude for sermon and devotion prep, Canva for bulletins, and a transcription tool for turning talks into written content. The goal isn't less heart — it's less spreadsheet.",
   tools=[
     card("ChatGPT","#10a37f","Ch","$20/mo","Sermon outlines and illustrations","https://chat.openai.com/?via=toolforge"),
     card("Claude","#d97706","Cl","$20/mo","Long-form writing and study notes","https://claude.ai/?via=toolforge"),
     card("Canva","#00c4cc","Ca","Free","Bulletins, slides, social graphics","https://www.canva.com/?via=toolforge"),
     card("Otter.ai","#4f46e5","Ot","$10/mo","Transcribe sermons into text","https://otter.ai/?via=toolforge"),
     card("Notion","#000000","No","Free","Sermon archive and planning","https://www.notion.so/?via=toolforge"),
     card("Mailchimp","#ffe01b","Mc","Free","Congregation newsletters","https://mailchimp.com/?via=toolforge"),
     card("Suno","#111827","Su","Free","Original worship music drafts","https://suno.com/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-chiropractors", title="The 6 Best AI Tools for Chiropractors in 2026",
   meta="From patient intake to social content, the AI stack that helps chiropractors grow their practice without hiring.",
   category="Healthcare", read="2",
   lead="Chiropractors run a business and a practice at once. AI in 2026 handles the marketing, intake, and content so you can stay hands-on with patients. Here's a lean stack that pays for itself.",
   verdict="Use an AI note-taker for visits, a social tool for local content, and an automation platform for no-shows and reminders. Most of this is free or under $30/mo — the ROI is in the rebooked appointments.",
   tools=[
     card("Fireflies.ai","#1f6feb","Fi","$10/mo","Auto notes from patient calls","https://fireflies.ai/?via=toolforge"),
     card("Canva","#00c4cc","Ca","Free","Educational posts and Reels","https://www.canva.com/?via=toolforge"),
     card("Make","#0a72ef","Mk","$9/mo","No-show and reminder automations","https://www.make.com/en?ref=toolforge"),
     card("ChatGPT","#10a37f","Ch","$20/mo","Blog and FAQ drafts","https://chat.openai.com/?via=toolforge"),
     card("Jasper","#7928ca","Ja","$49/mo","Local SEO landing pages","https://www.jasper.ai/?via=toolforge"),
     card("Calendly","#006bff","Cl","Free","Online booking","https://calendly.com/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-fitness-coaches", title="The 8 Best AI Tools for Fitness Coaches in 2026",
   meta="Program design, client check-ins, and content — the AI stack that lets online coaches scale without burning out.",
   category="Coaching", read="3",
   lead="Online fitness coaching is a content and personalization game. AI in 2026 writes the programs, drafts the posts, and handles the admin so you can coach more clients 1:1. Here's the stack top coaches use.",
   verdict="Pair a workout generator with a content tool and an automation layer. The coaches winning in 2026 aren't working more hours — they've automated the repetitive 60%.",
   tools=[
     card("ChatGPT","#10a37f","Ch","$20/mo","Custom program and meal plans","https://chat.openai.com/?via=toolforge"),
     card("Canva","#00c4cc","Ca","Free","Workout carousels and Reels","https://www.canva.com/?via=toolforge"),
     card("Notion","#000000","No","Free","Client progress tracking","https://www.notion.so/?via=toolforge"),
     card("Otter.ai","#4f46e5","Ot","$10/mo","Transcribe coaching calls","https://otter.ai/?via=toolforge"),
     card("Make","#0a72ef","Mk","$9/mo","Onboarding + check-in flows","https://www.make.com/en?ref=toolforge"),
     card("Descript","#000000","De","$12/mo","Edit training videos by text","https://www.descript.com/?via=toolforge"),
     card("Suno","#111827","Su","Free","Hype and promo music","https://suno.com/?via=toolforge"),
     card("Calendly","#006bff","Cl","Free","Discovery calls","https://calendly.com/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-notion-users", title="The 9 Best AI Tools for Notion Users in 2026",
   meta="Supercharge your Notion workspace with AI for writing, search, automation, and second brains.",
   category="Productivity", read="3",
   lead="Notion is where your work lives. The right AI tools turn it from a notes app into a thinking partner — writing, searching, and automating across your workspace. Here are the picks that pair best with Notion.",
   verdict="Start with Notion AI for in-doc writing, then add a second-brain tool for capture and an automation layer for workflows. The magic is when notes, tasks, and AI live in one connected system.",
   tools=[
     card("Notion AI","#000000","NA","$10/mo","In-doc writing and Q&A","https://www.notion.so/product/ai?via=toolforge"),
     card("Mem","#111827","Me","$10/mo","Self-organizing notes","https://mem.ai/?via=toolforge"),
     card("Recall","#7c3aed","Rc","$8/mo","Auto-summarize saved content","https://www.getrecall.ai/?via=toolforge"),
     card("Make","#0a72ef","Mk","$9/mo","Notion automations","https://www.make.com/en?ref=toolforge"),
     card("ChatGPT","#10a37f","Ch","$20/mo","Brainstorm inside your docs","https://chat.openai.com/?via=toolforge"),
     card("Claude","#d97706","Cl","$20/mo","Long-form doc drafting","https://claude.ai/?via=toolforge"),
     card("Whisper","#10a37f","Wh","Free","Voice notes to Notion","https://openai.com/research/whisper?via=toolforge"),
     card("Zapier","#ff4f00","Za","$20/mo","2,000+ app connections","https://zapier.com/?via=toolforge"),
     card("Obsidian","#7c3aed","Ob","Free","Local second brain","https://obsidian.md/?via=toolforge"),
   ]),
]

# ============================================================
# WRITE MISSING PAGES
# ============================================================
print("=== Writing missing pages ===")
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
entry = f"\n## {TODAY} — Sprint batch (cron cycle, _sprint_batch_jul17c.py)\n"
entry += f"- Tools created: {created['tools']} | Compares: {created['compare']} | Blogs: {created['blog']}\n"
entry += f"- Total new URLs: {len(new_urls)}\n"
entry += f"- Sitemap URLs after regen: {len(files)}\n"
entry += f"- IndexNow: {idx}\n"
if new_urls:
    entry += "- New slugs: " + ", ".join(u.split('/')[-1] for u in new_urls) + "\n"
with open(logpath, 'a') as f:
    f.write(entry)

print(f"\nCREATED: {created}")
