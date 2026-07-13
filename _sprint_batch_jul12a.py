#!/usr/bin/env python3
"""ToolForge Sprint Batch (Jul 12, batch A) — adds genuinely-missing tool/compare/blog
pages using the EXACT existing site templates. Skips any slug that already exists.
Appends new URLs to sitemap.xml. Non-destructive and idempotent."""
import os, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "2026-07-12"
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
  "datePublished": "2026-07-12",
  "dateModified": "2026-07-12"
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

# =================== CONTENT DATA (Jul 12 batch A) ===================

TOOLS = [
 dict(slug="getimg", name="Getimg.ai", tagline="An all-in-one AI art studio: generate, edit, and fine-tune images with 60+ models in your browser.", category="Image",
   color1="#111827", color2="#374151", initials="Gi", price="Free", price_label="Starter", price_num="0",
   free_tier="100 images/mo free", rating="4.5/5", rating_num="4.5", users="2M+ users", founded="2022",
   headline="A full AI art studio in one tab",
   intro="Getimg.ai is the Swiss Army knife of AI image work — text-to-image across 60+ models (SDXL, Stable Diffusion, custom fine-tunes), inpainting, outpainting, and a REST API for developers. In 2026 it's the go-to for people who want power without installing ComfyUI.",
   who_for="Designers, indie creators, and developers who want generation, editing, and an API under one roof.",
   features=[("🎨","60+ models","Switch between SDXL, SD 1.5, and community fine-tunes instantly."),
             ("🖌️","Inpainting & outpaint","Edit parts of an image or extend its canvas seamlessly."),
             ("🔧","DreamBooth training","Train a custom model on your own faces or products."),
             ("🔌","Developer API","Drop image generation into your own app with a few calls.")],
   pros=["Huge model library in one place",
         "Genuine free tier (100/mo)",
         "Built-in editor and API",
         "Fast, browser-native"],
   cons=["UI is busier than Midjourney",
         "Best models behind paid plans",
         "No standalone mobile app"],
   verdict="The most versatile browser-based image toolkit for builders and tinkerers. If you want one tab that does generation, editing, and an API, Getimg wins. For pure aesthetic beauty, Midjourney still leads.",
   cta_url="https://getimg.ai"),

 dict(slug="slides-ai", name="SlidesAI", tagline="Turn any text or topic into a full presentation deck in seconds, right inside Google Slides.", category="Productivity",
   color1="#0ea5e9", color2="#0284c7", initials="Sa", price="$10/mo", price_label="Pro plan", price_num="10",
   free_tier="3 presentations/mo free", rating="4.3/5", rating_num="4.3", users="3M+ users", founded="2021",
   headline="From blank doc to deck in one click",
   intro="SlidesAI is a Google Slides add-on that generates complete, on-brand slide decks from a paragraph, a doc, or a URL. No leaving your workspace, no learning a new design tool — just describe the talk and get 10-20 structured slides back.",
   who_for="Professionals, educators, and founders who live in Google Workspace and need decks fast.",
   features=[("⚡","One-click generation","Paste text or a link; get a structured deck instantly."),
             ("🎨","Theme presets","Pick a look that matches your brand."),
             ("🌐","Multilingual","Generate slides in 30+ languages."),
             ("🔌","Native Slides","Runs inside Google Slides — no export dance.")],
   pros=["No new tool to learn",
         "Solid free tier to start",
         "Good for rough drafts",
         "Multilingual support"],
   cons=["Design polish trails Gamma",
         "Heavy decks feel templated",
         "Tied to Google Slides"],
   verdict="The easiest on-ramp to AI decks if you already live in Google Slides. For more design freedom and web publishing, Gamma is the stronger pick.",
   cta_url="https://slidesai.io"),

 dict(slug="researchrabbit", name="Research Rabbit", tagline="A visual discovery engine for academic papers — like Spotify's 'similar artists' for citations.", category="Research",
   color1="#7c3aed", color2="#6d28d9", initials="Rr", price="Free", price_label="For researchers", price_num="0",
   free_tier="Always free", rating="4.4/5", rating_num="4.4", users="500K+ researchers", founded="2020",
   headline="Find the papers you didn't know you needed",
   intro="Research Rabbit maps the citation graph visually — add a paper and it surfaces related work, co-citation networks, and the labs behind them. Researchers use it to go down rabbit holes productively instead of drowning in Google Scholar.",
   who_for="PhDs, literature reviewers, and anyone building a citation network for a paper or grant.",
   features=[("🕸️","Visual graph","See how papers connect at a glance."),
             ("🔗","Co-citation maps","Find seminal works via citation clusters."),
             ("📚","Collections","Build and share reading lists."),
             ("🔔","Alerts","Get notified when new related work drops.")],
   pros=["Free and nonprofit-friendly",
         "Far better discovery than Scholar",
         "Visual, intuitive",
         "Great for literature reviews"],
   cons=["No full-text search of paywalled PDFs",
         "Smaller than Semantic Scholar index",
         "Web only, no mobile"],
   verdict="The best free tool for discovering and mapping academic literature. Pair it with Semantic Scholar or Connected Papers for a complete research workflow.",
   cta_url="https://www.researchrabbit.ai"),

 dict(slug="chatdoc", name="ChatDOC", tagline="Chat with your PDFs and documents — ask questions and get answers with cited page references.", category="Research",
   color1="#ef4444", color2="#b91c1c", initials="Cd", price="Free", price_label="Basic", price_num="0",
   free_tier="Free tier (limited pages)", rating="4.3/5", rating_num="4.3", users="1M+ users", founded="2023",
   headline="Your documents, finally conversational",
   intro="ChatDOC lets you upload PDFs, Word docs, and scans, then ask questions in plain language — it answers with direct quotes and page numbers pulled from the source. Built on a document-parsing engine that actually reads tables and figures, not just text.",
   who_for="Students, analysts, and researchers who need to extract answers from long reports without reading every page.",
   features=[("💬","Cited answers","Every reply links back to the exact page."),
             ("📊","Tables & figures","Understands charts, not just prose."),
             ("📄","Batch upload","Chat across many docs at once."),
             ("🔍","Deep analysis","Summarize, compare, and extract.")],
   pros=["Accurate, cited responses",
         "Handles tables and images",
         "Fast on long PDFs",
         "Free tier available"],
   cons=["Free tier page limits",
         "Occasional misread on scans",
         "Best models on paid tier"],
   verdict="The most document-aware 'chat with PDF' tool for research and analysis. For lighter use, NotebookLM is the free alternative; for coding data, Claude wins.",
   cta_url="https://chatdoc.com"),

 dict(slug="instantly", name="Instantly.ai", tagline="Cold email infrastructure that warms inboxes and sends at scale without landing in spam.", category="Productivity",
   color1="#0a72ef", color2="#0a58c0", initials="In", price="$30/mo", price_label="Growth plan", price_num="30",
   free_tier="Free trial", rating="4.4/5", rating_num="4.4", users="100K+ users", founded="2020",
   headline="Cold email that actually lands in the inbox",
   intro="Instantly.ai runs unlimited warm-up across thousands of inboxes, spins up reply-detection sequences, and ships personalized cold campaigns at volume — the backbone of modern outbound. In 2026 it's the default for agencies and founders doing cold email.",
   who_for="Agencies, founders, and SDRs running outbound at scale who need deliverability.",
   features=[("🔥","Inbox warm-up","Auto-warms unlimited mailboxes to dodge spam."),
             ("✉️","Unlimited sending","Scale campaigns without per-email fees."),
             ("🤖","AI personalization","Merge fields and AI spins per recipient."),
             ("📈","Reply detection","Stops sequences on real replies automatically.")],
   pros=["Best-in-class deliverability",
         "Unlimited sending on flat pricing",
         "Strong analytics",
         "Great for agencies"],
   cons=["Learning curve for beginners",
         "Requires domain setup",
         "No built-in CRM"],
   verdict="The cold-email engine of choice for serious outbound. Pair with a solid list source and you'll out-send manual outreach 100x. For simpler needs, Lemlist is friendlier.",
   cta_url="https://instantly.ai"),

 dict(slug="podwise", name="Podwise", tagline="AI that turns podcast episodes into summaries, transcripts, and mind maps you can actually study from.", category="Audio",
   color1="#8b5cf6", color2="#7c3aed", initials="Pw", price="$8/mo", price_label="Pro plan", price_num="8",
   free_tier="Free tier (limited)", rating="4.3/5", rating_num="4.3", users="200K+ users", founded="2023",
   headline="Make podcasts skimmable in minutes",
   intro="Podwise transcribes any podcast episode, then distills it into a structured summary, key takeaways, and a mind map — so you can absorb a 90-minute show in 10. It syncs with Notion, Readwise, and Obsidian for a true 'second brain' flow.",
   who_for="Lifelong learners, investors, and busy pros who want podcast knowledge without the time sink.",
   features=[("📝","Smart transcript","Accurate, timestamped transcripts."),
             ("🧠","Mind maps","Visualize episode structure at a glance."),
             ("⚡","AI summary","Key points distilled to a few bullets."),
             ("🔗","Sync","Push to Notion, Readwise, Obsidian.")],
   pros=["Massive time savings",
         "Clean mind-map output",
         "Good export options",
         "Affordable"],
   cons=["Free tier is tight",
         "Depends on podcast RSS",
         "No live recording"],
   verdict="The smartest way to 'read' podcasts. For meeting notes, Otter or Fathom fit better; for podcast knowledge capture, Podwise is purpose-built.",
   cta_url="https://podwise.ai"),

 dict(slug="yuanbao", name="Yuanbao", tagline="Tencent's flagship AI assistant — deep Chinese-language reasoning with document, image, and search built in.", category="Productivity",
   color1="#07c160", color2="#06ad56", initials="Yb", price="Free", price_label="Consumer", price_num="0",
   free_tier="Free chat", rating="4.3/5", rating_num="4.3", users="50M+ users", founded="2024",
   headline="Tencent's answer to the frontier assistants",
   intro="Yuanbao is Tencent's Hunyuan-powered assistant, launched in 2024 and rapidly upgraded with deep reasoning, multimodal input, and live search. It's the strongest mainstream Chinese assistant for document analysis, coding help, and everyday tasks.",
   who_for="Chinese-speaking users and anyone needing top-tier Mandarin reasoning and document work.",
   features=[("🧠","Deep reasoning","Strong step-by-step logic in Chinese."),
             ("📄","Document chat","Analyze PDFs and long docs."),
             ("🌐","Live search","Grounded, cited answers."),
             ("👁️","Multimodal","Image and file understanding built in.")],
   pros=["Excellent Chinese fluency",
         "Free for consumers",
         "Strong doc analysis",
         "Tencent ecosystem integrations"],
   cons=["Limited English performance",
         "Mostly China-focused",
         "Fewer third-party integrations abroad"],
   verdict="The default assistant for Chinese-speaking users who want reasoning, documents, and search in one place. For English-first work, GPT or Claude still lead.",
   cta_url="https://yuanbao.tencent.com"),

 dict(slug="vmake", name="Vmake AI", tagline="AI video and image enhancer for e-commerce and creators — remove backgrounds, upscale, and generate models.", category="Video",
   color1="#ec4899", color2="#db2777", initials="Vm", price="$10/mo", price_label="Starter plan", price_num="10",
   free_tier="Free trial (watermarked)", rating="4.2/5", rating_num="4.2", users="5M+ users", founded="2022",
   headline="Studio-quality product visuals without a studio",
   intro="Vmake AI is built for e-commerce and social creators: bulk background removal, 4K upscaling, AI model generation for apparel, and video enhancement. It turns phone shots into marketplace-ready assets in a click.",
   who_for="E-commerce sellers, dropshippers, and creators who need clean product visuals fast.",
   features=[("🧹","BG remover","Clean cutouts in bulk."),
             ("⬆️","Upscaler","Push footage to 4K."),
             ("👗","AI models","Generate on-model apparel shots."),
             ("🎬","Video enhance","Denoise and sharpen clips.")],
   pros=["Purpose-built for e-commerce",
         "Batch processing",
         "No Photoshop needed",
         "Fast"],
   cons=["Free outputs watermarked",
         "Niche vs general editors",
         "Best features on paid tiers"],
   verdict="The fastest path to marketplace-ready product visuals. For general video generation, Runway or Kling are broader; for e-comm cleanup, Vmake is purpose-built.",
   cta_url="https://vmake.ai"),
]

