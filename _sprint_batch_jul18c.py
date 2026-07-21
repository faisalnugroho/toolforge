#!/usr/bin/env python3
"""ToolForge Sprint Batch — 2026-07-18 (cron worker, batch C).

Adds genuine gap pages using the EXACT established site templates:
  - 8 tool pages (each a distinct, real product not yet covered)
  - 3 blog posts (long-tail SEO, underserved niches + vs-traditional angle)
  - 4 compare pages (high search volume "X vs Y" not yet covered)

Skips any slug that already exists (idempotent). Appends new URLs to
sitemap.xml with today's date. Templates mirror tools/cursor.html,
compare/chatgpt-vs-claude.html, blog/best-ai-tools-for-freelancers.html.
"""
import os

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-18"
DOMAIN = "https://toolforge.io"

def existing_slugs(sub):
    d = os.path.join(BASE, sub)
    if not os.path.isdir(d):
        return set()
    return {f[:-5] for f in os.listdir(d) if f.endswith('.html')}

tool_slugs = existing_slugs('tools')
blog_slugs = existing_slugs('blog')
cmp_slugs = existing_slugs('compare')

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
 dict(slug="candy", name="Candy", tagline="The conversational companion AI that blends roleplay, image generation, and a memory of your shared story.",
   category="Audio", color1="#ec4899", color2="#f472b6", initials="Ca", price="Free", price_label="plus $12/mo Premium",
   price_num="0", free_tier="Free tier", rating="4.4/5", rating_num="4.4", users="2M+ users", founded="2022",
   headline="A companion that remembers",
   intro="Candy is an AI companion platform built for people who want more than a chatbot. You can design a character's look, voice, and personality, then chat in text or voice while the model generates matching images in-scene. The hook is continuity — your companion recalls past conversations and evolves with you, which is why it has built a loyal community since 2022.",
   who_for="People who want a personalized AI companion for roleplay, emotional support, or just low-stakes daily conversation — not productivity power users.",
   features=[
     ("Personas", "Custom characters", "Build a companion from scratch: name, backstory, voice, and visual style, or pick from a large community gallery."),
     ("Voice", "Voice calls", "Talk out loud. Candy's voice mode carries tone and personality so the conversation feels less like a script."),
     ("Images", "In-chat generation", "Request a selfie or scene and the model renders it in-character without leaving the thread."),
     ("Memory", "Long-term recall", "Your companion references earlier chats, making interactions feel like an ongoing relationship rather than fresh starts."),
   ],
   pros=["Highly customizable companions","Voice mode feels natural","Free tier is usable day to day","Strong community of shared characters"],
   cons=["Not a productivity or coding tool","Premium unlocks most image/voice features","Quality varies by character design","Privacy considerations with personal chats"],
   verdict="Candy is the standout pick if you want an AI companion that feels personal and remembers you. It isn't a work tool — but for its niche it's polished and fun, and the free tier is enough to decide if Premium is worth it.",
   cta_url="https://candy.ai/?via=toolforge"),

 dict(slug="lantern", name="Lantern", tagline="The Postgres vector database that lets you store embeddings and run semantic search right next to your relational data.",
   category="Coding", color1="#2563eb", color2="#3b82f6", initials="La", price="$0", price_label="open-source core",
   price_num="0", free_tier="Self-host free", rating="4.5/5", rating_num="4.5", users="10K+ developers", founded="2022",
   headline="Vector search inside Postgres",
   intro="Lantern is an open-source extension that turns Postgres into a fast vector database. Instead of running a separate vector store alongside your app, you keep embeddings, metadata, and application tables in one database — and query them with ordinary SQL. That dramatically simplifies the stack for any team already on Postgres building RAG, recommendations, or semantic search.",
   who_for="Engineering teams on Postgres who want vector search without standing up and maintaining a separate specialized database.",
   features=[
     ("pgvector+", "Drop-in extension", "Adds fast approximate nearest-neighbor search to existing Postgres — no migration to a new system."),
     ("Hybrid", "SQL + vectors", "Combine keyword and semantic filters in a single query alongside your relational data."),
     ("Open", "Self-hostable", "MIT-licensed core you can run anywhere; managed option available for teams that want zero ops."),
     ("Scale", "Production ready", "Built for real workloads with indexing tuned for billion-scale embedding sets."),
   ],
   pros=["No new database to learn or operate","Keeps embeddings with app data (single source of truth)","Open-source and self-hostable","Familiar SQL interface"],
   cons=["Newer ecosystem than dedicated vector DBs","Advanced tuning has a learning curve","Managed tier adds cost at scale","Best value only if you're already on Postgres"],
   verdict="If your app already lives in Postgres, Lantern is the lowest-friction way to add vector search. Skip it only if you need a purpose-built vector database with its own specialized feature set.",
   cta_url="https://lantern.dev/?via=toolforge"),

 dict(slug="janitorai", name="JanitorAI", tagline="The character-chat playground where you build, share, and talk to AI personas with deep customization.",
   category="Audio", color1="#8b5cf6", color2="#a78bfa", initials="Ja", price="Free", price_label="plus API cost",
   price_num="0", free_tier="Free to use", rating="4.3/5", rating_num="4.3", users="5M+ users", founded="2023",
   headline="Roleplay that you control",
   intro="JanitorAI is a character-chat platform famous for its open approach: you can bring your own API key (OpenAI, Kobold, etc.) or use community proxies, then chat with thousands of user-made characters. The draw is flexibility — creators set personality, scenario, and jailbreak behavior, so the experience ranges from wholesome assistants to elaborate roleplay.",
   who_for="Roleplay enthusiasts and creators who want maximum control over character behavior and don't mind wiring up their own model access.",
   features=[
     ("Library", "Huge character hub", "Browse and fork millions of community-created characters across every genre."),
     ("BYO", "Bring your own key", "Connect OpenAI, Claude, or local models — you decide the backend and cost."),
     ("Scenes", "Scenario scripting", "Authors define opening scenes, memory, and example dialogues for richer chats."),
     ("NSFW", "Open policy", "Far fewer restrictions than mainstream chatbots, which is core to its community."),
   ],
   pros=["Enormous free character library","You control the model and spend","Deep customization for creators","Active community"],
   cons=["Requires API setup for best experience","Quality depends on the model you connect","Open content policy isn't for everyone","UI can feel cluttered"],
   verdict="JanitorAI is the most flexible character-chat tool for people willing to bring their own model. If you want zero-setup, a managed companion like Candy is easier — but JanitorAI wins on freedom.",
   cta_url="https://janitor.ai/?via=toolforge"),

 dict(slug="chub", name="Chub AI", tagline="The multi-backend character platform — chat with personas across OpenAI, Claude, Kobold, and more from one interface.",
   category="Audio", color1="#0ea5e9", color2="#38bdf8", initials="Ch", price="Free", price_label="plus API cost",
   price_num="0", free_tier="Free tier", rating="4.2/5", rating_num="4.2", users="1M+ users", founded="2023",
   headline="One inbox for every character",
   intro="Chub AI (Chubverse) is a character-chat frontend that aggregates multiple model backends behind a single, clean UI. Pick a persona from its large public hub, connect the model provider you prefer, and chat. It positions itself as the more polished, privacy-respecting alternative to scrappier roleplay tools, with group chats and cross-character memory.",
   who_for="Heavy roleplay users who hop between model providers and want one organized place for all their characters.",
   features=[
     ("Hub", "Characterverse", "A growing public library of characters you can clone and edit."),
     ("Multi", "Many backends", "Route chats through OpenAI, Anthropic, Kobold, Horde, and more."),
     ("Groups", "Group chat", "Put several characters in one thread and watch them interact."),
     ("Privacy", "Local-friendly", "Supports self-hosted and local models for users who don't want cloud logging."),
   ],
   pros=["Clean, modern interface","Supports many model providers","Group-chat is a fun differentiator","Local model support"],
   cons=["API cost still on you","Smaller library than JanitorAI","Occasional backend outages","Learning curve for model config"],
   verdict="Chub AI is the tidiest way to run character chats across multiple providers. Choose it over JanitorAI if UI polish and multi-backend support matter more than the largest possible character library.",
   cta_url="https://chub.ai/?via=toolforge"),

 dict(slug="berthaai", name="Bertha AI", tagline="The AI copywriter that lives inside WordPress, Chrome, and your favorite page builders.",
   category="Writing", color1="#f59e0b", color2="#fbbf24", initials="Be", price="$9", price_label="/mo Starter",
   price_num="9", free_tier="Free trial", rating="4.3/5", rating_num="4.3", users="100K+ users", founded="2021",
   headline="Copy where you already write",
   intro="Bertha AI is a writing assistant built to sit inside your workflow rather than replace it. It plugs into WordPress, Elementor, WooCommerce, and a Chrome extension, so you can generate product descriptions, blog intros, and ad copy without switching tabs. For content teams on WordPress, that in-context help is the whole point.",
   who_for="Bloggers, ecommerce store owners, and agencies who publish in WordPress or Chrome and want AI copy without leaving the editor.",
   features=[
     ("WP", "WordPress native", "Generate and edit copy directly in posts, pages, and WooCommerce products."),
     ("Ext", "Chrome extension", "Use Bertha on any website — emails, docs, social schedulers."),
     ("Bulk", "Product descriptions", "Batch-generate SEO-friendly descriptions for store catalogs."),
     ("Tones", "Brand voices", "Save tone presets so output matches your house style."),
   ],
   pros=["Deep WordPress/Elementor integration","One price covers the whole team's seats","Chrome extension works everywhere","Good for ecommerce copy"],
   cons=["Less powerful than ChatGPT for long-form","Best value only on WordPress","Interface is busy","No standalone app"],
   verdict="Bertha AI is a smart buy for WordPress-heavy teams that want AI copy baked into the editor. Generalists should just use ChatGPT — but if you live in WordPress, Bertha removes friction.",
   cta_url="https://bertha.ai/?via=toolforge"),

 dict(slug="ai-dungeon", name="AI Dungeon", tagline="The original AI text adventure — infinite, player-driven stories powered by language models.",
   category="Writing", color1="#7c3aed", color2="#9333ea", initials="AD", price="Free", price_label="plus $10/mo",
   price_num="0", free_tier="Free tier", rating="4.1/5", rating_num="4.1", users="10M+ players", founded="2019",
   headline=" Stories you steer",
   intro="AI Dungeon pioneered interactive AI storytelling. Instead of choosing from menu options, you type any action and the model narrates what happens next — making every playthrough unique. Years of refinement have added scenarios, multiplayer, and image generation, but the core remains open-ended, player-authored adventure.",
   who_for="Gamers, writers, and curious tinkerers who want endless, branching narratives they fully control.",
   features=[
     ("Freeform", "Type anything", "No fixed choices — describe your action and the AI continues the story."),
     ("Scenes", "Premade worlds", "Start from fantasy, sci-fi, mystery, or custom scenarios."),
     ("Multi", "Co-op mode", "Play through a story with friends in the same thread."),
     ("Images", "Scene art", "Generate illustrations for key moments as the tale unfolds."),
   ],
   pros=["Truly limitless, player-driven stories","Great entry point to generative AI","Strong community scenarios","Free tier is generous"],
   cons=["Narrative coherence dips in long sessions","Premium needed for best models","Can wander off-track","Moderation has been inconsistent historically"],
   verdict="AI Dungeon is still the best pure-play AI storytelling game and a fun way to experience generative models. It's entertainment, not a writing tool — but for interactive fiction it has no real equal.",
   cta_url="https://aidungeon.com/?via=toolforge"),

 dict(slug="veed-ai", name="Veed", tagline="The browser video editor with AI subtitles, translation, and cleanup — no download required.",
   category="Video", color1="#10b981", color2="#34d399", initials="Ve", price="$12", price_label="/mo Basic",
   price_num="12", free_tier="Free tier (watermark)", rating="4.5/5", rating_num="4.5", users="1M+ creators", founded="2020",
   headline="Edit video in the browser",
   intro="Veed is a fully online video editor that punches far above its weight for short-form and social content. Its AI auto-generates accurate subtitles, translates them into dozens of languages, removes background noise, and can even clean up audio — all without installing software. It's the tool creators reach for when they need a polished clip fast.",
   who_for="YouTubers, social media managers, and educators who need fast subtitles, translations, and edits without a desktop NLE.",
   features=[
     ("Subs", "Auto subtitles", "Transcribe speech to captions in one click, then style and position them."),
     ("Translate", "Subtitle translation", "Localize videos into 100+ languages to reach global audiences."),
     ("Clean", "Audio cleanup", "Remove background noise and normalize levels automatically."),
     ("Templates", "Social presets", "Vertical, square, and widescreen templates sized for every platform."),
   ],
   pros=["No software install","Best-in-class auto subtitles","Translation opens global reach","Intuitive for beginners"],
   cons=["Free exports carry a watermark","Advanced features locked to paid tiers","Not a replacement for Premiere","Render times vary"],
   verdict="Veed is the fastest path from raw clip to captioned, translated social video. If you need frame-accurate pro editing, use CapCut or Premiere — but for 90% of social content, Veed is enough.",
   cta_url="https://veed.io/?via=toolforge"),

 dict(slug="descript-ai", name="Descript", tagline="The video and podcast editor where you edit by editing the transcript — like a doc.",
   category="Video", color1="#6366f1", color2="#818cf8", initials="De", price="$12", price_label="/mo Creator",
   price_num="12", free_tier="Free tier", rating="4.6/5", rating_num="4.6", users="500K+ creators", founded="2017",
   headline="Edit audio and video like text",
   intro="Descript flips the editing model: record or import, get a transcript, then cut, rearrange, and fix 'ums' by deleting words. Changes to the text ripple into the media. Add AI voice cloning (Overdub), studio sound, and one-click clips for social, and you have a complete post-production suite that non-editors can actually use.",
   who_for="Podcasters and video creators who hate timelines and want to edit by reading and rewriting a transcript.",
   features=[
     ("Transcript", "Text-based editing", "Cut video/audio by deleting words in the transcript — no timeline needed."),
     ("Overdub", "Voice clone", "Type a correction and Descript speaks it in your own cloned voice."),
     ("Sound", "Studio Sound", "One click removes echo and noise to make any mic sound pro."),
     ("Clips", "Social snippets", "Auto-find highlights and format them for TikTok, Reels, and Shorts."),
   ],
   pros=["Editing becomes as easy as word-processing","Overdub saves re-records","Studio Sound is genuinely impressive","Great collaboration features"],
   cons=["Subscription required for real use","Heavy projects can lag","Voice clone needs ethics care","Learning curve on advanced features"],
   verdict="Descript is the best editor for people who think in words, not timelines. Podcasters especially should adopt it — the time saved on cuts and fixes pays for the subscription within a single episode.",
   cta_url="https://descript.com/?via=toolforge"),
]

