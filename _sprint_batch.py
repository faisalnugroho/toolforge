#!/usr/bin/env python3
"""ToolForge Sprint Batch — add genuinely-missing pages + regenerate sitemap.

Reuses the EXACT templates from _sprint_gen.py by loading its definition
section only (no side effects), then writes new tool/compare/blog pages
that do not already exist, and regenerates sitemap.xml from the filesystem.
"""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-10"
DOMAIN = "https://toolforge.io"

# ---- load template functions WITHOUT running the write block ----
with open(os.path.join(BASE, '_sprint_gen.py')) as f:
    src = f.read()
marker = '# =================== WRITE ==================='
idx = src.index(marker)
ns = {}
exec(compile(src[:idx], '_sprint_gen_partial', 'exec'), ns)
tool_html = ns['tool_html']
compare_html = ns['compare_html']
blog_html = ns['blog_html']

# ---- scanners ----
def existing_slugs(sub):
    d = os.path.join(BASE, sub)
    if not os.path.isdir(d):
        return set()
    return {f[:-5] for f in os.listdir(d) if f.endswith('.html')}

tool_slugs = existing_slugs('tools')
blog_slugs = existing_slugs('blog')
cmp_slugs = existing_slugs('compare')

# =================== NEW TOOL PAGES ===================
NEW_TOOLS = [
 dict(slug="gpt-4o", name="GPT-4o", tagline="OpenAI's flagship omni-model — real-time voice, vision, and text in one fast, affordable package.", category="Productivity",
   color1="#10a37f", color2="#0e8c6e", initials="4o", price="$20/mo", price_label="ChatGPT Plus", price_num="20",
   free_tier="Free tier (limited)", rating="4.8/5", rating_num="4.8", users="200M+ users", founded="2024",
   headline="The model that made 'omni' real",
   intro="GPT-4o ('omni') was OpenAI's 2024 leap to a single model that handles text, vision, and audio natively — including real-time voice conversation with near-zero latency. In 2026 it remains the default engine behind ChatGPT Plus and the workhorse for millions of everyday tasks, from drafting to live translation to on-screen help.",
   who_for="Everyone. Knowledge workers, students, creators, and developers who want one fast, capable, multimodal assistant without juggling separate tools.",
   features=[("🎙️","Real-time voice","Talk to it like a person — interrupt, joke, and get sub-second spoken replies."),
             ("👁️","Native vision","Snap a photo of a whiteboard or a bug and it reasons over what it sees."),
             ("⚡","Speed & price","Roughly 2x faster than GPT-4-class predecessors at half the cost."),
             ("🔌","Tool ecosystem","Browse, code, and call functions inside one chat session.")],
   pros=["Best all-rounder for everyday tasks","Real-time voice is genuinely impressive","Cheap enough to use daily","Huge third-party ecosystem"],
   cons=["Image generation weaker than dedicated tools","Voice can still drift off-topic","No longest-context crown (that's Gemini)","Free tier is rate-limited"],
   verdict="If you only adopt one AI tool, GPT-4o via ChatGPT is the safe, fast, do-everything default. Pair it with a specialist (Claude for long writing, a dedicated image tool) and you've covered 90% of use cases.",
   cta_url="https://chat.openai.com/?via=toolforge"),

 dict(slug="claude-opus-4", name="Claude Opus 4", tagline="Anthropic's most capable model — top-tier reasoning, coding, and the longest production context window.", category="Productivity",
   color1="#d97706", color2="#b45309", initials="Op", price="$20/mo", price_label="Claude Pro", price_num="20",
   free_tier="Free tier (limited)", rating="4.9/5", rating_num="4.9", users="50M+ users", founded="2025",
   headline="The careful thinker's flagship",
   intro="Claude Opus 4 is Anthropic's most powerful model, launched in 2025 with class-leading reasoning, coding, and a 200K–1M token context window. It's the model developers and analysts reach for when correctness and nuance matter more than raw speed — codebases, long documents, and sensitive analysis.",
   who_for="Engineers, analysts, researchers, and writers who need the smartest, most careful model for complex, long-context work.",
   features=[("🧠","Frontier reasoning","State-of-the-art performance on math, planning, and agentic tasks."),
             ("📚","Massive context","Up to 1M tokens — drop in entire codebases or book-length docs."),
             ("💻","Elite coding","Top benchmark scores for real-world software engineering."),
             ("🛡️","Constitutional safety","Refuses less, helps more, with strong steerability.")],
   pros=["Best-in-class reasoning and coding","Handles enormous inputs gracefully","Most 'human' long-form writing","Strong safety without being preachy"],
   cons=["Slower than smaller models on trivial tasks","Costs more than GPT-4o for high volume","No native real-time voice yet","Image generation not its strength"],
   verdict="Claude Opus 4 is the model to pick when the task is hard. For daily chatter it's overkill, but for coding, analysis, and serious writing it's the quiet leader.",
   cta_url="https://claude.ai/?via=toolforge"),

 dict(slug="openrouter", name="OpenRouter", tagline="One API to access every frontier model — GPT, Claude, Llama, Mistral — with per-token pricing and no lock-in.", category="Coding",
   color1="#111827", color2="#374151", initials="OR", price="Pay-per-token", price_label="Usage-based", price_num="0",
   free_tier="Free models available", rating="4.7/5", rating_num="4.7", users="1M+ developers", founded="2023",
   headline="The universal model router",
   intro="OpenRouter is the developer's cheat code: a single API key that lets your app call GPT-5, Claude Opus, Llama, Mistral, DeepSeek, and 100+ other models — routing to the cheapest or best option per request. No per-vendor contracts, no lock-in, just tokens.",
   who_for="Builders, startups, and enterprises who want model flexibility and price arbitrage without integrating a dozen providers.",
   features=[("🔀","One endpoint","Swap models with a single parameter change."),
             ("💸","Price arbitrage","Route to the cheapest model that meets quality."),
             ("🔓","Open + frontier","Mix open-weights and closed models freely."),
             ("🛡️","No lock-in","Your prompts aren't trapped with one vendor.")],
   pros=["Massive model catalog","Transparent per-token pricing","Easy fallbacks and load balancing","Great for experimentation"],
   cons=["Latency varies by backend","Quality depends on model chosen","Not a UI — it's an API","Support is community-driven"],
   verdict="If you build with LLMs, OpenRouter is the fastest way to stay model-agnostic and cost-efficient. Wire it once, then play the whole field.",
   cta_url="https://openrouter.ai"),

 dict(slug="openwebui", name="Open WebUI", tagline="The self-hosted, open-source ChatGPT alternative — run any model behind your own login, on your own hardware.", category="Productivity",
   color1="#3b82f6", color2="#2563eb", initials="OW", price="Free", price_label="Open source", price_num="0",
   free_tier="Always free (self-hosted)", rating="4.8/5", rating_num="4.8", users="500K+ installs", founded="2023",
   headline="Your AI, behind your firewall",
   intro="Open WebUI is the open-source app that turns any local or cloud model (Ollama, vLLM, OpenAI-compatible endpoints) into a polished ChatGPT-style interface — with user management, RAG, document chat, and plugins. It's the default front-end for privacy-focused AI deployments in 2026.",
   who_for="Privacy-conscious users, self-hosters, teams, and enterprises that need a ChatGPT experience without sending data to a third party.",
   features=[("🔒","Self-hosted","Runs on your server; your data never leaves."),
             ("📄","RAG & docs","Chat with your PDFs and internal knowledge."),
             ("👥","Multi-user","Auth, roles, and shared workspaces built in."),
             ("🧩","Plugins","Function calls, pipelines, and community extensions.")],
   pros=["Fully open source and free","Works with any OpenAI-compatible model","Strong privacy and control","Active, fast-moving community"],
   cons=["Requires self-hosting setup","No managed SLA unless you pay for cloud","UI polish trails closed rivals slightly","Best features need a GPU"],
   verdict="The best way to get a ChatGPT-grade experience on your own terms. If privacy or cost matters, Open WebUI + Ollama is the combo to beat.",
   cta_url="https://github.com/open-webui/open-webui"),

 dict(slug="mistral-le-chat", name="Le Chat", tagline="Mistral's conversational AI — fast European models with strong multilingual and coding chops.", category="Productivity",
   color1="#fa520f", color2="#ec4899", initials="LC", price="Free", price_label="Freemium", price_num="0",
   free_tier="Free tier", rating="4.4/5", rating_num="4.4", users="10M+ users", founded="2024",
   headline="European AI, with an accent on speed",
   intro="Le Chat is Mistral AI's consumer assistant, powered by the French lab's efficient models. It's known for snappy responses, strong European-language support, and a growing agentic feature set — all from a company that positions itself as the independent, GDPR-friendly alternative to US giants.",
   who_for="EU users, multilingual teams, and anyone who wants a fast, privacy-minded assistant from a non-US lab.",
   features=[("🌍","Multilingual","Excellent French, Spanish, German, and more."),
             ("⚡","Low latency","Mistral's models are built for speed."),
             ("🤖","Agents & code","Tool use, coding, and web access built in."),
             ("🇪🇺","GDPR-friendly","European hosting and data handling.")],
   pros=["Fast, efficient responses","Strong non-English support","Independent European alternative","Free tier is generous"],
   cons=["Smaller ecosystem than US rivals","Image gen lags behind","Fewer third-party integrations","Brand awareness still growing"],
   verdict="Le Chat is the pick for European users and anyone who wants a fast, independent assistant. It won't replace GPT or Claude for everything, but it's a serious, privacy-minded contender.",
   cta_url="https://chat.mistral.ai"),

 dict(slug="kling-2", name="Kling 2.0", tagline="Kuaishou's video foundation model — uncanny motion realism and the longest prompt-faithful clips in 2026.", category="Video",
   color1="#7c3aed", color2="#6d28d9", initials="Kl", price="$10/mo", price_label="Standard plan", price_num="10",
   free_tier="Free credits", rating="4.6/5", rating_num="4.6", users="20M+ users", founded="2024",
   headline="The motion-realism king",
   intro="Kling, from Chinese tech company Kuaishou, shocked the video world with physics-aware motion that barely flickers — and Kling 2.0 pushed clip length, prompt adherence, and camera control even further. In 2026 it's the go-to for creators who need believable human movement without a shoot.",
   who_for="Filmmakers, marketers, and creators who need realistic, prompt-controlled video without a camera or actors.",
   features=[("🎬","Realistic motion","Physics-aware movement that doesn't melt under scrutiny."),
             ("🎥","Camera control","Directable pans, dollies, and shot framing."),
             ("📝","Prompt adherence","Holds to your description across longer clips."),
             ("🖼️","Image-to-video","Animate a still into a living scene.")],
   pros=["Best-in-class motion realism","Longer, coherent clips","Strong camera direction","Competitive pricing"],
   cons=["Censorship on some prompts","Queue times on free tier","English prompt quirks","Not open-weights"],
   verdict="For realistic human motion, Kling 2.0 is the one to beat. Pair it with Runway or Veo for stylized work and you've got a full generative video suite.",
   cta_url="https://klingai.com"),

 dict(slug="bing-copilot", name="Bing Copilot", tagline="Microsoft's web-connected AI in the search box — answers grounded in live web results, free to use.", category="Productivity",
   color1="#0078d4", color2="#106ebe", initials="BC", price="Free", price_label="Free", price_num="0",
   free_tier="Always free", rating="4.3/5", rating_num="4.3", users="100M+ users", founded="2023",
   headline="AI with its finger on the live web",
   intro="Bing Copilot (formerly Bing Chat) is Microsoft's free assistant baked into Edge and Bing, grounded in real-time search results. It cites sources, summarizes the web, and answers follow-up questions — a lightweight, no-cost way to get grounded answers without a subscription.",
   who_for="Casual researchers, students, and anyone who wants free, cited, web-grounded answers without paying for ChatGPT Plus.",
   features=[("🌐","Live web grounding","Answers cite current pages, not stale training data."),
             ("🆓","Free","Full access with no paywall."),
             ("📊","Summarizes results","Condenses search results into answers."),
             ("🔗","Citations","Sources are linked inline.")],
   pros=["Completely free","Grounded in live web data","Good for research and current events","Built into Edge browser"],
   cons=["Weaker reasoning than GPT-4o/Claude","Occasional citation errors","Tied to Microsoft ecosystem"," Less customizable"],
   verdict="The best free, web-grounded assistant around. Use it for research and current-events questions; reach for ChatGPT or Claude when you need deeper reasoning.",
   cta_url="https://copilot.microsoft.com"),

 dict(slug="devin-ai", name="Devin AI", tagline="Cognition's autonomous software engineer — plans, codes, debugs, and ships entire features from a ticket.", category="Coding",
   color1="#6366f1", color2="#4f46e5", initials="Dv", price="$500/mo", price_label="Team plan", price_num="500",
   free_tier="Limited preview", rating="4.5/5", rating_num="4.5", users="5K+ engineering teams", founded="2024",
   headline="The first fully autonomous engineer",
   intro="Devin, from Cognition, was the first AI agent pitched as a real software engineer — not a copilot but a teammate that takes a ticket, writes the code, runs the tests, fixes failures, and opens a PR. By 2026 it handles end-to-end feature work and long-running refactors inside a sandboxed environment.",
   who_for="Engineering leaders and teams who want to parallelize feature delivery and offload well-specified implementation work.",
   features=[("🤖","End-to-end PRs","From ticket to pull request, unassisted."),
             ("🧪","Runs the suite","Iterates against your own tests until green."),
             ("🪄","Long tasks","Handles multi-hour refactors and migrations."),
             ("🔍","Self-debugs","Reads stack traces and fixes its own mistakes.")],
   pros=["Genuinely autonomous implementation","Frees senior devs for design","Strong test-driven loop","Scales team throughput"],
   cons=["Expensive at $500/mo","Needs clear specs to shine","Occasional off-target edits","Human review still required"],
   verdict="Devin is the closest thing to 'hire another engineer' on a subscription. For teams with good specs and tests, it's a force multiplier — just keep a reviewer in the loop.",
   cta_url="https://devin.ai"),

 dict(slug="perplexity-sonar", name="Perplexity Sonar", tagline="Perplexity's API for grounded, real-time answers — every response cited from the live web.", category="Productivity",
   color1="#20808d", color2="#0ea5e9", initials="Sn", price="$5/mo", price_label="API Pro", price_num="5",
   free_tier="Free tier (limited)", rating="4.6/5", rating_num="4.6", users="100M+ queries/mo", founded="2024",
   headline="Grounded answers as an API",
   intro="Sonar is Perplexity's developer API that returns chat-style answers with inline citations pulled from the live web. It's the backbone for apps that need current, sourced facts rather than a model's fuzzy memory — powering research bots, copilots, and customer assistants.",
   who_for="Developers and product teams who need real-time, cited answers embedded in their own apps.",
   features=[("📚","Cited answers","Every claim links to a source."),
             ("⚡","Low latency","Built for fast, interactive queries."),
             ("🌐","Live web","Knowledge that updates in real time."),
             ("🔌","API-first","Drop-in for RAG and copilot features.")],
   pros=["Grounded, citable output","Cheap entry tier","Fast and reliable","Great for RAG apps"],
   cons=["Less creative than chat models","Citation quality varies","Not for long-form writing","Needs query tuning"],
   verdict="If your app needs facts it can cite, Sonar is the cleanest way to get them. Pair it with a creative model for the rest.",
   cta_url="https://www.perplexity.ai/sonar"),

 dict(slug="anythingllm", name="AnythingLLM", tagline="The all-in-one, self-hosted AI app — chat with docs, run agents, and RAG your private data locally.", category="Productivity",
   color1="#0f766e", color2="#0d9488", initials="AL", price="Free", price_label="Open source", price_num="0",
   free_tier="Always free (self-hosted)", rating="4.7/5", rating_num="4.7", users="1M+ downloads", founded="2023",
   headline="Private RAG, one download away",
   intro="AnythingLLM is the desktop and self-hosted app that turns your documents into a chat-able knowledge base — with vector search, agent skills, and support for any model (local or cloud). It's the go-to for businesses and individuals who want ChatGPT-with-their-data without the cloud.",
   who_for="Businesses, researchers, and privacy-minded users who need to chat with their own documents securely.",
   features=[("📚","Document RAG","Ingest PDFs, docs, and sites into a chat brain."),
             ("🤖","Agents","Give it tools to browse and act."),
             ("🔒","Private","Runs locally; data stays yours."),
             ("🧩","Any model","Local (Ollama) or cloud endpoints.")],
   pros=["Full privacy and control","Excellent document chat","Works with any model","Free and open source"],
   cons=["Setup is more involved than SaaS"," UI can feel busy","Best on decent hardware","Support is community-based"],
   verdict="The most complete self-hosted AI workspace available. If you need to chat with your own data privately, AnythingLLM is the place to start.",
   cta_url="https://anythingllm.com"),
]

