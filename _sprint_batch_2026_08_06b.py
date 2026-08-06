#!/usr/bin/env python3
"""ToolForge sprint batch 2026-08-06b — self-contained generator (checks skips, prevents overwrites).
Adds: 3 tools (gemini-3-flash-lite, pebblo, azure-ai-foundry),
      6 compares (veo-3-2-vs-sora-4, gpt-image-3-vs-midjourney, seedance-vs-veo-3,
                  minimax-m2-vs-glm-4-6, devstral-vs-qwen3-coder, wandb-vs-langsmith),
      2 blogs (best-ai-tools-for-amazon-sellers-2026, ai-tools-for-general-contractors-2026).
"""
import os, sys, json, re

BASE = os.path.expanduser('~/projects/toolforge')
os.chdir(BASE)

src = open('_sprint_gen.py').read()
head = src.split('# =================== CONTENT DATA ===================')[0]
g = {'TODAY': '2026-08-06', 'DOMAIN': 'https://toolforge.io'}
exec(head, g)
tool_html = g['tool_html']; compare_html = g['compare_html']; blog_html = g['blog_html']
existing_slugs = g['existing_slugs']

assert 'TODAY' in g
for sub in ('tools', 'compare', 'blog'):
    print(sub, len(existing_slugs(sub)), 'slugs')

