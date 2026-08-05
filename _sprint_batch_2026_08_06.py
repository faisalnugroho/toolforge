#!/usr/bin/env python3
"""ToolForge sprint batch 2026-08-06 — self-contained generator (checks skips, prevents overwrites)."""
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
    dict(slug='seedream-5', name='Seedream 5',
         tagline='ByteDance\'s flagship text-to-image model, 2026 refresh',
         headline='ByteDance\'s photoreal-first image model',
         category='Image Generation', color1='#ee1d52', color2='#690007', initials='S5',
         intro='Seedream 5 is ByteDance\'s 2026 flagship text-to-image model. It pushes beyond Seedream 4 with stronger photorealism, better hand and finger geometry, much-improved text rendering inside images, and tighter prompt adherence on long compositional prompts. Seedream 5 ships inside Doubao, Jimeng, and CapCut, and is exposed via the Volcano Engine API.',
         features=[('Camera', 'Photoreal first', 'Skin tones, hair strands, and cloth texture are noticeably more realistic than Seedream 4 and on par with Midjourney v9 beauty shots.'),
                   ('Aa', 'Native text', 'Renders multi-line typography, signage, and product copy inside the image with very high legibility — a longstanding weakness addressed head-on.'),
                   ('Hand', 'Anatomy fixes', 'Hands, fingers, and reflections hold up under high-zoom inspection much more often than the previous generation.'),
                   ('Zap', 'Sub-second ideation', 'Returns a usable first-pass frame in under two seconds at draft size, enabling fast direction-search before committing tokens to a full render.')],
         pros=['Text-in-image is now competitive with Ideogram 3',
               'Photorealism that can sit next to Midjourney v9 without obvious giveaway',
               'Native tight integration with CapCut and Jimeng for direct video continuation',
               'Aggressive API pricing via Volcano Engine undercuts most Western providers'],
         cons=['The best quality tier is still rate-limited outside China without enterprise contracts',
               'Fewer stylistic presets than Midjourney\'s flagship character/style reference system',
               'Content moderation is stricter on identifiable public figures than Western peers',
               'Documentation and English-language prompt guides lag the model\'s actual capability'],
         price='$0.03', price_label='From $0.03 per image via Volcano Engine; free daily credits in Doubao/Jimeng', price_num=0.03,
         rating='4.4', rating_num=4.4, founded='2026 (ByteDance)', free_tier='Yes (daily generations in Doubao and Jimeng)',
         who_for='Ad creatives, poster artists, e-commerce teams needing text-in-image that doesn\'t look fake, and anyone running CapCut/Jimeng-centric video pipelines.',
         users='Integrated across Doubao, Jimeng, and CapCut user base',
         cta_url='https://www.volcengine.com/product/seedream?via=toolforge',
         verdict='If your workflow already lives in Jimeng or CapCut, Seedream 5 is the obvious 2026 default — it combines Seedream 4\'s speed with near-Midjourney photorealism and the best text-in-image pipeline available outside Ideogram.'),

    dict(slug='claude-opus-6', name='Claude Opus 6',
         tagline='Anthropic\'s flagship reasoning model, 2026 release',
         headline='Anthropic\'s deepest reasoning model to date',
         category='Chatbots / LLMs', color1='#d97757', color2='#8c4a2f', initials='C6',
         intro='Claude Opus 6 is Anthropic\'s 2026 flagship, replacing Claude Opus 5.2 at the top of the Anthropic stack. It extends the multi-hour agentic and long-context work Anthropic has been pushing, with a particular jump in end-to-end software engineering, scientific reasoning, and long-form synthesis. Opus 6 ships in Claude.ai, the Claude API, Amazon Bedrock, and Google Cloud Vertex AI.',
         features=[('Brain', 'Agentic engineering', 'Reliably completes multi-hour software tasks end-to-end — writing code, running tests, reading logs, and iterating — with far fewer interventions than Opus 5.2.'),
                   ('Book', 'Expanded context', 'Effective long-context retrieval has been pushed significantly past the previous generation, with much stronger performance at the deep end of the window.'),
                   ('Sigma', 'Frontier benchmarks', 'Posts best-in-class scores on SWE-bench Verified, GPQA Diamond, and 2026 software-engineering evals at launch.'),
                   ('Shield', 'Constitutional training', 'Built on Anthropic\'s updated constitutional approach with stronger refusal-curve behavior on adversarial and dual-use prompts.')],
         pros=['Best-in-class agentic coding and multi-step reasoning at launch',
               'Long-context retrieval quality is the strongest Anthropic has shipped',
               'Available across Claude.ai, Anthropic API, Bedrock, and Vertex AI on day one',
               'Noticeably better at admitting uncertainty instead of hallucinating an answer'],
         cons=['The most expensive flagship of 2026 on a per-token basis at list pricing',
               'Heavy reasoning mode is slow — expect multi-minute latencies on the hardest queries',
               'Image generation remains out of scope (text + vision understanding only)',
               'Some SWE-bench-style gains depend on Anthropic\'s scaffold, less on raw model skill'],
         price='$45', price_label='$45 / 1M output tokens (API); included in Claude Max plans', price_num=45,
         rating='4.8', rating_num=4.8, founded='2026 (Anthropic)', free_tier='Yes (limited Opus 6 access on Claude Free)',
         who_for='Software teams running long agentic workflows, researchers pushing on frontier reasoning, and enterprises already standardized on Claude via Bedrock or Vertex.',
         users='Flagship model for Claude Max and Claude API traffic',
         cta_url='https://www.anthropic.com/?via=toolforge',
         verdict='The strongest single reasoning model available in mid-2026 for software engineering and long-context work, with pricing to match. Pick it when quality matters more than latency or cost.'),

    dict(slug='udio-2', name='Udio 2',
         tagline='Udio\'s 2026 music-generation model with multitrack stems',
         headline='Studio-grade AI music with stem separation built in',
         category='Music & Audio', color1='#0ea5e9', color2='#0369a1', initials='U2',
         intro='Udio 2 is the 2026 flagship model from Udio. It produces full-length songs with significantly stronger vocal naturalness, real-time lyric editing, and — most importantly — native multitrack stem export (vocals, drums, bass, music, FX) so creators can mix, master, and re-arrange AI output inside a DAW instead of being locked to a stereo bounce.',
         features=[('Mic', 'Studio vocals', 'Lead and background vocals carry convincingly human breath control, vibrato, and phrasing — Udio 2 closes much of the gap to session singers.'),
                   ('Layers', 'Stem export', 'Every render downloads as up to 8 stems (vocals, drums, bass, harmony, FX) ready to drop into Logic, Ableton, or Pro Tools.'),
                   ('Edit', 'In-place lyric edit', 'Rewrite a single line or bridge and have Udio 2 regenerate just that section without re-rendering the whole song.'),
                   ('Clock', 'Full-length songs', 'Generates up to 8 minutes of coherent, structured music with intro/verse/chorus/bridge/outro instead of abrupt loop endings.')],
         pros=['Stem export is a genuine workflow unlock for serious music producers',
               'In-place section editing avoids the "re-roll the whole song" fatigue',
               'Vocals sit noticeably ahead of Suno v7 on breath and phrasing quality',
               'Free tier provides enough credits to evaluate a full song before paying'],
         cons=['Style and genre controls lag Suno v7\'s tagging system for niche micro-genres',
               'Stems occasionally bleed on dense harmony stacks (bgv + pads)',
               'API access is still in limited beta with high list pricing',
               'Occasional mastering-stage compression artifacts on loud/busy mixes'],
         price='$10', price_label='Free / $10 Standard / $30 Pro', price_num=10,
         rating='4.6', rating_num=4.6, founded='2026 (Udio)', free_tier='Yes (10 credits/day)',
         who_for='Music producers, songwriter-producers, and content creators who want AI-generated songs they can actually finish inside a DAW, not just ship as-is.',
         users='Top creator tier on the platform',
         cta_url='https://www.udio.com/?via=toolforge',
         verdict='The 2026 upgrade music producers were waiting for — stems and section-level edit make Udio 2 the first AI music model that fits a real production workflow instead of replacing it.'),

    dict(slug='pika-3', name='Pika 3',
         tagline='Pika Labs\' 2026 video model with native audio',
         headline='Text-to-video with built-in sound and speech',
         category='Video Generation', color1='#7c3aed', color2='#4c1d95', initials='P3',
         intro='Pika 3 is Pika Labs\' 2026 flagship video generation model. It pushes past Pika 2.2 with native audio generation (sound effects, ambient, and speech) synced to the visual output, noticeably stronger motion physics, and much better identity preservation across longer clips. Pika 3 positions itself as the creative-social leader, with templates designed for TikTok/Reels distribution.',
         features=[('Volume2', 'Native audio', 'Generates synced sound effects, ambience, and spoken dialogue alongside the video, no separate audio pass required.'),
                   ('Film', 'Longer clips', 'Up to 60 seconds of continuous video at 1080p, with shot transitions, camera moves, and consistent characters.'),
                   ('User', 'Identity lock', 'Character reference images hold identity across the full clip — useful for recurring-branded content and AI-driven characters.'),
                   ('Zap', 'Faster renders', 'Draft-quality renders complete in 30-60 seconds; final 1080p outputs in 2-4 minutes on the paid tier.')],
         pros=['Native audio is a major workflow win — no separate ElevenLabs pass needed for most social clips',
               'Identity preservation is strong enough for recurring-character content',
               'Excellent short-template library tuned for TikTok/Reels virality',
               'Free tier is generous enough to evaluate the model honestly'],
         cons=['60s is still short of runway for ads or long-form cuts',
               'Audio quality is good for social but not broadcast — speech sounds slightly processed',
               'Less cinematic control over lighting and lens than Runway Gen-6',
               'API access is invitation-only and pricey on a per-second basis'],
         price='$8', price_label='Free / $8 Standard / $28 Pro', price_num=8,
         rating='4.3', rating_num=4.3, founded='2026 (Pika Labs)', free_tier='Yes (limited monthly credits)',
         who_for='Social-first creators, TikTok/Reels shops, and marketers who want short AI video finished (with sound) in one pass.',
         users='Top-tier creator distribution on TikTok and Reels',
         cta_url='https://pika.art/?via=toolforge',
         verdict='The fastest path from prompt to a finished, sound-on social clip in 2026 — film-makers will still want Runway; TikTok teams will want this.'),

    dict(slug='elevenlabs-v4', name='ElevenLabs v4',
         tagline='ElevenLabs\' 2026 flagship voice model with real-time dub',
         headline='Multilingual voice at real-time dub speed',
         category='Voice & Audio', color1='#000000', color2='#1f1f1f', initials='E4',
         intro='ElevenLabs v4 is the 2026 flagship voice model from ElevenLabs. It improves on v3 across the board — pronunciation, multilingual prosody, breath and emotional range — and introduces real-time studio dubbing, where long-form content is dubbed to 70+ languages fast enough to be useful for live broadcast and sports highlights. v4 is exposed across the ElevenLabs app, API, and ElevenStudios.',
         features=[('Mic', 'Studio v4 voices', 'New flagship voice set with finer control over breath, pacing, and emphasis. Multi-speaker mixes hold identity across long scripts.'),
                   ('Globe', 'Real-time dub', 'Full-length videos dub to 70+ languages with lip-sync-grade timing, suitable for live events and broadcast highlights.'),
                   ('Sparkles', 'Emotion tags', 'Inline emotional markup (laughing, whispering, sighing, sarcastic) is more reliable and responsive than v3.'),
                   ('Shield', 'Stronger provenance', 'Cryptographic watermarking on every v4 render for rights-holders and platform compliance — a 2026 must-have.')],
         pros=['Best-in-class pronunciation and prosody across 70+ languages',
               'Real-time dubbing is fast enough for broadcast use, not just archive re-release',
               'Watermarking and consent workflow are now industry-standard compliant',
               'Steady API reliability that production teams can build on'],
         cons=['The very highest-quality "Studio" tier is expensive at scale',
               'Voice cloning from very short clips still produces occasional uncanny moments',
               'Competitors like Play.ht and OpenAI TTS are closing the gap on basic TTS use cases',
               'Occasional tone shifts mid-sentence on highly emotional scripts'],
         price='$5', price_label='Free / $5 Starter / $22 Creator / $99 Pro', price_num=5,
         rating='4.7', rating_num=4.7, founded='2026 (ElevenLabs)', free_tier='Yes (10k characters/month)',
         who_for='Podcast and video producers, localization studios, game developers, and any team that needs multilingual voice at broadcast speeds.',
         users='Standard voice platform for podcast/localization industry',
         cta_url='https://elevenlabs.io/?via=toolforge',
         verdict='The 2026 default for multilingual voice, dubbing, and long-form narration. The real-time dub capability alone re-prices the entire localization workflow.'),

    dict(slug='dia-browser', name='Dia',
         tagline='The Browser Company\'s AI-native browser',
         headline='The browser that writes with you, not for you',
         category='Productivity & Browsers', color1='#0a72ef', color2='#0842a0', initials='DB',
         intro='Dia is the AI-native browser from The Browser Company (the team behind Arc). It builds AI directly into the tab, address bar, and writing surface — instead of bolting a sidebar chat onto a legacy browser. Dia can read every open tab, summarize across them, help you write in-place on any text field, and execute multi-step tasks across sites with your permission.',
         features=[('Zap', 'AI address bar', 'The URL bar doubles as a chat prompt — search, navigate, or run a task without breaking flow.'),
                   ('BookOpen', 'Cross-tab memory', 'Dia reads your open tabs (with permission), so chat answers are grounded in what you\'re actually looking at, not generic web context.'),
                   ('Edit3', 'In-place writing', 'Inline writing help on any text field — email in Gmail, post in Twitter/X, doc in Notion — without leaving the page.'),
                   ('Sliders', 'Skill system', 'Custom "Skills" let you save and share reusable AI workflows (e.g. "summarize this news set into 5 bullets"), a step beyond simple shortcuts.')],
         pros=['Cross-tab context is a genuine step beyond ChatGPT or Perplexity sidebars',
               'In-place writing beats copy-paste-to-ChatGPT for email/social',
               'Skills let power users build and share reusable workflows',
               'Clean, Arc-influenced UI with strong keyboard navigation'],
         cons=['macOS-only at launch (Windows roadmap, no Ion) — cuts out a huge audience',
               'Extension compatibility is still catch-up vs Chrome/Edge',
               'Power users will feel the walled-garden fit-and-finish first features second',
               'Pricing for the paid tier is still being finalized in mid-2026'],
         price='$0', price_label='Free in beta, paid tier roadmap for 2026', price_num=0,
         rating='4.4', rating_num=4.4, founded='2025 (The Browser Company)', free_tier='Yes (full featured in beta)',
         who_for='Mac-based knowledge workers who live in the browser, especially writers, analysts, and researchers who want cross-tab context instead of a sidebar chatbot.',
         users='Hundreds of thousands on the waitlist and early-access rollout',
         cta_url='https://www.diabrowser.com/?via=toolforge',
         verdict='The most interesting browser AI play of 2026 — cross-tab context and in-place writing feel genuinely different from ChatGPT bolt-ons. Worth trying even if you keep Chrome as your daily driver.'),
]