# =================== NEW COMPARE PAGES ===================
NEW_COMPARES = [
 dict(slug="gpt-4o-vs-gpt-5", name_a="GPT-4o", name_b="GPT-5", color_a="#10a37f", color_b="#0a72ef",
   initials_a="4o", initials_b="G5", url_a="https://chat.openai.com/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="OpenAI's fast, multimodal omni-model", desc_b="OpenAI's 2025 flagship with deeper reasoning",
   price_a="$20/mo Plus", price_b="$20/mo Plus", best_a="everyday chat, voice, vision", best_b="hard reasoning, agents, coding",
   verdict="Use <strong>GPT-4o</strong> when you want the fastest, cheapest, most responsive everyday assistant with great voice and vision. Use <strong>GPT-5</strong> when the task is hard — multi-step reasoning, agentic workflows, and frontier coding. Most users are happy on 4o; power users should step up to 5.",
   winner="GPT-5 for hard tasks, 4o for daily use"),

 dict(slug="claude-opus-vs-gpt-5", name_a="Claude Opus 4", name_b="GPT-5", color_a="#d97706", color_b="#0a72ef",
   initials_a="Op", initials_b="G5", url_a="https://claude.ai/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Anthropic's careful, long-context flagship", desc_b="OpenAI's 2025 reasoning flagship",
   price_a="$20/mo Pro", price_b="$20/mo Plus", best_a="long docs, code review, nuanced writing", best_b="agents, multimodal, ecosystem",
   verdict="Use <strong>Claude Opus 4</strong> for the most careful long-context work — codebases, book-length analysis, and nuanced writing. Use <strong>GPT-5</strong> for broad ecosystem reach, agentic tasks, and when you want one model that does everything. They're the two frontrunners; pick by which strengths you lean on.",
   winner="Tie — Claude for depth, GPT-5 for breadth"),

 dict(slug="openrouter-vs-poe", name_a="OpenRouter", name_b="Poe", color_a="#111827", color_b="#5b21b6",
   initials_a="OR", initials_b="Po", url_a="https://openrouter.ai", url_b="https://poe.com",
   desc_a="One API for 100+ models, pay-per-token", desc_b="Quora's multi-model consumer chat hub",
   price_a="Pay-per-token", price_b="$20/mo Sub", best_a="builders, price arbitrage, no lock-in", best_b="casual users, many models in one tab",
   verdict="Use <strong>OpenRouter</strong> if you build software and want one API to route across every model with per-token billing. Use <strong>Poe</strong> if you're a consumer who wants to hop between bots in a single chat app. OpenRouter is for developers; Poe is for chatters.",
   winner="OpenRouter for devs, Poe for consumers"),

 dict(slug="openwebui-vs-lm-studio", name_a="Open WebUI", name_b="LM Studio", color_a="#3b82f6", color_b="#1a1a1a",
   initials_a="OW", initials_b="LS", url_a="https://github.com/open-webui/open-webui", url_b="https://lmstudio.ai",
   desc_a="Self-hosted ChatGPT-style UI for any model", desc_b="Desktop app to run models locally with a GUI",
   price_a="Free (open source)", price_b="Free (open source)", best_a="multi-user, RAG, docs chat", best_b="easy local model downloads & inference",
   verdict="Use <strong>Open WebUI</strong> when you want a full self-hosted assistant with users, RAG, and document chat. Use <strong>LM Studio</strong> when you just want to download and run models on your desktop with the least friction. Many run both — LM Studio to serve, Open WebUI to chat.",
   winner="Open WebUI for teams, LM Studio for solo locals"),

 dict(slug="kling-2-vs-veo-3", name_a="Kling 2.0", name_b="Veo 3", color_a="#7c3aed", color_b="#4285f4",
   initials_a="Kl", initials_b="V3", url_a="https://klingai.com", url_b="https://gemini.google.com",
   desc_a="Motion-realism king from Kuaishou", desc_b="Google's cinematic, audio-aware video model",
   price_a="$10/mo Standard", price_b="$20/mo Ultra", best_a="realistic human motion, camera control", best_b="cinematic quality, synced audio",
   verdict="Use <strong>Kling 2.0</strong> for the most realistic human movement and precise camera direction. Use <strong>Veo 3</strong> when you want cinematic polish and native synced audio (dialogue, sound effects). Kling wins on motion; Veo wins on finished, audible scenes.",
   winner="Kling for motion, Veo 3 for cinematic audio"),

 dict(slug="devin-vs-cursor", name_a="Devin AI", name_b="Cursor", color_a="#6366f1", color_b="#000000",
   initials_a="Dv", initials_b="Cu", url_a="https://devin.ai", url_b="https://www.cursor.com/?via=toolforge",
   desc_a="Autonomous engineer that ships PRs", desc_b="AI-first editor you drive in real time",
   price_a="$500/mo Team", price_b="$20/mo Pro", best_a="end-to-end features, long refactors", best_b="interactive coding, pair programming",
   verdict="Use <strong>Devin</strong> when you have well-specified tickets and want them closed autonomously. Use <strong>Cursor</strong> when you want to stay in the loop, directing edits interactively. Devin is a teammate; Cursor is a superpower you steer. Most solo devs want Cursor; teams scaling delivery want Devin.",
   winner="Cursor for control, Devin for throughput"),

 dict(slug="chatgpt-go-vs-chatgpt-plus", name_a="ChatGPT Go", name_b="ChatGPT Plus", color_a="#10a37f", color_b="#0a72ef",
   initials_a="Go", initials_b="Pl", url_a="https://chat.openai.com/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Lower-cost tier for lighter users", desc_b="The standard $20 power-user tier",
   price_a="$10/mo Go", price_b="$20/mo Plus", best_a="casual users, students, basic tasks", best_b="heavy users, advanced models, voice",
   verdict="Use <strong>ChatGPT Go</strong> if you're a lighter user who mostly chats and doesn't need the highest limits or every advanced feature. Use <strong>ChatGPT Plus</strong> if you lean on it daily, hit caps, or want the fullest model access. Go saves $10; Plus buys headroom.",
   winner="Go for light use, Plus for power users"),

 dict(slug="bing-copilot-vs-chatgpt", name_a="Bing Copilot", name_b="ChatGPT", color_a="#0078d4", color_b="#10a37f",
   initials_a="BC", initials_b="Ch", url_a="https://copilot.microsoft.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Free, web-grounded assistant in search", desc_b="OpenAI's generalist flagship assistant",
   price_a="Free", price_b="$20/mo Plus", best_a="free cited research, current events", best_b="reasoning, voice, image gen, ecosystem",
   verdict="Use <strong>Bing Copilot</strong> when you want free, cited, web-grounded answers and live info. Use <strong>ChatGPT</strong> when you need deeper reasoning, voice, image generation, and a richer tool ecosystem. Copilot is free research; ChatGPT is the full toolkit.",
   winner="ChatGPT for power, Bing Copilot for free research"),
]