TOOLS = [
    dict(slug='gemini-3-flash-lite', name='Gemini 3 Flash-Lite',
         tagline='Google\'s cheapest 2026 Gemini tier — sub-cent pricing at scale',
         headline='Frontier-adjacent quality at near-free prices',
         category='Chatbots / LLMs', color1='#4285f4', color2='#1a53c0', initials='GL',
         intro='Gemini 3 Flash-Lite is Google\'s 2026 budget tier, sitting below Gemini 3 Flash. It targets the price-sensitive high-volume use cases — classification, extraction, summarization, chat boilerplate — where GPT-4o-mini, Claude Haiku 4.5, and Gemini 2.5 Flash-Lite used to fight. It keeps the 1M-token context window, adds stronger multilingual support, and ships with the lowest list pricing of any major-provider 2026 model.',
         features=[('Zap', 'Sub-second responses', 'P50 latency under 400ms on typical prompts, fast enough to sit inline in a UI without a spinner.'),
                   ('Book', '1M token context', 'Retains the Gemini long-context window, useful for batch document work and long transcript parsing.'),
                   ('DollarSign', 'Cheapest 2026 frontier', 'Roughly 1/3 the price of Gemini 3 Flash and an order of magnitude below flagships — viable for massive parallelizable jobs.'),
                   ('Globe', 'Multilingual by default', 'Strong on low-resource languages that smaller open-weight models mangle.')],
         pros=['Pricing is the headline — cheap enough to run on every click, not just every task',
               'Keeps Gemini 3\'s long-context advantage (most "mini" rivals are 128k-200k)',
               'Fast enough for real-time UI inline use',
               'Strong multilingual coverage beyond English/EU languages'],
         cons=['Reasoning depth clearly below flagships — skip for multi-step analysis',
               'Instruction following degrades on very long, nested prompts',
               'Image generation not included; text + image understanding only',
               'Tool/function-calling is present but less reliable than Gemini 3 Flash'],
         price='$0.08', price_label='$0.08 / 1M output tokens (API); free tier via AI Studio', price_num=0.08,
         rating='4.2', rating_num=4.2, founded='2026 (Google)', free_tier='Yes (AI Studio free quota)',
         who_for='Teams running massive classification/extraction pipelines, builders of real-time chat features, and anyone who needs "good enough" LLM calls at a price that rounds to zero.',
         users='High-volume API tier across Google Cloud and AI Studio',
         cta_url='https://ai.google.dev/?via=toolforge',
         verdict='If your workload is high-volume and "good enough" really is good enough, Gemini 3 Flash-Lite is the obvious 2026 default — nothing else at the frontier labs comes close on cost-per-token. For anything nuanced, step up to Flash or Pro.'),

    dict(slug='pebblo', name='Pebblo',
         tagline='Data governance and lineage for RAG and GenAI pipelines',
         headline='Know what data your AI is actually touching',
         category='Security & Governance', color1='#0f766e', color2='#115e59', initials='PB',
         intro='Pebblo is an open-source data-governance layer for GenAI apps, from Daxa AI. It scans the documents flowing into your RAG pipeline, classifies sensitive data (PII, PCI, HIPAA, source-code secrets), and builds a live data lineage graph so security teams can answer "what did the model see?" without reverse-engineering a vector DB. It slots in next to LangChain/LlamaIndex and reports to a console.',
         features=[('Shield', 'Sensitive-data scanner', 'Detects PII, PCI, HIPAA, secrets, IP, and custom entity classes inside documents before they hit the vector store.'),
                   ('Network', 'Lineage graph', 'Maps document-to-chunk-to-embedding-to-prompt flow so you can answer "who touched this file" after the fact.'),
                   ('Sliders', 'Policy enforcement', 'Block or redact in flight — deny-list an entire SharePoint folder, redact SSNs, or route flagged docs for review.'),
                   ('FileText', 'Compliance reports', 'One-click HTML/PDF reports for security review boards and customer audits.')],
         pros=['Open-source core with a self-hostable server — no SaaS lock-in for the scanner itself',
               'Works with LangChain and LlamaIndex out of the box; 10-line integration',
               'Fills the "what data went into the model" hole most RAG teams ignore until an incident',
               'Custom entity classes let you encode "our internal codenames" or "customer-record ID format" as first-class entities'],
         cons=['Smaller community and ecosystem than LangSmith/LangFuse — fewer blog posts, fewer answers',
               'Commercial UI is young and less polished than the incumbents',
               'Classification accuracy on multilingual docs is patchy outside English',
               'Does not help with prompt-injection or output-side safety — it is input/data-side only'],
         price='$0', price_label='Open-source core; paid Pebblo Cloud tier for multi-team UI', price_num=0,
         rating='4.1', rating_num=4.1, founded='2023 (Daxa AI)', free_tier='Yes (full open-source core)',
         who_for='Platform and security teams at regulated-industry companies who need provable data lineage on their RAG stack, and any team that has had a "wait — did customer data just hit the LLM?" scare.',
         users='Open-source community plus early enterprise adopters',
         cta_url='https://github.com/daxa-ai/pebblo?via=toolforge',
         verdict='If you are shipping RAG into production at a company with any compliance surface at all, Pebblo belongs in the stack — it solves the input-side data-governance problem that none of the big observability tools touch.'),

    dict(slug='azure-ai-foundry', name='Azure AI Foundry',
         tagline='Microsoft\'s unified GenAI studio, model catalog, and agent runtime',
         headline='One front door for every model Microsoft sells (or hosts)',
         category='ML Platforms', color1='#0364b8', color2='#0a4a88', initials='AF',
         intro='Azure AI Foundry is Microsoft\'s 2026 re-architecture of the Azure AI stack into a single studio: model catalog (OpenAI, Anthropic, Meta, Mistral, DeepSeek, Cohere, plus Microsoft\'s own), agent service with hosted agents and tools, evaluation harness, fine-tuning, observability, and content-safety filters in one pane. It replaced the older Azure AI Studio and consolidates what used to be three consoles.',
         features=[('Layers', 'Catalog breadth', 'OpenAI, Anthropic Claude, Meta Llama, Mistral, DeepSeek, Stable Diffusion, plus Microsoft Phi — all deployable from one UI with unified billing.'),
                   ('Bot', 'Hosted agents', 'Agent Service with managed threads, code interpreter, file search, and SharePoint grounding — no LangChain host to wire up.'),
                   ('FlaskConical', 'Built-in evals', 'Pre-registered quality and safety evaluators (groundedness, fluency, harm, jailbreak) runnable as CI checks.'),
                   ('Lock', 'Enterprise controls', 'CMK, private endpoints, customer lockbox, EU data boundary — works out of the box for regulated industries.')],
         pros=['The broadest single-pane model catalog of the big three clouds in 2026',
               'Agent Service handles much of the plumbing that Bedrock forces you to write',
               'Compliance story (CMK, EU boundary, Purview integration) is years ahead of startups',
               'Tight integration with the rest of the Microsoft stack — Entra ID, Purview, Microsoft 365'],
         cons=['UI comprehensibility still lags the ambition; deep menus and slow blades remain',
               'Cold-start latency on fresh deploys can be 5-10 minutes',
               'Costs are high — Azure premium + OpenAI pricing markup stacks quickly',
               'Foundry-branded SDK rework has broken backwards compatibility more than once in 2025-2026'],
         price='$0', price_label='Studio free; consumption billed on the underlying model + compute SKUs', price_num=0,
         rating='4.3', rating_num=4.3, founded='2023 (as Azure AI Studio; re-launched as Foundry 2024-25, expanded 2026)', free_tier='Yes (studio + evaluators)',
         who_for='Enterprise platform teams already on Azure, ops teams migrating from Azure OpenAI Service, and any org that needs Anthropic + OpenAI + open-weight under one compliance umbrella.',
         users='Default GenAI control plane across Microsoft enterprise accounts',
         cta_url='https://azure.microsoft.com/en-us/products/ai-foundry?via=toolforge',
         verdict='The most complete "all the models, all the compliance" control plane available in 2026 — heavier and pricier than cobbling Bedrock + a vector DB + LangSmith, but worth it if your InfoSec team reads the Azure bill.'),
]

