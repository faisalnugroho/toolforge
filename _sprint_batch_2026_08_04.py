#!/usr/bin/env python3
"""ToolForge sprint batch 2026-08-04 — self-contained generator (checks skips, prevents overwrites)."""
import os, sys, json, re

BASE = os.path.expanduser('~/projects/toolforge')
os.chdir(BASE)

src = open('_sprint_gen.py').read()
head = src.split('# =================== CONTENT DATA ===================')[0]
g = {'TODAY': '2026-08-04', 'DOMAIN': 'https://toolforge.io'}
exec(head, g)
tool_html = g['tool_html']; compare_html = g['compare_html']; blog_html = g['blog_html']
existing_slugs = g['existing_slugs']

assert 'TODAY' in g
for sub in ('tools', 'compare', 'blog'):
    print(sub, len(existing_slugs(sub)), 'slugs')

TOOLS = [
    dict(slug='grok-imagine', name='Grok Imagine',
         tagline='xAI image and video generation, natively in Grok',
         headline='xAI\'s native multimodal canvas',
         category='Image Generation', color1='#1d9bf0', color2='#0a72ef', initials='GI',
         intro='Grok Imagine is xAI\'s image-and-short-video generation feature baked into the Grok assistant. It generates photorealistic or stylised images in seconds, then animates them into 6-15 second video clips with sound on SuperGrok tiers. Imagine is built for speed and a permissive creative stance, and ships with free access on X (Twitter) plus higher limits for Premium/Premium+ and SuperGrok subscribers.',
         features=[('Bolt', 'Image in seconds', 'Text-to-image renders complete in roughly 3-6 seconds — fast enough to keep iteration velocity high inside a chat session.'),
                   ('Video', 'Image to 15s video', 'Any generated or uploaded image can be animated into a 6-15s clip with synced audio using the companion video model.'),
                   ('Spicy', 'Fewer guardrails', 'A permissive content stance compared to DALL-E 3 or Midjourney, enabling edgier creative directions within legal limits.'),
                   ('Chat', 'Built into Grok', 'No separate app — generate, refine, and animate without leaving your Grok conversation on X or grok.com.')],
         pros=['Generates in under 10 seconds inside the Grok chat',
               'Free tier available to any X account',
               'Native video animation with audio, no separate editor needed',
               'Significantly fewer content restrictions than mainstream image models'],
         cons=['Video clips top out at 15 seconds with no extension workflow',
               'No inpaint/outpaint or mask-based editing tools yet',
               'Output carries a visible xAI watermark on non-premium tiers',
               'API access for automated pipelines is still limited'],
         price='Free / $8', price_label='Free on X, $8/mo Premium, $30/mo SuperGrok', price_num=8,
         rating='4.2', rating_num=4.2, founded='2025 (xAI)', free_tier='Yes (limited daily generations on X)',
         who_for='X creators, meme makers, social-first teams, and anyone who values generation speed over pixel-level control.',
         users='30M+ monthly X users',
         cta_url='https://grok.com/?via=toolforge',
         verdict='The fastest image-to-video pipeline inside a chat assistant, and the least filtered of the mainstream generators.'),

    dict(slug='grok-4-heavy', name='Grok 4 Heavy',
         tagline='Multi-agent parallel reasoning from xAI\'s flagship tier',
         headline='Multi-agent test-time compute for hard problems',
         category='Chatbots / LLMs', color1='#0f0f0f', color2='#3a3a3a', initials='GH',
         intro='Grok 4 Heavy is the highest tier of xAI\'s Grok 4 family. Unlike the standard Grok 4, Heavy runs multiple internal agents in parallel — each working the problem from a different angle — then compares, synthesizes, and votes internally before answering. xAI positions it for mathematics, hard reasoning, and scientific analysis rather than quick Q&A.',
         features=[('Agents', 'Multi-agent reasoning', '4-8 internal agents tackle the problem in parallel with divergent strategies, then debate and selectively share findings.'),
                   ('Sigma', 'Benchmarks leader', 'Won or tied first place on Humanity\'s Last Exam (50.7%) and AIME 2025 math at launch among public reasoning models.'),
                   ('Clock', 'Multi-minute compute', 'Responses can spend several minutes of extra test-time compute on heavy reasoning when the query warrants it.'),
                   ('X', 'Native X integration', 'Ships inside SuperGrok subscriptions on grok.com and the Grok iOS/Android apps, with DeepSearch built in.')],
         pros=['Highest public scores on hard reasoning benchmarks like HLE and AIME among 2025-2026 launches',
               'Multi-agent ensemble reduces single-path failure modes on math/proof work',
               'Larger reliably usable context than Grok 3 across coding and analysis sessions',
               'DeepSearch available inline without a separate tool call'],
         cons=['Heavy tier is slow by design — expect multi-minute answers on hard prompts',
               'Most expensive consumer LLM plan at roughly $300/mo SuperGrok Heavy',
               'Rate limits on Heavy reasoning are tight even for paying users',
               'Web browsing is weaker than Gemini 3 Pro Deep Research or Perplexity Max'],
         price='$300', price_label='$300/mo SuperGrok Heavy', price_num=300,
         rating='4.4', rating_num=4.4, founded='2025 (xAI)', free_tier='Basic Grok 4 free; Heavy requires subscription',
         who_for='Researchers, mathematicians, and analysts whose workday includes genuinely hard reasoning where a wrong answer costs more than a slow one.',
         users='Undisclosed',
         cta_url='https://grok.com/?via=toolforge',
         verdict='The brute-force compute champion — best when the answer has to be right, not fast or cheap.'),

    dict(slug='gemini-deep-think', name='Gemini Deep Think',
         tagline='Extended parallel reasoning for Google\'s Gemini flagship',
         headline='Parallel thought-chains, scored on olympiad math',
         category='Chatbots / LLMs', color1='#1e68d7', color2='#8ab4f8', initials='DT',
         intro='Gemini Deep Think is Google\'s extended-reasoning mode for the Gemini 2.5/3 family. Like Grok 4 Heavy, it evaluates multiple reasoning paths in parallel rather than committing to a single chain, then uses a scoring pass to select and synthesize. Google reports it performs at a gold-medal level on IMO-style mathematics and leads on benchmarks like Humanity\'s Last Exam and LiveCodeBench.',
         features=[('Brain', 'Parallel reasoning', 'Multiple simultaneous thought paths with a selection-and-scoring step before the final answer is assembled.'),
                   ('Trophy', 'IMO gold level', 'Reported to solve 5 of 6 IMO 2025 problems under competition time, matching human gold-medal performance.'),
                   ('Layers', 'Multimodal native', 'Images, audio, video, and PDFs can be dropped into the prompt and reasoned over without conversion.'),
                   ('Zap', 'Integrated via Ultra', 'Available to Google AI Ultra subscribers ($249.99/mo tier) in the Gemini app and web UI, with$/rate limited daily.')],
         pros=['Gold-medal-class math and olympiad problem solving',
               'Tightly integrated with Google\'s ecosystem (Search grounding, Workspace)',
               'Strong long-context performance alongside 1M-token input windows',
               'Much cheaper entry point than Grok 4 Heavy via AI Pro if you don\'t need full Heavy'],
         cons=['Deep Think is rate-limited even on Ultra — daily caps kick in quickly',
               'Rollout was phased, so some regions/plans still don\'t see it in the app',
               'Less transparent than Claude about chain-of-thought (summary only)',
               'Hallucinations persist on niche factual topics despite grounding'],
         price='$19.99', price_label='From $19.99/mo AI Pro (limited), $249.99/mo Ultra (full)', price_num=19.99,
         rating='4.5', rating_num=4.5, founded='2025 (Google DeepMind)', free_tier='Limited trial via AI Pro',
         who_for='Quantitative researchers, olympiad-prep students, and Google-ecosystem teams who want top reasoning without leaving the Gemini UI.',
         users='Hundreds of millions (Gemini app)',
         cta_url='https://gemini.google.com/?via=toolforge',
         verdict='The best-reasoning-per-dollar of the heavy tiers, especially if you already pay for Google One.'),

    dict(slug='ideogram-3', name='Ideogram 3',
         tagline='The text-in-image leader for design work',
         headline='Typography and layout that actually spell things right',
         category='Image Generation', color1='#7c3aed', color2='#a855f7', initials='I3',
         intro='Ideogram 3 (also shipped as Ideogram 2.0 → 3.x) is the image model that made its name on legible in-image text — logos, posters, social banners, memes. Version 3 ships improved photorealism, a dedicated style-reference system, and batch generation of up to 8 variants per prompt, all aimed at graphic designers and marketers.',
         features=[('Type', 'Best-in-class text', 'In-image text is legible, on-style, and commercially usable — the model\'s original claim to fame.'),
                   ('Layers', 'Style references', 'Upload up to 3 reference images to lock a visual style across a batch of generations.'),
                   ('Images', 'Batch 8 variants', 'Generate up to 8 compositional variants per prompt at Standard quality for rapid direction scouting.'),
                   ('Palette', 'Palette control', 'Choose output color palettes explicitly when you need brand-consistent output.')],
         pros=['Best typography and text-in-image rendering in the industry',
               'Style-reference system reduces art-direction drift across a series',
               'Free daily credits on the standard tier',
               'API available for programmatic marketing pipelines'],
         cons=['Photorealism still behind Midjourney v8 and Flux 2 on human skin and material rendering',
               'No native video animation — stills only',
               'Prompt-following on complex multi-subject scenes degrades with more than 3-4 entities',
               'Paid tiers gate higher resolutions and priority queue'],
         price='Free / $20', price_label='Free tier; Plus $20/mo, Pro $60/mo', price_num=20,
         rating='4.4', rating_num=4.4, founded='2022 (Ideogram AI)', free_tier='Yes (daily credits, public gallery)',
         who_for='Graphic designers, social media marketers, and e-commerce sellers who need text in image to actually read correctly.',
         users='10M+ registered creators',
         cta_url='https://ideogram.ai/?via=toolforge',
         verdict='If your poster, ad, or meme has words in it, start here — text in image is still unsolved for most rivals.'),

    dict(slug='qwen-image-edit', name='Qwen Image Edit',
         tagline='Open-source image editing powered by Alibaba\'s Qwen-VL family',
         headline='Instruct-based photo edits that understand text',
         category='Image Generation', color1='#4f46e5', color2='#6366f1', initials='QE',
         intro='Qwen Image Edit is the editing variant of Alibaba\'s Qwen-Image family. It follows natural-language instructions ("change the jacket to red", "remove the watermark, keep the person") while preserving everything else with high fidelity. The 20B-parameter model runs locally on a single consumer GPU, is released under Apache 2.0, and is the strongest open instruct-image-editing model currently available.',
         features=[('Wand', 'Instruct-based editing', 'Describe the edit in plain English rather than masking regions manually; the model infers the target from context.'),
                   ('Shield', 'Structure preservation', 'Background, lighting, and non-edited regions survive the edit with minimal drift.'),
                   ('Cpu', 'Runs locally', 'Apache 2.0 licensed — you can run it on a single RTX 4090 or 32GB+ datacenter GPU.'),
                   ('Languages', 'Bilingual prompts', 'Trained on Chinese-English bilingual data for stronger cross-lingual instruction following.')],
         pros=['Fully open-source under Apache 2.0 (completely free for commercial use)',
               'Instruct-edit paradigm eliminates most manual masking work',
               'Preserves fine detail (faces, fabric, logos) better than Flux Kontext LoRAs',
               'Active community integrations (ComfyUI, diffusers, AUTOMATIC1111)'],
         cons=['Requires a 24GB+ VRAM GPU to run locally at practical speeds',
               'No first-party hosted UI; you need ComfyUI or a hosted provider like Replicate',
               'Complex compositional edits sometimes require 2-3 passes',
               'Video editing not supported — images only'],
         price='$0', price_label='Free and open source (Apache 2.0); hosted from ~$0.003/img on Replicate', price_num=0,
         rating='4.3', rating_num=4.3, founded='2025 (Alibaba Qwen team)', free_tier='Yes — fully open source',
         who_for='Developers, agencies, and creators who want per-image editing without per-seat SaaS pricing or sending data to a closed API.',
         users='Open source (1M+ model downloads in first month)',
         cta_url='https://huggingface.co/Qwen/?via=toolforge',
         verdict='The open-source answer to Flux Kontext — same paradigm, no license fee.'),

    dict(slug='hailuo-02', name='Hailuo 02',
         tagline='MiniMax\'s 1080p physics-aware video model',
         headline='Smooth motion at 1080p, priced for iteration',
         category='Video Generation', color1='#f59e0b', color2='#ef4444', initials='HO',
         intro='Hailuo 02 (also written Hailuo AI 02) is MiniMax\'s second-generation video model. It generates 6-10 second clips at native 1080p, handles multi-subject scenes with good physical coherence, and undercuts Veo and Sora on price by a wide margin. The model has climbed to the top of third-party video leaderboards on image-to-video tasks.',
         features=[('Film', '1080p native', 'Renders at native 1920x1080 with no upscaler artifacts on small text or fine textures.'),
                   ('Zap', 'Fast generation', '6-second 1080p clips typically return in 2-4 minutes on the standard tier.'),
                   ('Atom', 'Physics-aware motion', 'Object interactions, cloth, fluid, and body motion are significantly more physically plausible than Kling 1.6-era models.'),
                   ('Coins', 'Cheap credits', 'Generation credits are priced for high-volume iteration — typical cost is a fraction of Veo 3\'s per-clip price.')],
         pros=['Top-tier physics/motion realism among mid-2026 video releases',
               'Native 1080p output, no upscaling softness',
               'Very competitive per-clip pricing for agencies',
               'Reliable image-to-video workflow for creative teams'],
         cons=['Maximum clip length is 10 seconds (extend feature requires paid subscription)',
               'Audio generation lags Veo 3 — no native voice or dialogue sync',
               'English prompt fidelity is good but Chinese prompts often perform better',
               'Third-party watermark removal requires paid plan'],
         price='$9.99', price_label='From $9.99/mo (Standard), credit-based', price_num=9.99,
         rating='4.4', rating_num=4.4, founded='2021 (MiniMax, China)', free_tier='Yes (daily bonus credits)',
         who_for='Content studios, ad agencies, and short-form creators who generate 50+ clips/month and need per-clip cost under control.',
         users='40M+ MiniMax AI users worldwide',
         cta_url='https://hailuoai.video/?via=toolforge',
         verdict='The price-performance video pick for 2026 — Veo 3 quality on most shots at a third of the cost.'),
]