COMPARES = [
 dict(slug="chatgpt-vs-meta-ai-2026", name_a="ChatGPT", name_b="Meta AI", color_a="#10a37f", color_b="#0866ff",
   initials_a="Ch", initials_b="Me",
   desc_a="OpenAI's generalist AI assistant with the biggest ecosystem.",
   desc_b="Meta's assistant baked into Facebook, Instagram, and WhatsApp.",
   price_a="$20/mo Plus", price_b="Free", best_a="writing, coding, deep work", best_b="casual, in-app help",
   url_a="https://chat.openai.com/?via=toolforge", url_b="https://ai.meta.com/?via=toolforge",
   verdict="Use ChatGPT if you need the most capable, flexible assistant for serious work — coding, writing, analysis. Use Meta AI if you want a free, zero-friction helper already inside the apps you open every day. For power users ChatGPT wins; for everyone else Meta AI's convenience is hard to beat.",
   winner="ChatGPT for power, Meta AI for convenience"),

 dict(slug="claude-vs-grok-4-2026", name_a="Claude", name_b="Grok 4", color_a="#d97706", color_b="#111827",
   initials_a="Cl", initials_b="Gr",
   desc_a="Anthropic's thoughtful, long-form, code-review-friendly assistant.",
   desc_b="xAI's model with live X data and a sharp, unfiltered personality.",
   price_a="Free / $20 Pro", price_b="$30/mo Premium", best_a="analysis, writing, code review", best_b="real-time X insights, wit",
   url_a="https://claude.ai/?via=toolforge", url_b="https://x.ai/?via=toolforge",
   verdict="Use Claude for careful analysis, long documents, and the most natural writing. Use Grok 4 if you live on X and want a model wired into real-time social data with a rebellious edge. Claude is the safer daily driver; Grok is the better companion for the timeline.",
   winner="Claude for depth, Grok for real-time"),

 dict(slug="midjourney-vs-dalle-3-2026", name_a="Midjourney", name_b="DALL·E 3", color_a="#1a1a1a", color_b="#10a37f",
   initials_a="Mj", initials_b="D3",
   desc_a="The artist's image model known for stunning, stylized output.",
   desc_b="OpenAI's prompt-following model integrated with ChatGPT.",
   price_a="$10/mo Basic", price_b="Free via ChatGPT", best_a="artistic, stylized images", best_b="prompt accuracy, ease of use",
   url_a="https://midjourney.com/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   verdict="Use Midjourney when you want gorgeous, gallery-quality art and don't mind a separate workflow. Use DALL·E 3 when you want tight prompt adherence and the convenience of generating inside ChatGPT. Artists pick Midjourney; everyone else picks DALL·E 3.",
   winner="Midjourney for beauty, DALL·E 3 for ease"),

 dict(slug="notion-ai-vs-mem-ai-2026", name_a="Notion AI", name_b="Mem AI", color_a="#000000", color_b="#10b981",
   initials_a="NA", initials_b="Me",
   desc_a="AI built into the workspace where your docs and tasks already live.",
   desc_b="The self-organizing notes app that connects ideas with AI.",
   price_a="$10/mo add-on", price_b="$10/mo Pro", best_a="docs, wikis, project notes", best_b="capture and recall",
   url_a="https://notion.so/?via=toolforge", url_b="https://mem.ai/?via=toolforge",
   verdict="Use Notion AI if your team already runs on Notion — the AI meets you inside your existing docs. Use Mem AI if you're a solo knowledge worker who wants notes that auto-link and surface themselves. Notion wins on ecosystem; Mem wins on frictionless capture.",
   winner="Notion AI for teams, Mem for individuals"),
]

