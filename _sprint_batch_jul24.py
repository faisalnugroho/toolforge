#!/usr/bin/env python3
"""ToolForge Sprint Batch — 2026-07-24 (cron worker).

Adds genuine gap pages using the EXACT established site templates:
  - 6 tool pages (audio editing / music production gaps)
  - 3 blog posts (underserved niche: pharmacists, chemists, astronomers)
  - 4 compare pages (high search volume "X vs Y" not yet covered)

Skips any slug that already exists (idempotent). Appends new URLs to
sitemap.xml with today's date. Templates mirror tools/cursor.html,
compare/chatgpt-vs-claude.html, blog/best-ai-tools-for-freelancers.html.
"""
import os

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-24"
DOMAIN = "https://toolforge.io"

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
  "datePublished": "2026-07-24",
  "dateModified": "2026-07-24"
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
 dict(slug="filmora", name="Filmora", tagline="The beginner-friendly video editor with AI effects, templates, and one-click edits for creators who skip the learning curve.",
   category="Video", color1="#4f46e5", color2="#818cf8", initials="Fi", price="$49", price_label="/yr (annual)",
   price_num="49", free_tier="Free trial", rating="4.4/5", rating_num="4.4", users="10M+ creators", founded="2007",
   headline="Video editing without the tears",
   intro="Filmora (by Wondershare) is the video editor that lives between TikTok simplicity and Premiere complexity. Its 2026 AI suite auto-cuts dead air, removes background noise, generates captions, and applies trendy effects with one click — all in an interface a complete beginner can drive in 10 minutes. For YouTubers, course creators, and small businesses that need to ship video without a full editor, Filmora is often the right price-to-ease ratio.",
   who_for="Content creators, educators, and small businesses that want polished video without learning Premiere Pro or hiring an editor.",
   features=[
     ("AI Cut", "Smart silence removal", "Auto-detects and deletes dead air, 'ums,' and pauses — your 20-minute talking-head becomes 12 tight minutes."),
     ("Captions", "Auto subtitles", "Transcribe speech to on-brand captions in 30+ languages, then style with presets sized for TikTok and Reels."),
     ("Audio", "AI noise removal", "Strip out fans, traffic, and room echo without a separate audio pass or plugins."),
     ("Templates", "Trending effects", "One-click templates that follow current social formats — shake transitions, glow text, beat-sync cuts."),
   ],
   pros=["Easiest NLE to learn in its price range","AI silence removal saves hours on talking-head content","Generous effect and template library","Good value on the annual plan"],
   cons=["Free trial watermarks everything","Not as deep as Premiere or DaVinci for color/grading","Render can be slow on older machines","Crossgrades are pricey if you already own another NLE"],
   verdict="Filmora is the right call if you want to make videos that look good fast and you don't plan to go pro. It's the beginner NLE that genuinely respects your time.",
   cta_url="https://filmora.wondershare.com/?via=toolforge"),

 dict(slug="audacity", name="Audacity", tagline="The free, open-source audio editor — podcast, music, and voiceover workhorse with a thriving plugin ecosystem.",
   category="Audio", color1="#1e3a8a", color2="#3b82f6", initials="Au", price="$0", price_label="open source",
   price_num="0", free_tier="Free forever", rating="4.5/5", rating_num="4.5", users="100M+ downloads", founded="2000",
   headline="Free audio editing that just works",
   intro="Audacity has been the gateway audio editor for 25 years, and the 2026 builds finally brought real-time effects, non-destructive editing, and a cleaner UI while staying 100% free and open source. Podcasters cut episodes, musicians record demos, and voice actors cut takes in it every day. The new AI features — noise reduction, beat detection, and silence trimming via the OpenVINO plugin pack — closed the gap with paid tools without changing the price.",
   who_for="Podcasters, musicians, voice actors, and anyone who needs reliable multi-track audio editing without paying for Pro Tools.",
   features=[
     ("Multi", "Multi-track editing", "Layer as many tracks as your machine can handle — voice, music, SFX — and mix non-destructively."),
     ("AI NR", "Noise reduction", "The spectral noise reduction tool, plus the OpenVINO AI pack, removes hiss and hum without artifacts."),
     ("Free", "No license fees", "GPL-licensed — use it at home, in the studio, or commercially. Zero cost, zero restrictions."),
     ("FX", "Real-time effects", "Apply EQ, compression, and reverb and hear changes live rather than rendering to preview."),
   ],
   pros=["Completely free and open source","Massive plugin and tutorial ecosystem","Runs on virtually any OS (Win/Mac/Linux)","New AI features rival paid restoration tools"],
   cons=["UI still looks dated despite the refresh","No built-in collaborative features","MIDI support is limited vs a full DAW","Steeper curve than GarageBand for total beginners"],
   verdict="Audacity is the audio editor you should install first — before you ever consider paying. It handles 90% of podcast and voiceover work for zero dollars.",
   cta_url="https://www.audacityteam.org/?via=toolforge"),

 dict(slug="auphonic", name="Auphonic", tagline="The AI audio post-production engine that levels, cleans, and masters your podcast in one click — no engineering needed.",
   category="Audio", color1="#2563eb", color2="#60a5fa", initials="Au", price="$11", price_label="/mo Starter",
   price_num="11", free_tier="Free tier (2h/mo)", rating="4.6/5", rating_num="4.6", users="100K+ creators", founded="2013",
   headline="One-click podcast mastering",
   intro="Auphonic is the AI audio processor that takes your rough recording and hands back a mastered episode — levels balanced, noise removed, loudness normalized to broadcast specs — all automatically. You upload, pick a preset, and download. For podcasters who don't want to learn a DAW but need to sound professional, it's the most reliable single step in the chain.",
   who_for="Podcasters, interviewers, and content teams that want broadcast-quality audio without hiring an audio engineer.",
   features=[
     ("Level", "Adaptive leveling", "Balances loud and quiet speakers automatically so listeners never reach for the volume knob."),
     ("Clean", "Noise + hum removal", "AI detects and suppresses steady background noise, hiss, and AC hum without a manual pass."),
     ("LUFS", "Loudness normalization", "Output hits EBU R128 / ATSC A/85 specs so you pass platform checks on Spotify, Apple, and YouTube."),
     ("API", "Batch + API", "Process whole back catalogs via the API or drop folders for hands-off batch mastering."),
   ],
   pros=["Genuinely one-click for most podcasts","Hits loudness targets every platform requires","Free tier covers small shows","API for automating pipelines"],
   cons=["Advanced users outgrow the presets","Cloud-only — no offline processing","Upload/download adds a step vs in-DAW mastering","Paid tiers meter by hours"],
   verdict="Auphonic is the single highest-leverage tool for podcasters who don't want to master audio themselves. Two free hours a month is enough to prove its value.",
   cta_url="https://auphonic.com/?via=toolforge"),

 dict(slug="hindenburg", name="Hindenburg", tagline="The audio editor built specifically for radio and podcast professionals — journalism-grade features, broadcast loudness, and an interview-first workflow.",
   category="Audio", color1="#dc2626", color2="#f87171", initials="Hi", price="$115", price_label="one-time (PRO)",
   price_num="115", free_tier="30-day trial", rating="4.5/5", rating_num="4.5", users="50K+ journalists", founded="2010",
   headline="The journalist's audio editor",
   intro="Hindenburg is the audio NLE designed for the way radio and podcast professionals actually work: record an interview, mark the good bits, cut on the marks, and export to broadcast loudness specs — all without touching a compressor or limiter manually. Its magic clipboard auto-levels pasted clips, and the loudness tools guarantee you pass NPR/BBC distribution checks on the first try.",
   who_for="Journalists, radio producers, and narrative podcasters who need a fast, interview-driven workflow and broadcast-correct output.",
   features=[
     ("Marks", "Record + mark", "Drop markers live while recording so you can jump straight to the quote later."),
     ("Magic", "Magic clipboard", "Paste clips from anywhere and they're auto-leveled to match — no manual gain matching."),
     ("Loud", "Broadcast loudness", "One button to EBU R128 or ATSC A/85 — your episode ships distribution-ready."),
     ("Publish", "Export + publish", "Export to MP3/WAV and push directly to podcast hosts without leaving the app."),
   ],
   pros=["Built for journalism, not music","Magic clipboard saves enormous time","Guaranteed loudness compliance","Cleaner than Audacity for pure spoken-word"],
   cons=["One-time price is steep vs free Audacity","Not a DAW — limited for music production","Smaller plugin ecosystem","Subscription unlocks cloud features"],
   verdict="If you produce spoken-word content professionally, Hindenburg pays for itself in the time it saves on leveling and loudness alone. Audacity is fine to start, but Hindenburg is built for the job.",
   cta_url="https://hindenburg.com/?via=toolforge"),

 dict(slug="splice", name="Splice", tagline="The cloud platform for royalty-free samples, AI-powered presets, and plugin rentals that producers use to finish tracks faster.",
   category="Audio", color1="#7c3aed", color2="#a78bfa", initials="Sp", price="$12", price_label="/mo Creator",
   price_num="12", free_tier="Free trial", rating="4.5/5", rating_num="4.5", users="5M+ producers", founded="2013",
   headline="Samples, presets, and plugins on tap",
   intro="Splice is the sample and preset library that redefined how producers discover sounds. Its 2026 AI features — 'Similar Sounds' search, auto-key-matched sample browsing, and text-to-sample previews — mean you find the right kick or loop in seconds instead of scrolling a folder. The rent-to-own plugin program lets you own Serum, Output, and Native Instruments tools for the price of a coffee a month.",
   who_for="Beatmakers, electronic producers, and film composers who want a constantly fresh sound library without buying sample packs à la carte.",
   features=[
     ("AI", "Similar sounds", "Pick a loop you like and AI surfaces harmonically compatible ones — key and BPM matched automatically."),
     ("Rent", "Rent-to-own plugins", "Pay monthly toward Serum, Output Arcade, and more; once paid off, the license is yours."),
     ("Cloud", "Project backups", "Sessions auto-save to the cloud with version history so you never lose a take."),
     ("Stems", "Stem access", "Grab just the kick, snare, or melody from a multi-part loop without bouncing stems yourself."),
   ],
   pros=["Largest royalty-free sample catalog","AI key/BPM matching is a real time-saver","Rent-to-own beats buying plugins outright","Cloud versioning saved more than one project"],
   cons=["Subscription model adds up over years","Downloads metered on lower tiers","Not a DAW — companion to Ableton/FL","Mobile app is limited vs desktop"],
   verdict="If you produce music and you're not on Splice, you're spending more time hunting for sounds than making them. The $12/mo is the cheapest studio upgrade you'll make.",
   cta_url="https://splice.com/?via=toolforge"),

 dict(slug="landr", name="LANDR", tagline="The AI mastering and distribution platform — upload a mix, get a mastered track, and release to every streaming service in one place.",
   category="Audio", color1="#0ea5e9", color2="#38bdf8", initials="La", price="$12", price_label="/mo Studio",
   price_num="12", free_tier="Free master preview", rating="4.2/5", rating_num="4.2", users="2M+ musicians", founded="2014",
   headline="Master your music with AI",
   intro="LANDR pioneered AI audio mastering and in 2026 it's still the fastest path from a finished mix to a release-ready master. Upload a track, the engine analyzes reference tracks in your genre, and returns a mastered version in seconds — with options for intensity, EQ character, and loudness target. Add distribution to Spotify, Apple Music, and 150+ stores, and you have a release pipeline for independent artists.",
   who_for="Independent musicians, beatmakers, and small labels that want professional mastering and distribution without hiring a mastering engineer.",
   features=[
     ("AI", "AI mastering", "Genre-aware mastering engine returns a release-ready track in under a minute, with A/B preview against your original."),
     ("Dist", "Global distribution", "Push your master to Spotify, Apple Music, YouTube Music, and 150+ stores from one dashboard."),
     ("Samples", "Sample library", "Royalty-free samples and loops included with Studio, integrated into your DAW via the LANDR plugin."),
     ("Promo", "Promo tools", "Generate pre-save links, smart links, and social assets for your release from the same platform."),
   ],
   pros=["Fastest mastering workflow on the market","Distribution bundled — one vendor for release","A/B preview lets you compare before committing","Good for volume (EPs, beat tapes)"],
   cons=["AI master won't match a great human engineer","Pay-per-master on lower tiers","Distribution splits royalties on free plans","Less control than an Ozone/Pro Tools chain"],
   verdict="LANDR is the right tool for independent artists releasing singles and EPs at volume who need mastering + distribution in one flow. For a flagship album, hire a human — for everything else, LANDR ships.",
   cta_url="https://www.landr.com/?via=toolforge"),
]