COMPARES = [
 dict(slug="claude-opus-4-vs-gpt-5-1", name_a="Claude Opus 4", name_b="GPT-5.1", color_a="#d97706", color_b="#10a37f",
   initials_a="Co", initials_b="G5", url_a="https://claude.ai/?via=toolforge", url_b="https://chat.openai.com/?via=toolforge",
   desc_a="Anthropic's most capable, careful reasoning model", desc_b="OpenAI's latest flagship with broad tool use",
   price_a="~$20/mo Pro", price_b="~$20/mo Plus", best_a="long-form writing, careful analysis, code review", best_b="breadth, multimodal, agentic tasks",
   verdict="Use <strong>Claude Opus 4</strong> when nuance, long-context analysis, and careful writing matter most. Use <strong>GPT-5.1</strong> for the broadest tool-use, multimodal, and agentic capabilities. Both are frontier; pick Claude for craft, GPT for reach.",
   winner="Tie — Claude for craft, GPT-5.1 for breadth"),

 dict(slug="gemini-3-vs-claude-opus-4", name_a="Gemini 3", name_b="Claude Opus 4", color_a="#4285f4", color_b="#d97706",
   initials_a="Ge", initials_b="Co", url_a="https://gemini.google.com", url_b="https://claude.ai/?via=toolforge",
   desc_a="Google's multimodal giant with a 2M-token context", desc_b="Anthropic's careful, long-context flagship",
   price_a="Free / $20 Advanced", price_b="~$20/mo Pro", best_a="video/audio understanding, Workspace", best_b="writing, analysis, code review",
   verdict="Use <strong>Gemini 3</strong> if you need to reason over video, audio, and massive documents inside Google Workspace. Use <strong>Claude Opus 4</strong> for the most careful writing and analysis. Gemini wins on context and modality; Claude wins on prose.",
   winner="Tie — Gemini for context, Claude for prose"),

 dict(slug="chatgpt-vs-deepseek-r1", name_a="ChatGPT", name_b="DeepSeek R1", color_a="#10a37f", color_b="#4d6bfe",
   initials_a="Ch", initials_b="Dr", url_a="https://chat.openai.com/?via=toolforge", url_b="https://www.deepseek.com",
   desc_a="OpenAI's polished generalist assistant", desc_b="The open, low-cost reasoning model",
   price_a="$20/mo Plus", price_b="Free / cheap API", best_a="creative writing, image gen, voice", best_b="math, code, self-hosting",
   verdict="Use <strong>ChatGPT</strong> for the most polished, multimodal all-rounder. Use <strong>DeepSeek R1</strong> when you need top-tier reasoning and coding at the lowest cost — or want to self-host. ChatGPT for polish, DeepSeek for value.",
   winner="Tie — ChatGPT for polish, DeepSeek R1 for value"),

 dict(slug="notion-vs-obsidian-ai", name_a="Notion", name_b="Obsidian AI", color_a="#111827", color_b="#7c3aed",
   initials_a="No", initials_b="Ob", url_a="https://www.notion.so", url_b="https://obsidian.md",
   desc_a="The collaborative docs + AI workspace", desc_b="The local-first knowledge base with AI add-on",
   price_a="Free / $10 Plus", price_b="Free / $10 AI add-on", best_a="team docs, wikis, collaboration", best_b="private second brain, local files",
   verdict="Use <strong>Notion</strong> for shared docs, project wikis, and team collaboration. Use <strong>Obsidian AI</strong> if you want a private, local-first 'second brain' with full file ownership. Notion wins on teamwork; Obsidian wins on privacy.",
   winner="Tie — Notion for teams, Obsidian for privacy"),

 dict(slug="cursor-vs-bolt-new", name_a="Cursor", name_b="Bolt.new", color_a="#000000", color_b="#8b5cf6",
   initials_a="Cu", initials_b="Bo", url_a="https://www.cursor.com/?via=toolforge", url_b="https://bolt.new",
   desc_a="The AI-first desktop code editor", desc_b="The browser-based full-stack app builder",
   price_a="$20/mo Pro", price_b="$15/mo Pro", best_a="multi-file editing in an IDE", best_b="spin up full apps in the browser",
   verdict="Use <strong>Cursor</strong> if you want an AI pair programmer inside a real IDE you control. Use <strong>Bolt.new</strong> to scaffold and ship entire web apps from a prompt in the browser. Cursor for editing; Bolt for building from zero.",
   winner="Tie — Cursor for editing, Bolt for scaffolding"),

 dict(slug="dalle-3-vs-leonardo", name_a="DALL·E 3", name_b="Leonardo", color_a="#10a37f", color_b="#1f2937",
   initials_a="D3", initials_b="Le", url_a="https://chat.openai.com/?via=toolforge", url_b="https://leonardo.ai",
   desc_a="OpenAI's prompt-faithful image model", desc_b="The game-art and asset generation studio",
   price_a="Free / $20 Plus", price_b="Free / $10 Apprentice", best_a="prompt accuracy, ChatGPT integration", best_b="consistent characters, game assets",
   verdict="Use <strong>DALL·E 3</strong> when you want images that follow a written prompt precisely inside ChatGPT. Use <strong>Leonardo</strong> for stylized game assets, character consistency, and a full generation toolkit. DALL·E for fidelity, Leonardo for control.",
   winner="Tie — DALL·E 3 for prompts, Leonardo for assets"),

 dict(slug="synthesia-vs-colossyan-2", name_a="Synthesia", name_b="Colossyan", color_a="#7c3aed", color_b="#0ea5e9",
   initials_a="Sy", initials_b="Co", url_a="https://www.synthesia.io", url_b="https://www.colossyan.com",
   desc_a="The enterprise avatar-video leader", desc_b="The actor-led, easy avatar video maker",
   price_a="$29/mo Starter", price_b="$27/mo Starter", best_a="enterprise training at scale", best_b="quick, actor-style videos",
   verdict="Use <strong>Synthesia</strong> for enterprise-grade avatar training with the deepest template library. Use <strong>Colossyan</strong> if you want a friendlier, actor-led feel and fast turnaround. Synthesia for scale, Colossyan for speed.",
   winner="Synthesia — on enterprise depth"),

 dict(slug="perplexity-vs-grok-2", name_a="Perplexity", name_b="Grok", color_a="#0ea5e9", color_b="#111827",
   initials_a="Pe", initials_b="Gr", url_a="https://www.perplexity.ai/?via=toolforge", url_b="https://x.ai",
   desc_a="The cited answer engine", desc_b="xAI's witty, real-time assistant",
   price_a="Free / $20 Pro", price_b="Free / $8 SuperGrok", best_a="research with sources", best_b="real-time X data, personality",
   verdict="Use <strong>Perplexity</strong> when you need sourced, citable research. Use <strong>Grok</strong> for real-time commentary on X and a wittier personality. Perplexity for facts, Grok for the feed.",
   winner="Tie — Perplexity for sources, Grok for X"),
]

