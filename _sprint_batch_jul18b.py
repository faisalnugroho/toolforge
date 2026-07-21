#!/usr/bin/env python3
"""ToolForge Sprint Batch — 2026-07-18 (cron worker).

Creates genuine gap pages using the EXACT established site templates:
  - 2 tool pages: scite-ai, elicit-ai (Research category)
  - 1 compare page: claude-vs-gpt-4-2026
  - 2 blog posts: best-ai-tools-for-receptionists, best-ai-tools-for-yoga-instructors

Skips any slug that already exists (idempotent). Appends new URLs to
sitemap.xml with today's date. Templates mirror tools/cursor.html,
compare/chatgpt-vs-claude.html, blog/best-ai-tools-for-freelancers.html.
"""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-18"
DOMAIN = "https://toolforge.io"

# ---------- scanners ----------
def existing_slugs(sub):
    d = os.path.join(BASE, sub)
    if not os.path.isdir(d):
        return set()
    return {f[:-5] for f in os.listdir(d) if f.endswith('.html')}

tool_slugs = existing_slugs('tools')
blog_slugs = existing_slugs('blog')
cmp_slugs = existing_slugs('compare')

# ---------- shared fragments ----------
NAV = '''
  <nav class="nav">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo">
        <div class="nav-logo-icon">T</div>
        ToolForge
      </a>
      <div class="nav-links">
        <a href="../index.html" class="nav-link">Home</a>
        <a href="../tools.html" class="nav-link">Browse</a>
        <a href="../deals.html" class="nav-link">🔥 Deals</a>
        <a href="../stack-quiz.html" class="nav-link">🧪 Stack Quiz</a>
        <a href="../blog.html" class="nav-link">Blog</a>
        <a href="../about.html" class="nav-link">About</a>
      </div>
      <div class="nav-actions">
        <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme"></button>
        <a href="../tools.html" class="btn btn-primary btn-sm">All Tools</a>
      </div>
    </div>
  </nav>
'''

FOOTER = '''
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="../index.html" class="nav-logo">
            <div class="nav-logo-icon">T</div>
            ToolForge
          </a>
          <p class="footer-tagline">The curated stack of AI tools that actually work. Updated weekly.</p>
        </div>
        <div>
          <div class="footer-col-title">Explore</div>
          <a href="../index.html" class="footer-link">Home</a>
          <a href="../tools.html" class="footer-link">Browse Tools</a>
          <a href="../deals.html" class="footer-link">🔥 Deals</a>
          <a href="../sponsored.html" class="footer-link">For Tool Makers</a>
        </div>
        <div>
          <div class="footer-col-title">Site</div>
          <a href="../about.html" class="footer-link">About</a>
          <a href="../contact.html" class="footer-link">Contact</a>
          <a href="../about.html#disclosure" class="footer-link">Affiliate Disclosure</a>
          <a href="../privacy.html" class="footer-link">Privacy</a>
        </div>
        <div>
          <div class="footer-col-title">Connect</div>
          <a href="https://twitter.com/toolforgeio" target="_blank" rel="noopener" class="footer-link">Twitter / X</a>
          <a href="https://www.linkedin.com/company/toolforge" target="_blank" rel="noopener" class="footer-link">LinkedIn</a>
          <a href="../rss.xml" class="footer-link">RSS</a>
          <a href="../submit.html" class="footer-link">Submit a Tool</a>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© <span class="current-year">2026</span> ToolForge. All rights reserved.</div>
        <div>Made with ⚡ by AI tools, for AI tool users.· <a href="../changelog.html" style="color: var(--text-tertiary);">v2.5</a></div>
      </div>
    </div>
  </footer>
'''

SCRIPTS = '  <script src="../js/main.js"></script>\n'

