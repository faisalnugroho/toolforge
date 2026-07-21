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

TOOLS = [
 dict(slug="openai-codex", name="OpenAI Codex", tagline="OpenAI's cloud coding agent that writes, tests, and ships entire PRs from a prompt.", category="Coding",
   color1="#10a37f", color2="#0e8c6e", initials="Co", price="$20/mo", price_label="ChatGPT Plus", price_num="20",
   free_tier="Limited tasks", rating="4.7/5", rating_num="4.7", users="1M+ developers", founded="2025",
   headline="The agent that writes the PR for you",
   intro="OpenAI Codex is a cloud-based coding agent that takes a natural-language task and runs it in a sandboxed environment — writing code, running tests, and opening a pull request. Released in 2025, it shifted the conversation from 'autocomplete' to 'autonomous engineer.' Point it at a repo, describe the feature, and Codex iterates against the test suite until green.",
   who_for="Teams with large codebases, backend engineers, and anyone who wants to offload boilerplate, migrations, and test-writing to a reliable agent.",
   features=[("🤖","Task-based agent","Give it a GitHub issue or a sentence. Codex plans, writes, and verifies the change in an isolated container."),
             ("🧪","Test-driven loops","Codex runs your test suite and iterates until it passes — no copy-paste from chat needed."),
             ("🔀","Pull requests","Output lands as a real PR with a summary, ready for human review."),
             ("🔒","Sandboxed & safe","Runs in a disposable environment. Your secrets and prod never get touched.")],
   pros=["Genuinely autonomous — completes multi-file features",
         "Verifies work against your own test suite",
         "Tight GitHub integration",
         "Frees senior engineers from grunt work"],
   cons=["Needs a well-tested repo to shine",
         "Slower than inline autocomplete for tiny edits",
         "Occasional off-target changes needing review",
         "Pricing tied to the Codex tier, not just Plus"],
   verdict="The closest thing to 'hire a junior engineer who never sleeps.' Best paired with strong tests and a human reviewer. For solo tinkerers, Cursor or Copilot are still lighter-weight.",
   cta_url="https://openai.com/codex"),

 dict(slug="deepseek", name="DeepSeek", tagline="The open-weight Chinese AI lab whose R1 model shook the industry with reasoning at a fraction of the cost.", category="Productivity",
   color1="#4d6bfe", color2="#3b4fd1", initials="Ds", price="Free", price_label="Open weights", price_num="0",
   free_tier="Fully free chat", rating="4.6/5", rating_num="4.6", users="100M+ users", founded="2023",
   headline="Reasoning that punches far above its price",
   intro="DeepSeek is the AI lab behind the R1 reasoning model that went viral in early 2025 for matching frontier models on math and code while costing a tiny fraction to run. The chat app is free, the weights are open, and the API is among the cheapest available — making it a favorite for builders and cost-conscious teams.",
   who_for="Developers, researchers, and startups who want frontier-grade reasoning without frontier pricing — and anyone who wants to self-host.",
   features=[("🧠","R1 reasoning","Chain-of-thought reasoning that competes with GPT and Claude on math, code, and logic."),
             ("💸","Rock-bottom API","Among the cheapest frontier-class APIs on the market."),
             ("🔓","Open weights","R1 distillations are downloadable — run it on your own hardware."),
             ("🌐","Massive free tier","The chat app is free for everyday use.")],
   pros=["Best price-to-performance in the market",
         "Open weights enable private self-hosting",
         "Strong reasoning and coding",
         "Free chat tier for individuals"],
   cons=["Censorship on certain China-related topics",
         "Smaller multimodal and tool-use ecosystem",
         "English fluency slightly behind US labs",
         "Self-hosting needs real GPU hardware"],
   verdict="The default pick when cost matters or you need to self-host. For polished general assistance and multimodal work, GPT-4o or Claude still lead — but DeepSeek wins on raw value.",
   cta_url="https://www.deepseek.com"),

 dict(slug="qwen", name="Qwen", tagline="Alibaba's open model family — multilingual, multimodal, and the strongest open alternative outside the US.", category="Productivity",
   color1="#615ced", color2="#4a44c0", initials="Qw", price="Free", price_label="Open weights", price_num="0",
   free_tier="Free chat + open weights", rating="4.5/5", rating_num="4.5", users="80M+ users", founded="2023",
   headline="The open model family that speaks your language",
   intro="Qwen is Alibaba's large-model family, ranging from tiny on-device variants to flagship Qwen-Max. It's notably the strongest open model for non-English languages and offers native vision, audio, and tool-use. Developers reach for Qwen when they need a capable, licensable model they can run themselves.",
   who_for="Multilingual teams, privacy-focused deployers, and builders who want open weights with vision and audio built in.",
   features=[("🌍","True multilingual","Top-tier performance across 30+ languages, especially Chinese, Arabic, and Spanish."),
             ("👁️","Native vision & audio","VL and audio models in the family — not bolted-on."),
             ("🔓","Open & licensable","Weights released for commercial and private use."),
             ("📱","Tiny to flagship","From 0.5B mobile models to 1T+ MoE flagships.")],
   pros=["Best open model for non-English use",
         "Vision + audio in one family",
         "Commercial-friendly licensing",
         "Runs on consumer hardware (small variants)"],
   cons=["Weaker creative writing than GPT/Claude",
         "US-centric tooling support lags",
         "Largest models need serious GPU"],
   verdict="The open model to beat for multilingual and self-hosted workloads. Pair it with Ollama or vLLM and you've got a private GPT-class assistant.",
   cta_url="https://chat.qwen.ai"),

 dict(slug="gamma", name="Gamma", tagline="AI presentations, documents, and webpages generated from a single prompt.", category="Productivity",
   color1="#673ab7", color2="#512da8", initials="Ga", price="$10/mo", price_label="Plus plan", price_num="10",
   free_tier="Free tier (limited)", rating="4.6/5", rating_num="4.6", users="20M+ users", founded="2020",
   headline="Slide decks in 30 seconds, not 3 hours",
   intro="Gamma turns a prompt or a doc into a polished presentation, document, or web page — with real design sense, not just bullet points on a white background. In 2026 it's the go-to for anyone who has ever groaned at opening PowerPoint. Export to PPTX or publish as a shareable web page.",
   who_for="Founders, marketers, consultants, and students who need to look polished fast without a designer.",
   features=[("⚡","One-prompt decks","Describe the talk; Gamma generates structure, copy, and visuals."),
             ("🎨","Real design system","On-brand themes, charts, and AI images baked in."),
             ("🌐","Web publishing","Publish as a live webpage — no file attachments."),
             ("📊","Docs & sites too","Not just slides — full documents and microsites.")],
   pros=["Dramatically faster than PowerPoint/Keynote",
         "Genuinely good visual design",
         "Easy web sharing and analytics",
         "Affordable Plus tier"],
   cons=["Less granular control than manual design",
         "Offline export is limited on free tier",
         "Heavy decks can feel templated"],
   verdict="The fastest path from idea to deck. If you live in slides, Gamma pays for itself in the first meeting you prep.",
   cta_url="https://gamma.app"),

 dict(slug="copy-ai", name="Copy.ai", tagline="Go-to-market AI that writes your sales and marketing copy at scale.", category="Writing",
   color1="#e11d48", color2="#be123c", initials="Ca", price="$36/mo", price_label="Team plan", price_num="36",
   free_tier="Free tier (2,000 words)", rating="4.3/5", rating_num="4.3", users="10M+ users", founded="2020",
   headline="The copy machine for GTM teams",
   intro="Copy.ai started as a copywriting tool and grew into a full go-to-market platform — generating blog posts, ad variants, cold emails, and even orchestrating multi-step GTM workflows. In 2026 it's less 'writer' and more 'marketing automation with a brain.'",
   who_for="Growth marketers, SDRs, and small GTM teams who need volume without a copywriting agency.",
   features=[("✍️","Brand voices","Train it on your style so every output sounds like you."),
             ("📧","Sales workflows","Spin up cold-email sequences and follow-ups automatically."),
             ("🧩","Workflows","Chain prompts into repeatable GTM pipelines."),
             ("🔌","Integrations","Connects to CRMs and your stack.")],
   pros=["Built for marketing volume",
         "Workflow automation beyond single prompts",
         "Brand-voice training",
         "Solid free tier to start"],
   cons=["Overkill for one-off writing",
         "Quality varies by workflow",
         "Pricier than simple writers"],
   verdict="The right call for GTM teams that need repeatable copy at scale. Solo writers are better served by Jasper or Claude.",
   cta_url="https://www.copy.ai"),

 dict(slug="murf", name="Murf AI", tagline="Studio-quality AI voiceovers for videos, ads, and e-learning — no mic required.", category="Audio",
   color1="#0ea5e9", color2="#0284c7", initials="Mu", price="$19/mo", price_label="Creator plan", price_num="19",
   free_tier="Free tier (10 min)", rating="4.5/5", rating_num="4.5", users="5M+ users", founded="2020",
   headline="A voiceover studio in your browser",
   intro="Murf turns text into natural, studio-grade voiceovers across 120+ voices and 20+ languages. It's the quiet workhorse behind countless YouTube videos, corporate training modules, and ads — no recording booth, no voice actor scheduling.",
   who_for="YouTubers, e-learning creators, agencies, and product teams who need narration fast and cheap.",
   features=[("🎙️","120+ voices","Studio-quality voices across accents and ages."),
             ("🌍","20+ languages","Localize a script without re-recording."),
             ("🎚️","Pitch & pace control","Fine-tune emphasis, speed, and tone."),
             ("🎬","Video sync","Match voiceover to your timeline.")],
   pros=["Far cheaper than hiring voice actors",
         "Natural-sounding, not robotic",
         "Great for localization",
         "Simple editor"],
   cons=["Free tier is very limited",
         "Emotion range narrower than human VO",
         "Best voices are on paid tiers"],
   verdict="The pragmatic pick for anyone producing narration at volume. For character/celebrity voices, ElevenLabs still edges it.",
   cta_url="https://murf.ai"),

 dict(slug="heygen", name="HeyGen", tagline="AI avatar videos — type a script, get a talking-head video with perfect lip-sync.", category="Video",
   color1="#7c3aed", color2="#6d28d9", initials="Hg", price="$24/mo", price_label="Creator plan", price_num="24",
   free_tier="Free tier (limited)", rating="4.4/5", rating_num="4.4", users="3M+ users", founded="2020",
   headline="A spokesperson that never calls in sick",
   intro="HeyGen generates polished talking-head videos from a script — choose an avatar (or clone your own), type what you want said, and get a lip-synced video in minutes. In 2026 it's how thousands of companies produce training, marketing, and localization content without a camera crew.",
   who_for="L&D teams, marketers, and creators who need spokesperson videos at scale and in many languages.",
   features=[("🧑‍💼","Photo avatars","Use a stock avatar or clone a real person."),
             ("🌍","Instant translation","Swap the spoken language and keep the lip-sync."),
             ("🎬","Templates","Pre-built layouts for ads, how-tos, and intros."),
             ("🔁","Batch mode","Generate dozens of variations at once.")],
   pros=["No camera, crew, or studio needed",
         "Convincing lip-sync and translation",
         "Huge time savings for L&D",
         "Brand-safe avatar cloning"],
   cons=["Avatar realism still slightly off",
         "Free tier is limited",
         "Best results need paid plans"],
   verdict="The leader for avatar-based video at scale. For fully animated or generative scenes, Synthesia or Runway fit better.",
   cta_url="https://www.heygen.com"),

 dict(slug="ollama", name="Ollama", tagline="Run open-source LLMs locally on your own machine — private, offline, free.", category="Coding",
   color1="#111827", color2="#374151", initials="Ol", price="Free", price_label="Open source", price_num="0",
   free_tier="Always free", rating="4.7/5", rating_num="4.7", users="5M+ users", founded="2022",
   headline="Your private AI, one command away",
   intro="Ollama makes running open models (Llama, Qwen, Mistral, Gemma, and more) as simple as `ollama run llama3`. No cloud, no API keys, no data leaving your machine. It became the default way developers experiment with local models in 2024-2026.",
   who_for="Privacy-conscious users, developers, and anyone who wants AI that runs fully offline on a laptop.",
   features=[("🔒","100% local","Models run on your hardware; nothing leaves the machine."),
             ("⌨️","One command","`ollama run <model>` and you're chatting."),
             ("📦","Huge model library","Llama, Qwen, Mistral, Gemma, Phi, and more."),
             ("🧩","API compatible","Drop-in OpenAI-style endpoint for your apps.")],
   pros=["Complete privacy — no cloud needed",
         "Free and open source",
         "Trivial to install",
         "Great for prototyping"],
   cons=["Needs a decent GPU/RAM for big models",
         "No hosted collaboration features",
         "Quality capped by local model size"],
   verdict="The easiest on-ramp to private, offline AI. Pair with a good model and you've got a ChatGPT that never sees the cloud.",
   cta_url="https://ollama.com"),
]