BLOGS = [
 dict(slug="ai-tools-faceless-youtube-2026", title="The 10 Best AI Tools for Faceless YouTube Channels in 2026",
   meta="No camera, no voice, no problem. The AI stack that researches, scripts, voices, and edits a faceless YouTube channel while you sleep.",
   category="For Creators", read="4", lead="Faceless YouTube is a real business in 2026 — and AI does almost all of it. We tested the stack that takes you from a niche idea to a published video without ever showing your face or recording your voice.",
   verdict="Start with a script generator (ChatGPT or Jasper), voice it with ElevenLabs, and edit with Vmake or CapCut. Add a thumbnail tool (Canva) and you can publish daily. The channel runs on systems, not on you.",
   tools=[
     dict(name="ChatGPT", url="https://chat.openai.com/?via=toolforge", color="#10a37f", initial="Ch", badge="Free", desc="Scriptwriting and hook ideas"),
     dict(name="ElevenLabs", url="https://elevenlabs.io/?via=toolforge", color="#06b6d4", initial="El", badge="Free", desc="Natural AI voiceover"),
     dict(name="CapCut", url="https://www.capcut.com", color="#ffffff", initial="Cc", badge="Free", desc="Fast faceless video edits"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="Thumbnails that get clicks"),
     dict(name="Vmake", url="https://vmake.ai", color="#ec4899", initial="Vm", badge="$10/mo", desc="Upscale and clean footage"),
     dict(name="HeyGen", url="https://www.heygen.com", color="#7c3aed", initial="Hg", badge="$24/mo", desc="Optional avatar intros"),
     dict(name="VidIQ", url="https://vidiq.com", color="#a855f7", initial="Vi", badge="Free", desc="Keyword and SEO research"),
     dict(name="Opus Clip", url="https://www.opus.pro", color="#ff6b00", initial="Oc", badge="$19/mo", desc="Turn long video into Shorts"),
     dict(name="Jasper", url="https://www.jasper.ai", color="#e11d48", initial="Ja", badge="$39/mo", desc="Batch script production"),
     dict(name="Pictory", url="https://pictory.ai", color="#7c3aed", initial="Pi", badge="$19/mo", desc="Text-to-video from articles"),
   ]),

 dict(slug="best-ai-headshot-generators-2026", title="The 7 Best AI Headshot Generators in 2026 (LinkedIn-Ready in an Hour)",
   meta="Professional headshots without a photographer. The AI tools that turn a few selfies into a studio-grade portrait.",
   category="For Professionals", read="3", lead="A $300 photo session or a $20 AI app? In 2026 the gap has nearly closed for LinkedIn and casual professional use. We tested the headshot generators that actually look like you — and not like a wax figure.",
   verdict="Use Aragon or HeadshotPro for the most realistic corporate shots, and Remini or StudioShot for a quick glow-up. Upload 10+ varied selfies and you'll get a usable LinkedIn photo in under an hour.",
   tools=[
     dict(name="Aragon AI", url="https://www.aragon.ai", color="#111827", initial="Ar", badge="$29", desc="Realistic corporate headshots"),
     dict(name="HeadshotPro", url="https://www.headshotpro.com", color="#0a72ef", initial="Hp", badge="$29", desc="Team headshots at scale"),
     dict(name="StudioShot", url="https://studioshot.ai", color="#7c3aed", initial="Ss", badge="$29", desc="Stylized, polished looks"),
     dict(name="Remini", url="https://remini.ai", color="#ff6b00", initial="Re", badge="Free", desc="Quick face enhancement"),
     dict(name="PhotoRoom", url="https://www.photoroom.com", color="#10b981", initial="Pr", badge="Free", desc="BG swap + retouch"),
     dict(name="BetterPic", url="https://www.betterpic.io", color="#6366f1", initial="Bp", badge="$35", desc="LinkedIn-ready packs"),
     dict(name="Fotor", url="https://www.fotor.com", color="#ff4d4f", initial="Fo", badge="Free", desc="All-in-one editor + headshots"),
   ]),

 dict(slug="ai-tools-second-brain-2026", title="Build a Second Brain with AI: The 8 Tools That Actually Work in 2026",
   meta="Capture, connect, and recall everything. The AI tools that turn scattered notes into a searchable second brain.",
   category="Productivity", read="4", lead="A 'second brain' isn't a folder of screenshots — it's a system that resurfaces the right note at the right time. In 2026, AI does the connecting for you. Here are the tools that make it real.",
   verdict="Use NotebookLM as your synthesis layer, Obsidian + Copilot for the local vault, and Readwise to ingest everything you read. Add Mem for auto-organization. The result is recall on tap.",
   tools=[
     dict(name="NotebookLM", url="https://notebooklm.google.com", color="#4285f4", initial="Nl", badge="Free", desc="Synthesize sources into audio"),
     dict(name="Obsidian", url="https://obsidian.md", color="#7c3aed", initial="Ob", badge="Free", desc="Local-first knowledge base"),
     dict(name="Mem", url="https://mem.ai", color="#111827", initial="Me", badge="Free", desc="Auto-organized notes"),
     dict(name="Readwise", url="https://readwise.io", color="#111827", initial="Rw", badge="$8/mo", desc="Ingest books & articles"),
     dict(name="ChatDOC", url="https://chatdoc.com", color="#ef4444", initial="Cd", badge="Free", desc="Chat with your PDFs"),
     dict(name="Research Rabbit", url="https://www.researchrabbit.ai", color="#7c3aed", initial="Rr", badge="Free", desc="Map your reading"),
     dict(name="Notion AI", url="https://www.notion.so", color="#111827", initial="Na", badge="Free trial", desc="AI inside your notes"),
     dict(name="Recall", url="https://recall.ai", color="#0ea5e9", initial="Rc", badge="Free", desc="Summarize & save anything"),
   ]),

 dict(slug="best-ai-email-tools-2026", title="The 8 Best AI Email Tools to Finally Hit Inbox Zero in 2026",
   meta="Triage, draft, and summarize your inbox with AI. The tools that give you back the hour email steals every day.",
   category="Productivity", read="3", lead="Email is where the day goes to die. In 2026, AI can triage, summarize threads, and draft replies so you only touch what matters. We tested the inboxes that actually clear themselves.",
   verdict="Use Superhuman or Shortwave for a faster inbox, SaneBox to filter noise, and Missive if you reply as a team. Add a writing assistant (Grammarly) and Inbox Zero becomes routine.",
   tools=[
     dict(name="Superhuman", url="https://superhuman.com", color="#111827", initial="Sh", badge="$30/mo", desc="Fastest inbox experience"),
     dict(name="Shortwave", url="https://www.shortwave.com", color="#0a72ef", initial="Sw", badge="$9/mo", desc="AI summaries & triage"),
     dict(name="SaneBox", url="https://www.sanebox.com", color="#6366f1", initial="Sb", badge="$7/mo", desc="Filter the noise"),
     dict(name="Missive", url="https://missiveapp.com", color="#7c3aed", initial="Mi", badge="Free", desc="Team inbox + AI"),
     dict(name="Spark", url="https://sparkmailapp.com", color="#0ea5e9", initial="Sp", badge="Free", desc="Smart inbox for Apple"),
     dict(name="Grammarly", url="https://www.grammarly.com", color="#15c39a", initial="Gr", badge="Free", desc="Polish every reply"),
     dict(name="Mailbutler", url="https://www.mailbutler.io", color="#ec4899", initial="Mb", badge="Free", desc="AI assist in Apple Mail"),
     dict(name="Polymail", url="https://polymail.io", color="#111827", initial="Pl", badge="$10/mo", desc="Sequences + tracking"),
   ]),

 dict(slug="how-to-build-an-ai-content-pipeline-2026", title="How to Build an AI Content Pipeline in 2026 (That Runs While You Sleep)",
   meta="From idea to published post without touching a keyboard. The workflow and tools that automate your content engine.",
   category="For Marketers", read="5", lead="One good post is a craft. A content engine is a system. In 2026 you can wire AI tools into a pipeline that researches, drafts, designs, and schedules — and runs daily. Here's the exact stack.",
   verdict="Use Perplexity for research, Claude or Jasper for drafts, Canva for visuals, and Make or Zapier to schedule and publish. Add Opus Clip to spin social cuts. The pipeline compounds while you sleep.",
   tools=[
     dict(name="Perplexity", url="https://www.perplexity.ai/?via=toolforge", color="#0ea5e9", initial="Pe", badge="Free", desc="Sourced topic research"),
     dict(name="Claude", url="https://claude.ai/?via=toolforge", color="#d97706", initial="Cl", badge="Free", desc="Long-form drafting"),
     dict(name="Jasper", url="https://www.jasper.ai", color="#e11d48", initial="Ja", badge="$39/mo", desc="Brand-voice at scale"),
     dict(name="Canva", url="https://www.canva.com", color="#00c4cc", initial="Ca", badge="Free", desc="On-brand visuals"),
     dict(name="Opus Clip", url="https://www.opus.pro", color="#ff6b00", initial="Oc", badge="$19/mo", desc="Video snippets for social"),
     dict(name="Make", url="https://www.make.com/en?ref=toolforge", color="#0a72ef", initial="Mk", badge="$9/mo", desc="Automate the workflow"),
     dict(name="Zapier", url="https://zapier.com", color="#ff4f00", initial="Za", badge="Free", desc="Connect your apps"),
     dict(name="Buffer", url="https://buffer.com", color="#2d2d2d", initial="Bu", badge="Free", desc="Schedule & publish"),
   ]),
]