COMPARES = [
    dict(slug='veo-3-2-vs-sora-4',
         name_a='Veo 3.2', name_b='Sora 4',
         color_a='#4285f4', color_b='#1f2937',
         initials_a='V3', initials_b='S4',
         url_a='https://deepmind.google/models/veo/?via=toolforge',
         url_b='https://openai.com/sora?via=toolforge',
         desc_a='Google DeepMind 2026 — physics realism, sound, cinematography',
         desc_b='OpenAI 2026 — longer clips, character persistence, social templates',
         price_a='Included in Gemini Advanced / Google One AI Premium; API on Vertex',
         price_b='Included in ChatGPT Plus/Pro; API via OpenAI',
         best_a='Photorealism, physics accuracy, professional cinematography',
         best_b='Character consistency, scene length, fast social output',
         verdict='<strong>Use Veo 3.2</strong> if you are producing anything where physics, lighting, or camera behavior will be judged frame-by-frame — ads, product shots, cinematography pre-viz. Its photorealism and camera control are a step ahead. <strong>Use Sora 4</strong> if you need longer coherent clips with persistent characters (brand mascots, story cuts), or if you are producing high-volume social content where the social-template library is worth more than the last few points of realism.',
         winner='Veo 3.2 for cinematography; Sora 4 for character-driven social work'),

    dict(slug='gpt-image-3-vs-midjourney',
         name_a='GPT Image 3', name_b='Midjourney',
         color_a='#10a37f', color_b='#1f2937',
         initials_a='GI', initials_b='MJ',
         url_a='https://openai.com/?via=toolforge',
         url_b='https://www.midjourney.com/?via=toolforge',
         desc_a='OpenAI 2026 — text-in-image, instruction following, integrated into ChatGPT',
         desc_b='Midjourney 2026 — aesthetic quality, artistic styles, character/style refs',
         price_a='Included in ChatGPT Plus/Pro; API on OpenAI',
         price_b='From $10/mo (Basic) to $120/mo (Mega)',
         best_a='Text-in-image, instruction following, product/illustration compositing',
         best_b='Aesthetic quality, artistic styles, visual identity exploration',
         verdict='<strong>Use GPT Image 3</strong> if your work is product marketing, UX comps, or anything requiring legible text inside the image — it is the only 2026 model that reliably nails instructions like "put the headline on the left, price tag in the lower right" without three retries. <strong>Use Midjourney</strong> if your work is visual identity, moodboards, editorial illustration, or anywhere the output\'s aesthetic quality is the deliverable — Midjourney v9 still hits looks no one else can, and its style/character reference system is deeper.',
         winner='GPT Image 3 for compositing and copy; Midjourney for craft'),

    dict(slug='seedance-vs-veo-3',
         name_a='Seedance', name_b='Veo 3',
         color_a='#ee1d52', color_b='#4285f4',
         initials_a='SD', initials_b='V3',
         url_a='https://seed.bytedance.com/?via=toolforge',
         url_b='https://deepmind.google/models/veo/?via=toolforge',
         desc_a='ByteDance 2026 — speed, multi-shot, cost, Jimeng/CapCut-native',
         desc_b='Google 2026 — audio sync, cinematography, physics realism',
         price_a='Aggressive API via Volcano Engine; low-cost daily credits in Jimeng/CapCut',
         price_b='Bundled in Google AI Premium; premium pricing on Vertex AI',
         best_a='Volume output, rapid iteration, Asian-market social platforms',
         best_b='Premium photoreal work, audio-integrated clips',
         verdict='<strong>Use Seedance</strong> if you are running a high-volume social or ad pipeline and budget-per-clip matters — its Volcano Engine pricing is materially lower than Veo and the multi-shot sequencing has gotten very good in 2026. <strong>Use Veo 3</strong> if audio-sync, cinematography, or physics realism are the differentiator on the deliverable — Veo is still the model the top-tier ad shops reach for on premium work, and the built-in audio pipeline is noticeably stronger.',
         winner='Seedance for volume and cost; Veo 3 for premium cinematic work'),

    dict(slug='minimax-m2-vs-glm-4-6',
         name_a='MiniMax M2', name_b='GLM-4.6',
         color_a='#ef4444', color_b='#7c3aed',
         initials_a='M2', initials_b='G4',
         url_a='https://www.minimax.io/?via=toolforge',
         url_b='https://www.zhipuai.cn/?via=toolforge',
         desc_a='MiniMax 2026 flagship open-weights — MoE, agentic coding, long context',
         desc_b='Zhipu AI 2026 flagship — agentic, tool use, reasoning depth',
         price_a='Open weights (Apache 2.0); MiniMax API at low per-token rates',
         price_b='Open weights; z.ai API at low per-token rates',
         best_a='Self-host agentic coding and long-context reasoning',
         best_b='Tool use, agentic scaffolding, Mandarin + English bilingual',
         verdict='<strong>Use MiniMax M2</strong> if you are running an agentic coding pipeline on your own infrastructure — its MoE architecture is tuned for tool-call chains and long autonomous runs, and it benchmarks at the top of the open-weights class on SWE-bench-style evals. <strong>Use GLM-4.6</strong> if you are building agent pipelines with heavy tool use and care about Mandarin + English bilingual performance out of the box — GLM-4.6 has been the more stable choice for multi-tool agent scaffolds in 2026, and Zhipu\'s Cookbook and agent framework are deeper.',
         winner='MiniMax M2 for self-host coding; GLM-4.6 for bilingual agent pipelines'),

    dict(slug='devstral-vs-qwen3-coder',
         name_a='Devstral', name_b='Qwen3 Coder',
         color_a='#7c3aed', color_b='#b91c1c',
         initials_a='DV', initials_b='QC',
         url_a='https://mistral.ai/?via=toolforge',
         url_b='https://qwen.ai/?via=toolforge',
         desc_a='Mistral 2026 — agentic coding, 24B-class, SWE-bench top of class',
         desc_b='Alibaba 2026 — agentic coding, multi-language, long context',
         price_a='Open weights (Apache 2.0); Mistral API',
         price_b='Open weights (Apache 2.0); Alibaba Cloud API',
         best_a='Laptop-friendly agentic coding, low-latency local runs',
         best_b='Multilingual projects, longer-context file piles',
         verdict='<strong>Use Devstral</strong> if you want an agentic coding model that fits on a developer laptop (24B class) without giving up too much on SWE-bench — it is the 2026 default for "run local, agent-like CLI workflows." <strong>Use Qwen3 Coder</strong> for longer-context projects, multilingual codebases (Java/C++/TypeScript all fare well), and teams already using other Qwen models — the long-context retrieval is meaningfully better than Devstral\'s on 100k+ token repos.',
         winner='Devstral for local-first; Qwen3 Coder for long-context projects'),

    dict(slug='wandb-vs-langsmith',
         name_a='Weights & Biases', name_b='LangSmith',
         color_a='#f59e0b', color_b='#0ea5e9',
         initials_a='WB', initials_b='LS',
         url_a='https://wandb.ai/?via=toolforge',
         url_b='https://www.langchain.com/langsmith?via=toolforge',
         desc_a='W&B 2026 — experiment tracking, model registry, Weave for LLMs',
         desc_b='LangChain 2026 — tracing, evals, prompt versioning, agent observability',
         price_a='Free tier; Team from $50/user/mo',
         price_b='Free tier; Plus from $39/seat/mo',
         best_a='Teams training models + doing LLM observability in one pane',
         best_b='LangChain-native LLM observability and evals',
         verdict='<strong>Use Weights & Biases</strong> if you are training models (fine-tuning, full training, RL) and want one pane of glass for experiments, artifacts, and LLM observability via Weave — no other tool in 2026 does both halves as well. <strong>Use LangSmith</strong> if you are shipping LLM apps built on LangChain/LangGraph and want the deepest possible tracing and eval integration — LangSmith\'s agent-trajectory view and prompt versioning are unmatched on that stack.',
         winner='W&B for training + LLMs; LangSmith for LangChain-native observability'),
]

