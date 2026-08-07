"""ToolForge batch 2026-08-07 B — 2 tools + 2 compares + 2 blogs (head-exec of _sprint_gen.py)."""
import os
BASE = os.path.expanduser('~/projects/toolforge')
os.chdir(BASE)
TODAY = '2026-08-07'

# --- load template head (constants + tool_html / compare_html / blog_html) ---
head = open('_sprint_gen.py').read().split('# =================== CONTENT DATA ===================')[0]
g = {'TODAY': TODAY, 'DOMAIN': 'https://toolforge.io'}
exec(head, g)
tool_html = g['tool_html']; compare_html = g['compare_html']; blog_html = g['blog_html']

TOOLS = [
  dict(
    slug='mistral-medium-3', name='Mistral Medium 3', category='AI',
    tagline='Mistral\'s mid-size frontier model: near-flagship quality at a fraction of Large pricing.',
    color1='#ff7000', color2='#ffb020', initials='MM',
    rating='4.7', rating_num='4.7', users='1M+ developers', founded='2023', free_tier='API free tier',
    price='$0.40', price_num='0.40', price_label='/ 1M input tokens', cta_url='https://mistral.ai/?via=toolforge',
    headline='Frontier-class performance without frontier-class pricing',
    intro='Mistral Medium 3 occupies the sweet spot between Mistral Large and Small: it beats Claude Sonnet 3.7 on most benchmarks at roughly one-eighth the API cost, and supports multimodal input plus function calling out of the box.',
    who_for='Cost-conscious teams running high-volume production workloads who still need near-flagship quality.',
    features=[
      ('💰', '8x cheaper than Large', 'MMLU, HumanEval and MATH scores within a few points of flagship models at ~$0.40/M input tokens.'),
      ('📷', 'Multimodal input', 'Understands images, documents and charts alongside text — no separate vision endpoint needed.'),
      ('🔧', 'Native function calling', 'Structured outputs and tool use are first-class, so agents and RAG pipelines work out of the box.'),
      ('🏗️', 'Deploy anywhere', 'Available via La Plateforme, Azure AI, Amazon Bedrock, and self-hosted weights for enterprise.'),
      ('🌍', 'Strong multilingual', 'Especially good on European languages versus US-centric competitors.'),
      ('⚡', 'Low latency streaming', 'Fast token generation suitable for chat UX and real-time copilots.'),
    ],
    pros=[
      'Outstanding price-to-performance — beats models 8x its cost on standard benchmarks',
      'Multimodal and function calling included at the same price point',
      'Self-host option via Azure/Bedrock/on-prem for data-residency compliance',
      'Strong multilingual coverage, especially EU languages',
    ],
    cons=[
      'Still a step behind Mistral Large / GPT-5 / Claude Opus on the hardest reasoning tasks',
      'Smaller context window than flagship peers (128K vs 200K+)',
      'Ecosystem and tooling less mature than OpenAI or Anthropic',
    ],
    verdict='If your bill is scaling faster than your traffic, Mistral Medium 3 is the first place to look. It delivers 90% of frontier quality for a tenth of the price, with real multimodal and function-calling support. For the last 10% of hard reasoning, keep a flagship on standby — but route the default path here.',
  ),
  dict(
    slug='perplexity-sonar-pro', name='Perplexity Sonar Pro', category='Search',
    tagline='Perplexity\'s API-first answer engine with citations, built for products that need grounded search.',
    color1='#20b2aa', color2='#1f8f89', initials='SP',
    rating='4.6', rating_num='4.6', users='100K+ apps', founded='2022', free_tier='Free credits',
    price='$5', price_num='5', price_label='/ 1K requests', cta_url='https://perplexity.ai/?via=toolforge',
    headline='Grounded answers with citations, delivered as an API',
    intro='Sonar Pro is Perplexity\'s flagship search-augmented LLM exposed as a developer API. Unlike generic chat models, every response is grounded in live web results with inline citations — ideal for products, agents, and research tools that need verifiable answers rather than hallucinated ones.',
    who_for='Builders shipping search, research or answer-engine features who want Perplexity-quality grounding without building their own RAG pipeline.',
    features=[
      ('🔗', 'Inline citations', 'Every factual claim is backed by a source link — critical for trust, fact-checking, and compliance.'),
      ('🌐', 'Live web grounding', 'Real-time index, no knowledge cutoff. Answers reflect today, not 6 months ago.'),
      ('🔎', 'Deep research mode', 'Sonar Pro runs multi-step queries to synthesize conclusions across dozens of pages.'),
      ('⚙️', 'Simple REST API', 'Drop-in replacement for chat-completion APIs — same shape, just grounded.'),
      ('📊', 'Structured output', 'Ask for JSON answers with citations as first-class fields.'),
      ('💰', 'Predictable pricing', 'Per-request pricing with a free tier — no surprises at volume.'),
    ],
    pros=[
      'Only major API where citations are a first-class primitive, not an afterthought',
      'Live web grounding built-in — no separate search API to wire up',
      'Competitive pricing versus building your own retrieval + LLM stack',
      'Trusted Perplexity quality without hiring a research team',
    ],
    cons=[
      'Per-request cost adds up at consumer-scale volumes',
      'Less customization than rolling your own RAG (no custom index weighting)',
      'Latency higher than non-grounded models — search takes time',
    ],
    verdict='If your product needs to answer "what\'s true right now" with receipts, Sonar Pro is the fastest path to shipping. Skip it only if you have very specific index requirements or billions of requests — otherwise the build-vs-buy math strongly favors buying.',
  ),
]