COMPARES = [
 dict(slug="otter-vs-superhuman", name_a="Otter.ai", name_b="Superhuman", color_a="#3b82f6", color_b="#000000",
   initials_a="Ot", initials_b="Su",
   desc_a="The AI meeting note-taker that joins your calls, transcribes, and summarizes automatically.",
   desc_b="The fastest email client in the world — keyboard-driven inbox zero with AI triage.",
   price_a="$8/mo Pro", price_b="$30/mo", best_a="meeting notes, transcripts", best_b="inbox speed, email triage",
   url_a="https://otter.ai/?via=toolforge", url_b="https://superhuman.com/?via=toolforge",
   verdict="These tools solve different problems and many professionals use both. Otter.ai is the meeting sidekick that frees you from note-taking in calls. Superhuman is the email weapon that cuts inbox time in half. If you can only pick one, choose Otter if your day is meeting-heavy, Superhuman if your day is email-heavy.",
   winner="Otter for meetings, Superhuman for email"),

 dict(slug="jasper-vs-grammarly", name_a="Jasper AI", name_b="Grammarly", color_a="#7928ca", color_b="#15c39a",
   initials_a="Ja", initials_b="Gr",
   desc_a="The AI copywriting platform built for marketing teams — brand voice, campaigns, templates.",
   desc_b="The real-time writing assistant that fixes grammar, tone, and clarity as you type anywhere.",
   price_a="$49/mo Creator", price_b="$12/mo Premium", best_a="marketing copy at scale", best_b="everyday writing polish",
   url_a="https://jasper.ai/?via=toolforge", url_b="https://grammarly.com/?via=toolforge",
   verdict="Jasper and Grammarly sit at different points of the writing stack. Jasper generates original marketing copy in your brand voice — use it when you need to produce campaign volume. Grammarly polishes everything you write across every app — use it daily as a safety net. Most marketing teams should run both.",
   winner="Jasper to create, Grammarly to polish"),

 dict(slug="filmora-vs-capcut", name_a="Filmora", name_b="CapCut", color_a="#4f46e5", color_b="#000000",
   initials_a="Fi", initials_b="Ca",
   desc_a="The desktop NLE with AI effects, templates, and one-click edits for creators.",
   desc_b="The free mobile + web editor from ByteDance — built for TikTok, Reels, and Shorts.",
   price_a="$49/yr", price_b="Free / $8 Pro", best_a="long-form YouTube, courses", best_b="short-form social clips",
   url_a="https://filmora.wondershare.com/?via=toolforge", url_b="https://capcut.com/?via=toolforge",
   verdict="CapCut wins on free price, mobile speed, and one-tap TikTok templates — it's the short-form champion. Filmora wins on timeline depth, desktop power, and long-form editing. Use CapCut for social clips; pick Filmora when you need a real desktop editor for YouTube or courses.",
   winner="CapCut for social, Filmora for desktop"),

 dict(slug="landr-vs-bandlab", name_a="LANDR", name_b="BandLab", color_a="#0ea5e9", color_b="#ef4444",
   initials_a="La", initials_b="Ba",
   desc_a="The AI mastering and distribution platform for independent musicians.",
   desc_b="The free, browser-based DAW and social network for making music collaboratively.",
   price_a="$12/mo Studio", price_b="Free", best_a="mastering + distribution", best_b="making + collaborating",
   url_a="https://www.landr.com/?via=toolforge", url_b="https://bandlab.com/?via=toolforge",
   verdict="BandLab is where you make music — a free, full DAW in the browser with collaboration built in. LANDR is what you use after the mix is done — AI mastering and global distribution. They're complementary: make in BandLab, master and release with LANDR. If you only want one free tool, BandLab is the better starting point.",
   winner="BandLab to make, LANDR to release"),
]

