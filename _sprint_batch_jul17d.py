#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sprint batch driver (2026-07-17, cron cycle ~14h).
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
 dict(slug="v0-dev", name="v0.dev", tagline="Vercel's AI UI generator — describe a component and get production-ready React/Tailwind code instantly.",
   category="Coding", color1="#000000", color2="#333333", initials="v0", price="Free", price_label="Pro $20/mo", price_num="0",
   free_tier="Free tier (limited generations)", rating="4.6/5", rating_num="4.6", users="Millions of builders", founded="2023",
   headline="Prompt-to-UI, shipped",
   intro="v0.dev is Vercel's AI-powered UI generation tool. You describe a component or page in plain English, and it returns clean, copy-pasteable React + Tailwind code that follows shadcn/ui conventions. Instead of fighting a design tool, you iterate on live code — regenerate, tweak the prompt, and drop the result straight into your Next.js app. It's the fastest way to go from idea to a deployed interface.",
   who_for="Frontend developers, indie hackers, and designers who want production-quality React components without hand-writing boilerplate.",
   features=[("💬","Prompt to component","Describe a button, card, or full page — get React + Tailwind code back."),
             ("🔁","Iterative regen","Refine with follow-up prompts; keep the versions you like."),
             ("🎨","shadcn/ui native","Output matches the conventions most modern React apps already use."),
             ("🚀","One-click deploy","Push generated UI straight to Vercel.")],
   pros=["Instant high-quality React code","Matches real component libraries","Great for rapid prototyping","Free tier to start"],
   cons=["Best inside the Vercel ecosystem","Less control than hand-coding","Pro needed for serious volume","Can produce inconsistent layouts"],
   verdict="For React/Next.js builders, v0 is the fastest path from prompt to deployed UI. Use it for prototypes and components, then hand-tune the code.",
   cta_url="https://v0.dev/?via=toolforge"),

 dict(slug="loveable", name="Lovable", tagline="The AI app builder that turns a sentence into a full-stack web app with a backend, auth, and deploy.",
   category="Coding", color1="#9b5de5", color2="#7b3fd1", initials="Lo", price="$20/mo", price_label="Starter", price_num="20",
   free_tier="Free tier (limited credits)", rating="4.5/5", rating_num="4.5", users="Hundreds of thousands", founded="2024",
   headline="Describe the app, ship it",
   intro="Lovable (formerly GPT Engineer) is a vibe-coding platform that builds complete full-stack web apps from a natural-language description. It wires up the frontend, a Supabase backend, authentication, and database, then deploys to a live URL. Non-engineers can ship a working SaaS in an afternoon, and engineers use it to skip the scaffolding. It iterates on your feedback and edits the codebase in real time.",
   who_for="Founders, product people, and engineers who want to go from idea to a deployed full-stack app without writing all the boilerplate.",
   features=[("🧠","Full-stack generation","Frontend, backend, auth, and DB from one prompt."),
             ("🔌","Supabase native","Real Postgres, auth, and storage wired automatically."),
             ("📝","Chat to edit","Describe changes in plain English; Lovable edits the code."),
             ("🌐","Instant deploy","Live URL with every build.")],
   pros=["Ships real full-stack apps fast","No backend setup needed","Great for non-coders","Live iteration loop"],
   cons=["Locked to its stack choices","Complex apps hit limits","Debugging generated code is hard","Credits run out quickly"],
   verdict="Lovable is the strongest 'describe an app, get an app' builder for full-stack web products. Pair it with v0 if you want more frontend control.",
   cta_url="https://lovable.dev/?via=toolforge"),

 dict(slug="jetbrains-ai", name="JetBrains AI", tagline="AI assistant built into IntelliJ, PyCharm, and the whole JetBrains IDE family — code, explain, and refactor in your editor.",
   category="Coding", color1="#ff318c", color2="#d6246f", initials="JB", price="$10/mo", price_label="per user", price_num="10",
   free_tier="Limited in some plans", rating="4.5/5", rating_num="4.5", users="Millions of IDE users", founded="2023",
   headline="AI, native to your IDE",
   intro="JetBrains AI brings assistant features directly inside the IDEs developers already live in — IntelliJ IDEA, PyCharm, WebStorm, and more. It explains code, generates functions, suggests refactors, and answers questions with full project context. Unlike a separate chatbot, it understands your language, framework, and codebase structure because it's part of the same tool. JetBrains AI Assistant also powers contextual commit messages and documentation.",
   who_for="Developers who work in JetBrains IDEs and want AI help without switching to a separate editor or tab.",
   features=[("💡","Inline generation","Generate and edit code without leaving the editor."),
             ("🔍","Project-aware chat","Ask questions with full context of your codebase."),
             ("📝","Commit & docs","Auto-write commit messages and explain functions."),
             ("🌐","Multi-model","Routes to Claude, GPT, and JetBrains' own models.")],
   pros=["Native to JetBrains IDEs","Strong project context","No editor-switching","Multi-model routing"],
   cons=["Requires a JetBrains subscription","Weaker than Cursor for some tasks","Not for VSCode users","Limited offline mode"],
   verdict="If you live in IntelliJ or PyCharm, JetBrains AI is the lowest-friction way to add AI help. Cursor refugees on JetBrains should start here.",
   cta_url="https://www.jetbrains.com/ai/?via=toolforge"),

 dict(slug="github-copilot-x", name="GitHub Copilot", tagline="GitHub's AI pair programmer — inline completions, chat, and agentic coding across every editor and the CLI.",
   category="Coding", color1="#6e40c9", color2="#5631a0", initials="Co", price="$10/mo", price_label="Individual", price_num="10",
   free_tier="Free tier for students/open-source", rating="4.7/5", rating_num="4.7", users="Millions of developers", founded="2021",
   headline="The original AI pair programmer",
   intro="GitHub Copilot, built with OpenAI, is the most widely adopted AI coding assistant. It offers whole-line and whole-function completions inside virtually every editor, a Chat surface for questions, slash commands for tests and docs, and Copilot Workspaces for agentic planning. The 2024-2025 additions — multi-model support, code review, and the CLI agent — turned it from an autocomplete into a full coding companion. Copilot Free now gives individuals a real monthly quota at no cost.",
   who_for="Every developer, from students to enterprise teams, who wants completions, chat, and reviews without leaving their workflow.",
   features=[("⚡","Inline completions","Whole-line and whole-function suggestions as you type."),
             ("💬","Copilot Chat","Ask about code, get explanations and fixes in-editor."),
             ("🔀","Code review"," Automated review comments on your pull requests."),
             ("🖥️","CLI agent","Run coding tasks from the terminal.")],
   pros=["Broadest editor support","Free tier for individuals","Backed by GitHub/OpenAI","Constantly improving"],
   cons=["Less agentic than Codex/Devin","Quality varies by language","Needs network","Can suggest stale patterns"],
   verdict="Copilot is still the safest default AI coding assistant — free to start, everywhere you work, and now with chat and review. Power users may want Cursor or Codex on top.",
   cta_url="https://github.com/features/copilot?via=toolforge"),

 dict(slug="pika-labs", name="Pika", tagline="Pika's playful AI video model — text and image to short clips with strong stylization and effects.",
   category="Video", color1="#ff5c8a", color2="#e63e6d", initials="Pi", price="$8/mo", price_label="Standard", price_num="8",
   free_tier="Free credits", rating="4.4/5", rating_num="4.4", users="Tens of millions", founded="2023",
   headline="Video that feels like play",
   intro="Pika is the community-loved AI video generator known for its playful, stylized output. Pika 2.0 and beyond added strong text-to-video, image-to-video, and video-to-video, plus signature effects like Pikaffects (explode, squish, melt) that became social-media staples. It's less 'filmmaker-grade' than Runway or Veo and more 'creator-grade' — fast, fun, and built for sharing. The Discord-native community keeps shipping meme-friendly features.",
   who_for="Content creators, social-media marketers, and anyone who wants fun, stylized AI video without a steep learning curve.",
   features=[("🎨","Stylized output","Distinctive looks that pop on social feeds."),
             ("✨","Pikaffects","Explode, squish, melt — viral-ready effects."),
             ("🖼️","Image to video","Animate a still into a moving clip."),
             ("⚡","Fast generations","Quick iterations for content calendars.")],
   pros=["Fun, shareable output","Easy to learn","Strong community","Cheap entry point"],
   cons=["Less photoreal than rivals","Shorter clips","Watermarks on free tier","Limited fine control"],
   verdict="For social-first, stylized AI video, Pika is the most fun and the fastest to results. Use Runway or Veo when you need photoreal control.",
   cta_url="https://pika.art/?via=toolforge"),

 dict(slug="udio-ai", name="Udio", tagline="Udio's music-generation model — type a genre and lyrics and get radio-quality original songs in seconds.",
   category="Audio", color1="#1ed760", color2="#169c46", initials="Ud", price="Free", price_label="Pro $10/mo", price_num="0",
   free_tier="Free tier (credits)", rating="4.5/5", rating_num="4.5", users="Millions of creators", founded="2023",
   headline="Songs from a sentence",
   intro="Udio is one of the two leading AI music generators (alongside Suno). Backed by ex-Google DeepMind talent, it produces surprisingly polished full songs — vocals, instrumentation, and structure — from a text prompt and optional lyrics. Its audio quality and vocal realism set an early bar for the category. Creators use it for background tracks, demos, and TikTok sounds without touching a DAW.",
   who_for="Musicians, video creators, and marketers who need original, license-friendly music fast.",
   features=[("🎵","Full songs","Vocals, instruments, and song structure from text."),
             ("🎤","Vocal realism","Among the most natural AI singing voices."),
             ("🎚️","Genre control","Dial in style, mood, and tempo."),
             ("⚡","Fast output","A finished track in seconds.")],
   pros=["High audio quality","Realistic vocals","Free to start","Great for shorts/ads"],
   cons=["Licensing still evolving","Less editable than a DAW","Credits on free tier","Hit-or-miss prompts"],
   verdict="Udio competes neck-and-neck with Suno on quality. Try both; many creators prefer Udio's vocals and Suno's UX. Either beats stock music.",
   cta_url="https://udio.com/?via=toolforge"),

 dict(slug="cleo-ai", name="Cleo", tagline="Cleo's AI money assistant — budgeting, roasting, and saving with a chatbot that actually has personality.",
   category="Productivity", color1="#21d07a", color2="#1aa85f", initials="Cl", price="Free", price_label="Premium $5.99/mo", price_num="0",
   free_tier="Free budgeting chatbot", rating="4.3/5", rating_num="4.3", users="Millions of users", founded="2016",
   headline="Your money, with attitude",
   intro="Cleo is a UK-born AI financial assistant that connects to your bank and helps you budget, save, and spend smarter — delivered through a chatbot with a sharp, meme-friendly personality. It 'roasts' your spending, sets challenges, and automates savings with round-ups and 'no-spend' streaks. In 2025-2026 Cleo added cash advances and investing, making it a lightweight neobank with an AI front end. It's the rare finance app people actually open daily.",
   who_for="Younger users, gig workers, and anyone who wants budgeting help that feels like a friend (with boundaries) rather than a spreadsheet.",
   features=[("🔥","Roast mode","Honest, funny take on your spending habits."),
             ("💰","Auto-save","Round-ups and challenges that build savings."),
             ("📊","Budget insights","Spending breakdowns in plain language."),
             ("⚡","Cash advances","Fee-free advances between paychecks (Premium).")],
   pros=["Engaging, habit-forming UX","Free core features","Real savings behavior change","Personality sets it apart"],
   cons=["US/UK focused","Premium for best features","Not a full bank","Advances have limits"],
   verdict="Cleo is the most fun way to build better money habits. If you've tried budgeting apps and quit, Cleo's personality is the hook that keeps you coming back.",
   cta_url="https://web.cleo.ai/?via=toolforge"),

 dict(slug="plaud-ai", name="Plaud", tagline="Plaud's pocket AI note-taker — record real-life conversations and get transcripts, summaries, and action items.",
   category="Productivity", color1="#2d6cdf", color2="#1f4fb0", initials="Pl", price="$9/mo", price_label="plus hardware", price_num="9",
   free_tier="Limited monthly minutes", rating="4.4/5", rating_num="4.4", users="Hundreds of thousands", founded="2022",
   headline="Capture every conversation",
   intro="Plaud makes a credit-card-sized recorder (the Plaud Note / NotePin) plus an AI app that turns real-world conversations — meetings, calls, lectures — into transcribed, summarized notes with auto-generated action items. Unlike phone-only apps, Plaud captures in-person audio through a magnetic wearable device, then runs GPT-powered analysis into templates like 'sales call' or 'medical note.' It's the physical-layer answer to Otter and Fireflies.",
   who_for="Salespeople, consultants, doctors, and students who need accurate capture of in-person and phone conversations without typing.",
   features=[("🎙️","Wearable recorder","Credit-card device captures in-person audio."),
             ("📝","Auto-transcribe","Accurate speech-to-text in many languages."),
             ("🧾","Smart templates","Sales, medical, meeting summaries out of the box."),
             ("✅","Action items","Extracts next steps automatically.")],
   pros=["Captures in-person audio well","Strong auto-summarization","Pocketable hardware","Good template library"],
   cons=["Hardware sold separately","Monthly minute limits","Privacy considerations","App less deep than Otter"],
   verdict="If you need to capture real-world conversations (not just Zoom calls), Plaud's hardware-plus-AI combo beats pure software. For remote-only, Otter or Fireflies suffice.",
   cta_url="https://www.plaud.ai/?via=toolforge"),

 dict(slug="granola-ai", name="Granola", tagline="Granola's AI notepad for meetings — you type rough notes, it fills in the polished version automatically.",
   category="Productivity", color1="#111827", color2="#374151", initials="Gr", price="$9/mo", price_label="Pro", price_num="9",
   free_tier="Free tier (limited)", rating="4.4/5", rating_num="4.4", users="Tens of thousands", founded="2023",
   headline="Notes that write themselves",
   intro="Granola is a macOS notepad for meetings that listens in the background and, as you jot rough bullet points, automatically enriches them into clean, complete notes with action items. You stay in control — it never transcribes verbatim; it completes your skeleton. The result feels like a co-pilot for note-taking rather than a black-box recorder. It's become a favorite among founders and operators who hate reviewing raw transcripts.",
   who_for="Mac-using professionals, founders, and operators who take their own meeting notes and want them polished without a full transcription service.",
   features=[("✍️","Note completion","Your bullets become full notes automatically."),
             ("🎧","Background listen","No bot joins the call — it runs locally."),
             ("🧠","AI summaries","Action items and decisions extracted."),
             ("🔗","Integrations","Syncs to Notion, Linear, and more.")],
   pros=["No awkward meeting bot","Fast, lightweight","Polished output","Privacy-friendly local capture"],
   cons=["Mac only","You must take some notes","No full transcript","Limited collaboration"],
   verdict="Granola is the best 'assisted note-taking' tool for Mac users who already write their own notes. If you want a hands-off transcript, Otter or Fireflies fit better.",
   cta_url="https://granola.ai/?via=toolforge"),
]