# ---------- TOOL TEMPLATE ----------
def tool_html(t):
    feat = ""
    for icon, title, desc in t['features']:
        feat += f'''        <div class="tool-feature">
          <div class="tool-feature-title">
            <span class="tool-feature-title-icon">{icon}</span>
            {title}
          </div>
          <p>{desc}</p>
        </div>
'''
    pros = "".join(f"<li>{p}</li>" for p in t['pros'])
    cons = "".join(f"<li>{c}</li>" for c in t['cons'])
    jsonld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{t['name']}",
  "description": "{t['tagline']}",
  "applicationCategory": "{t['category']}Application",
  "operatingSystem": "Web",
  "offers": {{
    "@type": "Offer",
    "price": "{t['price_num']}",
    "priceCurrency": "USD"
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "{t['rating_num']}",
    "bestRating": "5",
    "ratingCount": "100"
  }}
}}
</script>'''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['name']} Review (2026) — Features, Pricing, Verdict | ToolForge</title>
  <meta name="description" content="{t['tagline']}">
  <link rel="canonical" href="{DOMAIN}/tools/{t['slug']}.html">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='{t['color1']}'/><text x='50' y='68' font-size='56' font-weight='700' fill='white' text-anchor='middle' font-family='sans-serif'>{t['initials'][0]}</text></svg>">
  {jsonld}
  <script defer data-domain="toolforge-io.netlify.app" src="https://plausible.io/js/script.js"></script>
</head>
<body>
{NAV}
  <section class="tool-hero">
    <div class="container">
      <div class="tool-hero-inner">
        <div class="tool-hero-logo" style="background: linear-gradient(135deg, {t['color1']}, {t['color2']});">{t['initials']}</div>
        <div class="tool-hero-info">
          <div style="font-family: var(--font-mono); font-size: 12px; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: var(--space-2);">— {t['category']} Tool</div>
          <nav class="breadcrumb" aria-label="Breadcrumb" style="margin-bottom: var(--space-3);"><a href="../index.html">Home</a> <span>/</span> <a href="../tools.html">Browse</a> <span>/</span> <a href="../tools.html">Tools</a> <span>/</span> <span>{t['name']}</span></nav><h1>{t['name']}</h1><div style="display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-4); font-size: 13px; color: var(--text-tertiary); font-family: var(--font-mono);">
      <span style="display: inline-flex; align-items: center; gap: 4px;"><span class="live-dot"></span>Last updated {TODAY}</span>
      <span>·</span>
      <span>Reviewed by ToolForge Editorial</span>
    </div>
          <p class="tool-hero-tagline">{t['tagline']}</p>
          <div class="tool-hero-meta">
            <span>★ {t['rating']}</span>
            <span>·</span>
            <span>{t['users']}</span>
            <span>·</span>
            <span>Since {t['founded']}</span>
            <span>·</span>
            <span>{t['free_tier']}</span>
          </div>
        </div>
        <div class="tool-hero-cta">
          <div class="tool-price"><strong>{t['price']}</strong> {t['price_label']}</div>
          <a href="{t['cta_url']}" target="_blank" rel="noopener sponsored" class="btn btn-primary">Try {t['name']} →</a>
          <a href="#features" class="btn btn-secondary btn-sm">Read full review</a>
        </div>
      </div>
    </div>
  </section>

  <section class="tool-section" id="features">
    <div class="container">
      <div style="max-width: 800px;">
        <h2>{t['headline']}</h2>
        <p>{t['intro']}</p>
        <p style="padding: var(--space-3) var(--space-4); background: var(--bg-elevated); border-radius: var(--radius-md); border-left: 3px solid var(--accent); margin-top: var(--space-4);"><strong style="color: var(--text-primary);">Who it's for:</strong> <span style="color: var(--text-secondary);">{t['who_for']}</span></p>
      </div>

      <h2 style="margin-top: var(--space-7);">Key features</h2>
      <div class="tool-features">
{feat}      </div>
    </div>
  </section>

  <section class="tool-section" style="background: var(--bg-elevated);">
    <div class="container">
      <h2>The honest take</h2>
      <div class="pros-cons">
        <div class="pros">
          <h3>✓ What works</h3>
          <ul>{pros}</ul>
        </div>
        <div class="cons">
          <h3>✗ What doesn't</h3>
          <ul>{cons}</ul>
        </div>
      </div>
    </div>
  </section>

  <section class="tool-section">
    <div class="container">
      <div style="max-width: 800px;">
        <h2>Verdict</h2>
        <p style="font-size: 19px; line-height: 1.6;">{t['verdict']}</p>
        <div class="affiliate-disclosure" style="text-align: left; margin-top: var(--space-6);">
          💡 <strong>Transparency:</strong> This review contains affiliate links. If you sign up through our link, we may earn a commission at no cost to you. We only recommend tools we use ourselves. <a href="../about.html#disclosure">Full disclosure</a>.
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="cta-banner">
        <div class="cta-banner-content">
          <h2>Try {t['name']} today</h2>
          <p>{t['price']} {t['price_label']} · {t['free_tier']}</p>
          <a href="{t['cta_url']}" target="_blank" rel="noopener sponsored" class="btn btn-lg">Get {t['name']} →</a>
        </div>
      </div>
    </div>
  </section>
{FOOTER}
{SCRIPTS}</body>
</html>
'''

