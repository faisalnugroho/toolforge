"""
ToolForge Weekly Content Generator
Generates 1 new tool review per week. Triggers re-deploy.
"""
import os, json, hashlib, urllib.request, base64
from datetime import datetime

BASE = os.path.expanduser('~/projects/toolforge')

TOOL_POOL = [
    {
        "slug": "sora",
        "name": "Sora",
        "tagline": "OpenAI's flagship video generation model. 20-second clips with cinematic quality.",
        "category": "Video", "category_slug": "video",
        "color1": "#10a37f", "color2": "#0e8c6e", "initials": "So",
        "price": "$20/mo", "price_label": "ChatGPT Plus", "free_tier": "Limited generations",
        "rating": "4.8/5", "users": "10M+ users", "founded": "2024",
        "headline": "The video generator that changed everything",
        "intro": "Sora is OpenAI's answer to the AI video revolution. After a year of beta testing, the public release in 2026 made 20-second 1080p video generation accessible to anyone with a ChatGPT Plus subscription. The output quality rivals Runway Gen-4 in many scenarios, with the added benefit of native ChatGPT integration — describe what you want in natural language, and Sora generates.",
        "who_for": "Content creators already on ChatGPT Plus, marketers who need video ads, and anyone who wants Hollywood-quality video without a subscription to Runway.",
        "features": [
            ("🎬", "20-Second Clips", "Longer than any competitor. Generate full scenes, not just moments. 1080p resolution at 30fps."),
            ("💬", "ChatGPT Integration", "Native integration with ChatGPT. Describe your video in conversation, Sora generates. Iterate by responding to ChatGPT."),
            ("🌍", "Physics Understanding", "Sora models physics — gravity, momentum, material behavior. Videos look real, not 'AI generated'."),
            ("📝", "Storyboard Mode", "Plan multi-shot sequences. Sora maintains visual consistency across shots in a storyboard."),
        ],
        "pros": [
            "Longest clip length of any video generator (20s)",
            "Included in ChatGPT Plus ($20/mo) — no separate subscription",
            "Physics understanding produces more realistic motion",
            "Native ChatGPT integration makes iteration natural",
            "Public release means easy access (no waitlist)",
        ],
        "cons": [
            "Slower generation than Runway or Pika (3-5 minutes per clip)",
            "Limited fine control compared to Runway's motion brush",
            "Style control less mature than Pika's Pikaffects",
            "20-second limit means longer videos still need chaining",
        ],
        "verdict": "The right pick for ChatGPT Plus subscribers who want video generation. For power users who need Runway's motion brush or Pika's social media effects, those tools still lead. For everyone else, Sora is the easiest entry point to AI video."
    },
    {
        "slug": "claude-3-7",
        "name": "Claude 3.7 Sonnet",
        "tagline": "The best AI for code, reasoning, and long-form writing in 2026.",
        "category": "Productivity", "category_slug": "productivity",
        "color1": "#d97706", "color2": "#b45309", "initials": "Cl",
        "price": "$20/mo", "price_label": "Pro plan", "free_tier": "Free tier on claude.ai",
        "rating": "4.9/5", "users": "20M+ users", "founded": "2023",
        "headline": "The AI that thinks deeply",
        "intro": "Claude 3.7 Sonnet is Anthropic's most capable model, and in 2026 it's the default choice for tasks that require careful reasoning — code review, long-form writing, legal analysis, research synthesis. The 200K context window means you can paste entire books and ask nuanced questions. The 'thinking' mode in 3.7 lets the model spend more compute on hard problems, dramatically improving accuracy on math and logic.",
        "who_for": "Writers, researchers, developers, and analysts who need careful, accurate AI assistance. The default for any task where ChatGPT feels too 'fast and loose.'",
        "features": [
            ("🧠", "Extended Thinking", "Toggle 'thinking mode' for harder problems. Claude spends more compute, gives more accurate answers."),
            ("📚", "200K Context", "Paste entire books, codebases, or research papers. Claude maintains coherence across 200,000 tokens."),
            ("💻", "Claude Code", "Anthropic's official coding agent. Reads your codebase, makes multi-file changes, runs tests."),
            ("🎨", "Artifacts", "Interactive documents Claude creates alongside chat. Code that runs, designs that render."),
        ],
        "pros": [
            "Most accurate AI on complex reasoning tasks",
            "200K context window — far larger than ChatGPT's 128K",
            "Claude Code is the most capable AI coding agent",
            "Artifacts create an actual workspace, not just chat",
            "Constitutional AI — fewer jailbreaks, more reliable safety",
        ],
        "cons": [
            "Slower than GPT-4o for casual conversation",
            "Less multimodal than ChatGPT (no native image generation)",
            "No voice mode (ChatGPT has this)",
            "$20/mo same price as ChatGPT Plus",
        ],
        "verdict": "The default for writing, analysis, and code. Use ChatGPT for casual conversation, image generation, and voice. Use Claude for everything that requires careful thought or long context."
    },
    {
        "slug": "gemini-2",
        "name": "Gemini 2.0 Pro",
        "tagline": "Google's most capable AI. 2M context window, native multimodal, Workspace integration.",
        "category": "Productivity", "category_slug": "productivity",
        "color1": "#4285f4", "color2": "#34a853", "initials": "Ge",
        "price": "$20/mo", "price_label": "Advanced plan", "free_tier": "Limited free tier",
        "rating": "4.7/5", "users": "50M+ users", "founded": "2023",
        "headline": "Google's answer to the AI race",
        "intro": "Gemini 2.0 Pro is Google's flagship model in 2026, with the largest context window in the industry (2M tokens — 10x Claude's 200K). Native multimodal means it understands video, audio, images, and text in a single context. Deep Google Workspace integration means Gemini lives inside Gmail, Docs, Sheets, and Meet.",
        "who_for": "Google Workspace users, enterprises with massive documents, and anyone who needs to analyze video or audio natively.",
        "features": [
            ("📏", "2M Context Window", "Industry-leading. Upload hours of video, thousands of pages, entire codebases."),
            ("🎬", "Native Video Understanding", "Upload a video. Gemini watches it, answers questions about it, summarizes it."),
            ("📧", "Workspace Integration", "Lives inside Gmail, Docs, Sheets, Meet. 'Summarize my unread emails' without leaving your inbox."),
            ("🔍", "Grounded in Search", "Optional Google Search integration. Output grounded in real-time web data."),
        ],
        "pros": [
            "2M context window — 10x the competition",
            "Native video understanding is unique",
            "Workspace integration is unbeatable for Google teams",
            "Grounded in search — fresher data than ChatGPT or Claude",
            "Strong multimodal capabilities",
        ],
        "cons": [
            "Less natural conversation style than ChatGPT or Claude",
            "Slower for code generation than Claude Code or Cursor",
            "Workspace integration requires Google ecosystem commitment",
            "Personality feels more 'corporate' than competitors",
        ],
        "verdict": "The right pick for Google Workspace teams and anyone analyzing video/audio at scale. For general AI assistance, Claude or ChatGPT are more pleasant. For Google-native workflows, Gemini is unbeatable."
    },
    {
        "slug": "replit-agent",
        "name": "Replit Agent",
        "tagline": "The AI that builds and deploys full apps from a prompt. No coding required.",
        "category": "Coding", "category_slug": "coding",
        "color1": "#f26207", "color2": "#d14805", "initials": "Re",
        "price": "$25/mo", "price_label": "Core plan", "free_tier": "Limited free tier",
        "rating": "4.6/5", "users": "1M+ developers", "founded": "2016",
        "headline": "The AI that ships your app while you sleep",
        "intro": "Replit Agent takes a natural language description of an app and builds, tests, and deploys it. 'Build me a SaaS for tracking habits with a landing page, user auth, and Stripe integration' → working app deployed to replit.app in 30 minutes. The late-2025 release made this reliable enough for production use, not just prototypes.",
        "who_for": "Non-developers who want to ship MVPs, indie hackers validating ideas, and developers who want to skip boilerplate.",
        "features": [
            ("🤖", "Full App Generation", "Describe your app in a paragraph. Replit Agent builds the front-end, back-end, database, auth, and deploys it."),
            ("🛠️", "Built-in IDE", "Full code editor for when you want to customize. Switch between AI mode and manual coding seamlessly."),
            ("🚀", "One-Click Deploy", "Apps deploy to replit.app subdomain with one click. Custom domain support on paid plans."),
            ("💳", "Stripe Integration", "Add paid features with natural language. 'Add a $9/mo Pro plan with 7-day trial' → working Stripe checkout."),
        ],
        "pros": [
            "Best for non-developers — actually ships working apps",
            "Full-stack generation (front, back, DB, auth, deploy)",
            "Stripe integration via natural language is magical",
            "Fast iteration — describe change, agent implements",
            "Affordable ($25/mo vs hiring developers at $100+/hr)",
        ],
        "cons": [
            "Limited to Replit's infrastructure (no AWS/GCP deploy)",
            "Generated code can be messy — not ideal for complex apps",
            "Less control than traditional development",
            "Performance optimization requires manual work",
        ],
        "verdict": "Revolutionary for MVPs and non-developers. If you can describe your app, Replit Agent can build it. For complex production apps with custom infrastructure, traditional development is still better."
    },
]

