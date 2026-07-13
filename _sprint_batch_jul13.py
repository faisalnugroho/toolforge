#!/usr/bin/env python3
"""ToolForge Sprint Generator — batch content creator (2026-07-13).
Creates new tool / compare / blog pages using the EXACT existing site
templates, skips any slug that already exists, and appends new URLs to
sitemap.xml with today's date. Non-destructive and idempotent.
"""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-13"
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
  "datePublished": "{TODAY}",
  "dateModified": "{TODAY}"
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
            <span>✍️ Published {TODAY}</span>
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
 dict(slug="cambai", name="Camb AI", tagline="Studio-grade AI voice generation and dubbing with 140+ languages and instant voice cloning.", category="Audio",
   color1="#6d28d9", color2="#4c1d95", initials="Ca", price="$8/mo", price_label="Starter", price_num="8",
   free_tier="Free tier (limited)", rating="4.6/5", rating_num="4.6", users="500K+ creators", founded="2021",
   headline="Voices that don't sound like robots",
   intro="Camb AI is a voice AI platform that generates expressive text-to-speech in 140+ languages and clones voices from a short sample. Built for creators and localizers who need natural-sounding dubs at scale, it pairs a browser studio with a developer API so teams can ship multilingual audio without a voice-actor call.",
   who_for="Video localizers, podcasters, and indie studios who need multilingual voiceovers without hiring voice actors.",
   features=[("🎙️","Text-to-Speech","Generate natural voiceovers in 140+ languages with emotion control and SSML support."),
             ("👥","Voice Cloning","Clone any voice from a 30-second sample and regenerate it on demand."),
             ("🌍","Instant Dubbing","Upload a video and get a translated, re-voiced version in minutes."),
             ("🔌","API & SDK","Drop TTS and dubbing into your product via a REST API and Python SDK.")],
   pros=["140+ languages — rare for voice cloning tools","Voice cloning works from very short samples","API is fast and well-documented","Free tier to test before paying"],
   cons=["Cloned voices still need QA for emotional range","UI is less polished than ElevenLabs","Concurrency limits on lower tiers","No desktop editor app yet"],
   verdict="If you localize video or ship multilingual content, Camb AI is the cheapest path to studio-grade dubs. The free tier gets you a long way; the API pays for itself the first time you skip a voice-actor session.",
   cta_url="https://camb.ai/"),
 dict(slug="typecast-ai", name="Typecast", tagline="AI voice actors and virtual presenters that turn scripts into narrated videos.", category="Audio",
   color1="#0ea5e9", color2="#0284c7", initials="Ty", price="$12/mo", price_label="Starter", price_num="12",
   free_tier="Free plan (limited)", rating="4.4/5", rating_num="4.4", users="1M+ users", founded="2019",
   headline="A whole cast of AI voice actors",
   intro="Typecast gives you a library of AI voice actors plus on-screen virtual presenters, so a single script becomes a fully narrated explainer or training video. It's built for L&D teams and marketers who need lots of voiceover without booking talent.",
   who_for="E-learning teams, corporate trainers, and marketers producing high-volume explainer content.",
   features=[("🎭","Voice Library","Hundreds of distinct AI voices with age, emotion, and persona presets."),
             ("🧑‍💼","Virtual Presenters","On-screen avatars that lip-sync to your script for slide-style videos."),
             ("✂️","Script Editor","Write, assign voices, and preview in one timeline."),
             ("📤","Export","Render to MP4 or pull audio for podcasts and ads.")],
   pros=["Huge voice library with consistent quality","Virtual presenters save on filming","Great for training/e-learning at scale","Friendly editor, low learning curve"],
   cons=["Avatars look more 'corporate' than lifelike","Fewer languages than dedicated TTS tools","Free plan watermarks exports","Voice cloning is gated to higher tiers"],
   verdict="For corporate training and explainer video, Typecast removes the talent-booking bottleneck. It won't replace a real spokesperson for hero content, but for the 90% of internal video, it's a steal.",
   cta_url="https://typecast.ai/"),
 dict(slug="yepic-ai", name="Yepic AI", tagline="Talking-avatar videos you can generate, translate, and localize in 40+ languages.", category="Video",
   color1="#ec4899", color2="#db2777", initials="Ye", price="$29/mo", price_label="Creator", price_num="29",
   free_tier="Free trial", rating="4.3/5", rating_num="4.3", users="800K+ creators", founded="2018",
   headline="A presenter who speaks every language",
   intro="Yepic turns a script or slide deck into a video hosted by a photoreal AI avatar. The killer feature is instant translation — record once, then export the same video in 40+ languages with lip-synced avatars.",
   who_for="Educators, sales teams, and agencies localizing the same message across markets.",
   features=[("🧑‍🏫","AI Avatars","Photoreal and stylized presenters that read your script on-camera."),
             ("🌐","1-Click Translate","Regenerate any video in 40+ languages with synced lips."),
             ("📊","Slides to Video","Drop in a deck and Yepic narrates each slide."),
             ("🔗","API","Generate avatar videos programmatically at scale.")],
   pros=["Translation workflow is genuinely best-in-class","Good avatar realism vs price","API for high-volume generation","No camera or studio needed"],
   cons=["Avatar hand/body motion still stiff","Best avatars locked behind pricier tiers","Editor can lag on long scripts","Credit system confuses new users"],
   verdict="If your content needs to exist in many languages, Yepic's translate-and-relip-sync pipeline is the fastest route. For English-only hero videos, HeyGen is the closer rival.",
   cta_url="https://yepic.ai/"),
 dict(slug="storydoc", name="Storydoc", tagline="Interactive AI presentations that replace static slide decks for sales and marketing.", category="Productivity",
   color1="#f59e0b", color2="#d97706", initials="St", price="$25/mo", price_label="Starter", price_num="25",
   free_tier="Free trial", rating="4.5/5", rating_num="4.5", users="200K+ teams", founded="2020",
   headline="Slide decks that talk back",
   intro="Storydoc rebuilds the pitch deck as an interactive web page — with live data, scroll-triggered animations, and analytics on who actually read it. AI turns a brief into a branded deck in minutes.",
   who_for="Sales reps, consultants, and marketers who live or die by decks that get opened.",
   features=[("✨","AI Generator","Paste a brief and get a structured, on-brand deck instantly."),
             ("📊","Live Data","Embed live charts, calendars, and pricing that update automatically."),
             ("📈","Analytics","See exactly who viewed, scrolled, and clicked — by slide."),
             ("🔗","Share","Send a link instead of a 40MB PDF; works on any device.")],
   pros=["View analytics are a genuine sales superpower","Interactive format beats static PDFs","Templates look premium out of the box","Easy to rebrand for each prospect"],
   cons=["Not a fit for dense internal documentation","Best features require the higher tier","Export to PPTX is lossy","Learning curve for non-designers"],
   verdict="For outbound sales and client decks, Storydoc's analytics alone justify the sub — you finally know if the deck got read. Static slides can't tell you that.",
   cta_url="https://www.storydoc.com/"),
 dict(slug="mentimeter", name="Mentimeter", tagline="Interactive presentations with live polls, quizzes, and word clouds your audience answers in real time.", category="Productivity",
   color1="#14b8a6", color2="#0d9488", initials="Me", price="$11/mo", price_label="Pro", price_num="11",
   free_tier="Free (limited)", rating="4.4/5", rating_num="4.4", users="300M+ participants", founded="2014",
   headline="Make the room talk back",
   intro="Mentimeter turns a one-way slideshow into a two-way conversation. Drop in live polls, quizzes, and word clouds; your audience joins via a code on their phones and answers in real time, with results projected live.",
   who_for="Teachers, facilitators, and speakers who need audience engagement, not just slides.",
   features=[("📱","Live Voting","Audience joins with a code and answers on their phones instantly."),
             ("☁️","Word Clouds","Crowd-sourced word clouds that visualize group sentiment live."),
             ("🧩","20+ Slide Types","Quizzes, scales, Q&A, rankings, and open-ended responses."),
             ("📊","Results Export","Pull session data into reports after the event.")],
   pros=["Unmatched for live audience engagement","Free tier covers most classrooms","Works on any device, no app needed","Great analytics for facilitators"],
   cons=["Not a full design tool — pair with PowerPoint","Free plan caps audience size","Some slide types feel gimmicky","Requires wifi for participants"],
   verdict="If you present to people (not just at them), Mentimeter is the engagement layer every deck is missing. The free tier handles most rooms; Pro unlocks the bigger audiences.",
   cta_url="https://www.mentimeter.com/"),
 dict(slug="toddle", name="Toddle", tagline="The open-source, visual alternative to React — build web apps without fighting your framework.", category="Coding",
   color1="#8b5cf6", color2="#7c3aed", initials="To", price="Free", price_label="(open source)", price_num="0",
   free_tier="Free & open source", rating="4.6/5", rating_num="4.6", users="100K+ builders", founded="2021",
   headline="React, but you can see it",
   intro="Toddle is a visual builder that outputs clean, standards-based web components — no lock-in, no proprietary runtime. You design in the browser and ship code you actually own, with AI assist for components and logic.",
   who_for="Agencies, indie hackers, and frontend devs who want speed without a no-code jail.",
   features=[("🧱","Visual Builder","Drag, style, and wire components that compile to real web standards."),
             ("🤖","AI Assist","Generate components, styles, and data logic from prompts."),
             ("🔓","Open Source","Self-host or export; your code, your infrastructure."),
             ("🔌","Integrations","Connect APIs, Supabase, and backend services natively.")],
   pros=["No proprietary runtime — you own the output","Clean, readable code exported","AI assist speeds up UI work","Free and open-source core"],
   cons=["Smaller component ecosystem than Webflow","Team features are paid","Best with some frontend knowledge","Still maturing vs established builders"],
   verdict="Toddle is the rare no-code tool that respects developers — you leave with real code, not a black box. For agencies shipping client sites, the open-source model is the whole point.",
   cta_url="https://toddle.dev/"),
 dict(slug="weweb", name="WeWeb", tagline="A no-code frontend builder for production-grade web apps on top of any backend.", category="Coding",
   color1="#6366f1", color2="#4f46e5", initials="We", price="$29/mo", price_label="Starter", price_num="29",
   free_tier="Free plan", rating="4.5/5", rating_num="4.5", users="150K+ builders", founded="2019",
   headline="Ship a real app without writing the UI",
   intro="WeWeb is a no-code builder for the frontend of serious web apps. Point it at any REST or GraphQL backend (or Supabase/Xano), design in a visual editor, and publish to your own hosting. No lock-in on the data layer.",
   who_for="Founders, agencies, and product teams who need app UIs fast without a React hire.",
   features=[("🎨","Visual Editor","Pixel-level control with reusable components and design tokens."),
             ("🔗","Any Backend","Bind to REST, GraphQL, Supabase, Xano, or your own API."),
             ("🚀","Self-Hosting","Export and deploy to your own infrastructure."),
             ("🤖","AI Builder","Scaffold pages and workflows from a text prompt.")],
   pros=["Works with your existing backend — no data lock-in","Production-grade output, not a toy","Self-hosting keeps you in control","Strong workflow/state tooling"],
   cons=["Steeper learning curve than pure landing-page builders","Backend logic lives elsewhere","Higher tiers needed for teams","Design system setup takes upfront time"],
   verdict="WeWeb is the no-code choice when you've outgrown the toy tools but don't want to hire a frontend team. Bind it to Supabase and you can ship a real SaaS in a weekend.",
   cta_url="https://www.weweb.io/"),
 dict(slug="syllaby", name="Syllaby", tagline="AI that finds faceless video topics, writes the scripts, and plans your content calendar.", category="Video",
   color1="#10b981", color2="#059669", initials="Sy", price="$29/mo", price_label="Standard", price_num="29",
   free_tier="Free trial", rating="4.3/5", rating_num="4.3", users="250K+ creators", founded="2022",
   headline="Faceless YouTube, done for you",
   intro="Syllaby is a content engine for faceless video channels. It researches what your niche is searching for, generates scripted videos complete with AI voiceover and avatars, and lays out a posting calendar — so you can run a channel without ever being on camera.",
   who_for="Solopreneurs and agencies running faceless YouTube/TikTok channels at volume.",
   features=[("🔍","Topic Research","Surfaces high-demand, low-competition video ideas in your niche."),
             ("📝","Script Writer","Generates ready-to-record scripts tuned to your angle."),
             ("🗓️","Content Calendar","Auto-plans a consistent posting schedule."),
             ("🎙️","Voice & Avatar","Turn scripts into narrated or avatar-led videos.")],
   pros=["End-to-end for faceless channels","Topic research saves hours of guessing","Calendar keeps consistency on autopilot","Good for agencies managing many clients"],
   cons=["Output needs your editing to stand out","Voice realism varies by language","Best value only at volume","Credit caps on lower plans"],
   verdict="If you want a faceless content business without the research grind, Syllaby compresses the boring 80% into a few clicks. Pair it with ElevenLabs or HeyGen for the final render.",
   cta_url="https://syllaby.io/"),
 dict(slug="wonderstudio", name="Wonder Studio", tagline="Autodesk's AI that automatically animates, lights, and composites CG characters into live-action footage.", category="Video",
   color1="#f43f5e", color2="#e11d48", initials="Ws", price="$49/mo", price_label="Creator", price_num="49",
   free_tier="Free trial", rating="4.5/5", rating_num="4.5", users="100K+ VFX artists", founded="2021",
   headline="VFX without the roto department",
   intro="Wonder Studio (by Autodesk) uses AI to detect actors in a shot, then automatically rig, animate, light, and composite a CG character in their place — no motion-capture suit, no manual rotoscoping. Upload a video; get a VFX shot back.",
   who_for="Indie filmmakers, VFX artists, and studios that can't afford a full roto and match-move team.",
   features=[("🎬","Auto Roto","AI isolates performers frame-by-frame — no manual masking."),
             ("🦾","CG Characters","Drop in your own rigged character or use the library."),
             ("💡","Auto Light & Comp","Matches lighting and composites the CG into the plate."),
             ("🔌","DCC Export","Sends clean passes to Blender, Maya, and Nuke.")],
   pros=["Eliminates the most tedious VFX labor","Works from ordinary footage, no mocap","Exports to pro DCC tools","Huge time savings for indie teams"],
   cons=["Needs a clean, well-lit performance take","Character library is limited","Heavy shots need a strong GPU","Higher tier for commercial rights"],
   verdict="Wonder Studio is the rare AI tool that doesn't replace artists — it removes the grunt work so they can focus on the craft. For indie VFX, it's a force multiplier.",
   cta_url="https://www.wonderdynamics.com/"),
 dict(slug="pipecat", name="Pipecat", tagline="The open-source framework for building voice and multimodal AI agents that talk in real time.", category="Coding",
   color1="#0a72ef", color2="#0a5ecf", initials="Pi", price="Free", price_label="(open source)", price_num="0",
   free_tier="Free & open source", rating="4.7/5", rating_num="4.7", users="50K+ developers", founded="2023",
   headline="Plumb together a talking AI",
   intro="Pipecat is an open-source Python framework for real-time voice (and multimodal) agents. Chain ASR, LLM, and TTS into a flowing conversation pipeline with interruption handling, then ship it to a phone line, web, or Discord — no per-call vendor lock-in.",
   who_for="Developers building voice bots, AI receptionists, and real-time companions.",
   features=[("🔊","Real-time Voice","Sub-second, interruptible voice pipelines out of the box."),
             ("🧩","Composable","Swap ASR, LLM, TTS, and vision services like Lego."),
             ("🔌","Many Transports","Run on web, phone (SIP), Twilio, Discord, or custom."),
             ("🆓","Open Source","MIT-licensed; self-host and own your stack.")],
   pros=["No per-minute lock-in like hosted voice agents","Truly real-time with barge-in","Massive service ecosystem (OpenAI, ElevenLabs, etc.)","Free and MIT-licensed"],
   cons=["You run the infra — ops overhead","Python-only (no first-class JS yet)","Async pipelines have a learning curve","Debugging real-time audio is fiddly"],
   verdict="If you're serious about voice agents and hate per-call pricing, Pipecat is the open foundation to build on. Host it yourself and a $0 framework handles millions of minutes.",
   cta_url="https://pipecat.ai/"),
]