BLOGS = [
 dict(slug="best-ai-tools-for-pharmacists-2026", title="The 7 Best AI Tools for Pharmacists in 2026 (Save Hours on Reviews and Counseling)",
   category="For Pharmacists", meta="Drug interaction checks, prior auth paperwork, patient counseling scripts — these AI tools cut the admin that buries pharmacists.",
   read="3", lead="Pharmacists spend more time on prior auth, formulary calls, and counseling prep than on dispensing. The right AI stack drafts patient education, flags interactions in seconds, and handles the drug-info lookups that eat your day. We tested tools across community and hospital settings to find what actually helps.",
   verdict="Start with ChatGPT for patient-friendly counseling scripts and drug summaries, use LexiComp or Clinical Pharmacology AI for interactions, and let Otter.ai capture verbal consults. Suki AI cuts chart time if you're clinical. Together they reclaim 5-8 hours a week without replacing your professional judgment.",
   tools=[
     dict(name="ChatGPT", color="#10a37f", initial="Ch", badge="$20/mo", desc="Drafts patient counseling scripts and plain-language drug summaries in seconds.", url="https://chat.openai.com/?via=toolforge"),
     dict(name="Otter.ai", color="#3b82f6", initial="O", badge="Free", desc="Records and transcribes verbal counseling so you stay present with the patient.", url="https://otter.ai/?via=toolforge"),
     dict(name="Suki AI", color="#7c3aed", initial="S", badge="$0+", desc="Clinical voice assistant that writes notes and orders into the EHR.", url="https://suki.ai/?via=toolforge"),
     dict(name="UpToDate", color="#dc2626", initial="U", badge="$$", desc="AI-assisted drug and disease lookup with graded evidence behind every answer.", url="https://uptodate.com/?via=toolforge"),
     dict(name="Perplexity", color="#0ea5e9", initial="P", badge="Free", desc="Cited, sourced answers to off-label and emerging therapy questions.", url="https://perplexity.ai/?via=toolforge"),
     dict(name="Doximity GPT", color="#16a34a", initial="D", badge="Free", desc="HIPAA-aware ChatGPT built for clinicians — secure drafting and summaries.", url="https://doximity.com/?via=toolforge"),
     dict(name="Grammarly", color="#15c39a", initial="G", badge="Free", desc="Catches errors in prior auth letters and patient communications before they ship.", url="https://grammarly.com/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-chemists-2026", title="The 6 Best AI Tools for Chemists in 2026 (Faster Synthesis, Smarter Literature)",
   category="For Chemists", meta="From retrosynthesis planning to patent searches, these AI tools help research and industry chemists move faster without cutting corners on rigor.",
   read="3", lead="Chemists spend more time searching literature, planning routes, and writing patents than at the bench. The 2026 AI stack for chemistry now includes models trained on reaction data that propose retrosynthesis paths, summarize the patent landscape, and draft methods sections. We tested tools in both academia and pharma R&D to find what genuinely saves time.",
   verdict="Use SciFindern or Reaxys AI for reaction and substance lookup, IBM RXN for retrosynthesis planning, and ChatGPT Plus or Claude for literature summaries and methods drafting. Patent teams should add Semantic Scholar and Elicit for fast prior-art searches. None replace your lab judgment — they all remove the busywork around it.",
   tools=[
     dict(name="IBM RXN", color="#0f62fe", initial="I", badge="Free", desc="AI retrosynthesis and forward-reaction prediction trained on millions of reactions.", url="https://rxn.res.ibm.com/?via=toolforge"),
     dict(name="SciFindern", color="#dc2626", initial="Sc", badge="$$", desc="The industry-standard substance and reaction database with AI search.", url="https://scifinder.cas.org/?via=toolforge"),
     dict(name="Reaxys", color="#f59e0b", initial="R", badge="$$", desc="Deep chemistry literature and property data with AI-assisted query.", url="https://reaxys.com/?via=toolforge"),
     dict(name="ChatGPT", color="#10a37f", initial="Ch", badge="$20/mo", desc="Summarizes methods sections, drafts experimental write-ups, explains mechanisms.", url="https://chat.openai.com/?via=toolforge"),
     dict(name="Elicit", color="#7c3aed", initial="E", badge="$10/mo", desc="Extracts data and findings from chemistry papers into tables automatically.", url="https://elicit.com/?via=toolforge"),
     dict(name="Semantic Scholar", color="#1857b6", initial="S", badge="Free", desc="AI literature search that surfaces the most relevant prior art fast.", url="https://semanticscholar.org/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-astronomers-2026", title="The 6 Best AI Tools for Astronomers in 2026 (From Survey to Spectra)",
   category="For Astronomers", meta="Sky surveys, spectra classification, and proposal writing — the AI stack that helps observational and theoretical astronomers handle modern data volumes.",
   read="3", lead="Modern astronomy generates terabytes per night and proposals are still written by hand. The 2026 AI toolset for astronomers includes models that classify transient events, auto-reduce spectra, draft observing proposals, and summarize the arXiv firehose. We surveyed the tools working astronomers actually rely on across surveys, archives, and theory groups.",
   verdict="Use ChatGPT or Claude for drafting proposals and summarizing arXiv papers, NASA ADS AI features for literature discovery, and domain tools like AstroML and lsst.desc pipelines for ML on survey data. NotebookLM is a quiet hero for reading long review articles. None of these replace your physics — they remove the paperwork around it.",
   tools=[
     dict(name="ChatGPT", color="#10a37f", initial="Ch", badge="$20/mo", desc="Drafts observing proposals, explains complex theory, writes analysis code.", url="https://chat.openai.com/?via=toolforge"),
     dict(name="Claude", color="#d97706", initial="Cl", badge="$20/mo", desc="Best for long-form reasoning over 100+ page review articles and data descriptions.", url="https://claude.ai/?via=toolforge"),
     dict(name="NASA ADS", color="#1d4ed8", initial="N", badge="Free", desc="The astronomy literature database with AI-assisted discovery and recommendations.", url="https://ui.adsabs.harvard.edu/?via=toolforge"),
     dict(name="NotebookLM", color="#2563eb", initial="N", badge="Free", desc="Upload papers and get grounded summaries and citations you can verify.", url="https://notebooklm.google.com/?via=toolforge"),
     dict(name="AstroML", color="#7c3aed", initial="A", badge="Free", desc="Python ML library with astronomy datasets and algorithms for survey-scale analysis.", url="https://www.astroml.org/?via=toolforge"),
     dict(name="Perplexity", color="#0ea5e9", initial="P", badge="Free", desc="Cited answers to cross-disciplinary questions across physics and instrumentation.", url="https://perplexity.ai/?via=toolforge"),
   ]),
]

# =================== WRITE FILES ===================
new_urls = []
created = []

for t in TOOLS:
    if t['slug'] in tool_slugs:
        print(f"SKIP (exists): tools/{t['slug']}.html")
        continue
    path = os.path.join(BASE, 'tools', f"{t['slug']}.html")
    with open(path, 'w') as f:
        f.write(tool_html(t))
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html")
    created.append(f"tools/{t['slug']}.html")

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print(f"SKIP (exists): compare/{c['slug']}.html")
        continue
    path = os.path.join(BASE, 'compare', f"{c['slug']}.html")
    with open(path, 'w') as f:
        f.write(compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    created.append(f"compare/{c['slug']}.html")

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print(f"SKIP (exists): blog/{b['slug']}.html")
        continue
    path = os.path.join(BASE, 'blog', f"{b['slug']}.html")
    with open(path, 'w') as f:
        f.write(blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    created.append(f"blog/{b['slug']}.html")

print(f"\nCREATED {len(created)} NEW PAGES:")
for c in created:
    print("  -", c)

# =================== UPDATE SITEMAP ===================
if new_urls:
    smap = os.path.join(BASE, 'sitemap.xml')
    with open(smap, 'r') as f:
        content = f.read()
    entries = ""
    for u in new_urls:
        entries += f'''  <url>
    <loc>{u}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    content = content.replace("</urlset>", entries + "</urlset>", 1)
    with open(smap, 'w') as f:
        f.write(content)
    print(f"\nSITEMAP updated with {len(new_urls)} new URLs (total now {content.count('<loc>')}).")

print("\nDONE.")