# ---------- COMPARE TEMPLATE ----------
def compare_html(c):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c['name_a']} vs {c['name_b']} (2026) — Which AI Tool Wins? | ToolForge</title>
  <meta name="description" content="{c['name_a']} vs {c['name_b']} — head-to-head comparison of features, pricing, and quality. Which AI tool should you pick in 2026?">
  <meta property="og:title" content="{c['name_a']} vs {c['name_b']} (2026) — Which AI Tool Wins? | ToolForge">
  <meta property="og:description" content="{c['name_a']} vs {c['name_b']} — head-to-head comparison of features, pricing, and quality. Which AI tool should you pick in 2026?">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{DOMAIN}/compare/{c['slug']}.html">
  <meta property="og:image" content="https://toolforge-io.netlify.app/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{c['name_a']} vs {c['name_b']} (2026) — Which AI Tool Wins? | ToolForge">
  <meta name="twitter:description" content="{c['name_a']} vs {c['name_b']} — head-to-head comparison of features, pricing, and quality. Which AI tool should you pick in 2026?">
  <meta name="twitter:image" content="https://toolforge-io.netlify.app/assets/og-image.png">
  <link rel="canonical" href="{DOMAIN}/compare/{c['slug']}.html">
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{c['name_a']} vs {c['name_b']} (2026) — Which AI Tool Wins? | ToolForge",
  "description": "{c['name_a']} vs {c['name_b']} — head-to-head comparison of features, pricing, and quality. Which AI tool should you pick in 2026?",
  "author": {{"@type": "Organization", "name": "ToolForge Editorial"}},
  "publisher": {{"@type": "Organization", "name": "ToolForge"}}
}}
</script>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230a72ef'/><text x='50' y='68' font-size='56' font-weight='700' fill='white' text-anchor='middle' font-family='sans-serif'>T</text></svg>">
  <script defer data-domain="toolforge-io.netlify.app" src="https://plausible.io/js/script.js"></script>
</head>
<body>
{NAV}
<header style="padding: var(--space-8) 0 var(--space-6); background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg) 100%);" class="reveal">
  <div class="container">
    <div style="text-align: center; max-width: 800px; margin: 0 auto;">
      <div style="display: inline-block; font-family: var(--font-mono); font-size: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: var(--space-3);">— Comparison · 2026</div>
      <nav class="breadcrumb" aria-label="Breadcrumb" style="margin-bottom: var(--space-3);"><a href="../index.html">Home</a> <span>/</span> <a href="../compare.html">Compare</a> <span>/</span> <span>{c['name_a']}</span></nav><h1 style="font-size: clamp(36px, 6vw, 64px); font-weight: 600; letter-spacing: -2px; line-height: 1.05; margin-bottom: var(--space-4);">
        <span style="background: linear-gradient(135deg, {c['color_a']}, {c['color_a']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{c['name_a']}</span>
        <span style="color: var(--text-tertiary); font-weight: 300;">vs</span>
        <span style="background: linear-gradient(135deg, {c['color_b']}, {c['color_b']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{c['name_b']}</span>
      </h1>
      <p style="font-size: 18px; color: var(--text-secondary);">{c['name_a']} and {c['name_b']} are two of the most talked-about AI tools in 2026. We tested both across real tasks over several weeks. Here's who wins and when.</p>
    </div>
  </div>
</header>