# ============================================================
# NEW COMPARE PAGES (high search volume, verified missing)
# ============================================================
COMPARES = [
 dict(slug="v0-vs-loveable", name_a="v0.dev", name_b="Lovable",
   color_a="#000000", color_b="#9b5de5", initials_a="v0", initials_b="Lo",
   desc_a="Vercel's AI React/Tailwind component generator.",
   desc_b="AI full-stack app builder with backend and auth.",
   price_a="Free / $20 Pro", price_b="$20/mo",
   best_a="Frontend components, React/Next.js", best_b="Full-stack apps, non-coders",
   url_a="https://v0.dev/?via=toolforge", url_b="https://lovable.dev/?via=toolforge",
   verdict="v0 is the better pick when you need polished React components and already have an app. Lovable wins when you want a complete full-stack product — frontend, backend, auth, deploy — from one prompt, especially if you don't write code.",
   winner="v0 for components, Lovable for full apps"),

 dict(slug="chatgpt-vs-claude-opus-4-5", name_a="ChatGPT", name_b="Claude Opus 4.5",
   color_a="#10a37f", color_b="#d97706", initials_a="Ch", initials_b="O4",
   desc_a="OpenAI's generalist flagship with voice, vision, and image gen.",
   desc_b="Anthropic's most capable model for deep reasoning and long work.",
   price_a="$20/mo Plus", price_b="$20/mo Pro",
   best_a="Multimodal, image gen, broad ecosystem", best_b="Deep reasoning, long docs, agentic coding",
   url_a="https://chat.openai.com/?via=toolforge", url_b="https://claude.ai/?via=toolforge",
   verdict="ChatGPT is the better all-rounder with image generation and voice; Claude Opus 4.5 is the better choice for the hardest reasoning, longest documents, and most careful agentic work. Power users keep both.",
   winner="Tie — ChatGPT for breadth, Opus for depth"),

 dict(slug="claude-vs-chatgpt-2026", name_a="Claude", name_b="ChatGPT",
   color_a="#d97706", color_b="#10a37f", initials_a="Cl", initials_b="Ch",
   desc_a="Anthropic's thoughtful, writing-strong assistant.",
   desc_b="OpenAI's multimodal generalist assistant.",
   price_a="Free / $20 Pro", price_b="Free / $20 Plus",
   best_a="Long-form writing, analysis, code review", best_b="Brainstorming, image gen, voice",
   url_a="https://claude.ai/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   verdict="In 2026 both are excellent. Claude edges writing, analysis, and careful reasoning; ChatGPT edges multimodal features and third-party integrations. Most people are happy with either — pick by which strengths you use most.",
   winner="Tie — pick by use case"),
]