COMPARES = [
  dict(
    slug='mistral-medium-3-vs-claude-haiku-4-5',
    name_a='Mistral Medium 3', name_b='Claude Haiku 4.5',
    color_a='#ff7000', color_b='#d97757', initials_a='MM', initials_b='CH',
    desc_a='Mistral\'s mid-size frontier model — multi-modal, function-calling, ~8x cheaper than flagship.', 
    desc_b='Anthropic\'s newest small model — Claude 4.5 quality at Haiku speed and cost.',
    price_a='$0.40/M input', price_b='$1/M input',
    best_a='Cost-perf at scale', best_b='Long-context chat',
    url_a='https://mistral.ai/?via=toolforge', url_b='https://anthropic.com/?via=toolforge',
    verdict='Pick Mistral Medium 3 if you\'re optimizing for cost at high volume and can live with 128K context. Pick Claude Haiku 4.5 if you need Anthropic\'s constitutional-AI safety profile, 200K context, or tight AWS Bedrock integration. On raw benchmark-per-dollar, Mistral wins decisively — that\'s the whole product thesis.',
    winner='Mistral Medium 3 for cost-perf; Haiku 4.5 for long context and safety',
  ),
  dict(
    slug='perplexity-sonar-vs-chatgpt-search',
    name_a='Perplexity Sonar', name_b='ChatGPT Search',
    color_a='#20b2aa', color_b='#10a37f', initials_a='PS', initials_b='CS',
    desc_a='Perplexity\'s search-native LLM, built from day one around citations and live web grounding.',
    desc_b='OpenAI\'s answer engine inside ChatGPT — GPT-5 with real-time browsing and inline sources.',
    price_a='Free / $20 Pro', price_b='Free / $20 Plus',
    best_a='Deep research and citations', best_b='Conversational follow-ups',
    url_a='https://perplexity.ai/?via=toolforge', url_b='https://openai.com/?via=toolforge',
    verdict='Perplexity Sonar wins when the question is open-ended research and you want verifiable sources — its citation density and multi-step reasoning are unmatched. ChatGPT Search wins when the search is one step in a longer task, because it inherits ChatGPT\'s full toolset (canvas, code interpreter, image gen). Power users end up paying for both; casual users should start with whichever they already use.',
    winner='Perplexity Sonar for research; ChatGPT Search as a general assistant',
  ),
]