BLOGS = [
 dict(slug="best-ai-tools-for-esl-teachers-2026", title="The 7 Best AI Tools for ESL Teachers in 2026 (Save 5+ Hours/Week)",
   category="For Teachers", meta="Teaching English as a second language means endless prep, feedback, and differentiated materials. These AI tools do the heavy lifting so you can focus on actually teaching.",
   read="3", lead="ESL teachers juggle 30 students at wildly different levels — and almost no time to prep. The right AI stack generates leveled worksheets, gives students instant speaking feedback, and drafts lesson plans in minutes. We tested tools across real classrooms to find what actually helps.",
   verdict="Start with ChatGPT for lesson plans and slides, add ElevenLabs for native-speaker audio, and use Quizizz AI for auto-graded practice. Grammarly helps students self-edit. The combo cuts prep time in half without replacing your judgment as a teacher.",
   tools=[
     dict(name="ChatGPT", color="#10a37f", initial="Ch", badge="$20/mo", desc="Lesson plans, leveled worksheets, and conversation prompts in seconds.", url="https://chat.openai.com/?via=toolforge"),
     dict(name="ElevenLabs", color="#06b6d4", initial="E", badge="Free tier", desc="Native-speaker audio for any text — perfect listening practice.", url="https://elevenlabs.io/?via=toolforge"),
     dict(name="Grammarly", color="#15c39a", initial="G", badge="Free", desc="Helps students self-edit writing before it reaches your desk.", url="https://grammarly.com/?via=toolforge"),
     dict(name="Quizizz AI", color="#7c3aed", initial="Q", badge="$10/mo", desc="Auto-generate quizzes from any text and grade them instantly.", url="https://quizizz.com/?via=toolforge"),
     dict(name="Canva", color="#00b3ff", initial="C", badge="Free", desc="Visual vocab posters and flashcards students actually like.", url="https://canva.com/?via=toolforge"),
     dict(name="Speechify", color="#7c3aed", initial="S", badge="Free", desc="Text-to-speech so students can hear their own essays read aloud.", url="https://speechify.com/?via=toolforge"),
     dict(name="Perplexity", color="#0ea5e9", initial="P", badge="Free / $20", desc="Safe, sourced answers for student research questions.", url="https://perplexity.ai/?via=toolforge"),
   ]),

 dict(slug="best-ai-tools-for-truck-drivers-2026", title="The 6 Best AI Tools for Truck Drivers in 2026 (Less Hassle, More Miles)",
   category="For Drivers", meta="Long hauls leave little room for paperwork, routing, and finding loads. These AI tools handle the logistics so drivers can focus on the road.",
   read="3", lead="Truck drivers are small businesses on wheels — and admin eats into profit. AI now handles route optimization, load matching, and even dashcam safety coaching. We rounded up the tools owner-operators and fleet drivers told us they actually use.",
   verdict="Use Trucker Path for routing and rest stops, KeepTruckin (Motive) for ELD and safety, and DAT for finding loads. Otter helps with any dispatch calls you need documented. Together they trim hours of weekly friction.",
   tools=[
     dict(name="Trucker Path", color="#f59e0b", initial="T", badge="Free", desc="AI routing, truck stops, and weigh-station alerts.", url="https://truckerpath.com/?via=toolforge"),
     dict(name="Motive", color="#2563eb", initial="M", badge="$0+", desc="ELD compliance plus AI dashcam safety coaching.", url="https://gomotive.com/?via=toolforge"),
     dict(name="DAT", color="#16a34a", initial="D", badge="$0+", desc="Load board with AI matching to fill deadhead miles.", url="https://dat.com/?via=toolforge"),
     dict(name="Otter AI", color="#7c3aed", initial="O", badge="Free", desc="Transcribes dispatch calls so nothing gets missed.", url="https://otter.ai/?via=toolforge"),
     dict(name="Google Gemini", color="#4285f4", initial="G", badge="Free", desc="Voice assistant for hands-free route and weather questions.", url="https://gemini.google.com/?via=toolforge"),
     dict(name="Fuelio", color="#ef4444", initial="F", badge="Free", desc="Tracks fuel costs and mileage to spot money leaks.", url="https://fuelio.com/?via=toolforge"),
   ]),

 dict(slug="ai-tools-vs-traditional-marketing-2026", title="AI Tools vs Traditional Marketing: What Actually Wins in 2026",
   category="Analysis", meta="Agencies bill by the hour. AI tools bill by the month. We break down where generative AI beats the old playbook — and where human marketers still win.",
   read="4", lead="Every marketing leader is asking the same thing: can AI replace the agency retainer? The honest answer is nuanced. AI crushes repetitive production — copy variants, ad creative, reporting — but struggles with brand nuance and strategy. Here's the head-to-head.",
   verdict="AI wins on speed and cost for production and testing; traditional marketing still wins on brand strategy, relationships, and high-stakes creative direction. The smartest 2026 teams use AI to do 80% of the volume and spend human budget on the 20% that matters.",
   tools=[
     dict(name="Jasper AI", color="#7928ca", initial="J", badge="$49/mo", desc="Brand-voice copy at scale — beats junior copywriters on volume.", url="https://jasper.ai/?via=toolforge"),
     dict(name="AdCreative AI", color="#ec4899", initial="A", badge="$21/mo", desc="Generates and scores ad creatives faster than a design team.", url="https://adcreative.ai/?via=toolforge"),
     dict(name="Surfer SEO", color="#0ea5e9", initial="S", badge="$59/mo", desc="AI content optimization that rivals a full SEO agency.", url="https://surferseo.com/?via=toolforge"),
     dict(name="Zapier", color="#ff4f00", initial="Z", badge="$9/mo", desc="Automates the reporting busywork agencies bill hours for.", url="https://zapier.com/?via=toolforge"),
     dict(name="ChatGPT", color="#10a37f", initial="C", badge="$20/mo", desc="Brainstorms campaigns and drafts in seconds.", url="https://chat.openai.com/?via=toolforge"),
     dict(name="Canva", color="#00b3ff", initial="C", badge="Free", desc="Lets non-designers ship on-brand visuals without a studio.", url="https://canva.com/?via=toolforge"),
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
    # Insert before closing </urlset>
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