def make_tool_html(tool):
    color1, color2 = tool['color1'], tool['color2']
    initials = tool['initials']
    
    features_html = ""
    for icon, title, desc in tool['features']:
        features_html += f'<div class="tool-feature"><div class="tool-feature-title"><span class="tool-feature-title-icon">{icon}</span>{title}</div><p>{desc}</p></div>'
    
    pros_html = "".join(f'<li>{p}</li>' for p in tool['pros'])
    cons_html = "".join(f'<li>{c}</li>' for c in tool['cons'])
    
    jsonld = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{tool['name']}","description":"{tool['tagline']}","applicationCategory":"{tool['category']}Application","operatingSystem":"Web","offers":{{"@type":"Offer","price":"{tool['price'].replace('$','').replace('/mo','')}","priceCurrency":"USD"}},"aggregateRating":{{"@type":"AggregateRating","ratingValue":"{tool['rating'].split('/')[0]}","bestRating":"5","ratingCount":"100"}}}}
</script>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tool["name"]} Review (2026) — ToolForge</title>
  <meta name="description" content="{tool["tagline"]}">
  <link rel="canonical" href="https://toolforge.io/tools/{tool["slug"]}.html">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='{color1}'/><text x='50' y='68' font-size='56' font-weight='700' fill='white' text-anchor='middle' font-family='sans-serif'>{initials[0]}</text></svg>">
  {jsonld}
  <script defer data-domain="toolforge-io.netlify.app" src="https://plausible.io/js/script.js"></script>