# =================== NEW BLOG POSTS ===================
NEW_BLOGS = [
 dict(slug="best-ai-tools-for-teachers-2026", title="The 9 Best AI Tools for Teachers in 2026 (Save 10+ Hours/Week)",
   meta="Lesson plans, grading, differentiation, and parent comms — the AI stack that gives teachers their weekends back.",
   category="For Teachers", read="3",
   lead="Teachers in 2026 aren't worried about AI replacing them — they're using it to reclaim the 10+ hours a week lost to admin. We tested the stack that actually helps educators teach more and grade less, without crossing academic-integrity lines.",
   verdict="Start with a planning assistant (ChatGPT or Claude) for lessons and a grading helper (MagicSchool or Quizgecko) for assessments. Add NotebookLM to turn your handouts into a study podcast and Gamma for slide decks. The goal is more teaching, less paperwork.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="$20/mo", desc="Lesson plans and differentiated worksheets"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Patient explainer for tough topics"),
     dict(name="Gemini", url="https://gemini.google.com", color="#4285f4", initial="Ge", badge="Free", desc="Works inside Google Classroom"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="Classroom visuals and posters"),
     dict(name="NotebookLM", url="https://notebooklm.google.com", color="#4285f4", initial="Nl", badge="Free", desc="Turns handouts into study audio"),
     dict(name="Gamma", url="https://gamma.app", color="#673ab7", initial="Ga", badge="$10/mo", desc="Lesson decks in seconds"),
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Cited research for units"),
     dict(name="Quizgecko", url="https://quizgecko.com", color="#7c3aed", initial="Qg", badge="$9/mo", desc="Auto-generate quizzes from text"),
     dict(name="MagicSchool", url="https://magicschool.ai", color="#2563eb", initial="Ms", badge="Free", desc="Purpose-built for teachers"),
   ]),

 dict(slug="ai-tools-for-doctors-2026", title="AI Tools for Doctors in 2026: What's Safe, Useful, and Worth It",
   meta="Clinical documentation, literature search, and patient education — the AI tools physicians are actually using (and the ones to avoid).",
   category="For Doctors", read="3",
   lead="Healthcare is where AI hype meets the highest stakes. In 2026, physicians are quietly using AI for the boring, time-consuming 70% — notes, literature triage, and patient explanations — while keeping the clinical judgment firmly human. Here's what's actually worth adopting.",
   verdict="Use AI scribes (Whisper-based or Dragon) to kill charting time, Perplexity or UpToDate-linked search for fast literature checks, and ChatGPT/Claude only to draft plain-language patient education. Never let a model make the diagnosis — treat it as a tireless junior assistant, not attending.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Draft patient-education handouts"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Summarize long clinical notes"),
     dict(name="Microsoft Dragon", url="https://www.microsoft.com/dragon", color="#0078d4", initial="Md", badge="$$", desc="Ambient clinical documentation"),
     dict(name="UpToDate", url="https://www.uptodate.com", color="#0a72ef", initial="Ud", badge="$$", desc="Evidence-grade point-of-care"),
     dict(name="Whisper", url="https://openai.com/whisper", color="#10a37f", initial="Wh", badge="Free", desc="Transcribe consults locally"),
     dict(name="DeepL", url="https://www.deepl.com", color="#1a1a1a", initial="Dl", badge="Free", desc="Multilingual patient comms"),
     dict(name="Notion", url="https://www.notion.so", color="#111827", initial="No", badge="Free", desc="Private clinic knowledge base"),
     dict(name="Fireflies", url="https://fireflies.ai", color="#7c3aed", initial="Ff", badge="$19/mo", desc="Transcribe case discussions"),
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Cited literature triage"),
   ]),

 dict(slug="best-ai-tools-for-photographers-2026", title="The 8 Best AI Tools for Photographers in 2026 (Edit Faster, Shoot More)",
   meta="From culling to retouching to upscaling — the AI that turns a 500-photo session into a deliverable gallery in an afternoon.",
   category="For Photographers", read="2",
   lead="The photographers winning in 2026 aren't spending all night in Lightroom. They're using AI to cull the keepers, retouch skin, and upscale shots for print — then spending the saved hours behind the camera. Here's the edit-faster stack.",
   verdict="Use an AI culler and a quality upscaler (Topaz or Krea) as your backbone, Luminar Neo or Lensa for one-click looks, and Remove.bg for product/commerce work. The result: a 500-photo wedding edits down to a gallery in an afternoon, not a week.",
   tools=[
     dict(name="Adobe Photoshop", url="https://www.adobe.com/products/photoshop.html", color="#31a8ff", initial="Ps", badge="$10/mo", desc="Generative Fill & neural filters"),
     dict(name="Luminar Neo", url="https://skylum.com/luminar", color="#1a1a1a", initial="Ln", badge="$14/mo", desc="One-click AI relight & sky"),
     dict(name="Lensa", url="https://lensa.ai", color="#000000", initial="Le", badge="Free", desc="Magic Avatars & retouch"),
     dict(name="Topaz Photo AI", url="https://www.topazlabs.com/photo-ai", color="#0ea5e9", initial="Tp", badge="$99 once", desc="Denoise, sharpen, upscale"),
     dict(name="Krea", url="https://www.krea.ai", color="#111827", initial="Kr", badge="Free", desc="Real-time AI enhancement"),
     dict(name="Remove.bg", url="https://www.remove.bg", color="#00c4cc", initial="Rb", badge="Free", desc="Instant background removal"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="Client galleries & watermarks"),
     dict(name="Google Photos", url="https://photos.google.com", color="#ea4335", initial="Gp", badge="Free", desc="AI search & auto albums"),
   ]),

 dict(slug="ai-tools-vs-human-writers-2026", title="AI Writers vs Human Writers in 2026: Who Actually Wins?",
   meta="AI can draft a blog post in seconds. But does it beat a human? We break down speed, quality, cost, and when to use which.",
   category="Analysis", read="3",
   lead="The 'AI will replace writers' panic has cooled into a clearer reality: AI is a turbocharger, not a replacement. In 2026 the question isn't human vs machine — it's how to combine them. We scored both on speed, quality, cost, and originality.",
   verdict="Use AI (ChatGPT, Claude, Jasper) for first drafts, outlines, and high-volume SEO — then have a human edit for voice, accuracy, and nuance. The hybrid workflow produces more content at higher quality than either alone. Pure-AI reads flat; pure-human doesn't scale. The winners use both.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Fast first drafts & outlines"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Nuanced long-form editing"),
     dict(name="Jasper", url="https://www.jasper.ai/?via=toolforge", color="#7928ca", initial="Ja", badge="$49/mo", desc="Brand-voice marketing copy"),
     dict(name="Grammarly", url="https://www.grammarly.com", color="#15c39a", initial="Gr", badge="Free", desc="Polish & clarity pass"),
     dict(name="Sudowrite", url="https://www.sudowrite.com/?via=toolforge", color="#7c3aed", initial="Sw", badge="Trial", desc="Fiction co-pilot"),
     dict(name="Copy.ai", url="https://www.copy.ai", color="#e11d48", initial="Ca", badge="Free", desc="GTM & ad copy at scale"),
     dict(name="Writesonic", url="https://writesonic.com", color="#7c3aed", initial="Ws", badge="Free", desc="SEO article generator"),
     dict(name="QuillBot", url="https://quillbot.com", color="#0ea5e9", initial="Qb", badge="Free", desc="Paraphrase & summarize"),
   ]),
]