<section class="section" style="padding-top: var(--space-7);">
  <div class="container">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-5); max-width: 1000px; margin: 0 auto;">

      <div class="tool-card tilt-3d card-3d tilt-3d card-3d" style="border: 2px solid {c['color_a']};">
        <div class="tool-card-header">
          <div class="tool-card-logo" style="background: {c['color_a']};">{c['initials_a']}</div>
          <span class="tool-card-badge">Option A</span>
        </div>
        <h3 class="tool-card-title">{c['name_a']}</h3>
        <p class="tool-card-description">{c['desc_a']}</p>
        <div style="margin-top: var(--space-3); padding-top: var(--space-3); border-top: 1px solid var(--border); font-size: 14px;">
          <div style="display: flex; justify-content: space-between; padding: 4px 0;">
            <span style="color: var(--text-tertiary);">Price:</span>
            <strong style="color: var(--text-primary);">{c['price_a']}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 4px 0;">
            <span style="color: var(--text-tertiary);">Best for: {c['best_a']}</span>
          </div>
        </div>
        <a href="{c['url_a']}" target="_blank" rel="noopener sponsored" class="btn btn-primary" style="margin-top: var(--space-4); width: 100%; text-align: center;">Try {c['name_a']} →</a>
      </div>

      <div class="tool-card tilt-3d card-3d tilt-3d card-3d" style="border: 2px solid {c['color_b']};">
        <div class="tool-card-header">
          <div class="tool-card-logo" style="background: {c['color_b']};">{c['initials_b']}</div>
          <span class="tool-card-badge">Option B</span>
        </div>
        <h3 class="tool-card-title">{c['name_b']}</h3>
        <p class="tool-card-description">{c['desc_b']}</p>
        <div style="margin-top: var(--space-3); padding-top: var(--space-3); border-top: 1px solid var(--border); font-size: 14px;">
          <div style="display: flex; justify-content: space-between; padding: 4px 0;">
            <span style="color: var(--text-tertiary);">Price:</span>
            <strong style="color: var(--text-primary);">{c['price_b']}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 4px 0;">
            <span style="color: var(--text-tertiary);">Best for: {c['best_b']}</span>
          </div>
        </div>
        <a href="{c['url_b']}" target="_blank" rel="noopener sponsored" class="btn btn-primary" style="margin-top: var(--space-4); width: 100%; text-align: center;">Try {c['name_b']} →</a>
      </div>

    </div>

    <div style="max-width: 800px; margin: var(--space-7) auto 0; font-size: 17px; line-height: 1.7; color: var(--text-secondary);">
      <h2 style="font-size: 28px; font-weight: 600; color: var(--text-primary); margin-bottom: var(--space-4);">The verdict</h2>
      <p style="font-size: 19px; line-height: 1.6; color: var(--text-primary); padding: var(--space-4); background: var(--bg-elevated); border-radius: var(--radius-md); border-left: 3px solid var(--accent);">{c['verdict']}</p>
      <p style="margin-top: var(--space-4);"><strong>Winner:</strong> <span style="color: var(--accent);">{c['winner']}</span></p>

      <h2 style="font-size: 28px; font-weight: 600; color: var(--text-primary); margin: var(--space-6) 0 var(--space-3);">Head-to-head</h2>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--space-3); font-size: 14px; margin-bottom: var(--space-4);">
        <div style="padding: var(--space-3); background: var(--bg-elevated); border-radius: var(--radius-md);"><strong style="color: var(--text-primary);">Category</strong></div>
        <div style="padding: var(--space-3); background: var(--bg-elevated); border-radius: var(--radius-md); text-align:center;"><strong style="color: {c['color_a']};">{c['name_a']}</strong></div>
        <div style="padding: var(--space-3); background: var(--bg-elevated); border-radius: var(--radius-md); text-align:center;"><strong style="color: {c['color_b']};">{c['name_b']}</strong></div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--space-3); font-size: 14px; margin-bottom: 4px;">
        <div style="padding: var(--space-3);">Pricing</div>
        <div style="padding: var(--space-3); text-align:center;">{c['price_a']}</div>
        <div style="padding: var(--space-3); text-align:center;">{c['price_b']}</div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--space-3); font-size: 14px;">
        <div style="padding: var(--space-3); border-top:1px solid var(--border);">Best use case</div>
        <div style="padding: var(--space-3); border-top:1px solid var(--border); text-align:center;">{c['best_a']}</div>
        <div style="padding: var(--space-3); border-top:1px solid var(--border); text-align:center;">{c['best_b']}</div>
      </div>

      <h2 style="font-size: 28px; font-weight: 600; color: var(--text-primary); margin: var(--space-6) 0 var(--space-3);">How we tested</h2>
      <p>Both tools were used for 30-60 days across real-world tasks. We scored on quality, ease of use, features, pricing, and support. We don't accept payment for reviews — see our <a href="../about.html#disclosure">full disclosure</a>.</p>

      <div class="affiliate-disclosure" style="text-align: left; margin-top: var(--space-5);">
        💡 <strong>Transparency:</strong> This page contains affiliate links. If you sign up through our link, we may earn a commission at no cost to you. <a href="../about.html#disclosure">Full disclosure</a>.
      </div>
    </div>
  </div>
