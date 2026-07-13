#!/usr/bin/env python3
"""ToolForge Sprint Batch (2026-07-11) — add genuinely-missing pages + regenerate sitemap.

Reuses the EXACT templates from _sprint_gen.py by loading its definition
section only (no side effects), then writes new tool/compare/blog pages
that do not already exist, and regenerates sitemap.xml from the filesystem.
"""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-11"
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
 dict(slug="opencode", name="OpenCode", tagline="An open-source, terminal-native coding agent that runs Claude, GPT, and local models with full tool use and a TUI.", category="Coding",
   color1="#0a72ef", color2="#084cc4", initials="OC", price="Free", price_label="Open source", price_num="0",
   free_tier="Always free (OSS)", rating="4.6/5", rating_num="4.6", users="200K+ devs", founded="2024",
   headline="The terminal agent that isn't locked to one vendor",
   intro="OpenCode is a community-driven coding agent that lives in your terminal and works with any model — Anthropic, OpenAI, Google, or a local Ollama instance. Unlike editors that pin you to a single provider, OpenCode gives you a unified agent loop, diff view, and tool calling across providers, all from a fast TUI you can drop into any repo.",
   who_for="Developers who want a portable, model-agnostic coding agent they can self-host and extend without vendor lock-in.",
   features=[("🖥️","Terminal-native","Runs in any shell with a snappy TUI — no IDE required."),
             ("🔀","Any model","Point it at Claude, GPT, Gemini, or a local model via one config."),
             ("🛠️","Tool use","File edits, shell, search, and multi-step agent loops built in."),
             ("🔓","Open source","Auditable, free, and extensible under a permissive license.")],
   pros=["Model-agnostic by design","Fast, lightweight terminal UX","Self-hostable and private","Strong community momentum"],
   cons=["No GUI — terminal only","Setup is more hands-on than SaaS","Fewer polished integrations","Docs still maturing"],
   verdict="If you want a coding agent you actually own, OpenCode is the most flexible terminal option in 2026. Pair it with Claude or a local model and you get Cursor-grade autonomy without the subscription.",
   cta_url="https://github.com/opencode-ai/opencode"),

 dict(slug="supabase", name="Supabase", tagline="The open-source Firebase alternative — Postgres, auth, vector search, and AI helpers in one backend platform.", category="Coding",
   color1="#3ecf8e", color2="#249a64", initials="Sb", price="$25/mo", price_label="Pro plan", price_num="25",
   free_tier="Free tier (2 projects)", rating="4.7/5", rating_num="4.7", users="2M+ developers", founded="2020",
   headline="Your AI app's backend, in an afternoon",
   intro="Supabase wraps a managed Postgres database with auth, real-time subscriptions, storage, edge functions, and a pgvector-powered semantic search — the exact stack AI apps need. In 2026 it ships first-class AI helpers (embeddings, RAG templates, and an AI SQL editor) so builders can ship a grounded product without stitching six services together.",
   who_for="Indie hackers, startups, and teams who want a batteries-included backend with vectors and AI features without managing infrastructure.",
   features=[("🐘","Postgres core","A real relational database you can query with SQL."),
             ("🔎","pgvector search","Native vector embeddings for RAG and semantic search."),
             ("🔐","Auth & realtime","User management, row security, and live subscriptions."),
             ("🤖","AI helpers","Embeddings, AI SQL, and RAG starter templates.")],
   pros=["Open source and portable","Vectors + relational in one place","Generous free tier","Great DX and docs"],
   cons=["Vendor lock-in risk on edge functions","Scaling needs plan tuning","Vector perf at huge scale varies","Some features still beta"],
   verdict="Supabase is the fastest way to give an AI app a real backend. If you're building RAG or an agent with memory, the pgvector + auth combo alone saves weeks.",
   cta_url="https://supabase.com"),

 dict(slug="qdrant", name="Qdrant", tagline="A high-performance vector database built for production semantic search and RAG at scale.", category="Data",
   color1="#dc244c", color2="#a81232", initials="Qd", price="Free", price_label="Open source", price_num="0",
   free_tier="Self-host free", rating="4.6/5", rating_num="4.6", users="10K+ teams", founded="2021",
   headline="Vectors that don't fall over at scale",
   intro="Qdrant is a purpose-built vector similarity engine written in Rust, designed for fast, filtered semantic search across billions of embeddings. It's the backbone for RAG systems, recommendations, and deduplication where latency and recall both matter. In 2026 it offers a managed cloud plus a hybrid (dense + sparse) retrieval pipeline.",
   who_for="ML engineers and platform teams shipping RAG, recommendations, or similarity features that must stay fast under load.",
   features=[("⚡","Rust-fast","Sub-millisecond search even at billion-scale."),
             ("🧮","Hybrid retrieval","Combine dense and sparse vectors for better recall."),
             ("☁️","Managed cloud","Serverless tier that scales to zero."),
             ("🔒","On-prem ready","Self-host for full data control.")],
   pros=["Excellent performance/price","Strong filtering and payloads","Easy to self-host","Active open-source community"],
   cons=["Steeper than a hosted API","Operational care at scale","Smaller ecosystem than Pinecone","Learning curve for tuning"],
   verdict="Qdrant is the pragmatic choice when you outgrow a toy vector store but don't want to overpay. For production RAG, it's hard to beat on speed per dollar.",
   cta_url="https://qdrant.tech"),

 dict(slug="cloudflare", name="Cloudflare AI", tagline="Run inference, generate embeddings, and ship AI features at the edge — no servers, billed per token.", category="Coding",
   color1="#f6821f", color2="#c2410c", initials="CF", price="Pay-per-token", price_label="Usage-based", price_num="0",
   free_tier="Free tier (limited)", rating="4.4/5", rating_num="4.4", users="100K+ builders", founded="2023",
   headline="AI at the edge, milliseconds from users",
   intro="Cloudflare AI runs popular open models (Llama, Mistral, SDXL, Whisper) on Cloudflare's global network, so inference happens close to your users with no cold servers. Combined with Workers and Vectorize, you can build a full RAG app that lives entirely at the edge and scales automatically.",
   who_for="Full-stack developers who want low-latency AI inference and embeddings without managing GPU servers.",
   features=[("🌐","Edge inference","Models run in 300+ cities, near your users."),
             ("🧠","Many models","LLM, vision, speech, and embeddings in one API."),
             ("📈","Auto-scale","No servers to size; pay only for what you use."),
             ("🗂️","Vectorize","Edge vector store for RAG.")],
   pros=["Near-zero latency worldwide","No GPU ops","Generous free allowance","Tight Workers integration"],
   cons=["Model choice narrower than clouds","Cold-start nuances on free tier","Less control than self-host","Vendor-specific API"],
   verdict="For latency-sensitive, globally-distributed AI features, Cloudflare AI is the laziest path to production. Great for prototypes that need to stay fast everywhere.",
   cta_url="https://www.cloudflare.com/products/ai"),

 dict(slug="jina-ai", name="Jina AI", tagline="The search and embeddings API for RAG — long-context embeddings, rerankers, and a reader for any URL.", category="Data",
   color1="#5b8def", color2="#3b6fd1", initials="Ji", price="Free", price_label="Freemium", price_num="0",
   free_tier="Free tier", rating="4.5/5", rating_num="4.5", users="500K+ devs", founded="2020",
   headline="The plumbing that makes RAG actually work",
   intro="Jina AI builds the unglamorous but essential pieces of retrieval: best-in-class embedding models (including long-context and code), a Reader API that turns any URL into clean markdown, and rerankers that fix what naive similarity misses. It's the toolkit teams reach for when 'just stuff chunks in a vector DB' stops being good enough.",
   who_for="Developers building RAG, search, and knowledge apps who need better retrieval than default embeddings.",
   features=[("🔢","Embeddings","Long-context and code embeddings in one endpoint."),
             ("📑","Reader API","Convert any webpage to clean, LLM-ready markdown."),
             ("🔁","Rerankers","Re-order results for far better precision."),
             ("🔍","Segmenter","Chunk long docs intelligently.")],
   pros=["Excellent retrieval quality","Generous free tier","Simple, focused APIs","Great for RAG pipelines"],
   cons=["Not a full model host","Reranker adds latency","Best features are paid at scale","Niche outside search"],
   verdict="If your RAG answers feel off, Jina's embeddings + reranker combo is the cheapest quality jump you can make. Pair with Qdrant or Pinecone and watch recall climb.",
   cta_url="https://jina.ai"),

 dict(slug="chatbase", name="Chatbase", tagline="Build a custom ChatGPT-style chatbot trained on your own docs, site, or data — no code required.", category="Productivity",
   color1="#7c3aed", color2="#5b21b6", initials="Cb", price="$19/mo", price_label="Starter plan", price_num="19",
   free_tier="Free tier", rating="4.3/5", rating_num="4.3", users="100K+ businesses", founded="2023",
   headline="Your knowledge, as a chatbot",
   intro="Chatbase lets non-technical teams spin up a grounded chatbot from their website, PDFs, or help center in minutes. Upload sources, customize the widget, and embed it anywhere — the bot answers only from your data with citations. In 2026 it adds lead capture, human handoff, and multi-source sync.",
   who_for="Support, marketing, and ops teams who want a branded AI assistant without hiring an ML engineer.",
   features=[("📚","Train on your data","Ingest sites, PDFs, and docs automatically."),
             ("💬","Embed anywhere","Drop-in widget for web, Slack, or WhatsApp."),
             ("🔗","Citations","Answers link back to your sources."),
             ("🎯","Lead capture","Collect contacts from conversations.")],
   pros=["No-code setup","Fast time to value","Good for support deflection","Reasonable pricing"],
   cons=["Less flexible than custom RAG","Quality tied to source docs","Limited advanced tuning","Less control over prompts at free tier"],
   verdict="Chatbase is the fastest way to put your docs behind a chatbot. For SMB support and FAQs, it pays for itself in deflected tickets within a month.",
   cta_url="https://www.chatbase.co"),

 dict(slug="botpress", name="Botpress", tagline="An open-source conversational AI platform for building advanced chatbots and autonomous agents.", category="Productivity",
   color1="#1f9d55", color2="#157a40", initials="Bp", price="Free", price_label="Free tier", price_num="0",
   free_tier="Free (community)", rating="4.4/5", rating_num="4.4", users="500K+ builders", founded="2016",
   headline="Serious bots without a serious lock-in",
   intro="Botpress is the developer-friendly bot platform that blends a visual flow builder with a code SDK and LLM agents. It connects to 30+ channels (web, WhatsApp, Slack, Teams), ships NLU and knowledge bases, and lets you drop into code when flows aren't enough. In 2026 it leans hard into autonomous agents with memory and tool use.",
   who_for="Teams building customer-facing conversational experiences who want both a GUI and full programmatic control.",
   features=[("🧩","Visual + code","Flow builder and SDK in one."),
             ("📡","30+ channels","Web, WhatsApp, Slack, Teams, and more."),
             ("🧠","LLM agents","Autonomous loops with memory and tools."),
             ("🔓","Open core","Self-host the community edition.")],
   pros=["Flexible visual + code hybrid","Strong multi-channel reach","Free to start","Active open-source base"],
   cons=["Steeper than no-code tools","Cloud pricing climbs with usage","Some features enterprise-only","UI can feel busy"],
   verdict="Botpress is the sweet spot between 'no-code toy' and 'build it all yourself.' If you need a real agent across many channels, it's a top pick.",
   cta_url="https://botpress.com"),

 dict(slug="relevance-ai", name="Relevance AI", tagline="A no-code platform to build and deploy teams of AI agents for go-to-market and ops workflows.", category="Productivity",
   color1="#ff5a1f", color2="#cc3f0f", initials="RA", price="$19/mo", price_label="Starter", price_num="19",
   free_tier="Free trial", rating="4.3/5", rating_num="4.3", users="20K+ teams", founded="2020",
   headline="An AI team, not just a chatbot",
   intro="Relevance AI lets you assemble multiple specialized agents — researcher, writer, outreach, analyst — that hand work to each other to complete multi-step GTM and back-office jobs. Connect tools, set triggers, and watch a 'workforce' of agents run lead enrichment, content, and reporting without a human in the loop.",
   who_for="RevOps, marketing, and operations teams who want to automate workflows with a managed agent workforce.",
   features=[("👥","Multi-agent","Chain specialized agents into pipelines."),
             ("🔌","Tool integrations","CRM, email, scrapers, and APIs."),
             ("📊","Structured output","Tables and reports, not just chat."),
             ("🚀","Deploy","Trigger via schedule, API, or form.")],
   pros=["Powerful workflow automation","No-code agent building","Good for GTM use cases","Managed and scalable"],
   cons=["Pricing adds up at volume","Learning curve for complex flows","Less ideal for single tasks","Credit-based limits"],
   verdict="Relevance AI is where teams go when one chatbot isn't enough. If you're automating a whole process, the multi-agent model pays off fast.",
   cta_url="https://relevance.ai"),

 dict(slug="koboldcpp", name="KoboldCpp", tagline="A one-file, local LLM runner that serves GGUF models over a web UI and OpenAI-compatible API.", category="Productivity",
   color1="#6b7280", color2="#374151", initials="Kc", price="Free", price_label="Open source", price_num="0",
   free_tier="Always free", rating="4.6/5", rating_num="4.6", users="1M+ users", founded="2023",
   headline="Run frontier models on your own laptop",
   intro="KoboldCpp is the go-to single-binary app for running quantized LLMs (GGUF) on CPU, GPU, or both — with a friendly web UI, story-mode features, and an OpenAI-compatible endpoint so any tool can use your local model. It's the privacy-first runtime behind countless self-hosted setups in 2026.",
   who_for="Privacy-conscious users and hobbyists who want ChatGPT-grade chat entirely offline.",
   features=[("🔒","Fully local","No data leaves your machine."),
             ("📦","One binary","No install hell — download and run."),
             ("🔌","OpenAI API","Works with any compatible client."),
             ("🎛️","Flexible","CPU, CUDA, Metal, and Vulkan backends.")],
   pros=["Zero cost and private","Runs on modest hardware","Simple to launch","Broad model support"],
   cons=["Needs a decent machine for big models","No hosted SLA","UI is utilitarian","Manual model management"],
   verdict="KoboldCpp is the easiest on-ramp to private, local AI. Pair it with a good GGUF and you've got a personal assistant that never phones home.",
   cta_url="https://github.com/LostRuins/koboldcpp"),

 dict(slug="mintlify", name="Mintlify", tagline="The docs platform with AI that writes, translates, and keeps your documentation in sync with your code.", category="Productivity",
   color1="#6d28d9", color2="#4c1d95", initials="Ml", price="$0/mo", price_label="Free tier", price_num="0",
   free_tier="Free for OSS", rating="4.5/5", rating_num="4.5", users="20K+ teams", founded="2021",
   headline="Docs your users actually read",
   intro="Mintlify is a modern documentation platform built on MDX with a beautiful default design and AI features that draft docs from code, translate to 20+ languages, and flag stale pages. In 2026 its AI answers reader questions over your docs and auto-generates API references from OpenAPI specs.",
   who_for="Developer-tools companies and OSS projects who need polished docs without a design team.",
   features=[("✨","AI drafting","Generate and update docs from code."),
             ("🌍","Auto-translate","Ship 20+ language versions."),
             ("📚","API autogen","OpenAPI → live reference."),
             ("🤖","AI answers","Chat over your documentation.")],
   pros=["Beautiful out of the box","Strong AI assist","Great DX (MDX, Git)","Good free tier"],
   cons=["Customization has ceilings","Best on paid plans","Learning curve for advanced theming","Tied to their hosting"],
   verdict="Mintlify makes documentation a feature, not a chore. For dev tools, the AI drafting and translation alone justify the switch.",
   cta_url="https://mintlify.com"),

 dict(slug="deepinfra", name="DeepInfra", tagline="Serverless inference for 200+ open models — pay per token, no GPUs to manage.", category="Coding",
   color1="#111827", color2="#374151", initials="Di", price="Pay-per-token", price_label="Usage-based", price_num="0",
   free_tier="Free tier (limited)", rating="4.4/5", rating_num="4.4", users="100K+ devs", founded="2023",
   headline="Open models, zero ops",
   intro="DeepInfra hosts a huge catalog of open-weight models — Llama, Qwen, Mistral, SDXL, Whisper — behind a single OpenAI-compatible API. You get serverless inference that scales to zero and bills by the token, so you can swap models freely without renting GPUs.",
   who_for="Developers who want open-model flexibility and per-token pricing without running infrastructure.",
   features=[("🤖","200+ models","One endpoint for the whole open field."),
             ("🔌","OpenAI-compatible","Drop-in for existing clients."),
             ("💸","Per-token","No idle GPU cost."),
             ("⚡","Auto-scale","From zero to burst instantly.")],
   pros=["Massive model choice","Cheap at low volume","No infra to run","Easy model swapping"],
   cons=["Cold starts on idle","Less control than self-host","Quality varies by model","Support is community-leaning"],
   verdict="DeepInfra is the pragmatic home for open models in production. If you want flexibility without a GPU bill, it's a strong OpenRouter alternative.",
   cta_url="https://deepinfra.com"),

 dict(slug="softr", name="Softr", tagline="Turn Airtable, Notion, or any data source into client portals, marketplaces, and internal tools — no code.", category="Productivity",
   color1="#0ea5e9", color2="#0284c7", initials="St", price="$0/mo", price_label="Free tier", price_num="0",
   free_tier="Free tier", rating="4.4/5", rating_num="4.4", users="300K+ makers", founded="2019",
   headline="From spreadsheet to app in an afternoon",
   intro="Softr is the no-code builder that connects to your data (Airtable, Google Sheets, Supabase, SQL) and emits polished web apps — client portals, directories, marketplaces, and internal tools — with auth and permissions. In 2026 it adds AI blocks that generate pages and summarize records.",
   who_for="Consultants, agencies, and ops teams who need custom apps without hiring developers.",
   features=[("🧩","Data-connected","Bind to Airtable, Sheets, SQL, Supabase."),
             ("🔐","Auth & roles","Granular user permissions."),
             ("⚡","AI blocks","Generate UI and summarize data."),
             ("🎨","Templates","Portals, directories, CRMs out of the box.")],
   pros=["Fast to ship","Real permissions and auth","Great templates","No code required"],
   cons=["Bound to source data model","Design flexibility has limits","Pricier at scale","Not for heavy logic"],
   verdict="Softr is the fastest way to turn a spreadsheet into a real product. For client portals and internal tools, it's a no-brainer.",
   cta_url="https://www.softr.io"),

 dict(slug="glide", name="Glide", tagline="Build AI-powered apps from a spreadsheet that work on web and mobile — in minutes.", category="Productivity",
   color1="#6c5ce7", color2="#5b4bd6", initials="Gl", price="$0/mo", price_label="Free tier", price_num="0",
   free_tier="Free tier", rating="4.3/5", rating_num="4.3", users="500K+ makers", founded="2018",
   headline="Spreadsheets, but make them apps",
   intro="Glide turns Google Sheets and Glide Tables into polished, mobile-ready apps with a drag-and-drop builder. Its AI features auto-build layouts from your data, generate text, and classify inputs — so a non-developer can ship a field app, directory, or tracker the same day.",
   who_for="Small businesses and teams who need a custom mobile app without a dev project.",
   features=[("📱","Mobile-ready","Apps that feel native on phones."),
             ("🤖","AI builder","Generate screens from data."),
             ("📊","Sheet-powered","Driven by Sheets or Glide Tables."),
             ("🔗","Integrations","Slack, Zapier, BigQuery, and more.")],
   pros=["Very fast to build","Great on mobile","AI accelerates layout","Free to start"],
   cons=["Logic depth is limited","Pricing per app/user adds up","Design is template-ish","Not for complex backends"],
   verdict="Glide is the quickest route from 'idea' to 'app on everyone's phone.' Perfect for internal tools and small customer apps.",
   cta_url="https://www.glideapps.com"),

 dict(slug="baseten", name="Baseten", tagline="Deploy and scale ML models as production APIs with autoscaling, GPUs, and Python — built for AI startups.", category="Coding",
   color1="#f43f5e", color2="#be123c", initials="Bt", price="Pay-per-use", price_label="Usage-based", price_num="0",
   free_tier="Free dev tier", rating="4.5/5", rating_num="4.5", users="5K+ teams", founded="2021",
   headline="From model file to production API",
   intro="Baseten is the infrastructure layer for shipping ML — wrap any model in a Python class and get a autoscaling, GPU-backed API with observability. It's where many AI startups host proprietary models and fine-tunes, with scale-to-zero and per-request billing so dev is free and prod is efficient.",
   who_for="ML engineers and AI startups who need reliable, scalable model serving without Kubernetes.",
   features=[("🚀","Autoscale","Scale to zero and burst on demand."),
             ("🐍","Python-native","Deploy from a class, not YAML hell."),
             ("📈","Observability","Latency, logs, and usage built in."),
             ("💡","Chains","Compose models into workflows.")],
   pros=["Fast path to production","No K8s to manage","Good dev experience","Efficient scaling"],
   cons=["Costs rise with traffic","Less control than raw cloud","Best for model serving, not full apps","Some features enterprise-priced"],
   verdict="Baseten is the least-painful way to serve your own models in production. If you're past prototypes, it removes the infra tax.",
   cta_url="https://www.baseten.com"),

 dict(slug="hyperbolic", name="Hyperbolic", tagline="Open-source AI cloud with cheap GPU compute and inference for open models — chat, image, and code.", category="Coding",
   color1="#8b5cf6", color2="#6d28d9", initials="Hy", price="Pay-per-token", price_label="Usage-based", price_num="0",
   free_tier="Free credits", rating="4.3/5", rating_num="4.3", users="100K+ devs", founded="2023",
   headline="Open models without the markup",
   intro="Hyperbolic is an AI cloud built around open models and affordable GPUs. Beyond chat and image inference, it lets you rent on-demand GPUs for training and fine-tuning at competitive rates — a favorite for builders who want transparency and low cost.",
   who_for="Builders who want open-model inference plus on-demand GPUs without hyperscaler pricing.",
   features=[("🤖","Open models","LLM, image, and code endpoints."),
             ("🖥️","Cheap GPUs","On-demand compute for training."),
             ("💸","Low cost","Transparent, per-token and per-hour."),
     ("🔌","OpenAI-compatible","Easy drop-in.")],
   pros=["Strong price/performance","Open-model focus","GPU rental flexibility","Simple API"],
   cons=["Smaller ecosystem than giants","Younger platform","Support still growing","Some regions limited"],
   verdict="Hyperbolic is a cost-conscious home for open models and ad-hoc GPU work. Worth it if you're watching every token and GPU-hour.",
   cta_url="https://www.hyperbolic.xyz"),

 dict(slug="milvus", name="Milvus", tagline="The open-source vector database engineered for billion-scale embedding search and RAG.", category="Data",
   color1="#00b4d8", color2="#0077b6", initials="Mv", price="Free", price_label="Open source", price_num="0",
   free_tier="Self-host free", rating="4.5/5", rating_num="4.5", users="10K+ teams", founded="2019",
   headline="Vectors at planetary scale",
   intro="Milvus is the battle-tested open-source vector DB behind some of the largest embedding deployments on earth. It supports multiple index types, hybrid search, and ten-billion-scale collections, with a managed Zilliz Cloud for teams that don't want to run it themselves.",
   who_for="Enterprises and platforms building RAG and similarity search at very large scale.",
   features=[("🪐","Massive scale","Billions of vectors, distributed."),
             ("🔎","Hybrid search","Dense, sparse, and metadata filters."),
             ("🧩","Many indexes","Pick the right trade-off per use case."),
             ("☁️","Zilliz Cloud","Fully managed option.")],
   pros=["Proven at huge scale","Truly open source","Flexible indexing","Strong community"],
   cons=["Ops-heavy to self-host","Steeper learning curve","Smaller managed feature set than some","Tuning takes expertise"],
   verdict="When your vector needs outgrow a starter store, Milvus is the open-source standard. Self-host for control or use Zilliz for convenience.",
   cta_url="https://milvus.io"),

 dict(slug="voyage-ai", name="Voyage AI", tagline="Best-in-class embedding and reranking models, now part of MongoDB, purpose-built for RAG.", category="Data",
   color1="#10b981", color2="#047857", initials="Vo", price="$0.02/1M", price_label="Per tokens", price_num="0",
   free_tier="Free tier", rating="4.6/5", rating_num="4.6", users="50K+ devs", founded="2023",
   headline="Embeddings that just rank better",
   intro="Voyage AI builds domain-tuned embedding and reranking models that consistently top retrieval benchmarks — legal, code, finance, and multilingual. Acquired by MongoDB in 2024, it's the default upgrade teams make when generic embeddings aren't cutting it for RAG.",
   who_for="Developers who need top-tier retrieval quality for RAG and search.",
   features=[("🏆","SOTA embeddings","Domain-tuned for code, law, finance."),
             ("🔁","Rerankers","Big precision gains on top of vectors."),
             ("🌐","Multilingual","Strong across languages."),
             ("🔌","Simple API","Drop-in for any pipeline.")],
   pros=["Best-in-class retrieval","Domain-specific models","Easy to swap in","Backed by MongoDB"],
   cons=["Paid beyond free tier","Narrower than a full platform","Less known than giants","Best value at scale"],
   verdict="If retrieval quality is your bottleneck, Voyage's embeddings + reranker is the highest-leverage upgrade you can make. Pair with Qdrant or Pinecone.",
   cta_url="https://www.voyageai.com"),

 dict(slug="godmode", name="Godmode", tagline="An open-source web agent that autonomously researches and completes goals using multiple AI models.", category="Productivity",
   color1="#f59e0b", color2="#b45309", initials="Gm", price="Free", price_label="Open source", price_num="0",
   free_tier="Free (bring key)", rating="4.2/5", rating_num="4.2", users="200K+ users", founded="2023",
   headline="Point it at a goal, walk away",
   intro="Godmode is the open-source 'agentic' web app that takes a high-level objective and chains model calls, web browsing, and self-reflection to get there — adjusting its plan as it learns. Bring your own API key and let it research, draft, and iterate on open-ended tasks.",
   who_for="Researchers, founders, and tinkerers who want an autonomous assistant for messy, multi-step goals.",
   features=[("🎯","Goal-driven","Describe the outcome, not the steps."),
             ("🌐","Web browsing","Researches live as it works."),
             ("🔁","Self-reflect","Replans when stuck."),
             ("🔓","Open source","Bring your own model key.")],
   pros=["Great for open-ended tasks","Free and extensible","Fun, fast experimentation","Model-agnostic"],
   cons=["Can go off the rails","Needs your API key","Not reliable for critical work","UI is experimental"],
   verdict="Godmode is the sandbox for autonomous agents — impressive on research and brainstorming, best treated as a tireless intern, not a guarantee.",
   cta_url="https://godmode.space"),

 dict(slug="vercel", name="Vercel AI", tagline="The framework and edge platform for shipping AI apps — the AI SDK, streaming, and instant global deploys.", category="Coding",
   color1="#000000", color2="#333333", initials="Vc", price="Pay-as-you-go", price_label="Usage-based", price_num="0",
   free_tier="Free tier (Hobby)", rating="4.6/5", rating_num="4.6", users="5M+ devs", founded="2015",
   headline="Where AI front-ends get shipped",
   intro="Vercel's AI SDK is the de-facto toolkit for building LLM apps in TypeScript — unified provider access, streaming UI, tool calling, and structured output — deployable to Vercel's global edge in one command. It's how a huge share of AI chat and agent UIs ship in 2026.",
   who_for="Front-end and full-stack developers building production AI experiences in JS/TS.",
   features=[("🧩","AI SDK","One API across providers, with streaming."),
             ("⚡","Edge deploy","Global, instant rollouts."),
             ("🔧","Tool calling","Structured actions and functions."),
             ("🎨","UI kits","React hooks for chat and generative UI.")],
   pros=["Best-in-class DX for AI UI","Unified provider access","Instant global deploys","Huge ecosystem"],
   cons=["Tied to Next.js/Vercel-ish","Costs climb at scale","Opinionated conventions","Some features cloud-only"],
   verdict="If you're building an AI app in TypeScript, the Vercel AI SDK + platform is the path of least resistance. Streaming and tool calling just work.",
   cta_url="https://vercel.com"),
]