COMPARES = [
    dict(slug='grok-4-heavy-vs-gemini-deep-think',
         name_a='Grok 4 Heavy', name_b='Gemini Deep Think',
         initials_a='GH', initials_b='DT', color_a='#0f0f0f', color_b='#1e68d7',
         price_a='$300/mo', price_b='$19.99-$249.99/mo',
         desc_a='xAI\'s multi-agent reasoning tier with 4-8 parallel internal agents.',
         desc_b='Google\'s extended parallel reasoning mode for Gemini 2.5/3.',
         best_a='Hardest math/proof/science problems where correctness beats speed',
         best_b='Google-ecosystem teams who want strong reasoning at consumer price',
         url_a='https://grok.com/?via=toolforge', url_b='https://gemini.google.com/?via=toolforge',
         verdict='Two multi-agent heavy hitters with different prices, ecosystems, and primary audiences.',
         winner='Gemini Deep Think (value); Grok 4 Heavy (raw ceiling)'),

    dict(slug='grok-imagine-vs-midjourney-v8',
         name_a='Grok Imagine', name_b='Midjourney V8',
         initials_a='GI', initials_b='MV', color_a='#1d9bf0', color_b='#000000',
         price_a='Free-$30/mo', price_b='$10-$120/mo',
         desc_a='xAI\'s fast image+short-video generator inside the Grok chat.',
         desc_b='The industry-standard aesthetic image generator, in its 8th major version.',
         best_a='Social/meme content, fast iteration, X-native workflows',
         best_b='Editorial, advertising, brand, and high-end visual work',
         url_a='https://grok.com/?via=toolforge', url_b='https://www.midjourney.com/?via=toolforge',
         verdict='Speed vs. quality ceiling — pick based on which one you run out of first.',
         winner='Midjourney V8 (images); Grok Imagine (speed + video)'),

    dict(slug='hailuo-02-vs-veo-3-fast',
         name_a='Hailuo 02', name_b='Veo 3 Fast',
         initials_a='HO', initials_b='VF', color_a='#f59e0b', color_b='#1e68d7',
         price_a='$9.99/mo+', price_b='$19.99/mo+',
         desc_a='MiniMax\'s physics-aware 1080p video model with aggressive credit pricing.',
         desc_b='Google\'s speed-optimized Veo 3 variant with native audio.',
         best_a='High-volume clip generation where per-clip cost matters',
         best_b='One-shot hero shots where audio and brand safety matter',
         url_a='https://hailuoai.video/?via=toolforge', url_b='https://deepmind.google/technologies/veo/?via=toolforge',
         verdict='Cost-per-clip vs. cost-per-shot — Hailuo for volume, Veo for flagship.',
         winner='Hailuo 02 (price); Veo 3 Fast (native audio)'),

    dict(slug='ideogram-3-vs-flux-kontext',
         name_a='Ideogram 3', name_b='Flux Kontext',
         initials_a='I3', initials_b='FK', color_a='#7c3aed', color_b='#6366f1',
         price_a='Free-$60/mo', price_b='Credit-based',
         desc_a='Typography-first image generator with batch variants and style references.',
         desc_b='Black Forest Labs\' editing-first multimodal model built around image transformation.',
         best_a='Logo, poster, social ad generation with in-image text',
         best_b='Photo-editing workflows (transforming existing imagery)',
         url_a='https://ideogram.ai/?via=toolforge', url_b='https://bfl.ai/?via=toolforge',
         verdict='Generation vs. transformation — they solve different halves of a design pipeline.',
         winner='Ideogram 3 (text-heavy); Flux Kontext (editing)'),

    dict(slug='qwen-image-edit-vs-flux-kontext',
         name_a='Qwen Image Edit', name_b='Flux Kontext',
         initials_a='QE', initials_b='FK', color_a='#4f46e5', color_b='#6366f1',
         price_a='Free (Apache 2.0)', price_b='Credit-based (closed)',
         desc_a='Open-source instruct-image editor, 20B params, runs locally on a 4090.',
         desc_b='Closed-source editing model via BFL API and hosted providers.',
         best_a='Developers and agencies scaling per-image edits without per-seat cost',
         best_b='Casual users who want best-output minimum-setup via a hosted UI',
         url_a='https://huggingface.co/Qwen/?via=toolforge', url_b='https://bfl.ai/?via=toolforge',
         verdict='Open source vs. managed — the classic developer/non-dev split.',
         winner='Qwen Image Edit (cost + self-host); Flux Kontext (convenience)'),
]

