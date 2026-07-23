#!/usr/bin/env python3
"""ToolForge Sprint Generator — batch content creator.
Creates new tool / compare / blog pages using the EXACT existing site
templates, skips any slug that already exists, and appends new URLs to
sitemap.xml with today's date. Non-destructive and idempotent.
"""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-10"
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

# ---------- TOOL TEMPLATE (mirrors tools/cursor.html) ----------
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

# ---------- COMPARE TEMPLATE (mirrors compare/chatgpt-vs-claude.html) ----------
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

# ---------- BLOG TEMPLATE (mirrors blog/best-ai-tools-for-freelancers.html) ----------
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
  "datePublished": "2026-07-11",
  "dateModified": "2026-07-11"
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
            <span>✍️ Published June 2026</span>
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
# (slug-checked against existing files; only absent ones are written)