# =================== NEW COMPARE PAGES ===================
NEW_COMPARES = [
 dict(slug="gpt-5.1-vs-claude-opus-4", name_a="GPT-5.1", name_b="Claude Opus 4", color_a="#10a37f", color_b="#d97706",
   initials_a="51", initials_b="Op", url_a="https://chat.openai.com/?via=toolforge", url_b="https://claude.ai/?via=toolforge",
   desc_a="OpenAI's refined 2025 flagship with tighter reasoning", desc_b="Anthropic's most capable, long-context model",
   price_a="$20/mo Plus", price_b="$20/mo Pro", best_a="ecosystem, multimodal, agents", best_b="long docs, code review, nuance",
   verdict="Use <strong>GPT-5.1</strong> when you want the broadest ecosystem, best multimodal feel, and agentic reach. Use <strong>Claude Opus 4</strong> for the most careful long-context work — codebases, book-length analysis, and nuanced writing. They're the two frontrunners; pick by which strengths you lean on.",
   winner="Tie — GPT-5.1 for breadth, Opus 4 for depth"),

 dict(slug="gpt-5.1-vs-gemini-3", name_a="GPT-5.1", name_b="Gemini 3", color_a="#10a37f", color_b="#4285f4",
   initials_a="51", initials_b="G3", url_a="https://chat.openai.com/?via=toolforge", url_b="https://gemini.google.com",
   desc_a="OpenAI's refined 2025 flagship", desc_b="Google's multimodal model with the longest context",
   price_a="$20/mo Plus", price_b="Free / $20 AI Pro", best_a="ecosystem, agents, voice", best_b="huge context, live web, Workspace",
   verdict="Use <strong>GPT-5.1</strong> for the deepest tool ecosystem and agentic workflows. Use <strong>Gemini 3</strong> when you need a million-token context, live web grounding, or tight Google Workspace integration. Both are excellent; Gemini wins on context, GPT on ecosystem.",
   winner="GPT-5.1 for tools, Gemini 3 for context"),

 dict(slug="gpt-5.1-vs-grok-4", name_a="GPT-5.1", name_b="Grok 4", color_a="#10a37f", color_b="#1d1d1f",
   initials_a="51", initials_b="G4", url_a="https://chat.openai.com/?via=toolforge", url_b="https://x.ai",
   desc_a="OpenAI's refined 2025 flagship", desc_b="xAI's reasoning model wired into X",
   price_a="$20/mo Plus", price_b="$30/mo SuperGrok", best_a="ecosystem, multimodal, agents", best_b="real-time X data, math",
   verdict="Use <strong>GPT-5.1</strong> for the most polished general assistant with the widest tooling. Use <strong>Grok 4</strong> if you live on X and want real-time social data and strong math reasoning. GPT is the safer default; Grok is the X-native pick.",
   winner="GPT-5.1 general, Grok 4 for X users"),

 dict(slug="claude-4-5-vs-gpt-5.1", name_a="Claude 4.5", name_b="GPT-5.1", color_a="#d97706", color_b="#10a37f",
   initials_a="45", initials_b="51", url_a="https://claude.ai/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Anthropic's balanced coding-and-reasoning model", desc_b="OpenAI's refined 2025 flagship",
   price_a="$18/mo Pro", price_b="$20/mo Plus", best_a="coding, careful reasoning, writing", best_b="multimodal, agents, ecosystem",
   verdict="Use <strong>Claude 4.5</strong> for elite coding and careful, long-form work at a slightly lower price. Use <strong>GPT-5.1</strong> when you want the fullest feature set, voice, and third-party ecosystem. They're close; Claude edges coding, GPT edges breadth.",
   winner="Claude 4.5 coding, GPT-5.1 breadth"),

 dict(slug="gemini-3-vs-gpt-5.1", name_a="Gemini 3", name_b="GPT-5.1", color_a="#4285f4", color_b="#10a37f",
   initials_a="G3", initials_b="51", url_a="https://gemini.google.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Google's longest-context multimodal model", desc_b="OpenAI's refined 2025 flagship",
   price_a="Free / $20 AI Pro", price_b="$20/mo Plus", best_a="context, web grounding, Workspace", best_b="ecosystem, agents, voice",
   verdict="Use <strong>Gemini 3</strong> for million-token context, live web, and Workspace workflows. Use <strong>GPT-5.1</strong> for the deepest tool ecosystem and agentic tasks. Context crown goes to Gemini; ecosystem crown to GPT.",
   winner="Gemini 3 context, GPT-5.1 ecosystem"),

 dict(slug="imagen-vs-midjourney", name_a="Imagen", name_b="Midjourney", color_a="#4285f4", color_b="#1a1a1a",
   initials_a="Im", initials_b="Mj", url_a="https://deepmind.google/technologies/imagen", url_b="https://www.midjourney.com",
   desc_a="Google's photoreal text-to-image model", desc_b="The artist's favorite for stylized art",
   price_a="Free / $20 AI Pro", price_b="$10/mo Basic", best_a="photorealism, prompt accuracy, text", best_b="artistic style, community, coherence",
   verdict="Use <strong>Imagen</strong> for photoreal output, accurate text in images, and Google ecosystem integration. Use <strong>Midjourney</strong> for the most distinctive artistic style and a vibrant community. Imagen wins realism; Midjourney wins vibe.",
   winner="Imagen realism, Midjourney style"),

 dict(slug="imagen-vs-dalle", name_a="Imagen", name_b="DALL·E", color_a="#4285f4", color_b="#10a37f",
   initials_a="Im", initials_b="Dl", url_a="https://deepmind.google/technologies/imagen", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Google's photoreal text-to-image model", desc_b="OpenAI's built-in image generator",
   price_a="Free / $20 AI Pro", price_b="$20/mo Plus", best_a="photorealism, text accuracy", best_b="chat integration, ease of use",
   verdict="Use <strong>Imagen</strong> when you need the highest photorealism and correct text rendering. Use <strong>DALL·E</strong> when you want image generation baked into ChatGPT with zero friction. Imagen is sharper; DALL·E is more convenient.",
   winner="Imagen quality, DALL·E convenience"),

 dict(slug="imagen-vs-flux", name_a="Imagen", name_b="FLUX", color_a="#4285f4", color_b="#111827",
   initials_a="Im", initials_b="Fx", url_a="https://deepmind.google/technologies/imagen", url_b="https://blackforestlabs.ai",
   desc_a="Google's photoreal text-to-image model", desc_b="Black Forest Labs' open-weight image model",
   price_a="Free / $20 AI Pro", price_b="Free (open weights)", best_a="photorealism, Google ecosystem", best_b="open weights, control, speed",
   verdict="Use <strong>Imagen</strong> for the cleanest Google-integrated photorealism. Use <strong>FLUX</strong> when you want open weights, fine-grained control, and self-hosting. Imagen is polished; FLUX is flexible.",
   winner="Imagen polish, FLUX freedom"),

 dict(slug="imagen-vs-leonardo", name_a="Imagen", name_b="Leonardo", color_a="#4285f4", color_b="#7c3aed",
   initials_a="Im", initials_b="Le", url_a="https://deepmind.google/technologies/imagen", url_b="https://leonardo.ai",
   desc_a="Google's photoreal text-to-image model", desc_b="Game-art and asset-focused image suite",
   price_a="Free / $20 AI Pro", price_b="Free / $10/mo", best_a="photorealism, text accuracy", best_b="consistent assets, game art, presets",
   verdict="Use <strong>Imagen</strong> for one-off photoreal images with correct text. Use <strong>Leonardo</strong> when you need consistent characters, game assets, and a full production toolkit. Imagen for realism; Leonardo for pipelines.",
   winner="Imagen realism, Leonardo production"),

 dict(slug="veo-3-vs-sora", name_a="Veo 3", name_b="Sora", color_a="#4285f4", color_b="#10a37f",
   initials_a="V3", initials_b="So", url_a="https://gemini.google.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Google's cinematic, audio-aware video model", desc_b="OpenAI's text-to-video flagship",
   price_a="$20/mo Ultra", price_b="$20/mo Plus", best_a="cinematic quality, synced audio", best_b="prompt adherence, ecosystem",
   verdict="Use <strong>Veo 3</strong> for cinematic polish and native synced audio (dialogue, effects). Use <strong>Sora</strong> for tight ChatGPT integration and strong prompt adherence. Veo wins finished audio scenes; Sora wins workflow.",
   winner="Veo 3 cinematic audio, Sora workflow"),

 dict(slug="sora-vs-veo-3", name_a="Sora", name_b="Veo 3", color_a="#10a37f", color_b="#4285f4",
   initials_a="So", initials_b="V3", url_a="https://chat.openai.com/?via=toolforge", url_b="https://gemini.google.com",
   desc_a="OpenAI's text-to-video flagship", desc_b="Google's cinematic, audio-aware video model",
   price_a="$20/mo Plus", price_b="$20/mo Ultra", best_a="prompt adherence, ecosystem", best_b="cinematic quality, synced audio",
   verdict="Use <strong>Sora</strong> when you live in ChatGPT and want seamless prompt-to-video. Use <strong>Veo 3</strong> when you want the most cinematic output with real, synced sound. Sora for integration; Veo 3 for finished film.",
   winner="Sora integration, Veo 3 cinematics"),

 dict(slug="kling-vs-veo-3", name_a="Kling", name_b="Veo 3", color_a="#7c3aed", color_b="#4285f4",
   initials_a="Kl", initials_b="V3", url_a="https://klingai.com", url_b="https://gemini.google.com",
   desc_a="Kuaishou's motion-realism king", desc_b="Google's cinematic, audio-aware model",
   price_a="$10/mo Standard", price_b="$20/mo Ultra", best_a="realistic human motion, camera control", best_b="cinematic polish, synced audio",
   verdict="Use <strong>Kling</strong> for the most believable human movement and precise camera direction. Use <strong>Veo 3</strong> when you want cinematic scenes with native audio. Kling for motion; Veo 3 for finished, audible film.",
   winner="Kling motion, Veo 3 audio"),

 dict(slug="pika-vs-veo-3", name_a="Pika", name_b="Veo 3", color_a="#ec4899", color_b="#4285f4",
   initials_a="Pi", initials_b="V3", url_a="https://pika.art", url_b="https://gemini.google.com",
   desc_a="Playful, effects-rich video generator", desc_b="Google's cinematic, audio-aware model",
   price_a="$8/mo Standard", price_b="$20/mo Ultra", best_a="fun effects, quick clips, ideation", best_b="cinematic quality, synced audio",
   verdict="Use <strong>Pika</strong> for fast, playful clips and creative effects on a budget. Use <strong>Veo 3</strong> when you need cinematic, audio-synced output for real productions. Pika for play; Veo 3 for polish.",
   winner="Pika speed, Veo 3 cinematics"),

 dict(slug="recraft-vs-ideogram", name_a="Recraft", name_b="Ideogram", color_a="#7c3aed", color_b="#10a37f",
   initials_a="Rc", initials_b="Id", url_a="https://www.recraft.ai", url_b="https://ideogram.ai",
   desc_a="Vector + image model tuned for brand design", desc_b="Top text-in-image generator",
   price_a="Free / $12/mo", price_b="Free / $10/mo", best_a="brand kits, vectors, consistency", best_b="text rendering, posters",
   verdict="Use <strong>Recraft</strong> when you need on-brand vectors, stylesets, and design assets. Use <strong>Ideogram</strong> when accurate text-in-image and posters are the priority. Recraft for brand systems; Ideogram for typographic art.",
   winner="Recraft brand, Ideogram text"),

 dict(slug="gemini-3-pro-vs-gpt-5.1", name_a="Gemini 3 Pro", name_b="GPT-5.1", color_a="#4285f4", color_b="#10a37f",
   initials_a="G3", initials_b="51", url_a="https://gemini.google.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Google's top-tier reasoning model", desc_b="OpenAI's refined 2025 flagship",
   price_a="$20/mo AI Ultra", price_b="$20/mo Plus", best_a="context, web grounding, Workspace", best_b="ecosystem, agents, voice",
   verdict="Use <strong>Gemini 3 Pro</strong> for the largest context window and Google Workspace synergy. Use <strong>GPT-5.1</strong> for the deepest tool ecosystem and agentic reach. Both are flagship-grade; choose by ecosystem.",
   winner="Gemini 3 Pro context, GPT-5.1 ecosystem"),
]