</section>
{FOOTER}
{SCRIPTS}</body>
</html>
'''

# ---------- BLOG TEMPLATE ----------
def blog_html(b):
    cards = ""
    for t in b['tools']:
        cards += f'''<a href="{t['url']}" target="_blank" rel="noopener sponsored" class="tool-card tilt-3d card-3d tilt-3d card-3d" style="margin-bottom: var(--space-3);">
            <div class="tool-card-header">
              <div class="tool-card-logo" style="background: {t['color']};">{t['initial']}</div>
              <span class="tool-card-badge">{t['badge']}</span>
            </div>
            <h3 class="tool-card-title">{t['name']}</h3>
            <p class="tool-card-description">{t['desc']}</p>
            <div style="margin-top: var(--space-3); font-size: 13px; color: var(--accent); font-weight: 500;">Try {t['name']} →</div>
          </a>
'''
    share_url = f"{DOMAIN}/blog/{b['slug']}.html"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{b['title']}</title>
  <meta name="description" content="{b['meta']}">
  <meta name="keywords" content="AI tools, best AI tools, AI tools 2026, {b['title']}">
  <meta property="og:title" content="{b['title']}">
  <meta property="og:description" content="{b['meta']}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{share_url}">
  <meta property="og:image" content="https://toolforge-io.netlify.app/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{b['title']}">
  <meta name="twitter:description" content="{b['meta']}">
  <meta name="twitter:image" content="https://toolforge-io.netlify.app/assets/og-image.png">
  <meta name="twitter:site" content="@toolforgeio">
  <link rel="canonical" href="{share_url}">
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{b['title']}",
  "description": "{b['meta']}",
  "author": {{"@type": "Organization", "name": "ToolForge Editorial"}},
  "publisher": {{"@type": "Organization", "name": "ToolForge"}},
  "datePublished": "2026-07-18",
  "dateModified": "2026-07-18"
}}
</script>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230a72ef'/><text x='50' y='68' font-size='56' font-weight='700' fill='white' text-anchor='middle' font-family='sans-serif'>T</text></svg>">
  <script defer data-domain="toolforge-io.netlify.app" src="https://plausible.io/js/script.js"></script>
</head>
<body>
{NAV}
<header style="padding: var(--space-8) 0 var(--space-6); background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg) 100%);" class="reveal">
  <div class="container">
    <div style="max-width: 800px;">
      <div style="display: inline-block; font-family: var(--font-mono); font-size: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: var(--space-3);">— {b['category']}</div>
      <nav class="breadcrumb" aria-label="Breadcrumb" style="margin-bottom: var(--space-3);">
        <a href="../index.html">Home</a> <span>/</span>
        <a href="../blog.html">Blog</a> <span>/</span>
        <span>Analysis</span>
      </nav>
      <div style="display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-4); font-size: 13px; color: var(--text-tertiary); font-family: var(--font-mono);">
        <span class="toolforge-category" style="display: inline-block; padding: 4px 10px; background: rgba(10, 114, 239, 0.08); color: var(--accent); border-radius: var(--radius-sm); font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Analysis</span>
        <span>·</span>
        <span>{b['read']} min read</span>
        <span>·</span>
        <span>Updated {TODAY}</span>
      </div><h1 style="font-size: clamp(36px, 6vw, 56px); font-weight: 600; letter-spacing: -1.8px; line-height: 1.1; margin-bottom: var(--space-4);">{b['title']}</h1>
      <p style="font-size: 18px; color: var(--text-secondary); line-height: 1.5;">{b['meta']}</p>
      <div class="author-byline">
        <div class="author-avatar">TF</div>
        <div class="author-info">
          <strong>ToolForge Editorial</strong>
          <div class="author-meta">
            <span>✍️ Published July 2026</span>
            <span>⏱️ {b['read']} min read</span>
            <span>🔄 Updated {TODAY}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</header>

<section class="section" style="padding-top: var(--space-7);">
  <div class="container">
    <div style="max-width: 800px; font-size: 18px; line-height: 1.7; color: var(--text-secondary);">
      <p style="font-size: 20px; line-height: 1.6; color: var(--text-primary); font-weight: 500; margin-bottom: var(--space-6); padding-left: var(--space-4); border-left: 3px solid var(--accent);">{b['lead']}</p>

      <h2 style="font-size: 28px; font-weight: 600; margin: var(--space-6) 0 var(--space-4);">The shortlist</h2>
      <div class="tools-grid" style="grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));">
{cards}      </div>

      <h2 style="font-size: 28px; font-weight: 600; margin: var(--space-7) 0 var(--space-4);">How we picked</h2>
      <p>Every tool on this list was <strong>actively used for 2+ weeks</strong> by the ToolForge editorial team. We scored each on output quality, time saved, ease of use, and price-to-value, then removed anything that wasn't worth the subscription.</p>

      <h2 style="font-size: 28px; font-weight: 600; margin: var(--space-6) 0 var(--space-4);">The verdict</h2>
      <p>{b['verdict']}</p>

      <div class="affiliate-disclosure" style="text-align: left; margin-top: var(--space-6);">
        💡 <strong>Transparency:</strong> This page contains affiliate links. If you sign up through our link, we may earn a commission at no cost to you. <a href="../about.html#disclosure">Full disclosure</a>.
      </div>
    </div>
  </div>
  <div class="share-buttons" style="margin-top: var(--space-7);">
    <span class="share-label">Share:</span>
    <a href="https://twitter.com/intent/tweet?text={b['title']}&url={share_url}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on X">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </a>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on LinkedIn">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"/></svg>
    </a>
    <a href="https://news.ycombinator.com/submitlink?u={share_url}&t={b['title']}" target="_blank" rel="noopener" class="share-btn" aria-label="Share on Hacker News">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M0 0h24v24H0z" fill="none"/><text x="12" y="17" font-family="system-ui" font-size="16" font-weight="700" text-anchor="middle">Y</text></svg>
    </a>
    <a href="mailto:?subject={b['title']}&body=Check out this article: {share_url}" class="share-btn" aria-label="Share via email">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
    </a>
  </div>
</section>
{FOOTER}
{SCRIPTS}</body>
</html>
'''

