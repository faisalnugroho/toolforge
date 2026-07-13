#!/usr/bin/env python3
"""ToolForge Sprint Batch — July 11 (batch B).
Reuses the exact templates from _sprint_gen.py (imported) and adds:
  - 10 new tool pages (model-family / non-Western LLMs)
  - 17 new compare pages (high-volume "X vs Y" long-tail)
  - 3 new blog posts (underserved long-tail angles)
Skips any slug that already exists, appends new URLs to sitemap.xml.
"""
import os, sys
sys.path.insert(0, os.path.expanduser('~/projects/toolforge'))
import _sprint_gen as sg   # importing runs its idempotent bottom block (writes nothing new)

BASE = sg.BASE
DOMAIN = sg.DOMAIN
TODAY = "2026-07-11"
sg.TODAY = TODAY   # patch module global so templates use the right date

tool_slugs = sg.existing_slugs('tools')
cmp_slugs  = sg.existing_slugs('compare')
blog_slugs = sg.existing_slugs('blog')

# =================== TOOLS ===================
TOOLS = [
 dict(slug="glm", name="GLM (Zhipu AI)", tagline="Zhipu AI's open-weight GLM family — a top Chinese LLM that rivals GPT-4-class models and runs on your own hardware.",
   category="Writing", color1="#4f46e5", color2="#7c3aed", initials="Gl", price="Free", price_label="open-weight", price_num="0",
   free_tier="Free tier + open weights", rating="4.6/5", rating_num="4.6", users="10M+ users", founded="2022",
   headline="China's strongest open LLM family",
   intro="GLM is the flagship model family from Zhipu AI (Zhipu Qingyan), one of China's 'AI Tigers.' The GLM-4.5 series matches many Western frontier models on reasoning and coding while shipping under open-weight licenses. You can chat in the cloud or self-host the weights — a rare combination of capability and control.",
   who_for="Bilingual (Chinese/English) users, developers who want open weights, and privacy-conscious teams that need to run an LLM on their own servers.",
   features=[("🌐","Bilingual by design","Native Chinese + English fluency — the strongest non-English LLM for most enterprise needs."),
             ("🔓","Open weights","GLM-4.5-Air and -Base are downloadable and self-hostable. No vendor lock-in."),
             ("🤔","Strong reasoning","Competes with GPT-class models on math, code, and agentic tasks."),
             ("🛠️","Tool use & agents","Built-in function calling and long context for agent workflows.")],
   pros=["Best open-weight option for Chinese-language work","Self-hostable for privacy and cost control","Competitive coding and reasoning","Free cloud tier"],
   cons=["Weaker than GPT-5/Claude 4 on hardest reasoning","Smaller Western ecosystem and plugins","English prose less polished than US models"],
   verdict="If you need a Chinese-capable LLM you can actually own and run yourself, <strong>GLM</strong> is the clear pick in 2026. For pure English creative writing, reach for Claude — but for bilingual, self-hosted power, GLM wins.",
   cta_url="https://www.zhipuai.cn"),

 dict(slug="sensechat", name="SenseChat (SenseTime)", tagline="SenseTime's SenseChat — a multi-modal Chinese LLM with deep roots in computer vision and real-world AI deployment.",
   category="Writing", color1="#0ea5e9", color2="#0369a1", initials="Sc", price="Free", price_label="freemium", price_num="0",
   free_tier="Free tier available", rating="4.4/5", rating_num="4.4", users="5M+ users", founded="2023",
   headline="The vision-native Chinese assistant",
   intro="SenseChat is SenseTime's conversational LLM, built on the same computer-vision heritage that made SenseTime a giant in facial and spatial recognition. It leans multi-modal — it reads images, charts, and documents — and is tuned hard for the Chinese market and enterprise deployment.",
   who_for="Chinese enterprises, educators, and users who want a vision-capable assistant that understands local context and documents.",
   features=[("👁️","Multi-modal","Accepts images, documents, and charts — not just text."),
             ("🏢","Enterprise-ready","Backed by SenseTime's deployment footprint in China."),
             ("📚","Document understanding","Strong at parsing long reports and forms."),
             ("🗣️","Bilingual","Solid Chinese fluency with workable English.")],
   pros=["Excellent document and image understanding","Strong enterprise/API presence in China","Free tier to start"],
   cons=["Less known outside China","English lags US frontier models","Smaller open-source community"],
   verdict="For document- and image-heavy Chinese-language work, <strong>SenseChat</strong> is a serious contender. Western users will still prefer ChatGPT for breadth — but SenseChat's vision chops are underrated.",
   cta_url="https://www.sensetime.com"),

 dict(slug="step", name="StepFun (Step)", tagline="StepFun's Step series — China's fast-rising image and video generation models with a consumer app to match.",
   category="Video", color1="#ec4899", color2="#db2777", initials="St", price="Free", price_label="freemium", price_num="0",
   free_tier="Free tier + credits", rating="4.5/5", rating_num="4.5", users="8M+ users", founded="2023",
   headline="China's generative video challenger",
   intro="StepFun builds the Step family of image and video models (Step-1X, Step-Video) and ships a slick consumer app. It's one of the few Chinese labs putting out genuinely competitive text-to-video next to Kling and Runway, with a focus on coherence and prompt adherence.",
   who_for="Creators and studios who want an alternative to Runway/Kling, especially with Chinese-language prompts and local deployment options.",
   features=[("🎬","Text-to-video","Generates coherent short clips from prompts."),
             ("🖼️","Image generation","Step-1X produces high-quality stills."),
             ("📱","Consumer app","Polished web/app experience, not just an API."),
             ("🌏","China-friendly","Strong Chinese prompt understanding and availability.")],
   pros=["Competitive with Kling/Runway on quality","Easy consumer app","Free tier to experiment"],
   cons=["Less mature ecosystem than Runway","English prompt tuning weaker","API access limited outside China"],
   verdict="If you're comparing generative video tools, <strong>StepFun</strong> deserves a spot next to Kling and Runway. It's not the default for Western studios yet — but the quality gap is closing fast.",
   cta_url="https://www.stepfun.com"),

 dict(slug="yi", name="Yi (01.AI)", tagline="01.AI's Yi model family — open-weight LLMs from Kai-Fu Lee's lab, built for enterprise and coding.",
   category="Writing", color1="#111827", color2="#374151", initials="Yi", price="Free", price_label="open-weight", price_num="0",
   free_tier="Open weights (Apache 2.0)", rating="4.5/5", rating_num="4.5", users="3M+ users", founded="2023",
   headline="The enterprise-open LLM from 01.AI",
   intro="Yi is the model family from 01.AI, founded by AI veteran Kai-Fu Lee. Released under permissive licenses, Yi models are tuned for long context, coding, and bilingual use — a favorite for companies that want to self-host without legal strings.",
   who_for="Engineering teams and enterprises that want open, license-friendly weights with strong coding and long-context behavior.",
   features=[("📜","Long context","200K-token context on larger variants."),
             ("💻","Coding focus","Solid code generation and explanation."),
             ("⚖️","Permissive license","Apache 2.0 — safe for commercial self-hosting."),
             ("🌐","Bilingual","Strong Chinese + English.")],
   pros=["Truly open, commercial-friendly license","Great long-context handling","Self-hostable"],
   cons=["Smaller than GLM/Qwen in China","English creative writing average","Less frequent releases lately"],
   verdict="For a license-clean, self-hostable LLM with long context, <strong>Yi</strong> is a strong, underrated pick. Choose Qwen or GLM if you want the biggest open ecosystem.",
   cta_url="https://01.ai"),

 dict(slug="o1", name="OpenAI o1", tagline="OpenAI's first reasoning model — it 'thinks' before answering, crushing math, science, and code benchmarks.",
   category="Writing", color1="#10a37f", color2="#0e8c6e", initials="o1", price="$20/mo", price_label="ChatGPT Plus", price_num="20",
   free_tier="Limited in free tier", rating="4.8/5", rating_num="4.8", users="100M+ users", founded="2024",
   headline="The model that reasons step by step",
   intro="o1 was OpenAI's breakthrough 'deliberative' model. Instead of blurting the first token, it spends compute internally reasoning through the problem — which is why it leaps ahead on competition math, PhD-level science, and tricky coding. It's slower, but when correctness matters, it shows.",
   who_for="Researchers, competitive programmers, and anyone solving hard quantitative or logical problems where a wrong answer is costly.",
   features=[("🧠","Deliberative reasoning","Internal chain-of-thought before responding."),
             ("🧮","Math & science","Top scores on Olympiad and PhD-level benchmarks."),
             ("💻","Hard coding","Excellent on complex algorithmic problems."),
             ("⏱️","Slower by design","Traders time for accuracy — not chat speed.")],
   pros=["Best-in-class on hard reasoning tasks","Strong coding and proofs","Backed into ChatGPT/API"],
   cons=["Slower responses than GPT-4o","More expensive per token","Overkill for casual chat"],
   verdict="When the problem is hard and wrong answers are expensive, <strong>o1</strong> earns its keep. For everyday chat, GPT-4o or o4-mini is faster and cheaper.",
   cta_url="https://chat.openai.com/?via=toolforge"),

 dict(slug="o4-mini", name="OpenAI o4-mini", tagline="OpenAI's small-but-mighty reasoning model — o1-class thinking at a fraction of the cost and latency.",
   category="Writing", color1="#10a37f", color2="#0e8c6e", initials="o4", price="$20/mo", price_label="ChatGPT Plus", price_num="20",
   free_tier="Available in free tier", rating="4.7/5", rating_num="4.7", users="100M+ users", founded="2025",
   headline="Reasoning that fits in your latency budget",
   intro="o4-mini is OpenAI's compact reasoning model: it keeps most of o1's deliberative strength while replying far faster and cheaper. It's the default 'smart but quick' option for coding assist, math help, and agent loops where you can't wait.",
   who_for="Developers and students who want reasoning quality without o1's latency and price — ideal for agentic workflows and high-volume calls.",
   features=[("⚡","Fast reasoning","Near-o1 quality at a fraction of latency."),
             ("💸","Cost-efficient","Much cheaper per token than full o1."),
             ("🤖","Agent-friendly","Great for multi-step tool-using loops."),
             ("💻","Coding","Strong on real-world code tasks.")],
   pros=["Best price/performance reasoning model","Fast enough for agents","Free-tier accessible"],
   cons=["Trails o1/o3 on the hardest problems","Still slower than GPT-4o for chat"],
   verdict="For almost everything except the very hardest reasoning, <strong>o4-mini</strong> is the sweet spot — cheap, fast, and genuinely smart. Pair with o3 when you need maximum depth.",
   cta_url="https://chat.openai.com/?via=toolforge"),

 dict(slug="claude-haiku", name="Claude Haiku", tagline="Anthropic's fastest, cheapest Claude — near-instant responses with surprising reasoning for the price.",
   category="Writing", color1="#d97706", color2="#b45309", initials="Hk", price="Free", price_label="freemium", price_num="0",
   free_tier="Free tier available", rating="4.6/5", rating_num="4.6", users="50M+ users", founded="2024",
   headline="The speed demon of the Claude family",
   intro="Claude Haiku is Anthropic's lightweight model: it returns answers in a blink and costs pennies, while still handling classification, extraction, and light reasoning better than models twice its size. Haiku 3.5 / 4-class variants are the workhorse for high-volume, latency-sensitive jobs.",
   who_for="Builders who need a cheap, instant model for classification, routing, summarization, and high-volume chat — where cost and speed beat max intelligence.",
   features=[("⚡","Near-instant","Lowest latency in the Claude family."),
             ("💸","Cheapest Claude","Fraction of the cost of Opus/Sonnet."),
             ("📑","Extraction & classify","Excellent at structured output at scale."),
             ("🔒","Safe & steerable","Anthropic's guardrails included.")],
   pros=["Best latency/price in Claude lineup","Strong for routing and extraction","Free tier to start"],
   cons=["Not for deepest reasoning","Weaker long-form than Sonnet/Opus"],
   verdict="Use <strong>Claude Haiku</strong> as your default for fast, cheap, high-volume tasks — routing, tagging, summaries. Step up to Sonnet or Opus when the task needs real depth.",
   cta_url="https://claude.ai/?via=toolforge"),

 dict(slug="claude-4", name="Claude 4 (Opus & Sonnet)", tagline="Anthropic's 4th-generation Claude — top-tier coding and agentic reasoning with a 1M-token context.",
   category="Writing", color1="#d97706", color2="#b45309", initials="C4", price="$20/mo", price_label="Claude Pro", price_num="20",
   free_tier="Sonnet in free tier", rating="4.9/5", rating_num="4.9", users="50M+ users", founded="2025",
   headline="The agentic coding flagship",
   intro="Claude 4 (Opus 4 and Sonnet 4) is Anthropic's most capable generation — built for long-running agentic work, software engineering, and massive context. It holds a 1M-token window, follows complex multi-step instruction, and tops coding leaderboards alongside GPT-5-class models.",
   who_for="Engineers, researchers, and knowledge workers who need frontier-level reasoning, coding, and document analysis in one model.",
   features=[("🧠","Frontier reasoning","Competes with GPT-5 on hard tasks."),
             ("💻","Agentic coding","Best-in-class on software-engineering benchmarks."),
             ("📚","1M context","Ingest entire codebases or book-length docs."),
             ("🎯","Instruction-following","Handles nuance and long briefs.")],
   pros=["Elite coding and reasoning","Huge context window","Strong safety/steerability"],
   cons=["Opus is pricey at scale","Still rate-limited on free tier"],
   verdict="If you do serious work — code, research, long documents — <strong>Claude 4</strong> is a co-leader with GPT-5. Pick it over GPT when you value nuanced writing and agentic coding.",
   cta_url="https://claude.ai/?via=toolforge"),

 dict(slug="gemini-flash", name="Gemini Flash", tagline="Google's fast, cheap Gemini tier — multimodal and blazing quick, perfect for high-volume and on-device use.",
   category="Writing", color1="#4285f4", color2="#1a73e8", initials="Gf", price="Free", price_label="freemium", price_num="0",
   free_tier="Generous free tier", rating="4.7/5", rating_num="4.7", users="200M+ users", founded="2024",
   headline="Speed and multimodality on a budget",
   intro="Gemini Flash is the lightweight tier of Google's Gemini family — and it's the secret weapon for production. It's multimodal (text, image, audio, video), extremely fast, and cheap enough to call millions of times. Flash 2.5/3-class versions match much larger models on many tasks.",
   who_for="Developers shipping high-volume apps, and anyone who wants a free, multimodal model with a massive context window.",
   features=[("⚡","Blazing fast","Lowest latency in the Gemini line."),
             ("🌈","Multimodal","Native image/audio/video understanding."),
             ("🪟","Long context","1M-token window on Flash tiers."),
             ("💸","Cheap at scale","Free tier + rock-bottom API pricing.")],
   pros=["Best value multimodal model","Massive context","Great free tier"],
   cons=["Trails Gemini Pro / Opus on hardest reasoning","English prose less characterful"],
   verdict="For production and high-volume use, <strong>Gemini Flash</strong> is the pragmatic winner — fast, cheap, multimodal. Reach for Pro when you need maximum intelligence.",
   cta_url="https://gemini.google.com"),

 dict(slug="command-r", name="Cohere Command R", tagline="Cohere's Retrieval-Augmented Generation model — built for enterprise search, RAG, and tool use.",
   category="Writing", color1="#39594d", color2="#22d3a8", initials="Cr", price="Free", price_label="freemium", price_num="0",
   free_tier="Free tier + open weights", rating="4.4/5", rating_num="4.4", users="1M+ users", founded="2023",
   headline="The RAG-and-tools workhorse",
   intro="Command R and Command R+ are Cohere's models purpose-built for enterprises: they excel at retrieval-augmented generation, citation, and tool use. Cohere ships them with a focus on grounded, sourced answers and easy private deployment — exactly what banks and Fortune 500s want.",
   who_for="Enterprise teams building RAG search, grounded Q&A, and agents where citations and data privacy matter more than chit-chat.",
   features=[("🔎","RAG-native","Designed for retrieval-augmented answers."),
             ("📎","Citations","Returns grounded, sourced responses."),
             ("🛠️","Tool use","First-class function calling."),
             ("🔒","Private deploy","On-prem / VPC options for enterprises.")],
   pros=["Best-in-class for grounded enterprise RAG","Strong citations","Deployable privately"],
   cons=["Less known for creative writing","Smaller consumer ecosystem"],
   verdict="If your use case is enterprise search and grounded Q&A, <strong>Command R</strong> is purpose-built and beats general chat models. For open-ended creativity, look elsewhere.",
   cta_url="https://cohere.com"),
]