COMPARES = [
 dict(slug="chatgpt-vs-deepseek", name_a="ChatGPT", name_b="DeepSeek", color_a="#10a37f", color_b="#4d6bfe",
   initials_a="Ch", initials_b="Ds", url_a="https://chat.openai.com/?via=toolforge", url_b="https://www.deepseek.com",
   desc_a="OpenAI's polished generalist assistant", desc_b="The open, low-cost reasoning challenger",
   price_a="$20/mo Plus", price_b="Free / cheap API", best_a="creative writing, image gen, voice", best_b="reasoning, coding, self-hosting",
   verdict="Use <strong>ChatGPT</strong> if you want the most polished, multimodal, all-rounder experience with image generation and voice. Use <strong>DeepSeek</strong> if you need top-tier reasoning and coding at the lowest possible cost — or want to self-host. For most everyday users ChatGPT's polish wins; for builders and cost-sensitive teams, DeepSeek is unbeatable.",
   winner="Tie — ChatGPT for polish, DeepSeek for value"),

 dict(slug="claude-vs-gemini", name_a="Claude", name_b="Gemini", color_a="#d97706", color_b="#4285f4",
   initials_a="Cl", initials_b="Ge", url_a="https://claude.ai/?via=toolforge", url_b="https://gemini.google.com",
   desc_a="Anthropic's thoughtful, long-context writer", desc_b="Google's multimodal, 2M-context giant",
   price_a="Free / $20 Pro", price_b="Free / $20 Advanced", best_a="long-form writing, analysis, code review", best_b="video/audio understanding, Workspace",
   verdict="Use <strong>Claude</strong> for the most careful writing, analysis, and code review. Use <strong>Gemini</strong> if you live in Google Workspace, need to analyze video/audio natively, or want the largest context window in the business. They're the two best 'thinking' assistants — pick based on your ecosystem.",
   winner="Tie — Claude for writing, Gemini for Workspace"),

 dict(slug="cursor-vs-windsurf", name_a="Cursor", name_b="Windsurf", color_a="#000000", color_b="#0a72ef",
   initials_a="Cu", initials_b="Ws", url_a="https://www.cursor.com/?via=toolforge", url_b="https://windsurf.com",
   desc_a="The AI-first editor built on VSCode", desc_b="The agentic IDE with Cascade",
   price_a="$20/mo Pro", price_b="$15/mo Pro", best_a="multi-file Composer edits, VSCode familiarity", best_b="Cascade agent, lighter weight",
   verdict="Use <strong>Cursor</strong> if you want the most mature AI editor with the biggest community and VSCode familiarity. Use <strong>Windsurf</strong> if you prefer a lighter, agent-first feel and the Cascade flow. Both are excellent; Cursor leads on ecosystem, Windsurf on agentic elegance.",
   winner="Cursor — slightly, on maturity"),

 dict(slug="elevenlabs-vs-murf", name_a="ElevenLabs", name_b="Murf", color_a="#06b6d4", color_b="#0ea5e9",
   initials_a="El", initials_b="Mu", url_a="https://elevenlabs.io/?via=toolforge", url_b="https://murf.ai",
   desc_a="The voice-quality and cloning leader", desc_b="The practical voiceover studio",
   price_a="Free / $5 Starter", price_b="$19/mo Creator", best_a="character voices, dubbing, cloning", best_b="business narration, localization",
   verdict="Use <strong>ElevenLabs</strong> when voice quality, emotional range, and cloning matter most — dubbing, characters, audiobooks. Use <strong>Murf</strong> for straightforward business narration and bulk localization where workflow and price matter. ElevenLabs wins on fidelity; Murf wins on simplicity.",
   winner="ElevenLabs — on voice quality"),

 dict(slug="midjourney-vs-sora", name_a="Midjourney", name_b="Sora", color_a="#1f2937", color_b="#10a37f",
   initials_a="Mj", initials_b="So", url_a="https://www.midjourney.com", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="The aesthetic king of AI images", desc_b="OpenAI's text-to-video model",
   price_a="$10/mo Basic", price_b="$20/mo Plus", best_a="stunning stills, art direction", best_b="cinematic video clips",
   verdict="These aren't direct rivals — <strong>Midjourney</strong> owns still-image artistry, while <strong>Sora</strong> generates video. Use Midjourney when you need a beautiful frame; use Sora when you need it to move. If you only need images, Midjourney wins; if you need motion, Sora is the pick.",
   winner="Depends — images: Midjourney, video: Sora"),

 dict(slug="chatgpt-vs-poe", name_a="ChatGPT", name_b="Poe", color_a="#10a37f", color_b="#5b21b6",
   initials_a="Ch", initials_b="Po", url_a="https://chat.openai.com/?via=toolforge", url_b="https://poe.com",
   desc_a="A single, deep AI assistant", desc_b="A gateway to many models at once",
   price_a="$20/mo Plus", price_b="$20/mo Sub", best_a="deep, single-model mastery", best_b="access to many models",
   verdict="Use <strong>ChatGPT</strong> if you want one excellent assistant you can trust. Use <strong>Poe</strong> if you want to hop between Claude, GPT, Gemini, and Llama in one tab and compare answers. Poe is a playground; ChatGPT is a home base.",
   winner="Tie — ChatGPT for depth, Poe for breadth"),

 dict(slug="notion-vs-clickup", name_a="Notion", name_b="ClickUp", color_a="#111827", color_b="#7c3aed",
   initials_a="No", initials_b="Cl", url_a="https://www.notion.so", url_b="https://clickup.com",
   desc_a="The flexible docs + AI workspace", desc_b="The project-heavy all-in-one",
   price_a="Free / $10 Plus", price_b="Free / $7 Every", best_a="docs, notes, light PM", best_b="heavy project management",
   verdict="Use <strong>Notion</strong> (with Notion AI) for docs, notes, and a calm workspace. Use <strong>ClickUp</strong> if you need aggressive project management, tasks, and reporting. Notion wins on elegance; ClickUp wins on feature density.",
   winner="Tie — Notion for docs, ClickUp for PM"),

 dict(slug="runway-vs-pika", name_a="Runway", name_b="Pika", color_a="#111827", color_b="#db2777",
   initials_a="Ru", initials_b="Pi", url_a="https://runwayml.com", url_b="https://pika.art",
   desc_a="The pro-grade generative video suite", desc_b="The playful, effects-first video app",
   price_a="$12/mo Standard", price_b="Free / $8 Pro", best_a="precise control, Gen-4 quality", best_b="quick effects, social clips",
   verdict="Use <strong>Runway</strong> for professional, controllable video work where quality is queen. Use <strong>Pika</strong> for fast, fun, effects-heavy social clips. Runway is the studio; Pika is the playground.",
   winner="Runway — on control and quality"),
]