# =================== NEW BLOG POSTS ===================
NEW_BLOGS = [
 dict(slug="best-ai-tools-for-course-creators-2026", title="The 9 Best AI Tools for Course Creators in 2026 (Build Faster, Teach Better)",
   meta="From scripting to slides to voiceover to student support — the AI stack that turns a course idea into a launched product in weeks, not months.",
   category="For Course Creators", read="3",
   lead="Course creators in 2026 aren't slowed by writer's block or editing marathons — they're using AI to script, produce, and support an entire course solo. We tested the stack that gets a course from idea to launch without a studio or a team.",
   verdict="Start with ChatGPT or Claude for scripting and outlines, use Gamma or Beautiful.ai for decks, and ElevenLabs or HeyGen for narration and on-camera presence. Add Opus Clip to chop long lessons into social promos and NotebookLM to give students a study buddy. The result: a polished course shipped in weeks.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="$20/mo", desc="Lesson scripts and outlines"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Long-form course writing"),
     dict(name="Gamma", url="https://gamma.app", color="#673ab7", initial="Ga", badge="$10/mo", desc="Slide decks in seconds"),
     dict(name="Beautiful.ai", url="https://www.beautiful.ai", color="#7c3aed", initial="Ba", badge="$12/mo", desc="Smart branded decks"),
     dict(name="ElevenLabs", url="https://elevenlabs.io", color="#111827", initial="El", badge="Free", desc="Natural voiceover at scale"),
     dict(name="HeyGen", url="https://www.heygen.com", color="#111827", initial="Hg", badge="$29/mo", desc="AI avatar lectures"),
     dict(name="Opus Clip", url="https://www.opus.pro", color="#ff5a1f", initial="Oc", badge="Free", desc="Clip lessons for social"),
     dict(name="NotebookLM", url="https://notebooklm.google.com", color="#4285f4", initial="Nl", badge="Free", desc="Student study companion"),
     dict(name=" descript ", url="https://www.descript.com/?via=toolforge", color="#6c5ce7", initial="De", badge="$12/mo", desc="Edit video by transcript"),
   ]),

 dict(slug="ai-tools-for-public-speakers-2026", title="AI Tools for Public Speakers in 2026: Write, Rehearse, and Own the Stage",
   meta="Speechwriting, teleprompter, coaching, and slide design — the AI toolkit that turns nervous speakers into polished presenters.",
   category="For Public Speakers", read="2",
   lead="The best speakers in 2026 treat AI like a personal speech coach: drafting the talk, timing the pauses, and flagging the filler words before they ever hit the stage. Here's the stack that helps you write tighter and deliver bolder.",
   verdict="Use ChatGPT or Claude to draft and restructure your talk, Yoodli or Orai to rehearse and kill filler words, and Gamma for slides that don't bore. Record a run-through in Descript to hear yourself and fix the rough spots. Confidence is a practice problem AI can help you solve.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Draft and restructure talks"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Narrative and pacing help"),
     dict(name="Yoodli", url="https://www.yoodli.ai", color="#0ea5e9", initial="Yo", badge="Free", desc="AI speech coaching"),
     dict(name="Orai", url="https://orai.com", color="#f43f5e", initial="Or", badge="Free", desc="Rehearse & cut fillers"),
     dict(name="Gamma", url="https://gamma.app", color="#673ab7", initial="Ga", badge="Free", desc="Compelling slide decks"),
     dict(name="Descript", url="https://www.descript.com/?via=toolforge", color="#6c5ce7", initial="De", badge="$12/mo", desc="Review your run-through"),
     dict(name="Speechify", url="https://speechify.com", color="#7c3aed", initial="Sp", badge="Free", desc="Hear your script aloud"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="Stage-friendly visuals"),
   ]),

 dict(slug="best-ai-tools-for-entrepreneurs-2026", title="The 10 Best AI Tools for Entrepreneurs in 2026 (Run Lean, Move Fast)",
   meta="From idea validation to branding to ops — the AI stack that lets a solo founder operate like a 10-person team.",
   category="For Entrepreneurs", read="3",
   lead="In 2026, a single founder with the right AI stack out-executes a small team. We pressure-tested the tools that handle the work entrepreneurs usually can't afford to delegate — so you can validate, build, and sell faster.",
   verdict="Use ChatGPT/Claude for strategy and copy, Perplexity for market research, and Gamma or Framer for pitches and landing pages. Lovable or Bolt ship the MVP, while Notion AI and Motion keep operations tidy. The goal: a lean founder who moves like a company.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="$20/mo", desc="Strategy, copy, brainstorming"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Deep planning & writing"),
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Cited market research"),
     dict(name="Gamma", url="https://gamma.app", color="#673ab7", initial="Ga", badge="$10/mo", desc="Pitch & deck builder"),
     dict(name="Framer", url="https://www.framer.com", color="#7c3aed", initial="Fr", badge="$20/mo", desc="Landing pages that convert"),
     dict(name="Lovable", url="https://lovable.dev", color="#111827", initial="Lo", badge="$20/mo", desc="Ship the MVP, no code"),
     dict(name="Notion AI", url="https://www.notion.so", color="#111827", initial="No", badge="Free", desc="Docs & ops hub"),
     dict(name="Motion", url="https://www.usemotion.com", color="#f59e0b", initial="Mo", badge="$19/mo", desc="Auto-plan your calendar"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="Brand & social visuals"),
     dict(name="Zapier", url="https://zapier.com", color="#ff4f00", initial="Za", badge="Free", desc="Glue your stack together"),
   ]),

 dict(slug="ai-tools-for-management-consultants-2026", title="AI Tools for Management Consultants in 2026: Research, Decks, and Diligence on Autopilot",
   meta="How top consultants use AI for market scans, synthesis, and slide production — without sacrificing rigor or confidentiality.",
   category="For Consultants", read="3",
   lead="Consultants live and die by the deck and the data room. In 2026 the best analysts use AI to compress the grunt work — scanning hundreds of sources, drafting the storyboard, and building the slides — while keeping the judgment human. Here's the stack that wins engagements.",
   verdict="Use Perplexity and Consensus for fast, cited research, Claude for synthesis of long documents, and Gamma or Beautiful.ai for decks. NotebookLM turns your client's data room into a queryable brain, and Julius or ChatGPT handle the numbers. Keep the recommendation human; let AI do the lifting.",
   tools=[
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Cited market scans"),
     dict(name="Consensus", url="https://consensus.app", color="#7c3aed", initial="Co", badge="Free", desc="Research-paper answers"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Synthesize long docs"),
     dict(name="Gamma", url="https://gamma.app", color="#673ab7", initial="Ga", badge="$10/mo", desc="Client-ready decks"),
     dict(name="Beautiful.ai", url="https://www.beautiful.ai", color="#7c3aed", initial="Ba", badge="$12/mo", desc="On-brand slides"),
     dict(name="NotebookLM", url="https://notebooklm.google.com", color="#4285f4", initial="Nl", badge="Free", desc="Query the data room"),
     dict(name="Julius", url="https://julius.ai", color="#10a37f", initial="Ju", badge="$20/mo", desc="Analyze datasets"),
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Models, frameworks, drafts"),
   ]),

 dict(slug="ai-tools-that-replaced-my-va-2026", title="The AI Tools That Replaced My Virtual Assistant in 2026",
   meta="Inbox, scheduling, CRM, and follow-ups — the automated stack that does what a VA used to, for a fraction of the cost.",
   category="Analysis", read="3",
   lead="Hiring a VA is the classic founder lever — but in 2026 a tight AI stack handles the repetitive 80%: triage, scheduling, reminders, and note-taking. I ran mine for a month and tracked what actually held up versus what still needs a human.",
   verdict="Use Superhuman or SaneBox for inbox sanity, Motion or Reclaim for scheduling, Fyxer or Lindy for email drafts and follow-ups, and Fathom or Fireflies for meeting notes. The human still owns relationships and judgment — but the administrative drone work is now essentially free.",
   tools=[
     dict(name="Superhuman", url="https://superhuman.com", color="#7c3aed", initial="Sh", badge="$30/mo", desc="Fast, AI-assisted inbox"),
     dict(name="SaneBox", url="https://www.sanebox.com", color="#0ea5e9", initial="Sb", badge="$7/mo", desc="Auto-triage email"),
     dict(name="Motion", url="https://www.usemotion.com", color="#f59e0b", initial="Mo", badge="$19/mo", desc="Auto-schedule your day"),
     dict(name="Reclaim", url="https://reclaim.ai", color="#10a37f", initial="Rc", badge="Free", desc="Smart calendar defense"),
     dict(name="Lindy", url="https://www.lindy.ai", color="#111827", initial="Li", badge="$30/mo", desc="AI executive assistant"),
     dict(name="Fyxer", url="https://fyxer.ai", color="#7c3aed", initial="Fx", badge="$12/mo", desc="Draft & triage email"),
     dict(name="Fathom", url="https://fathom.video", color="#0ea5e9", initial="Fa", badge="Free", desc="Meeting notes & action items"),
     dict(name="Fireflies", url="https://fireflies.ai", color="#7c3aed", initial="Ff", badge="$19/mo", desc="Auto-meeting summaries"),
   ]),

 dict(slug="ai-tools-for-data-journalists-2026", title="AI Tools for Data Journalists in 2026: Analyze, Visualize, and Verify Faster",
   meta="From cleaning datasets to spotting trends to fact-checking — the AI toolkit that helps reporters turn data into stories.",
   category="For Journalists", read="3",
   lead="Data journalism is where AI earns its keep: parsing messy spreadsheets, finding the anomaly, and checking a claim in seconds. In 2026 reporters use AI to do more analysis with less SQL — without surrendering the skepticism the job demands.",
   verdict="Use ChatGPT Advanced Data Analysis or Julius for cleaning and exploration, Perplexity for source-backed fact-checking, and Claude for summarizing long reports. Flourish or Canva handle charts, and Whisper transcribes interviews for search. Keep the byline human; let AI do the legwork.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="$20/mo", desc="Data analysis & charts"),
     dict(name="Julius", url="https://julius.ai", color="#10a37f", initial="Ju", badge="$20/mo", desc="Analyze datasets by chat"),
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Cited fact-checking"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Summarize long docs"),
     dict(name="Flourish", url="https://flourish.studio", color="#e11d48", initial="Fl", badge="Free", desc="Interactive charts"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="Publish-ready graphics"),
     dict(name="Whisper", url="https://openai.com/whisper", color="#10a37f", initial="Wh", badge="Free", desc="Transcribe interviews"),
     dict(name="Consensus", url="https://consensus.app", color="#7c3aed", initial="Co", badge="Free", desc="Verify with research"),
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