# =================== COMPARES ===================
COMPARES = [
 dict(slug="glm-vs-chatgpt", name_a="GLM", name_b="ChatGPT", color_a="#4f46e5", color_b="#10a37f",
   initials_a="Gl", initials_b="Ch", url_a="https://www.zhipuai.cn", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="China's top open-weight LLM", desc_b="The world's most-used AI assistant",
   price_a="Free / open weights", price_b="$20/mo Plus", best_a="bilingual + self-hosted", best_b="breadth, plugins, English",
   verdict="Use <strong>GLM</strong> if you need a Chinese-capable, self-hostable open model you can own. Use <strong>ChatGPT</strong> for the broadest ecosystem, plugins, and polished English. GLM wins on control; ChatGPT wins on convenience.",
   winner="ChatGPT — on ecosystem, GLM on control"),

 dict(slug="yi-vs-llama", name_a="Yi", name_b="Llama", color_a="#111827", color_b="#0a72ef",
   initials_a="Yi", initials_b="La", url_a="https://01.ai", url_b="https://www.llama.com",
   desc_a="01.AI's Apache-licensed LLM", desc_b="Meta's open foundation model",
   price_a="Free (Apache 2.0)", price_b="Free (open)", best_a="long context, coding", best_b="huge ecosystem, community",
   verdict="<strong>Yi</strong> offers clean licensing and strong long-context coding; <strong>Llama</strong> has the largest open ecosystem, fine-tunes, and tooling. Pick Yi for a focused self-host, Llama for community and variety.",
   winner="Llama — on ecosystem, Yi on licensing clarity"),

 dict(slug="o1-vs-o3", name_a="o1", name_b="o3", color_a="#10a37f", color_b="#0e8c6e",
   initials_a="o1", initials_b="o3", url_a="https://chat.openai.com/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="OpenAI's first reasoning model", desc_b="OpenAI's next-gen reasoning flagship",
   price_a="$20/mo Plus", price_b="$20/mo Plus", best_a="hard math, proofs", best_b="deepest reasoning, agents",
   verdict="<strong>o3</strong> is the newer, deeper reasoning model and beats o1 on the hardest benchmarks. Use o1 if you're already tuned to it; otherwise o3 is the better buy for maximum reasoning power.",
   winner="o3 — deeper reasoning"),

 dict(slug="o1-vs-o4-mini", name_a="o1", name_b="o4-mini", color_a="#10a37f", color_b="#0ea5e9",
   initials_a="o1", initials_b="o4", url_a="https://chat.openai.com/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Deep, slow, accurate reasoning", desc_b="Fast, cheap reasoning",
   price_a="$20/mo Plus", price_b="$20/mo Plus", best_a="hardest problems", best_b="speed + cost at scale",
   verdict="Use <strong>o1</strong> only when the problem is genuinely hard and wrong answers are costly. For everything else, <strong>o4-mini</strong> is faster, cheaper, and nearly as sharp.",
   winner="o4-mini — best everyday value"),

 dict(slug="claude-haiku-vs-gpt-4o-mini", name_a="Claude Haiku", name_b="GPT-4o mini", color_a="#d97706", color_b="#10a37f",
   initials_a="Hk", initials_b="4m", url_a="https://claude.ai/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Anthropic's fastest Claude", desc_b="OpenAI's cheapest GPT",
   price_a="Free / low cost", price_b="Free / low cost", best_a="routing, extraction", best_b="broad tasks, ecosystem",
   verdict="Both are cheap, fast small models. <strong>Claude Haiku</strong> edges extraction and safety; <strong>GPT-4o mini</strong> wins on ecosystem and raw availability. Either is a great default for high-volume work.",
   winner="Tie — Haiku on extraction, 4o mini on reach"),

 dict(slug="gemini-flash-vs-gpt-4o-mini", name_a="Gemini Flash", name_b="GPT-4o mini", color_a="#4285f4", color_b="#10a37f",
   initials_a="Gf", initials_b="4m", url_a="https://gemini.google.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Fast multimodal Google model", desc_b="OpenAI's cheap multimodal model",
   price_a="Free / cheap", price_b="Free / cheap", best_a="multimodal, long context", best_b="ecosystem, speed",
   verdict="<strong>Gemini Flash</strong> brings native multimodality and a 1M-token window; <strong>GPT-4o mini</strong> brings the deepest OpenAI tooling. For vision + long docs, Flash wins; for pure text at scale, either is fine.",
   winner="Gemini Flash — on multimodal + context"),

 dict(slug="gemini-pro-vs-gpt-4", name_a="Gemini Pro", name_b="GPT-4", color_a="#4285f4", color_b="#10a37f",
   initials_a="Gp", initials_b="G4", url_a="https://gemini.google.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Google's flagship LLM", desc_b="OpenAI's workhorse flagship",
   price_a="Free / paid", price_b="$20/mo Plus", best_a="multimodal, long context", best_b="ecosystem, reliability",
   verdict="<strong>Gemini Pro</strong> leads on multimodal input and context length; <strong>GPT-4</strong>-class models lead on ecosystem maturity and tooling. New work favors Gemini Pro; legacy integrations favor GPT.",
   winner="Tie — Gemini on modality, GPT on ecosystem"),

 dict(slug="gemini-pro-vs-claude", name_a="Gemini Pro", name_b="Claude", color_a="#4285f4", color_b="#d97706",
   initials_a="Gp", initials_b="Cl", url_a="https://gemini.google.com", url_b="https://claude.ai/?via=toolforge",
   desc_a="Google's flagship LLM", desc_b="Anthropic's helpful, honest model",
   price_a="Free / paid", price_b="$20/mo Pro", best_a="multimodal, docs", best_b="writing, coding, safety",
   verdict="<strong>Gemini Pro</strong> for multimodal and Google-Workspace integration; <strong>Claude</strong> for nuanced writing, coding, and careful reasoning. Pick by workflow, not by spec sheet.",
   winner="Tie — Gemini on modality, Claude on writing"),

 dict(slug="command-r-vs-gpt-4", name_a="Command R", name_b="GPT-4", color_a="#39594d", color_b="#10a37f",
   initials_a="Cr", initials_b="G4", url_a="https://cohere.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Enterprise RAG + tools model", desc_b="General frontier assistant",
   price_a="Free / paid", price_b="$20/mo Plus", best_a="grounded search, citations", best_b="general capability",
   verdict="<strong>Command R</strong> is the specialist for grounded enterprise RAG with citations; <strong>GPT-4</strong> is the generalist. For search-and-answer over your docs, Command R; for everything else, GPT.",
   winner="Command R — for RAG, GPT-4 for general"),

 dict(slug="sensechat-vs-chatgpt", name_a="SenseChat", name_b="ChatGPT", color_a="#0ea5e9", color_b="#10a37f",
   initials_a="Sc", initials_b="Ch", url_a="https://www.sensetime.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="SenseTime's vision-native LLM", desc_b="The global default assistant",
   price_a="Free", price_b="$20/mo Plus", best_a="docs + images, Chinese", best_b="breadth, plugins",
   verdict="<strong>SenseChat</strong> shines on document and image understanding in Chinese; <strong>ChatGPT</strong> remains the broader, more polished global tool. Use SenseChat for vision-heavy Chinese enterprise work.",
   winner="ChatGPT — on breadth, SenseChat on vision"),

 dict(slug="step-vs-kling", name_a="StepFun", name_b="Kling", color_a="#ec4899", color_b="#7c3aed",
   initials_a="St", initials_b="Kl", url_a="https://www.stepfun.com", url_b="https://klingai.com",
   desc_a="China's rising video/image lab", desc_b="Top Chinese text-to-video model",
   price_a="Free / credits", price_b="Free / $10mo", best_a="coherent short clips", best_b="cinematic, realistic motion",
   verdict="<strong>Kling</strong> is the more established, higher-fidelity video model; <strong>StepFun</strong> is the fast-rising challenger with a polished app. For now Kling leads on realism; Step is worth watching (and trying) free.",
   winner="Kling — on fidelity, Step on momentum"),

 dict(slug="mixtral-vs-llama", name_a="Mixtral", name_b="Llama", color_a="#ff7000", color_b="#0a72ef",
   initials_a="Mx", initials_b="La", url_a="https://mistral.ai", url_b="https://www.llama.com",
   desc_a="Mistral's sparse mixture-of-experts", desc_b="Meta's open foundation model",
   price_a="Free (open)", price_b="Free (open)", best_a="efficient, fast inference", best_b="ecosystem, variety",
   verdict="<strong>Mixtral</strong> is famously efficient — MoE means cheap, fast inference at quality near much larger models. <strong>Llama</strong> has the bigger community and more sizes. Pick Mixtral for cost-efficient serving, Llama for choice.",
   winner="Tie — Mixtral on efficiency, Llama on ecosystem"),

 dict(slug="doubao-vs-chatgpt", name_a="Doubao", name_b="ChatGPT", color_a="#3b82f6", color_b="#10a37f",
   initials_a="Db", initials_b="Ch", url_a="https://www.doubao.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="ByteDance's consumer AI", desc_b="The global default assistant",
   price_a="Free", price_b="$20/mo Plus", best_a="Chinese users, TikTok ecosystem", best_b="breadth, plugins",
   verdict="<strong>Doubao</strong> is ByteDance's fast-growing consumer assistant, huge in China and tied to its content ecosystem. <strong>ChatGPT</strong> remains the broader global tool. Doubao wins for Chinese consumers; ChatGPT for everyone else.",
   winner="ChatGPT — on breadth, Doubao on China"),

 dict(slug="ernie-vs-chatgpt", name_a="Ernie", name_b="ChatGPT", color_a="#2932e1", color_b="#10a37f",
   initials_a="Er", initials_b="Ch", url_a="https://yiyan.baidu.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Baidu's knowledge-grounded LLM", desc_b="The global default assistant",
   price_a="Free", price_b="$20/mo Plus", best_a="Chinese search + knowledge", best_b="breadth, plugins",
   verdict="<strong>Ernie</strong> (Wenxin Yiyan) rides Baidu's search knowledge and dominates Chinese web Q&A. <strong>ChatGPT</strong> leads globally on capability and tooling. Ernie for Chinese web grounding; ChatGPT for general power.",
   winner="ChatGPT — on capability, Ernie on Chinese web"),

 dict(slug="hunyuan-vs-chatgpt", name_a="Hunyuan", name_b="ChatGPT", color_a="#07c160", color_b="#10a37f",
   initials_a="Hy", initials_b="Ch", url_a="https://hunyuan.tencent.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Tencent's multimodal LLM", desc_b="The global default assistant",
   price_a="Free", price_b="$20/mo Plus", best_a="Chinese + WeChat ecosystem", best_b="breadth, plugins",
   verdict="<strong>Hunyuan</strong> is Tencent's model, deep in the WeChat/China ecosystem and strong multimodally. <strong>ChatGPT</strong> is the broader global standard. Hunyuan for Tencent-ecosystem users; ChatGPT for general use.",
   winner="ChatGPT — on breadth, Hunyuan on ecosystem"),

 dict(slug="minimax-vs-elevenlabs", name_a="MiniMax", name_b="ElevenLabs", color_a="#7c3aed", color_b="#111827",
   initials_a="Mm", initials_b="El", url_a="https://www.minimax.io", url_b="https://elevenlabs.io",
   desc_a="Chinese all-in-one AI (voice, video, LLM)", desc_b="The voice-cloning gold standard",
   price_a="Free / low", price_b="$5/mo", best_a="cheap TTS + video", best_b="voice quality, cloning",
   verdict="<strong>ElevenLabs</strong> remains the quality leader for voice cloning and expressive TTS. <strong>MiniMax</strong> is the cheaper, broader Chinese alternative (voice + video + LLM). Pick ElevenLabs for fidelity, MiniMax for price and range.",
   winner="ElevenLabs — on voice quality"),

 dict(slug="phi-3-vs-mistral", name_a="Phi-3", name_b="Mistral", color_a="#0078d4", color_b="#ff7000",
   initials_a="P3", initials_b="Mi", url_a="https://azure.microsoft.com", url_b="https://mistral.ai",
   desc_a="Microsoft's tiny, smart SLM", desc_b="Mistral's efficient open models",
   price_a="Free (open)", price_b="Free (open)", best_a="edge, on-device, cheap", best_b="balanced open capability",
   verdict="<strong>Phi-3</strong> is a small language model that punches above its weight — perfect for edge and on-device. <strong>Mistral</strong> (7B/8x7B) gives more headroom for general tasks. Phi-3 for tiny deployments, Mistral for general open use.",
   winner="Tie — Phi-3 on edge, Mistral on capability"),

 dict(slug="o3-vs-o4-mini", name_a="o3", name_b="o4-mini", color_a="#0e8c6e", color_b="#0ea5e9",
   initials_a="o3", initials_b="o4", url_a="https://chat.openai.com/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Deepest OpenAI reasoning", desc_b="Fast, cheap reasoning",
   price_a="$20/mo Plus", price_b="$20/mo Plus", best_a="hardest problems", best_b="everyday speed + cost",
   verdict="<strong>o3</strong> is for the hardest reasoning where accuracy is everything; <strong>o4-mini</strong> handles the daily load fast and cheap. Most users should default to o4-mini and escalate to o3 only when stuck.",
   winner="o4-mini — everyday, o3 for depth"),
]