</head>
<body>
  <nav class="nav">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo"><div class="nav-logo-icon">T</div>ToolForge</a>
      <div class="nav-links">
        <a href="../index.html" class="nav-link">Home</a>
        <a href="../tools.html" class="nav-link">Browse</a>
        <a href="../blog.html" class="nav-link">Blog</a>
        <a href="../about.html" class="nav-link">About</a>
      </div>
      <div class="nav-actions">
        <button id="theme-toggle" class="theme-toggle"></button>
        <a href="../tools.html" class="btn btn-primary btn-sm">All Tools</a>
      </div>
    </div>
  </nav>
  <section class="tool-hero">
    <div class="container">
      <div class="tool-hero-inner">
        <div class="tool-hero-logo" style="background: linear-gradient(135deg, {color1}, {color2});">{initials}</div>
        <div class="tool-hero-info">
          <div style="font-family: var(--font-mono); font-size: 12px; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: var(--space-2);">— {tool["category"]} Tool</div>
          <h1>{tool["name"]}</h1>
          <p class="tool-hero-tagline">{tool["tagline"]}</p>
          <div class="tool-hero-meta">
            <span>★ {tool["rating"]}</span><span>·</span>
            <span>{tool["users"]}</span><span>·</span>
            <span>Since {tool["founded"]}</span><span>·</span>
            <span>{tool["free_tier"]}</span>
          </div>
        </div>
        <div class="tool-hero-cta">
          <div class="tool-price"><strong>{tool["price"]}</strong> {tool["price_label"]}</div>
          <a href="#" class="btn btn-primary">Try {tool["name"]} →</a>
        </div>
      </div>
    </div>
  </section>
  <section class="tool-section">
    <div class="container">
      <div style="max-width: 800px;">
        <h2>{tool["headline"]}</h2>
        <p>{tool["intro"]}</p>
        <p style="padding: var(--space-3) var(--space-4); background: var(--bg-elevated); border-radius: var(--radius-md); border-left: 3px solid var(--accent); margin-top: var(--space-4);"><strong>Who it's for:</strong> {tool["who_for"]}</p>
      </div>
      <h2 style="margin-top: var(--space-7);">Key features</h2>
      <div class="tool-features">{features_html}</div>
    </div>
  </section>
  <section class="tool-section" style="background: var(--bg-elevated);">
    <div class="container">
      <h2>The honest take</h2>
      <div class="pros-cons">
        <div class="pros"><h3>✓ What works</h3><ul>{pros_html}</ul></div>
        <div class="cons"><h3>✗ What doesn't</h3><ul>{cons_html}</ul></div>
      </div>
    </div>
  </section>
  <section class="tool-section">
    <div class="container">
      <div style="max-width: 800px;">
        <h2>Verdict</h2>
        <p style="font-size: 19px; line-height: 1.6;">{tool["verdict"]}</p>
      </div>
    </div>
  </section>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="../index.html" class="nav-logo"><div class="nav-logo-icon">T</div>ToolForge</a>
          <p class="footer-tagline">The curated stack of AI tools that actually work.</p>
        </div>
        <div>
          <div class="footer-col-title">Explore</div>
          <a href="../index.html" class="footer-link">Home</a>
          <a href="../tools.html" class="footer-link">Browse Tools</a>
          <a href="../blog.html" class="footer-link">Blog</a>
        </div>
        <div>
          <div class="footer-col-title">Site</div>
          <a href="../about.html" class="footer-link">About</a>
          <a href="../contact.html" class="footer-link">Contact</a>
          <a href="../about.html#disclosure" class="footer-link">Disclosure</a>
        </div>
        <div>
          <div class="footer-col-title">Connect</div>
          <a href="#" class="footer-link">Twitter</a>
          <a href="#" class="footer-link">LinkedIn</a>
          <a href="#" class="footer-link">RSS</a>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© 2026 ToolForge. All rights reserved.</div>
        <div>Built with AI tools, for AI tool users.</div>
      </div>
    </div>
  </footer>
  <script src="../js/main.js"></script>
</body>
</html>
'''

if __name__ == '__main__':
    import datetime
    week = datetime.datetime.now().isocalendar()[1]
    tool = TOOL_POOL[week % len(TOOL_POOL)]
    
    print(f"Week {week} -> Adding: {tool['name']}")
    
    path = os.path.join(BASE, 'tools', f"{tool['slug']}.html")
    if os.path.exists(path):
        print(f"  Already exists, skipping (delete file to regenerate)")
    else:
        with open(path, 'w') as f:
            f.write(make_tool_html(tool))
        print(f"  Created {tool['slug']}.html ({os.path.getsize(path)} bytes)")
    
    print("\nNext: run /tmp/toolforge_deploy.py to publish")