COMPARES = [
    dict(slug='seedream-5-vs-flux-3',
         name_a='Seedream 5', name_b='FLUX 3',
         color_a='#ee1d52', color_b='#000000',
         initials_a='S5', initials_b='F3',
         url_a='https://www.volcengine.com/product/seedream?via=toolforge',
         url_b='https://blackforestlabs.ai/?via=toolforge',
         desc_a='ByteDance flagship 2026 — text-in-image, photorealism, speed',
         desc_b='Black Forest Labs 2026 — open weights, fine-tuning,style range',
         price_a='From $0.03/img (Volcano Engine); free in Doubao/Jimeng',
         price_b='From $0.04/img (BFL API); open weights for self-host',
         best_a='Text-in-image, photorealism, fast iteration',
         best_b='Open weights, custom fine-tunes, style range',
         verdict='<strong>Use Seedream 5</strong> if your work is social, advertising, or product marketing with text-in-image — Seedream 5 produces legible multi-line copy on posters/signage that FLUX 3 still mangles more often than not, and photorealistic skin/hair/cloth texture holds up at higher zoom. <strong>Use FLUX 3</strong> if you need open weights, custom LoRA full fine-tuning, or generation on infrastructure you control; the FLUX community ecosystem of styles, character refs, and LoRAs is far deeper than anything Seedream 5 ships with.',
         winner='Seedream 5 for marketing/social; FLUX 3 for control and self-hosting'),

    dict(slug='claude-opus-6-vs-gpt-5-5',
         name_a='Claude Opus 6', name_b='GPT-5.5',
         color_a='#d97757', color_b='#10a37f',
         initials_a='C6', initials_b='G5',
         url_a='https://www.anthropic.com/?via=toolforge',
         url_b='https://openai.com/?via=toolforge',
         desc_a='Anthropic flagship 2026 — agentic coding and long context',
         desc_b='OpenAI flagship 2026 — cheaper, image gen, consumer polish',
         price_a='$45 / 1M output tokens; included in Claude Max',
         price_b='$30 / 1M output tokens; included in ChatGPT Plus/Pro',
         best_a='Agentic coding, long-context retrieval, safer refusals',
         best_b='Cost, multimodal breadth, consumer app polish',
         verdict='<strong>Use Claude Opus 6</strong> for agentic software engineering and deep long-context work — multi-hour SWE tasks complete more reliably with fewer interventions, retrieval quality holds up at the deep end of the context window, and refusal behavior on security/safety work is the most calibrated of the frontier. <strong>Use GPT-5.5</strong> when cost, image generation, or consumer polish matter more than the last few points of SWE-bench — at roughly 2/3 the per-token price, with native image generation via GPT Image, and a more polished ChatGPT app stack.',
         winner='Opus 6 for engineering; GPT-5.5 for cost and consumer polish'),

    dict(slug='udio-2-vs-suno-v7',
         name_a='Udio 2', name_b='Suno v7',
         color_a='#0ea5e9', color_b='#1d4ed8',
         initials_a='U2', initials_b='S7',
         url_a='https://www.udio.com/?via=toolforge',
         url_b='https://suno.com/?via=toolforge',
         desc_a='Udio flagship 2026 — stems, section edit, studio vocals',
         desc_b='Suno flagship 2026 — genre tags, structure, virality',
         price_a='Free / $10 / $30',
         price_b='Free / $10 / $30',
         best_a='Producers finishing in a DAW',
         best_b='Creators shipping straight from the platform',
         verdict='<strong>Use Udio 2</strong> if you produce music seriously and want to mix/master in a DAW — stems, in-place section edit, and breath-controlled vocals are designed for a real production workflow. <strong>Use Suno v7</strong> if you want a finished song for social/video/meme use without ever touching a DAW — Suno\'s tagging system, structure awareness, and meme-style templates turn around social content faster than Udio 2.',
         winner='Udio 2 for production; Suno v7 for speed and virality'),

    dict(slug='dia-browser-vs-comet',
         name_a='Dia', name_b='Comet',
         color_a='#0a72ef', color_b='#6366f1',
         initials_a='DB', initials_b='CO',
         url_a='https://www.diabrowser.com/?via=toolforge',
         url_b='https://www.perplexity.ai/comet?via=toolforge',
         desc_a='Browser Company 2026 — cross-tab context, in-place writing',
         desc_b='Perplexity 2026 — answer engine integration, agent tasks',
         price_a='Free in beta',
         price_b='Free; $20/mo Comet Max for full agent',
         best_a='Writing, research, browsing flow',
         best_b='Executing multi-step web tasks for you',
         verdict='<strong>Use Dia</strong> if you want AI woven into your existing browsing, writing, and research flow — cross-tab context and inline writing help feel like a step beyond ChatGPT sidebars. <strong>Use Comet</strong> if you want an execution layer that does multi-step web tasks for you — autonomous form-fill, checkout, and scheduling with a more developed permission model, plus Perplexity\'s citation-tuned answers on every query.',
         winner='Dia for the writer; Comet for the delegator'),
]