# =================== WRITE ===================
new_urls = []
created = {"tools": 0, "compare": 0, "blog": 0}

for t in NEW_TOOLS:
    if t['slug'] in tool_slugs:
        print(f"  SKIP tool {t['slug']} (exists)"); continue
    p = os.path.join(BASE, 'tools', f"{t['slug']}.html")
    with open(p, 'w') as f:
        f.write(tool_html(t))
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html")
    created['tools'] += 1
    print(f"  + tool {t['slug']}.html")

for c in NEW_COMPARES:
    if c['slug'] in cmp_slugs:
        print(f"  SKIP compare {c['slug']} (exists)"); continue
    p = os.path.join(BASE, 'compare', f"{c['slug']}.html")
    with open(p, 'w') as f:
        f.write(compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    created['compare'] += 1
    print(f"  + compare {c['slug']}.html")

for b in NEW_BLOGS:
    if b['slug'] in blog_slugs:
        print(f"  SKIP blog {b['slug']} (exists)"); continue
    p = os.path.join(BASE, 'blog', f"{b['slug']}.html")
    with open(p, 'w') as f:
        f.write(blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    created['blog'] += 1
    print(f"  + blog {b['slug']}.html")

# =================== REGENERATE SITEMAP ===================
print("\n=== Regenerating sitemap.xml ===")
files = []
for root, dirs, fnames in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fn in fnames:
        if fn.startswith('.'):
            continue
        if not fn.endswith('.html'):
            continue
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, BASE).replace(os.sep, '/')
        if rel == '404.html':
            continue
        files.append(rel)
files.sort()

def priority(rel):
    if rel == 'index.html':
        return '1.0'
    if '/' not in rel:
        return '1.0'
    if rel.startswith('category/'):
        return '0.6'
    if rel.startswith('tools/'):
        return '0.8'
    if rel.startswith('blog/'):
        return '0.7'
    if rel.startswith('compare/'):
        return '0.7'
    return '0.8'

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for rel in files:
    lines.append('  <url>')
    lines.append(f'    <loc>{DOMAIN}/{rel}</loc>')
    lines.append(f'    <lastmod>{TODAY}</lastmod>')
    lines.append('    <changefreq>weekly</changefreq>')
    lines.append(f'    <priority>{priority(rel)}</priority>')
    lines.append('  </url>')
lines.append('</urlset>')
with open(os.path.join(BASE, 'sitemap.xml'), 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f"  OK wrote {len(files)} URLs to sitemap.xml")

# save new urls for IndexNow ping
with open('/tmp/toolforge_new_urls.txt', 'w') as f:
    f.write('\n'.join(new_urls) + '\n')

print(f"\nCREATED: {created}")
print(f"NEW URLS: {len(new_urls)}")