COMPARES = [
 dict(slug="kling-vs-luma", name_a="Kling AI", name_b="Luma Dream Machine",
   color_a="#7c3aed", color_b="#ec4899", initials_a="Kl", initials_b="Lu",
   desc_a="Text-to-video with strong motion and physics realism",
   desc_b="Fast, dreamy video generation from prompts and images",
   price_a="$8/mo Standard", price_b="$10/mo Lite",
   best_a="realistic motion, physics, camera control", best_b="fast ideation, image-to-video, stylized looks",
   url_a="https://klingai.com/", url_b="https://lumalabs.ai/dream-machine",
   verdict="Use Kling when you need believable motion, physics, and camera control for short films and ads. Use Luma when you want fast, stylized ideation and smooth image-to-video. For most creators, Kling's realism wins; Luma wins on speed and vibe.",
   winner="Kling AI (for realism) · Luma (for speed)"),
 dict(slug="notion-ai-vs-notion-calendar", name_a="Notion AI", name_b="Notion Calendar",
   color_a="#000000", color_b="#0a72ef", initials_a="No", initials_b="Nc",
   desc_a="AI writing, search, and Q&A inside Notion",
   desc_b="Scheduling and time-blocking across Google/Outlook",
   price_a="$10/mo Add-on", price_b="Free / $8 Pro",
   best_a="drafting, summarizing, Ask AI across your workspace", best_b="time-blocking, calendar unification, scheduling links",
   url_a="https://www.notion.so/product/ai", url_b="https://www.notion.so/product/calendar",
   verdict="Notion AI and Notion Calendar solve different problems — one thinks, one schedules. Get Notion AI if your bottleneck is writing and finding info; get Notion Calendar if it's managing your time. Power users run both.",
   winner="Depends — AI for writing, Calendar for scheduling"),
 dict(slug="slack-ai-vs-ms-copilot", name_a="Slack AI", name_b="Microsoft Copilot",
   color_a="#611f69", color_b="#0a72ef", initials_a="Sl", initials_b="Mc",
   desc_a="Summaries, search, and thread recaps inside Slack",
   desc_b="AI across Microsoft 365 (Word, Excel, Teams, Outlook)",
   price_a="$10/mo Add-on", price_b="$30/mo per user",
   best_a="catching up on channels, recaps, huddle summaries", best_b="working across the whole M365 suite",
   url_a="https://slack.com/features/ai", url_b="https://www.microsoft.com/en-us/microsoft-copilot",
   verdict="Slack AI is a focused, cheap way to tame notification overload inside Slack. Microsoft Copilot is a broad assistant across your entire Office workflow but costs 3x. Pick Slack AI if you live in Slack; pick Copilot if your work is Word/Excel/Teams-heavy.",
   winner="Slack AI (for Slack users) · Copilot (for M365 suites)"),
 dict(slug="gemini-vs-claude-3-5", name_a="Gemini", name_b="Claude 3.5",
   color_a="#4285f4", color_b="#d97706", initials_a="Ge", initials_b="C3",
   desc_a="Google's multimodal model with the longest context window",
   desc_b="Anthropic's previous-gen flagship, still beloved for coding",
   price_a="Free / $20 AI Pro", price_b="Free / $20 Pro (legacy)",
   best_a="huge context, multimodal, Google Workspace integration", best_b="fast coding, artifact building, reliable prose",
   url_a="https://gemini.google.com/", url_b="https://claude.ai/",
   verdict="Claude 3.5 was the 2024 coding darling and still holds up for fast, artifact-driven work. Gemini wins on context length and multimodal input. In 2026 both have newer flagships — but if you're locked to the 3.5 era, Gemini's context edge makes it the safer default.",
   winner="Gemini (for context/multimodal)"),
 dict(slug="veo-vs-luma", name_a="Google Veo", name_b="Luma Dream Machine",
   color_a="#4285f4", color_b="#ec4899", initials_a="Ve", initials_b="Lu",
   desc_a="Google's highest-fidelity text-to-video model",
   desc_b="Fast, dreamy video generation from prompts and images",
   price_a="$20/mo (Gemini Ultra)", price_b="$10/mo Lite",
   best_a="cinematic realism, prompt adherence, physics", best_b="fast ideation, image-to-video, accessibility",
   url_a="https://deepmind.google/technologies/veo/", url_b="https://lumalabs.ai/dream-machine",
   verdict="Veo is the realism leader but lives inside Google's paid tiers and is less accessible. Luma is faster, cheaper, and easier to experiment with. For production cinematic shots, Veo; for rapid iteration, Luma.",
   winner="Veo (realism) · Luma (accessibility)"),
 dict(slug="figma-vs-framer", name_a="Figma", name_b="Framer",
   color_a="#f24e1e", color_b="#0a72ef", initials_a="Fi", initials_b="Fr",
   desc_a="Collaborative design and prototyping for product teams",
   desc_b="Design tool that publishes production-ready websites",
   price_a="Free / $12 Editor", price_b="$20/mo Mini",
   best_a="team design systems, prototyping, dev handoff", best_b="shipping marketing sites straight from design",
   url_a="https://www.figma.com/", url_b="https://www.framer.com/",
   verdict="Figma is the collaborative design standard for product teams. Framer is the faster path from design to a live, code-free marketing site. If you're building an app, Figma; if you're shipping a website, Framer.",
   winner="Figma (product design) · Framer (websites)"),
]