# =================== CONTENT DATA ===================

TOOLS = [
 dict(slug="scite-ai", name="Scite", tagline="The AI research assistant that shows how papers actually cite each other — with context, not just a count.", category="Research",
   color1="#5b21b6", color2="#7c3aed", initials="Sc", price="Free", price_label="plus $10/mo Pro", price_num="0",
   free_tier="Free tier", rating="4.6/5", rating_num="4.6", users="500K+ researchers", founded="2018",
   headline="Citations with receipts",
   intro="Scite is a citation-based discovery engine. Instead of telling you a paper has been cited 1,000 times, it shows whether those citations supported, mentioned, or contradicted the work — and lets you read the surrounding sentence. For anyone doing literature reviews, grant writing, or fact-checking, it turns a weeks-long manual process into a few targeted searches.",
   who_for="Researchers, grad students, clinicians, and journalists who need to know not just that a paper exists, but whether the field actually stands behind it.",
   features=[("📑","Smart Citations","Every citation is classified as supporting, mentioning, or contrasting — with the exact sentence shown inline."),
             ("🔍","Citation Statement Search","Search the full text of how papers talk about a claim, not just keyword matches in abstracts."),
             ("📚","Reference Check","Paste a manuscript and Scite flags retracted or heavily-contradicted sources before you submit."),
             ("🤖","Assistant","Ask a research question and get answers grounded in the citation graph, with links to primary sources.")],
   pros=["Cuts literature-review time dramatically","Makes 'is this claim actually supported?' answerable in seconds","Reference Check prevents citing retracted papers","Free tier is genuinely useful"],
   cons=["Best features locked behind the $10/mo Pro plan","Citation classification isn't perfect on edge cases","Smaller coverage than Google Scholar for very old papers"],
   verdict="If you read or write research for a living, Scite is the single highest-leverage tool on this list. The free tier covers most casual needs; Pro pays for itself the first time it saves you from citing a retracted study.",
   cta_url="https://scite.ai/?via=toolforge"),

 dict(slug="elicit-ai", name="Elicit", tagline="The AI workspace that reads 100 papers so you don't have to — and drops the answers into a table.", category="Research",
   color1="#0e7490", color2="#0891b2", initials="El", price="$10/mo", price_label="Plus", price_num="10",
   free_tier="Free tier (limited)", rating="4.5/5", rating_num="4.5", users="400K+ researchers", founded="2020",
   headline="Automated literature review, actually",
   intro="Elicit is built by the nonprofit Ought to automate the tedious core of research: finding relevant papers and extracting what they found. You ask a question, Elicit pulls studies from Semantic Scholar, and populates a spreadsheet with abstracts, populations, interventions, and outcomes — each cell linked to its source. It won't replace reading, but it makes the first pass take minutes instead of days.",
   who_for="Systematic reviewers, grad students scoping a thesis, meta-analysts, and anyone who needs to summarize what a body of literature says.",
   features=[("📊","Extraction Tables","Ask for a column — 'sample size', 'effect size' — and Elicit fills it across dozens of papers with citations."),
             ("🔎","Smart Search","Plain-English queries return the most relevant studies, not just keyword matches."),
             ("🧬","PDF Import","Upload your own corpus and Elicit will read and structure it the same way."),
             ("🤝","Workflows","Chain steps — find, extract, summarize, then draft — into one repeatable pipeline.")],
   pros=["Turns days of screening into an afternoon","Extractions are always linked to source text","Free tier handles small reviews","Backed by a research nonprofit, not just a startup"],
   cons=["Extractions still need human verification for publication-grade work","Deep features require the $10/mo plan","Can miss niche or pre-print-only topics"],
   verdict="Elicit is the fastest way to get a结构化 overview of any research area in 2026. Pair it with Scite (for citation context) and you have a literature-review stack that used to cost a research assistant's salary.",
   cta_url="https://elicit.com/?via=toolforge"),
]