BLOGS = [
    dict(slug='ai-tools-for-film-composers-2026', title='AI Tools for Film Composers in 2026: From Sketch to Score',
         meta='The 2026 AI toolkit for film composers — sketch-to-score, temp music replacement, stem mixing, vocal mockups, and rights-safe AI instruments. Ranked by real-world fit.',
         category='Industry AI Tools', read='11 min read',
         lead='Film scoring in 2026 means competing with a machine that never sleeps — and using the same machine to stay competitive. These are the AI tools working composers actually use, not the demo-reel vaporware.',
         tools=[dict(name='Udio 2', initial='U', color='#0ea5e9', badge='Score Sketches',
                     desc='Generate full-orchestral score sketches from text in minutes, then export stems to refine inside your DAW. Replaces a week of sketching with an afternoon of art direction.',
                     url='https://www.udio.com/?via=toolforge'),
                dict(name='Suno v7', initial='S', color='#1d4ed8', badge='Temp Tracks',
                     desc='Produce convincing temp tracks for director alignment. Song structure and build/drop/outro feel production-shaped out of the box.',
                     url='https://suno.com/?via=toolforge'),
                dict(name='ElevenLabs v4', initial='E', color='#000000', badge='Vocal Mockups',
                     desc='Multilingual vocal mockups for demo reels and temp vocals. The v4 breath control and phrasing hold up at 48kHz final-mix quality.',
                     url='https://elevenlabs.io/?via=toolforge'),
                dict(name='AIVA', initial='A', color='#7c3aed', badge='Orchestral',
                     desc='The most mature AI orchestrator; emits MIDI + stems you own for commercial use. Strong for adaptive game/film cues.',
                     url='https://www.aiva.ai/?via=toolforge'),
                dict(name='LANDR', initial='L', color='#22c55e', badge='Mastering',
                     desc='AI mastering tuned for score-stem mixes. The 2026 model handles orchestral dynamics without smashing the quiet bits.',
                     url='https://www.landr.com/?via=toolforge'),
                dict(name='iZotope RX', initial='R', color='#f59e0b', badge='Dialogue Repair',
                     desc='Still the industry standard for rescuing production dialogue; the 2026 RX release uses its own AI to automate repair time by 5x.',
                     url='https://www.izotope.com/?via=toolforge')],
         verdict='Start with Udio 2 for sketches and stems, add Suno v7 for director-facing temp tracks, and keep ElevenLabs v4 in your back pocket for vocal mockups that don\'t embarrass you in front of the director. The craft is still human — the rough pass no longer has to be.'),

    dict(slug='ai-tools-for-mlops-engineers-2026', title='AI Tools for MLOps Engineers in 2026: Ship, Observe, Iterate',
         meta='The 2026 AI toolkit for MLOps — pipeline orchestration, model registries, drift detection, prompt/version control, and eval automation. Ranked by production-readiness.',
         category='Industry AI Tools', read='10 min read',
         lead='MLOps in 2026 means managing LLMs, agents, and classical models in the same pipeline. These are the AI tools that actually survive a production deploy — not just the ones that demo well.',
         tools=[dict(name='LangSmith', initial='L', color='#0ea5e9', badge='Observability',
                     desc='End-to-end tracing, evals, and prompt versioning for LLM apps. The 2026 release adds native agent-trajectory views.',
                     url='https://www.langchain.com/langsmith?via=toolforge'),
                dict(name='Weights & Biases', initial='W', color='#f59e0b', badge='Experiment Tracking',
                     desc='The standard for experiment and model-registry tracking; W&B Weave covers LLM observability without bolting on a second tool.',
                     url='https://wandb.ai/?via=toolforge'),
                dict(name='Braintrust', initial='B', color='#7c3aed', badge='Evals',
                     desc='Evals-first LLM platform with tight CI integration. Strongest for eval-driven development cultures.',
                     url='https://www.braintrust.dev/?via=toolforge'),
                dict(name='Modal', initial='M', color='#22c55e', badge='Compute',
                     desc='Serverless GPU compute for training and inference. The 2026 DX is the cleanest in the industry.',
                     url='https://modal.com/?via=toolforge'),
                dict(name='Baseten', initial='BT', color='#ef4444', badge='Inference',
                     desc='Production model serving with autoscaling; strong on cost-per-token for open-weight models.',
                     url='https://www.baseten.co/?via=toolforge'),
                dict(name='Arize Phoenix', initial='A', color='#6366f1', badge='Drift / Evals',
                     desc='Open-source observability for LLMs and classical models. Strong drift detection catching issues your dashboards miss.',
                     url='https://phoenix.arize.com/?via=toolforge')],
         verdict='Start with LangSmith or Braintrust for observability, layer on W&B for experiment tracking if you\'re training, and treat Modal/Baseten as the production compute/mesh layer. Arize Phoenix is the open-source floor you can graduate from.'),
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