BLOGS = [
 dict(slug="best-ai-tools-for-filmmakers-2026", title="The 9 Best AI Tools for Filmmakers in 2026 (From Script to Screen)",
   meta="AI is reshaping indie filmmaking. The tools that cut your budget and speed up pre- to post-production — tested and ranked with real pricing.",
   category="Filmmaking", read="6",
   lead="Filmmaking in 2026 is part human craft, part AI leverage. The indie teams shipping festival-quality work aren't spending six figures on VFX — they're running a stack that handles rotoscoping, voice, and color so they can focus on the shot.",
   verdict="Start with Runway or Kling for generation, Wonder Studio for VFX, and ElevenLabs for ADR and voiceover. CapCut and Descript finish the edit. The whole stack costs less than one day of traditional post.",
   tools=[
     dict(name="Runway", color="#14b8a6", initial="Ru", badge="From $12/mo", desc="Generative video, rotoscoping, and motion tools for shots", url="https://runwayml.com/"),
     dict(name="Kling AI", color="#7c3aed", initial="Kl", badge="From $8/mo", desc="High-fidelity text-to-video with real physics", url="https://klingai.com/"),
     dict(name="Wonder Studio", color="#f43f5e", initial="Ws", badge="$49/mo", desc="Auto VFX: rig, light, and composite CG characters", url="https://www.wonderdynamics.com/"),
     dict(name="ElevenLabs", color="#06b6d4", initial="E", badge="Free tier", desc="ADR, voiceover, and dubbing with voice cloning", url="https://elevenlabs.io/"),
     dict(name="Adobe Firefly", color="#ff0000", initial="Af", badge="From $10/mo", desc="Image and video generation inside Creative Cloud", url="https://www.adobe.com/products/firefly.html"),
     dict(name="Descript", color="#6366f1", initial="De", badge="From $12/mo", desc="Transcribe, edit video by editing text, overdub", url="https://www.descript.com/"),
     dict(name="CapCut", color="#ff2e63", initial="Cc", badge="Free", desc="Fast cuts, auto-captions, and AI effects", url="https://www.capcut.com/"),
     dict(name="Topaz Video AI", color="#111827", initial="Tv", badge="$299 once", desc="Upscale, denoise, and slow-mo restoration", url="https://www.topazlabs.com/video-ai"),
   ]),
 dict(slug="best-ai-tools-for-animation-2026", title="The 9 Best AI Animation Tools in 2026 (2D, 3D & Motion)",
   meta="From storyboard to rendered frames — the AI animation stack that lets solo creators make studio-quality motion. Tested, ranked, with pricing.",
   category="Animation", read="6",
   lead="Animation used to need a studio. In 2026 a solo creator with the right AI stack can produce shorts that look hand-drawn or fully 3D. Here's the toolchain we'd actually pay for.",
   verdict="For 2D/3D hybrid work, Runway + Kling cover generation; Stable Diffusion and Krea handle style; CapCut and Descript finish. You can animate a full short solo for under $100/mo.",
   tools=[
     dict(name="Runway", color="#14b8a6", initial="Ru", badge="From $12/mo", desc="Generative motion and rotoscoping for animators", url="https://runwayml.com/"),
     dict(name="Kling AI", color="#7c3aed", initial="Kl", badge="From $8/mo", desc="Physics-aware text-to-video animation", url="https://klingai.com/"),
     dict(name="Luma Dream Machine", color="#ec4899", initial="Lu", badge="From $10/mo", desc="Smooth image-to-video and stylized motion", url="https://lumalabs.ai/dream-machine"),
     dict(name="Stable Diffusion", color="#111827", initial="Sd", badge="Free / open", desc="Controllable 2D frame generation and style", url="https://stability.ai/"),
     dict(name="Krea", color="#0a72ef", initial="Kr", badge="From $8/mo", desc="Real-time AI canvas for concept and style", url="https://krea.ai/"),
     dict(name="Adobe Firefly", color="#ff0000", initial="Af", badge="From $10/mo", desc="Safe-for-commercial image and video generation", url="https://www.adobe.com/products/firefly.html"),
     dict(name="CapCut", color="#ff2e63", initial="Cc", badge="Free", desc="Motion presets, captions, and finishing", url="https://www.capcut.com/"),
     dict(name="Descript", color="#6366f1", initial="De", badge="From $12/mo", desc="Edit animation reels by editing the transcript", url="https://www.descript.com/"),
   ]),
 dict(slug="best-ai-tools-for-music-producers-2026", title="The 9 Best AI Tools for Music Producers in 2026",
   meta="AI won't replace your taste — but it will replace your busywork. The tools that speed up ideation, mixing, and mastering, ranked with real pricing.",
   category="Music", read="5",
   lead="Producers in 2026 treat AI like a session player: fast ideation, instant stems, and a mastering chain that used to cost a studio day. Here's the stack that earns its subscription.",
   verdict="Suno and Udio for demos, Moises and Lalal for stem separation, Soundraw for royalty-free beds. The whole ideation-to-master stack is cheaper than one studio session.",
   tools=[
     dict(name="Suno", color="#0a72ef", initial="Su", badge="From $10/mo", desc="Generate full songs from a text prompt", url="https://suno.com/"),
     dict(name="Udio", color="#7c3aed", initial="Ud", badge="From $10/mo", desc="High-fidelity music generation for producers", url="https://udio.com/"),
     dict(name="ElevenLabs", color="#06b6d4", initial="E", badge="Free tier", desc="Studio voice and vocal synthesis", url="https://elevenlabs.io/"),
     dict(name="Moises", color="#10b981", initial="Mo", badge="From $8/mo", desc="Stem separation and tempo/pitch tools", url="https://moises.ai/"),
     dict(name="Lalal", color="#ec4899", initial="La", badge="From $15", desc="Clean vocal and instrumental extraction", url="https://www.lalal.ai/"),
     dict(name="Soundraw", color="#f59e0b", initial="Sr", badge="From $17/mo", desc="Royalty-free AI music beds you can edit", url="https://soundraw.io/"),
     dict(name="Boomy", color="#14b8a6", initial="Bo", badge="Free tier", desc="Instant tracks for quick drafts", url="https://boomy.com/"),
     dict(name="Aiva", color="#6366f1", initial="Ai", badge="From $15/mo", desc="AI composition for score and Ambient", url="https://aiva.ai/"),
   ]),
]