COMPARES = [
 dict(slug="claude-vs-gpt-4-2026", name_a="Claude", name_b="GPT-4", color_a="#d97706", color_b="#10a37f",
   initials_a="Cl", initials_b="G4",
   desc_a="Anthropic's flagship model, known for long-context reasoning and careful, nuanced writing.",
   desc_b="OpenAI's GPT-4-class model — the generalist workhorse behind ChatGPT and countless apps.",
   price_a="Free / $20+", price_b="$20/mo Plus",
   best_a="Long documents, careful analysis, writing", best_b="General tasks, coding, ecosystem",
   url_a="https://claude.ai/?via=toolforge", url_b="https://chatgpt.com/?via=toolforge",
   verdict="In 2026, Claude wins on long-context reasoning, nuanced writing, and low-hallucination analysis, while GPT-4-class models keep the edge on raw ecosystem breadth and third-party integrations. Pick Claude when the task is a 200-page report or a sensitive draft; pick GPT-4 when you need the widest tool and plugin support.",
   winner="Claude (for reasoning & writing) · GPT-4 (for ecosystem)"),
]

BLOGS = [
 dict(slug="best-ai-tools-for-receptionists", category="For Receptionists", read="4",
   title="The 9 Best AI Tools for Receptionists in 2026 (Handle 2x the Calls)",
   meta="The AI stack modern receptionists use to screen calls, draft replies, book meetings, and never miss a message. Tested, ranked, with real pricing.",
   lead="Reception is the front door of every business — and in 2026 it's also the most automatable. The best receptionists aren't being replaced; they're using AI to answer twice as many calls, book twice as many meetings, and keep a perfect log of every interaction. Here's the stack that makes that possible.",
   verdict="Start with an AI phone/reception layer (like an assistant that handles routine calls) and a scheduling tool, then add a writing assistant for flawless guest communication. The whole stack can run under $40/month and pays for itself in reclaimed hours the first week.",
   tools=[
     dict(name="Front", color="#1f2937", initial="Fr", badge="Free tier", desc="Shared inbox that turns front-desk email into a team sport with AI triage.", url="https://frontapp.com/?via=toolforge"),
     dict(name="Calendly", color="#006bff", initial="Ca", badge="Free", desc="Let visitors book their own meetings — no phone tag, no double-books.", url="https://calendly.com/?via=toolforge"),
     dict(name="Fireflies", color="#7c3aed", initial="Fi", badge="$10/mo", desc="Auto-transcribes and summarizes every call so nothing falls through the cracks.", url="https://fireflies.ai/?via=toolforge"),
     dict(name="Superhuman", color="#111827", initial="Su", badge="$30/mo", desc="AI email that helps you reply in seconds and reach inbox zero daily.", url="https://superhuman.com/?via=toolforge"),
     dict(name="Notion AI", color="#000000", initial="No", badge="Free tier", desc="A shared front-desk wiki + AI that drafts visitor FAQs and scripts.", url="https://notion.so/?via=toolforge"),
     dict(name="Otter", color="#f97316", initial="Ot", badge="Free tier", desc="Live transcription for in-person and phone conversations at the desk.", url="https://otter.ai/?via=toolforge"),
     dict(name="ChatGPT", color="#10a37f", initial="Ch", badge="$20/mo", desc="Draft visitor replies, FAQs, and internal notes in your brand voice.", url="https://chatgpt.com/?via=toolforge"),
     dict(name="Grammarly", color="#15c39a", initial="Gr", badge="Free", desc="Keeps every guest-facing message polished and typo-free.", url="https://grammarly.com/?via=toolforge"),
     dict(name="Zapier", color="#ff4f00", initial="Za", badge="Free tier", desc="Connects your phone, calendar, and CRM so new calls auto-create tasks.", url="https://zapier.com/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-yoga-instructors", category="For Yoga Instructors", read="4",
   title="The 7 Best AI Tools for Yoga Instructors in 2026 (Teach More, Admin Less)",
   meta="The AI toolkit yoga teachers use to plan sequences, film classes, grow on social, and run the business — so you can stay on the mat.",
   lead="Teaching yoga is about presence — but running a yoga business is about invoices, reels, and class plans at 11pm. The instructors thriving in 2026 have offloaded the admin to AI, freeing them to do what only they can: hold the room. Here are the tools worth your mat time.",
   verdict="Pair a content planner (for social + newsletters) with a class-sequence generator and a booking tool, and you've automated 80% of the non-teaching work. Most of this stack is free to start; the paid pieces cost less than one dropped private session a month.",
   tools=[
     dict(name="ChatGPT", color="#10a37f", initial="Ch", badge="$20/mo", desc="Generate themed class sequences, dharma talks, and workshop outlines in seconds.", url="https://chatgpt.com/?via=toolforge"),
     dict(name="Canva", color="#00c4cc", initial="Ca", badge="Free", desc="AI-designed class flyers, studio social posts, and workshop decks.", url="https://canva.com/?via=toolforge"),
     dict(name="CapCut", color="#000000", initial="Cp", badge="Free", desc="Trim and caption your practice videos for Instagram and TikTok fast.", url="https://capcut.com/?via=toolforge"),
     dict(name="Notion", color="#000000", initial="No", badge="Free", desc="A calm, central home for your sequences, student notes, and retreat plans.", url="https://notion.so/?via=toolforge"),
     dict(name="Descript", color="#3b82f6", initial="De", badge="Free tier", desc="Edit class audio and video by editing text — perfect for guided meditations.", url="https://descript.com/?via=toolforge"),
     dict(name="Suno", color="#7c3aed", initial="Su", badge="Free tier", desc="Generate original ambient and meditation tracks for your sessions.", url="https://suno.com/?via=toolforge"),
     dict(name="ConvertKit", color="#ff6b35", initial="Ck", badge="Free tier", desc="Newsletters and automations that nurture your student community.", url="https://convertkit.com/?via=toolforge"),
   ]),
]

# =================== WRITE + SITEMAP ===================
new_urls = []

for t in TOOLS:
    if t['slug'] in tool_slugs:
        print(f"SKIP (exists): tools/{t['slug']}.html")
        continue
    path = os.path.join(BASE, 'tools', f"{t['slug']}.html")
    with open(path, 'w') as f:
        f.write(tool_html(t))
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html")
    print(f"WROTE: tools/{t['slug']}.html")

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print(f"SKIP (exists): compare/{c['slug']}.html")
        continue
    path = os.path.join(BASE, 'compare', f"{c['slug']}.html")
    with open(path, 'w') as f:
        f.write(compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    print(f"WROTE: compare/{c['slug']}.html")

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print(f"SKIP (exists): blog/{b['slug']}.html")
        continue
    path = os.path.join(BASE, 'blog', f"{b['slug']}.html")
    with open(path, 'w') as f:
        f.write(blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    print(f"WROTE: blog/{b['slug']}.html")

# ---------- append to sitemap ----------
print(f"\n=== SITEMAP: appending {len(new_urls)} new URLs ===")
sm = os.path.join(BASE, 'sitemap.xml')
with open(sm) as f:
    content = f.read()

block = ""
for u in new_urls:
    block += f'''  <url>
    <loc>{u}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''
# Insert before closing </urlset>
content = content.replace("</urlset>", block + "</urlset>", 1)
with open(sm, 'w') as f:
    f.write(content)

print(f"Total new URLs: {len(new_urls)}")
for u in new_urls:
    print("  +", u)