BLOGS = [
  dict(
    slug='best-ai-tools-for-ux-writers-2026',
    title='The 8 Best AI Tools for UX Writers in 2026 (Tested)',
    category='UX Writing', read='11',
    meta='The 8 AI tools UX writers actually use in 2026 — for microcopy, tone-of-voice consistency, user research synthesis, and shipping error-free strings at scale.',
    lead='UX writing is finally getting the AI tooling it deserves. In 2026 you can draft microcopy, enforce tone of voice across a whole app, and synthesize user research in hours instead of weeks. These are the 8 tools worth paying for.',
    verdict='ChatGPT and Claude cover 80% of UX writing needs. Add Frontitude or Ditto for string management, Grammarly for consistency, and Perplexity for competitive research. The best-paid upgrade is whichever one removes your current bottleneck — start free, then consolidate.',
    tools=[
      dict(name='ChatGPT', url='https://openai.com/?via=toolforge', color='#10a37f', initial='CG', badge='Best overall', desc='The default for microcopy drafts, error-message rewrites, and tone-of-voice brainstorming. Canvas mode is ideal for iterating on strings in context.'),
      dict(name='Claude', url='https://anthropic.com/?via=toolforge', color='#d97757', initial='CL', badge='Best for long-form', desc='Better long-context reasoning makes Claude ideal for onboarding flows, help docs, and in-app education. Superior instruction-following on tone.'),
      dict(name='Grammarly', url='https://grammarly.com/?via=toolforge', color='#15c39a', initial='GR', badge='Best for consistency', desc='Style guides plus tone detection ensure every writer ships on-brand copy. Browser + IDE integrations cover everywhere strings live.'),
      dict(name='Frontitude', url='https://frontitude.com/?via=toolforge', color='#6366f1', initial='FR', badge='Best UX-specific', desc='Purpose-built for product copy: syncs with Figma, manages strings in one place, and uses AI to keep tone consistent across screens.'),
      dict(name='Ditto', url='https://dittowords.com/?via=toolforge', color='#f59e0b', initial='DI', badge='Best for teams', desc='String management plus AI suggestions. Keeps design, engineering, and writing in sync from Figma to production.'),
      dict(name='Perplexity', url='https://perplexity.ai/?via=toolforge', color='#20b2aa', initial='PX', badge='Best for research', desc='Competitive copy audits, terminology research, and user-language mining from forums and reviews — with citations you can trust.'),
      dict(name='Notion AI', url='https://notion.so/?via=toolforge', color='#000000', initial='NA', badge='Best workspace', desc='Draft, review, and version strings where the team already lives. Inline AI edits are fast for polishing error messages and empty states.'),
      dict(name='Figma AI', url='https://figma.com/?via=toolforge', color='#a259ff', initial='FG', badge='Best in-design', desc='Generate and edit copy directly on mocks. Best when writing and design happen in the same pass, not as a handoff.'),
    ],
  ),
  dict(
    slug='ai-tools-for-fintech-startups-2026',
    title='The 9 Best AI Tools for Fintech Startups in 2026',
    category='Fintech', read='12',
    meta='The 9 AI tools fintech startups use in 2026 — fraud detection, KYC, compliance, underwriting, customer support, and analytics — tested and ranked.',
    lead='Fintech moves fast and regulators move slowly — but AI is eating both sides. These 9 tools let a small team ship fraud detection, KYC, underwriting, and support that used to require a 50-person ops org.',
    verdict='Chatbot support (Decagon, Intercom Fin) pays for itself fastest. Compliance (Norm Ai, Greenlite) is non-negotiable for licensed products. Underwriting and fraud (Zest AI, Sardine) are worth the enterprise pricing once you have volume. Everything else is a productivity multiplier on a small team.',
    tools=[
      dict(name='Decagon', url='https://decagon.ai/?via=toolforge', color='#7c3aed', initial='DE', badge='Best support agent', desc='AI agents that resolve real fintech support issues — disputes, chargebacks, KYC questions — without human handoff. Built for regulated industries.'),
      dict(name='Intercom Fin', url='https://intercom.com/?via=toolforge', color='#0a72ef', initial='IN', badge='Best existing users', desc='If you already use Intercom, Fin 2 is the obvious support upgrade. Handles 50%+ of tier-1 questions for most fintechs.'),
      dict(name='Norm Ai', url='https://norm.ai/?via=toolforge', color='#065f46', initial='NO', badge='Best compliance', desc='Regulatory AI trained on SEC, FINRA, and state rules. Turns marketing review and compliance checks from days to minutes.'),
      dict(name='Greenlite', url='https://greenlite.com/?via=toolforge', color='#10b981', initial='GR', badge='Best AML', desc='AI agents for AML/BSA — automates alert triage, case investigation, and SAR narratives. Used by major fintechs and community banks.'),
      dict(name='Sardine', url='https://sardine.ai/?via=toolforge', color='#dc2626', initial='SA', badge='Best fraud', desc='Real-time fraud, KYC and payments intelligence. Device, behavioral and transactional signals combined with explainable AI.'),
      dict(name='Zest AI', url='https://zest.ai/?via=toolforge', color='#eab308', initial='ZE', badge='Best underwriting', desc='AI underwriting that increases approval rates while reducing defaults. Required reading if you lend money at scale.'),
      dict(name='ChatGPT', url='https://openai.com/?via=toolforge', color='#10a37f', initial='CG', badge='Best general assistant', desc='Product specs, compliance memos, incident comms, and engineering copilot. The default for every non-specialized task.'),
      dict(name='Notion AI', url='https://notion.so/?via=toolforge', color='#000000', initial='NA', badge='Best workspace', desc='Fintechs run on docs. Notion AI keeps product specs, runbooks, and regulatory notes searchable and up to date.'),
      dict(name='ElevenLabs', url='https://elevenlabs.io/?via=toolforge', color='#6b21a8', initial='EL', badge='Best voice AI', desc='Voice agents for IVR, account verification, and proactive outreach. Multilingual support matters for global fintech.'),
    ],
  ),
]