BLOGS = [
    dict(slug='ai-tools-for-novelists-2026', title='12 AI Tools for Novelists in 2026: Draft Faster Without Losing Your Voice',
         meta='The honest 2026 guide to AI tools for fiction writers — what works for plot, prose, and revision, and where AI still fails novelists.',
         category='AI Tools for Professionals', read='11 min read',
         lead='Writing a novel in 2026 means confronting a hard question: which AI tools actually help, and which ones just add noise? After testing 30+ assistants across drafting, editing, world-building, and publishing, here are the 12 that novelists actually keep using after the free trial ends.',
         tools=[dict(name='Claude', initial='C', color='#d4a27f', badge='Top Pick',
                     desc='The strongest long-form prose model in 2026, with a 1M-token context window that holds an entire manuscript. Best for developmental editing, scene-level rewrites in your voice, and consistency-checking across 100k+ words.',
                     url='https://claude.ai/?via=toolforge'),
                dict(name='ChatGPT', initial='C', color='#10a37f', badge='Best Brainstorm',
                     desc='GPT-5-class reasoning for plot outlining, subplot weaving, and "what if" pivots mid-draft. Deep Research mode is useful for historical/technical accuracy without leaving the writing session.',
                     url='https://chatgpt.com/?via=toolforge'),
                dict(name='Sudowrite', initial='S', color='#7c3aed', badge='Fiction-First',
                     desc='Built on top of multiple frontier LLMs with a novelist-specific UI — Story Bible, Scene expansion, Sensory detail boosters. Still the best purpose-built fiction tool despite the monthly cost.',
                     url='https://www.sudowrite.com/?via=toolforge'),
                dict(name='ElevenLabs', initial='E', color='#000000', badge='Audio Drafts',
                     desc='Turn draft chapters into natural-sounding audio to hear your own prose read back. Audiobook-quality voices make the "read-aloud edit" painless.',
                     url='https://elevenlabs.io/?via=toolforge'),
                dict(name='Midjourney', initial='M', color='#000000', badge='Cover Concepts',
                     desc='Concept-stage cover art and character visual references before commissioning a professional designer. V8 produces editorial-quality imagery.',
                     url='https://www.midjourney.com/?via=toolforge'),
                dict(name='Grammarly', initial='G', color='#15c39a', badge='Line Edit Pass',
                     desc='The last pass grammar/style checker before submitting to agents or self-publishing. The 2026 model catches long-range repetition issues earlier passes miss.',
                     url='https://grammarly.com/?via=toolforge')],
         verdict='Start with Claude or ChatGPT for drafting assist, add Sudowrite if you want a fiction-native UI, and treat ElevenLabs + Grammarly as your polishing pair. AI won\'t write your novel — but it will cut weeks off your revision cycle.'),

    dict(slug='best-ai-tools-for-medical-billing-2026', title='Best AI Tools for Medical Billing in 2026: Cut Denials and Cash-Flow Lag',
         meta='We evaluated the leading AI-powered medical billing, coding, and denial-management tools of 2026 — ranked by denial reduction, coding accuracy, and integration fit.',
         category='Industry AI Tools', read='9 min read',
         lead='Denial rates average 10-15% across US healthcare in 2026, and a meaningful slice of those are preventable with better coding + claims scrubbing. These AI billing tools recover that revenue automatically — here\'s the shortlist that actually pays for itself.',
         tools=[dict(name='Abridge', initial='A', color='#2563eb', badge='Top Pick',
                     desc='Ambient clinical documentation that auto-generates billing-ready structured notes. Recovers lost coding detail and integrates with Epic, Athena, and eClinicalWorks.',
                     url='https://www.abridge.com/?via=toolforge'),
                dict(name='Nuance DAX', initial='N', color='#6b21a8', badge='Enterprise',
                     desc='Microsoft-owned ambient AI for large systems; adds codified documentation straight to Epic workflows with strong specialty coverage.',
                     url='https://www.nuance.com/?via=toolforge'),
                dict(name='Tali AI', initial='T', color='#ef4444', badge='Small Practice',
                     desc='Affordable ambient scribe + coding assist for independent clinics. Claims scrubbing is lighter than Abridge but priced for under-20-provider practices.',
                     url='https://tali.ai/?via=toolforge'),
                dict(name='athenahealth', initial='A', color='#00a88e', badge='Integrated RCM',
                     desc='Not a new AI entrant, but its built-in AI-powered claims intelligence remains one of the best ROI-managed care stack choices for US physician groups.',
                     url='https://www.athenahealth.com/?via=toolforge'),
                dict(name='Athelas', initial='A', color='#f59e0b', badge='Denial Recovery',
                     desc='AI-native revenue cycle management with automated appeal generation and real-time payer-behavior tracking. Commonly recovers 5-12% of previously written-off revenue.',
                     url='https://www.athelas.com/?via=toolforge'),
                dict(name='Suki AI', initial='S', color='#0ea5e9', badge='ICU & ED',
                     desc='Ambient AI tuned for high-acuity settings; auto-captures ICD-10 specificity that ED physicians typically undertype.',
                     url='https://www.suki.ai/?via=toolforge')],
         verdict='Abridge earns the top spot for system-wide integration and code-capture depth. Below the 20-provider line, Tali AI or a Suki/Athelas combo usually pays for itself in 60-90 days. Denial avoidance alone typically covers the license cost.'),
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