# =================== BLOGS ===================
BLOGS = [
 dict(slug="best-ai-tools-for-language-learners-2026", title="The 8 Best AI Tools for Language Learners in 2026 (Actually Speak Faster)",
   meta="From conversational partners to instant grammar fixes to native-content translation — the AI stack that gets you fluent faster.",
   category="For Learners", read="3",
   lead="Language learning used to mean rigid textbooks and overpriced tutors. In 2026, AI gives you a patient conversation partner, an instant editor, and a translator that actually gets context — available 24/7 at near-zero cost.",
   verdict="Use ChatGPT or Gemini as your conversation partner, add Speechling or Elsa for pronunciation, and DeepL or Qwen for reading native content. The combo slashes the time from 'studying' to 'speaking.'",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Role-play conversations in any language"),
     dict(name="Gemini", url="https://gemini.google.com", color="#4285f4", initial="Ge", badge="Free", desc="Explain grammar and culture instantly"),
     dict(name="DeepL", url="https://www.deepl.com", color="#1a1a1a", initial="Dl", badge="Free", desc="Natural, context-aware translation"),
     dict(name="Qwen", url="https://chat.qwen.ai", color="#615ced", initial="Qw", badge="Free", desc="Excellent for Asian languages"),
     dict(name="ELSA Speak", url="https://elsaspeak.com", color="#ff6b35", initial="Es", badge="Free", desc="AI pronunciation coach"),
     dict(name="Speechling", url="https://speechling.com", color="#7c3aed", initial="Sl", badge="Free", desc="Coach feedback on your speaking"),
     dict(name="Papago", url="https://papago.naver.com", color="#19b5b1", initial="Pa", badge="Free", desc="Best for KR/JP/ZH learners"),
     dict(name="LingQ", url="https://www.lingq.com", color="#16a34a", initial="Lq", badge="Free", desc="Learn from real native content"),
   ]),

 dict(slug="best-ai-tools-for-accessibility-2026", title="The 7 Best AI Accessibility Tools in 2026 (Tech That Removes Barriers)",
   meta="AI is quietly the best accessibility win in decades — live captions, screen-reader descriptions, and voice control for everyone.",
   category="For Everyone", read="3",
   lead="For people who are blind, Deaf, or have motor or reading differences, 2026's AI tools remove barriers that existed for generations. Live transcription, image description, and voice navigation are now free and shockingly good.",
   verdict="Start with Be My Eyes + GPT for visual description, Otter or Live Transcript for captions, and Voice Control / Whisper for hands-free input. Most of these are free — accessibility shouldn't cost extra.",
   tools=[
     dict(name="Be My Eyes", url="https://www.bemyeyes.com", color="#ff5a5f", initial="Be", badge="Free", desc="Live volunteers + AI describe the world"),
     dict(name="Otter.ai", url="https://otter.ai", color="#111827", initial="Ot", badge="Free", desc="Live captions for meetings & talks"),
     dict(name="Whisper", url="https://openai.com/research/whisper", color="#10a37f", initial="Wh", badge="Free", desc="Open speech-to-text engine"),
     dict(name="Seeing AI", url="https://www.seeingai.com", color="#0078d4", initial="Sa", badge="Free", desc="Microsoft's object & text reader"),
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Describe images via upload"),
     dict(name="Google Live Transcribe", url="https://play.google.com", color="#4285f4", initial="Lt", badge="Free", desc="Real-time speech to text"),
     dict(name="Speechify", url="https://speechify.com", color="#7c3aed", initial="Sf", badge="Free", desc="Text-to-speech for any doc"),
   ]),

 dict(slug="best-ai-tools-for-researchers-2026", title="The 9 Best AI Tools for Researchers in 2026 (From Lit Review to Write-Up)",
   meta="Literature reviews in minutes, cited search, and a writing partner that knows your field — the research stack that actually saves time.",
   category="For Researchers", read="3",
   lead="Research is mostly reading, organizing, and writing — exactly what 2026 AI does well. The right stack turns a two-week lit review into an afternoon and keeps your citations honest.",
   verdict="Use Elicit or Consensus for paper discovery, Perplexity for cited search, NotebookLM to synthesize your PDFs, and Claude/GPT for drafting. You'll publish faster without cutting corners.",
   tools=[
     dict(name="Elicit", url="https://elicit.com", color="#0ea5e9", initial="El", badge="Free", desc="AI literature review from queries"),
     dict(name="Consensus", url="https://consensus.app", color="#7c3aed", initial="Co", badge="Free", desc="Find what the research says"),
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Cited, sourced answers"),
     dict(name="NotebookLM", url="https://notebooklm.google.com", color="#4285f4", initial="Nl", badge="Free", desc="Synthesize your own PDFs"),
     dict(name="Semantic Scholar", url="https://www.semanticscholar.org", color="#1a1a1a", initial="Ss", badge="Free", desc="AI-powered paper search"),
     dict(name="Scite", url="https://scite.ai", color="#0ea5e9", initial="Sc", badge="Free", desc="Smart citations & context"),
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Draft & brainstorm with sources"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Long-doc analysis & writing"),
     dict(name="Zotero + AI", url="https://www.zotero.org", color="#cc2936", initial="Zo", badge="Free", desc="Reference manager with AI helpers"),
   ]),
]