BLOGS = [
    dict(slug='best-ai-tools-for-amazon-sellers-2026', title='Best AI Tools for Amazon Sellers in 2026: Listing, Ads, and Ops',
         meta='The 2026 AI stack for Amazon sellers — listing copy, product images, PPC, review mining, and inventory forecasting. Picked by working sellers, ranked by ROI.',
         category='Industry AI Tools', read='12 min read',
         lead='Amazon selling in 2026 is won on listing quality, ad efficiency, and ops accuracy. The AI stack that paid for itself last month is different from the one that worked in 2024 — here is what working 7-figure sellers actually run.',
         tools=[dict(name='ChatGPT', initial='C', color='#10a37f', badge='Listing Copy',
                     desc='The default for bullet-point and A+ content drafting, with the 2026 image-gen tier handling infographics and lifestyle comps. Hook up your brand voice doc once and re-use it across the catalog.',
                     url='https://chat.openai.com/?via=toolforge'),
                dict(name='Helium 10 AI', initial='H', color='#ef4444', badge='Listing Audit',
                     desc='AI-driven Listing Builder audits copy against top-10 SERP competitors and rewrites weak bullets. The 2026 release mines ATS keywords from your niche automatically.',
                     url='https://www.helium10.com/?via=toolforge'),
                dict(name='Perplexity', initial='P', color='#5b21b6', badge='Niche Research',
                     desc='Used for competitive landscape scans and "who is entering this niche" checks — the citation-backed answers beat raw ChatGPT for defensible research.',
                     url='https://www.perplexity.ai/?via=toolforge'),
                dict(name='Midjourney', initial='M', color='#1f2937', badge='Lifestyle Imagery',
                     desc='For hero lifestyle comps that don\'t look AI-flat. Pair with a photographer for final SKU imagery; use MJ for the surrounding scene plates and ad variants.',
                     url='https://www.midjourney.com/?via=toolforge'),
                dict(name='Quartile', initial='Q', color='#0ea5e9', badge='PPC Automation',
                     desc='Rule-based plus ML PPC optimization across Sponsored Products, Brands, and Display. The 2026 model factor DSP reach into bidding.',
                     url='https://www.quartile.com/?via=toolforge'),
                dict(name='SoStocked', initial='S', color='#22c55e', badge='Inventory Forecasting',
                     desc='AI inventory forecasting tuned for FBA lead-times and IPI score management. Catches the stockout risk the spreadsheets miss.',
                     url='https://www.sostocked.com/?via=toolforge')],
         verdict='Start with ChatGPT for listings and Perplexity for niche research, layer in Helium 10 AI for listing audits against top competitors, and let Quartile drive the ad account once you clear ~$30k/month in spend. Skip the lifestyle image budget until your conversion rate is north of 15%.'),

    dict(slug='ai-tools-for-general-contractors-2026', title='AI Tools for General Contractors in 2026: Bids, Schedules, Change Orders',
         meta='The 2026 AI stack for GCs — bid writing, schedule risk, change-order drafting, sub communication, and progress-photo documentation. Tools that pay for themselves on one job.',
         category='Industry AI Tools', read='11 min read',
         lead='General contracting in 2026 runs on documents: bids, RFIs, change orders, sub agreements, progress photos. The AI stack that wins is the one that drafts those documents faster and catches the risk the spreadsheet missed — here is what working GCs actually use.',
         tools=[dict(name='ChatGPT', initial='C', color='#10a37f', badge='Bid & CO Drafting',
                     desc='Train it on your standard once, then have it draft owner-facing change orders, RFI responses, and bid narratives in your voice, rewrite-free.',
                     url='https://chat.openai.com/?via=toolforge'),
                dict(name='Buildots', initial='B', color='#ef4444', badge='Progress Verification',
                     desc='Hardhat-camera AI walks the site and auto-compares actual progress against the BIM/schedule. Catches the delayed rough-in before Friday\'s OAC meeting does.',
                     url='https://buildots.com/?via=toolforge'),
                dict(name='Togal.AI', initial='T', color='#0ea5e9', badge='Takeoffs',
                     desc='AI plan takeoffs that turn a 400-page plan set into structured quantities in under an hour. The 2026 model handles multi-discipline sets without breaking.',
                     url='https://www.togal.ai/?via=toolforge'),
                dict(name='Procore Copilot', initial='P', color='#f97316', badge='PM Platform AI',
                     desc='Procore\'s AI layer drafts RFIs, summarizes sub updates, and flags schedule risk inside your existing PM tool — no rip-and-replace.',
                     url='https://www.procore.com/?via=toolforge'),
                dict(name='Claude', initial='C', color='#d97757', badge='Sub Comms',
                     desc='Subcontractor email drafting, Notice-to-Proceed letters, and dispute narratives. The long-context window is handy for "find the CO reference across these 200 emails."',
                     url='https://www.anthropic.com/?via=toolforge'),
                dict(name='OpenSpace', initial='O', color='#7c3aed', badge='Photo Documentation',
                     desc='360 walk documentation with AI auto-mapping to the plan set. Disputes with subs get a whole lot shorter when you have dated, located photos of the work.',
                     url='https://www.openspace.ai/?via=toolforge')],
         verdict='Start with ChatGPT and Claude for the paperwork layer — they pay for themselves in one change order. Add Togal.AI for takeoffs once bid volume justifies it, and put Buildots or OpenSpace on the next mid-size job to see progress verification actually work.'),
]

written, skipped = [], []
for t in TOOLS:
    path = f'tools/{t["slug"]}.html'
    full = os.path.join(BASE, path)
    if os.path.exists(full) and os.path.getsize(full) > 0:
        skipped.append(path); continue
    with open(full, 'w') as f:
        f.write(tool_html(t))
    written.append(path)

for c in COMPARES:
    path = f'compare/{c["slug"]}.html'
    full = os.path.join(BASE, path)
    if os.path.exists(full) and os.path.getsize(full) > 0:
        skipped.append(path); continue
    with open(full, 'w') as f:
        f.write(compare_html(c))
    written.append(path)

for b in BLOGS:
    path = f'blog/{b["slug"]}.html'
    full = os.path.join(BASE, path)
    if os.path.exists(full) and os.path.getsize(full) > 0:
        skipped.append(path); continue
    with open(full, 'w') as f:
        f.write(blog_html(b))
    written.append(path)

print('WROTE:', len(written))
for p in written: print('  +', p)
print('SKIPPED (already exist):', len(skipped))
for p in skipped: print('  =', p)
print('EXIT_OK')