# --- safety checks ---
existing_tools = set(os.listdir('tools')); existing_cmp = set(os.listdir('compare')); existing_blog = set(os.listdir('blog'))
for t in TOOLS:
    assert (t['slug']+'.html') not in existing_tools, "tool dup: "+t['slug']
for c in COMPARES:
    assert (c['slug']+'.html') not in existing_cmp, "cmp dup: "+c['slug']
for b in BLOGS:
    assert (b['slug']+'.html') not in existing_blog, "blog dup: "+b['slug']
    for tt in b['tools']:
        assert tt['url'].startswith('https://'), "url must be full https: "+tt['url']
        bg = tt['color']
        assert bg.lower() not in ('#ffffff','#fff','white'), "white bg won't show"

wrote=[]
for t in TOOLS:
    p='tools/'+t['slug']+'.html'
    html = tool_html(t)
    open(p,'w').write(html); wrote.append(p)
for c in COMPARES:
    p='compare/'+c['slug']+'.html'
    html = compare_html(c)
    open(p,'w').write(html); wrote.append(p)
for b in BLOGS:
    p='blog/'+b['slug']+'.html'
    html = blog_html(b)
    # post-process stale literals
    html = html.replace('"datePublished": "2026-07-11"','"datePublished": "'+TODAY+'"')
    html = html.replace('"dateModified": "2026-07-11"','"dateModified": "'+TODAY+'"')
    html = html.replace('Published June 2026','Published August 2026')
    open(p,'w').write(html); wrote.append(p)

print("WROTE:")
for p in wrote: print("  ", p, os.path.getsize(p), "bytes")