# =================== WRITE ===================
new_urls = []
created = {"tools":0, "compare":0, "blog":0}

for t in TOOLS:
    if t['slug'] in tool_slugs:
        print(f"  SKIP tool {t['slug']} (exists)"); continue
    p = os.path.join(BASE, 'tools', f"{t['slug']}.html")
    with open(p, 'w') as f: f.write(sg.tool_html(t))
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html"); created['tools'] += 1
    print(f"  + tool {t['slug']}.html")

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print(f"  SKIP compare {c['slug']} (exists)"); continue
    p = os.path.join(BASE, 'compare', f"{c['slug']}.html")
    with open(p, 'w') as f: f.write(sg.compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html"); created['compare'] += 1
    print(f"  + compare {c['slug']}.html")

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print(f"  SKIP blog {b['slug']} (exists)"); continue
    p = os.path.join(BASE, 'blog', f"{b['slug']}.html")
    with open(p, 'w') as f: f.write(sg.blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html"); created['blog'] += 1
    print(f"  + blog {b['slug']}.html")

# ---------- SITEMAP ----------
if new_urls:
    sp = os.path.join(BASE, 'sitemap.xml')
    with open(sp) as f: content = f.read()
    urls_xml = ""
    for u in new_urls:
        urls_xml += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    if "</urlset>" in content:
        content = content.replace("</urlset>", urls_xml + "</urlset>", 1)
    else:
        content = content.rstrip() + "\n" + urls_xml + "</urlset>\n"
    with open(sp, 'w') as f: f.write(content)
    print(f"\nSitemap: added {len(new_urls)} URLs (dated {TODAY})")
else:
    print("\nNo new URLs to add to sitemap.")

print(f"\nCREATED: {created}")
print(f"TOTAL NEW URLS: {len(new_urls)}")