# ============================================================
# NEW BLOG POSTS (fresh long-tail SEO, verified missing)
# ============================================================
def card(name, color, initial, badge, desc, url):
    return dict(name=name, color=color, initial=initial, badge=badge, desc=desc, url=url)

BLOGS = [
 dict(slug="best-ai-tools-for-plumbers", title="The 7 Best AI Tools for Plumbers in 2026 (Win More Jobs)",
   meta="From quoting to local SEO, the AI stack that helps plumbers book more calls and spend less time on paperwork.",
   category="Trades", read="3",
   lead="Plumbing is a hands-on trade, but the business runs on phones, quotes, and reviews. AI in 2026 handles the desk work so you can be on the job, not behind it. Here are the tools that pay for themselves in booked jobs.",
   verdict="Use an AI answering service for after-hours calls, a local-SEO writer for your Google Business Profile, and an estimating tool for fast quotes. The ROI is measured in jobs you'd have missed.",
   tools=[
     card("ChatGPT","#10a37f","Ch","$20/mo","Quote templates and follow-ups","https://chat.openai.com/?via=toolforge"),
     card("Canva","#00c4cc","Ca","Free","Before/after job cards","https://www.canva.com/?via=toolforge"),
     card("Jasper","#7928ca","Ja","$49/mo","Local SEO service pages","https://www.jasper.ai/?via=toolforge"),
     card("Make","#0a72ef","Mk","$9/mo","Lead routing automations","https://www.make.com/en?ref=toolforge"),
     card("Calendly","#006bff","Cl","Free","Online booking","https://calendly.com/?via=toolforge"),
     card("Otter.ai","#4f46e5","Ot","$10/mo","Transcribe site visits","https://otter.ai/?via=toolforge"),
     card("Suno","#111827","Su","Free","Radio ad jingles","https://suno.com/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-restaurant-owners", title="The 8 Best AI Tools for Restaurant Owners in 2026",
   meta="Menus, marketing, and staffing — the AI stack that helps restaurant owners fill tables and cut costs.",
   category="Hospitality", read="3",
   lead="Running a restaurant means wearing every hat: marketer, HR, and ops manager. AI in 2026 takes the repetitive 60% off your plate so you can focus on the guest experience. Here's the stack smart owners use.",
   verdict="Start with an AI menu and social writer, add a review responder, and automate shift scheduling. Most of this is free or under $30/mo — the payoff is in covers and 5-star reviews.",
   tools=[
     card("ChatGPT","#10a37f","Ch","$20/mo","Menu copy and specials","https://chat.openai.com/?via=toolforge"),
     card("Canva","#00c4cc","Ca","Free","Instagram and menu graphics","https://www.canva.com/?via=toolforge"),
     card("Notion","#000000","No","Free","Recipe and ops wiki","https://www.notion.so/?via=toolforge"),
     card("Make","#0a72ef","Mk","$9/mo","Reservation and review flows","https://www.make.com/en?ref=toolforge"),
     card("Otter.ai","#4f46e5","Ot","$10/mo","Transcribe staff meetings","https://otter.ai/?via=toolforge"),
     card("Fireflies.ai","#1f6feb","Fi","$10/mo","Auto meeting notes","https://fireflies.ai/?via=toolforge"),
     card("Suno","#111827","Su","Free","Background music drafts","https://suno.com/?via=toolforge"),
     card("Jasper","#7928ca","Ja","$49/mo","Local SEO landing pages","https://www.jasper.ai/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-virtual-assistants", title="The 9 Best AI Tools for Virtual Assistants in 2026",
   meta="The AI stack that lets VAs serve more clients, faster — without dropping the ball.",
   category="Virtual Assistants", read="3",
   lead="Virtual assistants live in other people's inboxes and calendars. AI in 2026 is the VA's force multiplier — drafting replies, summarizing meetings, and automating busywork across clients. Here are the tools top VAs rely on.",
   verdict="Pair a writing model with a note-taker and an automation platform, and you can handle 2-3x the clients. The best VAs in 2026 aren't working more hours — they've delegated the dull parts to AI.",
   tools=[
     card("ChatGPT","#10a37f","Ch","$20/mo","Drafts and research","https://chat.openai.com/?via=toolforge"),
     card("Claude","#d97706","Cl","$20/mo","Long email threads and docs","https://claude.ai/?via=toolforge"),
     card("Notion","#000000","No","Free","Client wikis and SOPs","https://www.notion.so/?via=toolforge"),
     card("Otter.ai","#4f46e5","Ot","$10/mo","Meeting transcription","https://otter.ai/?via=toolforge"),
     card("Fireflies.ai","#1f6feb","Fi","$10/mo","Auto call notes","https://fireflies.ai/?via=toolforge"),
     card("Make","#0a72ef","Mk","$9/mo","Client workflow automations","https://www.make.com/en?ref=toolforge"),
     card("Calendly","#006bff","Cl","Free","Scheduling across clients","https://calendly.com/?via=toolforge"),
     card("Canva","#00c4cc","Ca","Free","Client graphics and decks","https://www.canva.com/?via=toolforge"),
     card("Grammarly","#10a37f","Gr","Free","Polished client comms","https://www.grammarly.com/?via=toolforge"),
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
entry = f"\n## {TODAY} — Sprint batch (cron cycle, _sprint_batch_jul17d.py)\n"
entry += f"- Tools created: {created['tools']} | Compares: {created['compare']} | Blogs: {created['blog']}\n"
entry += f"- Total new URLs: {len(new_urls)}\n"
entry += f"- Sitemap URLs after regen: {len(files)}\n"
entry += f"- IndexNow: {idx}\n"
if new_urls:
    entry += "- New slugs: " + ", ".join(u.split('/')[-1] for u in new_urls) + "\n"
with open(logpath, 'a') as f:
    f.write(entry)

print(f"\nCREATED: {created}")