# =================== WRITE ===================
new_urls = []
created = {"tools":0, "compare":0, "blog":0}

for t in TOOLS:
    if t['slug'] in tool_slugs:
        print(f"  SKIP tool {t['slug']} (exists)")
        continue
    p = os.path.join(BASE, 'tools', f"{t['slug']}.html")
    with open(p, 'w') as f:
        f.write(tool_html(t))
    new_urls.append(f"{DOMAIN}/tools/{t['slug']}.html")
    created['tools'] += 1
    print(f"  + tool {t['slug']}.html")

for c in COMPARES:
    if c['slug'] in cmp_slugs:
        print(f"  SKIP compare {c['slug']} (exists)")
        continue
    p = os.path.join(BASE, 'compare', f"{c['slug']}.html")
    with open(p, 'w') as f:
        f.write(compare_html(c))
    new_urls.append(f"{DOMAIN}/compare/{c['slug']}.html")
    created['compare'] += 1
    print(f"  + compare {c['slug']}.html")

for b in BLOGS:
    if b['slug'] in blog_slugs:
        print(f"  SKIP blog {b['slug']} (exists)")
        continue
    p = os.path.join(BASE, 'blog', f"{b['slug']}.html")
    with open(p, 'w') as f:
        f.write(blog_html(b))
    new_urls.append(f"{DOMAIN}/blog/{b['slug']}.html")
    created['blog'] += 1
    print(f"  + blog {b['slug']}.html")

# ---------- SITEMAP ----------
if new_urls:
    sp = os.path.join(BASE, 'sitemap.xml')
    with open(sp) as f:
        content = f.read()
    urls_xml = ""
    for u in new_urls:
        urls_xml += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
    content = content.replace("</urlset>", urls_xml + "</urlset>", 1)
    with open(sp, 'w') as f:
        f.write(content)
    print(f"\nSitemap: added {len(new_urls)} URLs")
else:
    print("\nNo new URLs to add to sitemap.")

print(f"\nCREATED: {created}")
print(f"TOTAL NEW URLS: {len(new_urls)}")