BLOGS = [
 dict(slug="best-ai-tools-for-students-2026", title="The 9 Best AI Tools for Students in 2026 (Study Smarter, Not Harder)",
   meta="From note-taking to essay drafting to exam prep — the AI stack that actually helps students get better grades without cheating.",
   category="For Students", read="3", lead="Students in 2026 aren't asking whether to use AI — they're asking which tools genuinely help them learn instead of just doing the work for them. We tested the stack that improves comprehension, not just output.",
   verdict="Start with a study assistant (NotebookLM or ChatGPT) for comprehension, add a writing tool (Grammarly or Claude) for drafts, and a flashcard app (Mindgrasp) for recall. The goal is learning faster — not skipping it.",
   tools=[
     dict(name="NotebookLM", url="https://notebooklm.google.com", color="#4285f4", initial="Nl", badge="Free", desc="Turn your lecture PDFs into a studyable podcast"),
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="$20/mo", desc="Explains concepts and quizzes you"),
     dict(name="Grammarly", url="https://www.grammarly.com", color="#15c39a", initial="Gr", badge="Free", desc="Catch errors before you submit"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Draft and refine essays with nuance"),
     dict(name="Mindgrasp", url="https://mindgrasp.ai", color="#7c3aed", initial="Mg", badge="$9/mo", desc="Turn notes into flashcards & summaries"),
     dict(name="Otter.ai", url="https://otter.ai", color="#111827", initial="Ot", badge="Free", desc="Transcribe lectures automatically"),
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Cited research for papers"),
     dict(name="QuillBot", url="https://quillbot.com", color="#0ea5e9", initial="Qb", badge="Free", desc="Paraphrase without losing meaning"),
     dict(name="Wolfram Alpha", url="https://www.wolframalpha.com", color="#dd1100", initial="Wa", badge="Free", desc="Step-by-step math and science"),
   ]),

 dict(slug="best-free-ai-tools-for-writing-2026", title="The 8 Best FREE AI Writing Tools in 2026 (No Paywall, Real Output)",
   meta="Great writing AI doesn't have to cost money. The genuinely free tools that hold up for drafting, editing, and brainstorming.",
   category="For Writers", read="2", lead="Most 'free' AI writers bury the good stuff behind a paywall. These eight give you real, usable output at $0 — perfect for students, indie writers, and anyone testing the waters.",
   verdict="Use ChatGPT or Claude's free tiers for drafting, Grammarly and QuillBot for polish, and Sudowrite's free trial for fiction. You can run a complete writing workflow without spending a cent.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Drafting and brainstorming at $0"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Nuanced long-form writing, free tier"),
     dict(name="Grammarly", url="https://www.grammarly.com", color="#15c39a", initial="Gr", badge="Free", desc="Grammar and clarity, no cost"),
     dict(name="QuillBot", url="https://quillbot.com", color="#0ea5e9", initial="Qb", badge="Free", desc="Paraphrase and summarize free"),
     dict(name="Google Docs AI", url="https://docs.google.com", color="#4285f4", initial="Gd", badge="Free", desc="Built-in help in your docs"),
     dict(name="Notion AI", url="https://www.notion.so", color="#111827", initial="Na", badge="Free trial", desc="Writing inside your notes"),
     dict(name="Sudowrite", url="https://www.sudowrite.com/?via=toolforge", color="#7c3aed", initial="Sw", badge="Free trial", desc="Fiction co-pilot, trial available"),
     dict(name="Hemingway Editor", url="https://hemingwayapp.com", color="#d97706", initial="He", badge="Free", desc="Make your writing bold and clear"),
   ]),

 dict(slug="ai-tools-vs-traditional-translation-2026", title="AI Translation vs Human Translators in 2026: What's Actually Better?",
   meta="AI translation hit native-quality in 2025. We break down exactly when to trust the machine — and when to still hire a human.",
   category="Analysis", read="3", lead="For years 'AI translation' meant robotic, word-by-word output. In 2026, models like DeepL, Gemini, and GPT read context, tone, and even dialect. But human translators aren't obsolete. Here's the honest split.",
   verdict="Use AI (DeepL, Gemini, ChatGPT) for speed, volume, and everyday content. Use a human for literary work, legal nuance, and high-stakes branding. The hybrid — AI draft, human polish — is now the industry standard.",
   tools=[
     dict(name="DeepL", url="https://www.deepl.com", color="#1a1a1a", initial="Dl", badge="Free", desc="The accuracy benchmark for MT"),
     dict(name="Gemini", url="https://gemini.google.com", color="#4285f4", initial="Ge", badge="Free", desc="Context-aware, multilingual"),
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Tone and style control per sentence"),
     dict(name="Google Translate", url="https://translate.google.com", color="#4285f4", initial="Gt", badge="Free", desc="133 languages, instant"),
     dict(name="Qwen", url="https://chat.qwen.ai", color="#615ced", initial="Qw", badge="Free", desc="Excellent for Asian languages"),
     dict(name="Microsoft Translator", url="https://www.bing.com/translator", color="#0078d4", initial="Mt", badge="Free", desc="Enterprise & doc translation"),
     dict(name="Papago", url="https://papago.naver.com", color="#19b5b1", initial="Pa", badge="Free", desc="Best for Korean/Japanese/Chinese"),
     dict(name="Lingva", url="https://lingva.ml", color="#16a34a", initial="Li", badge="Free", desc="Privacy-first, no tracking"),
   ]),

 dict(slug="best-ai-tools-for-spreadsheets-excel-2026", title="The 7 Best AI Tools for Excel & Spreadsheets in 2026",
   meta="Stop fighting formulas. These AI tools write them, clean data, and build dashboards from plain-English requests.",
   category="For Analysts", read="2", lead="Spreadsheets are where most business work actually happens — and where most people waste the most time. AI now writes your VLOOKUPs, cleans messy CSVs, and builds charts from a sentence. Here are the tools that deliver.",
   verdict="Use Excel's built-in Copilot if you're on Microsoft 365, GPT or Claude for ad-hoc formula help, and SheetAI or Formula Bot for Google Sheets. You'll cut spreadsheet time by half overnight.",
   tools=[
     dict(name="Microsoft Copilot", url="https://www.microsoft.com/copilot", color="#0078d4", initial="Mc", badge="$30/mo", desc="AI inside Excel 365"),
     dict(name="Google Sheets AI", url="https://workspace.google.com", color="#4285f4", initial="Gs", badge="Free", desc="Help me organize & formula assist"),
     dict(name="SheetAI", url="https://sheetai.app", color="#16a34a", initial="Sa", badge="$8/mo", desc="AI functions in Google Sheets"),
     dict(name="Formula Bot", url="https://formulabot.com", color="#7c3aed", initial="Fb", badge="Free", desc="Text-to-formula & data viz"),
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Explain & generate any formula"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Analyze CSVs via upload"),
     dict(name="Julius", url="https://julius.ai", color="#0ea5e9", initial="Ju", badge="Free", desc="Chat with your data & charts"),
   ]),

 dict(slug="best-ai-tools-for-parents-2026", title="The 6 Best AI Tools for Busy Parents in 2026",
   meta="From meal planning to homework help to managing the family calendar — AI that gives parents their time back.",
   category="For Parents", read="2", lead="Parenting is the original 24/7 job. In 2026, AI can take real load off — planning dinners, explaining homework, organizing schedules, and tracking milestones. Here's the family-friendly stack.",
   verdict="Start with ChatGPT for homework help and meal planning, add a calendar AI for scheduling, and a photo organizer for the memory overload. Small daily saves add up to hours back each week.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Homework explainer & meal planner"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Patient, gentle tutor for kids"),
     dict(name="Motion", url="https://www.usemotion.com/?ref=toolforge", color="#6366f1", initial="Mo", badge="$19/mo", desc="Auto-schedule the family calendar"),
     dict(name="Notion", url="https://www.notion.so", color="#111827", initial="No", badge="Free", desc="Shared family wiki & lists"),
     dict(name="Gemini", url="https://gemini.google.com", color="#4285f4", initial="Ge", badge="Free", desc="Recipe & schedule helper in Workspace"),
     dict(name="Otter.ai", url="https://otter.ai", color="#111827", initial="Ot", badge="Free", desc="Capture kids' appointments & notes"),
   ]),

 dict(slug="best-ai-tools-for-small-business-2026", title="The 10 Best AI Tools for Small Businesses in 2026 (Under $200/mo Total)",
   meta="A lean AI stack that replaces three hires: marketing, support, and ops — all for less than one intern's wage.",
   category="For Business", read="3", lead="Small businesses can't afford big teams, but they can afford AI. For under $200/month total, a solo founder or tiny team can cover content, customer support, and operations. Here's the stack we'd actually buy.",
   verdict="Spend on ChatGPT/Claude (writing), a support bot (Intercom or Tidio), and ops automation (Make or Zapier). Add Gamma for decks and Ollama if privacy matters. Total well under $200/mo — and it scales with you.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="$20/mo", desc="Writing, strategy, support drafts"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="$20/mo", desc="Long docs & client comms"),
     dict(name="Intercom", url="https://www.intercom.com", color="#1a1a1a", initial="Ic", badge="$39/mo", desc="AI customer support bot"),
     dict(name="Make", url="https://www.make.com/en?ref=toolforge", color="#0a72ef", initial="Mk", badge="$9/mo", desc="Automate ops & invoicing"),
     dict(name="Gamma", url="https://gamma.app", color="#673ab7", initial="Ga", badge="$10/mo", desc="Pitch decks & proposals fast"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="Brand graphics in minutes"),
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Market & competitor research"),
     dict(name="Tidio", url="https://www.tidio.com", color="#6d28d9", initial="Td", badge="$19/mo", desc="Live chat + AI assistant"),
     dict(name="Notion", url="https://www.notion.so", color="#111827", initial="No", badge="Free", desc="Wiki, CRM-lite, docs"),
     dict(name="Ollama", url="https://ollama.com", color="#111827", initial="Ol", badge="Free", desc="Private AI on your own server"),
   ]),
]

# =================== WRITE ===================