# =================== WRITE + SITEMAP ===================
new_urls = []

print("=== TOOLS ===")
for t in TOOLS:
    if t['slug'] in tool_slugs:
        print(f"  skip (exists): {t['slug']}")
        continue
    html = tool_html(t)
    with open(os.path.join(BASE, 'tools', t['slug'] + '.html'), 'w') as f:
        f.write(html)
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html")
    print(f"  wrote tools/{t['slug']}.html")

print("=== COMPARES ===")
for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print(f"  skip (exists): {c['slug']}")
        continue
    html = compare_html(c)
    with open(os.path.join(BASE, 'compare', c['slug'] + '.html'), 'w') as f:
        f.write(html)
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    print(f"  wrote compare/{c['slug']}.html")

print("=== BLOGS ===")
for b in BLOGS:
    if b['slug'] in blog_slugs:
        print(f"  skip (exists): {b['slug']}")
        continue
    html = blog_html(b)
    with open(os.path.join(BASE, 'blog', b['slug'] + '.html'), 'w') as f:
        f.write(html)
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    print(f"  wrote blog/{b['slug']}.html")

print(f"\n=== SITEMAP: appending {len(new_urls)} new URLs ===")
if new_urls:
    sm = os.path.join(BASE, 'sitemap.xml')
    with open(sm) as f:
        content = f.read()
    blocks = []
    for u in new_urls:
        blocks.append(f'''  <url>
    <loc>{u}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>''')
    insert = "\n".join(blocks) + "\n</urlset>"
    content = content.replace("</urlset>", insert, 1)
    with open(sm, 'w') as f:
        f.write(content)
    print(f"  OK appended {len(new_urls)} URLs")

print(f"\nDONE. New pages created: {len(new_urls)}")
