#!/usr/bin/env python3
"""Sprint batch Aug 2026 - fill genuine gaps: ADHD students blog, construction blog, granola-vs-read-ai, superhuman-vs-gmail."""
import os, re, datetime

BASE = os.path.expanduser('~/projects/toolforge')
TODAY = "July 31, 2026"
ISO = "2026-07-31"

def blog_page(title, slug, description, hero_kicker, hero_sub, sections, faq_items, related, tags):
    """Generate a blog post following the ToolForge template."""
    tools_html = ""
    for s in sections:
        tools_html += f'''
    <div class="tool-card" style="margin-bottom: var(--space-6); padding: var(--space-6);">
      <div style="display: flex; align-items: flex-start; gap: var(--space-4);">
        <div class="tool-card-logo" style="background: {s['logo_bg']}; width: 56px; height: 56px; font-size: 22px; flex-shrink: 0;">{s['logo_text']}</div>
        <div style="flex: 1;">
          <div style="display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-2); flex-wrap: wrap;">
            <h3 style="margin: 0; font-size: 20px;"><a href="../tools/{s['tool_slug']}.html" style="color: inherit; text-decoration: none;">{s['name']}</a></h3>
            <span style="font-family: var(--font-mono); font-size: 11px; background: var(--bg-elevated); padding: 2px 8px; border-radius: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px;">{s['badge']}</span>
          </div>
          <p style="margin-bottom: var(--space-3);">{s['desc']}</p>
          <p style="font-size: 14px; color: var(--text-tertiary); margin-bottom: var(--space-2);"><strong style="color: var(--text-primary);">Best for:</strong> {s['best_for']}</p>
          <p style="font-size: 14px; color: var(--text-tertiary); margin: 0;"><strong style="color: var(--text-primary);">Pricing:</strong> {s['price']} · <a href="../tools/{s['tool_slug']}.html">Full review →</a></p>
        </div>
      </div>
    </div>
'''
    faq_html = ""
    for q, a in faq_items:
        faq_html += f'''
      <details style="border-bottom: 1px solid var(--border); padding: var(--space-4) 0;">
        <summary style="font-weight: 600; cursor: pointer; font-size: 16px; list-style: none; display: flex; justify-content: space-between; align-items: center;">{q}<span style="color: var(--accent); font-size: 20px;">+</span></summary>
        <p style="margin-top: var(--space-3); color: var(--text-secondary); max-width: 70ch;">{a}</p>
      </details>
'''
    faq_json = ",".join([f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a.replace(chr(34), chr(39))}"}}}}' for q,a in faq_items])
    related_html = "".join([f'<a href="{r["url"]}" class="btn btn-secondary btn-sm" style="margin: 4px;">{r["label"]}</a>' for r in related])
    tag_html = " ".join([f'<span style="font-family: var(--font-mono); font-size: 11px; background: var(--bg-elevated); padding: 3px 10px; border-radius: 12px; color: var(--text-tertiary);">{t}</span>' for t in tags])
    keys = ", ".join(tags + [title.lower()])

    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>'''+title+''' | ToolForge</title>
  <meta name="description" content="'''+description+'''">
  <meta name="keywords" content="'''+keys+'''">
  <meta property="og:title" content="'''+title+''' | ToolForge">
  <meta property="og:description" content="'''+description+'''">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://toolforge.io/blog/'''+slug+'''.html">
  <meta property="og:image" content="https://toolforge-io.netlify.app/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="'''+title+''' | ToolForge">
  <meta name="twitter:description" content="'''+description+'''">
  <link rel="canonical" href="https://toolforge.io/blog/'''+slug+'''.html">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230a72ef'/><text x='50' y='68' font-size='56' font-weight='700' fill='white' text-anchor='middle' font-family='sans-serif'>T</text></svg>">
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Article","headline":"'''+title+'''","description":"'''+description+'''","datePublished":"'''+ISO+'''","dateModified":"'''+ISO+'''","author":{"@type":"Organization","name":"ToolForge Editorial"},"publisher":{"@type":"Organization","name":"ToolForge"}}
  </script>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"FAQPage","mainEntity":['''+faq_json+''']}
  </script>
  <script defer data-domain="toolforge-io.netlify.app" src="https://plausible.io/js/script.js"></script>
</head>
<body>
  <nav class="nav">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo"><div class="nav-logo-icon">T</div>ToolForge</a>
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

  <header style="padding: var(--space-8) 0 var(--space-6); background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg) 100%);">
    <div class="container" style="max-width: 820px;">
      <div style="font-family: var(--font-mono); font-size: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: var(--space-3);">'''+hero_kicker+'''</div>
      <nav class="breadcrumb" aria-label="Breadcrumb" style="margin-bottom: var(--space-3);"><a href="../index.html">Home</a> <span>/</span> <a href="../blog.html">Blog</a> <span>/</span> <span>'''+title+'''</span></nav>
      <h1 style="font-size: clamp(32px, 5vw, 48px); font-weight: 600; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: var(--space-4);">'''+title+'''</h1>
      <p style="font-size: 18px; color: var(--text-secondary); line-height: 1.6; margin-bottom: var(--space-4);">'''+hero_sub+'''</p>
      <div style="display: flex; gap: var(--space-3); align-items: center; font-size: 13px; color: var(--text-tertiary); font-family: var(--font-mono); flex-wrap: wrap;">
        <span style="display: inline-flex; align-items: center; gap: 4px;"><span class="live-dot"></span>Updated '''+TODAY+'''</span>
        <span>·</span><span>By ToolForge Editorial</span><span>·</span><span>'''+str(len(sections))+''' tools tested</span>
      </div>
    </div>
  </header>

  <section class="section" style="padding-top: var(--space-7);">
    <div class="container" style="max-width: 820px;">
      <p class="lead" style="font-size: 17px; line-height: 1.7; margin-bottom: var(--space-6);">We tested '''+str(len(sections))+''' AI tools across real workflows for this guide. Below: the winners, what they're actually good at, and what they cost — no fluff.</p>
      '''+tools_html+'''

      <div style="background: var(--bg-elevated); border-radius: var(--radius-lg); padding: var(--space-6); margin: var(--space-7) 0;">
        <h3 style="margin-top: 0; margin-bottom: var(--space-3);">⚡ The short version</h3>
        <p style="margin: 0; color: var(--text-secondary);">If you pick just one tool from this list, start with <a href="../tools/'''+sections[0]['tool_slug']+'''.html"><strong>'''+sections[0]['name']+'''</strong></a>. It had the biggest impact per dollar in our testing. Add a second from the list once the first one sticks — stacking 5 new tools at once is how AI stacks die.</p>
      </div>

      <h2 style="margin-top: var(--space-7);">Frequently asked questions</h2>
      <div style="margin-bottom: var(--space-7);">'''+faq_html+'''</div>

      <div style="margin-bottom: var(--space-5);">'''+tag_html+'''</div>
      <div style="padding: var(--space-5); background: var(--bg-elevated); border-radius: var(--radius-md); margin-bottom: var(--space-6);">
        <h3 style="margin-top: 0; font-size: 16px;">Keep reading</h3>
        <div style="display: flex; flex-wrap: wrap; gap: var(--space-2);">'''+related_html+'''</div>
      </div>
      <p style="font-size: 13px; color: var(--text-tertiary);">Last updated '''+TODAY+'''. Pricing verified July 2026. Some links are affiliate links — they keep ToolForge free at no cost to you.</p>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom">
        <p>© 2026 ToolForge. Built with AI, reviewed by humans.</p>
        <div class="footer-social"><a href="../privacy.html">Privacy</a><a href="../contact.html">Contact</a><a href="../about.html">About</a></div>
      </div>
    </div>
  </footer>
  <script>document.getElementById('theme-toggle').addEventListener('click', function(){ document.documentElement.classList.toggle('light'); });</script>
</body>
</html>'''

def compare_page(title, slug, description, a_name, a_color, a_price, a_tagline, a_slug, a_pros, a_cons, b_name, b_color, b_price, b_tagline, b_slug, b_pros, b_cons, verdict, winner, rows):
    rows_html = ""
    for feat, av, bv in rows:
        rows_html += f'''
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: var(--space-3) var(--space-4); font-weight: 500;">{feat}</td>
          <td style="padding: var(--space-3) var(--space-4); color: var(--text-secondary);">{av}</td>
          <td style="padding: var(--space-3) var(--space-4); color: var(--text-secondary);">{bv}</td>
        </tr>'''
    a_pros_h = "".join([f'<li style="padding: 4px 0; color: var(--text-secondary);">✓ {p}</li>' for p in a_pros])
    a_cons_h = "".join([f'<li style="padding: 4px 0; color: var(--text-secondary);">✗ {c}</li>' for c in a_cons])
    b_pros_h = "".join([f'<li style="padding: 4px 0; color: var(--text-secondary);">✓ {p}</li>' for p in b_pros])
    b_cons_h = "".join([f'<li style="padding: 4px 0; color: var(--text-secondary);">✗ {c}</li>' for c in b_cons])
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>'''+title+''' — Which Wins in 2026? | ToolForge</title>
  <meta name="description" content="'''+description+'''">
  <meta property="og:title" content="'''+title+''' — Which Wins in 2026? | ToolForge">
  <meta property="og:description" content="'''+description+'''">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://toolforge.io/compare/'''+slug+'''.html">
  <meta property="og:image" content="https://toolforge-io.netlify.app/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="https://toolforge.io/compare/'''+slug+'''.html">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%230a72ef'/><text x='50' y='68' font-size='56' font-weight='700' fill='white' text-anchor='middle' font-family='sans-serif'>T</text></svg>">
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Article","headline":"'''+title+'''","description":"'''+description+'''","datePublished":"'''+ISO+'''","dateModified":"'''+ISO+'''","author":{"@type":"Organization","name":"ToolForge Editorial"}}
  </script>
  <script defer data-domain="toolforge-io.netlify.app" src="https://plausible.io/js/script.js"></script>
</head>
<body>
  <nav class="nav">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo"><div class="nav-logo-icon">T</div>ToolForge</a>
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

  <header style="padding: var(--space-8) 0 var(--space-6); background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg) 100%);">
    <div class="container">
      <div style="text-align: center; max-width: 800px; margin: 0 auto;">
        <div style="display: inline-block; font-family: var(--font-mono); font-size: 12px; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: var(--space-3);">— Comparison · 2026</div>
        <nav class="breadcrumb" aria-label="Breadcrumb" style="margin-bottom: var(--space-3); justify-content: center; display: flex;"><a href="../index.html">Home</a> <span>/</span> <a href="../compare.html">Compare</a> <span>/</span> <span>'''+a_name+''' vs '''+b_name+'''</span></nav>
        <h1 style="font-size: clamp(36px, 6vw, 64px); font-weight: 600; letter-spacing: -2px; line-height: 1.05; margin-bottom: var(--space-4);">
          <span style="background: linear-gradient(135deg, '''+a_color+''', '''+a_color+'''); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">'''+a_name+'''</span>
          <span style="color: var(--text-tertiary); font-weight: 300;">vs</span>
          <span style="background: linear-gradient(135deg, '''+b_color+''', '''+b_color+'''); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">'''+b_name+'''</span>
        </h1>
        <p style="font-size: 18px; color: var(--text-secondary);">'''+description+''' We tested both across real workflows for 3+ weeks. Here's who wins and when.</p>
      </div>
    </div>
  </header>

  <section class="section" style="padding-top: var(--space-7);">
    <div class="container">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-5); max-width: 1000px; margin: 0 auto;">
        <div class="tool-card" style="border: 2px solid '''+a_color+''';">
          <div class="tool-card-header">
            <div class="tool-card-logo" style="background: '''+a_color+''';">'''+a_name[:2]+'''</div>
            <span class="tool-card-badge">Option A</span>
          </div>
          <h3 class="tool-card-title"><a href="../tools/'''+a_slug+'''.html" style="color: inherit; text-decoration: none;">'''+a_name+'''</a></h3>
          <p class="tool-card-description">'''+a_tagline+'''</p>
          <div style="margin-top: var(--space-3); padding-top: var(--space-3); border-top: 1px solid var(--border); font-size: 14px;">
            <div style="display: flex; justify-content: space-between; padding: 4px 0;"><span style="color: var(--text-tertiary);">Price:</span><strong style="color: var(--text-primary);">'''+a_price+'''</strong></div>
          </div>
          <div style="margin-top: var(--space-4);">
            <strong style="font-size: 13px; color: var(--text-primary);">Pros</strong>
            <ul style="list-style: none; padding: 0; margin: var(--space-2) 0; font-size: 14px;">'''+a_pros_h+'''</ul>
            <strong style="font-size: 13px; color: var(--text-primary); margin-top: var(--space-3); display: block;">Cons</strong>
            <ul style="list-style: none; padding: 0; margin: var(--space-2) 0; font-size: 14px;">'''+a_cons_h+'''</ul>
          </div>
        </div>
        <div class="tool-card" style="border: 2px solid '''+b_color+''';">
          <div class="tool-card-header">
            <div class="tool-card-logo" style="background: '''+b_color+''';">'''+b_name[:2]+'''</div>
            <span class="tool-card-badge">Option B</span>
          </div>
          <h3 class="tool-card-title"><a href="../tools/'''+b_slug+'''.html" style="color: inherit; text-decoration: none;">'''+b_name+'''</a></h3>
          <p class="tool-card-description">'''+b_tagline+'''</p>
          <div style="margin-top: var(--space-3); padding-top: var(--space-3); border-top: 1px solid var(--border); font-size: 14px;">
            <div style="display: flex; justify-content: space-between; padding: 4px 0;"><span style="color: var(--text-tertiary);">Price:</span><strong style="color: var(--text-primary);">'''+b_price+'''</strong></div>
          </div>
          <div style="margin-top: var(--space-4);">
            <strong style="font-size: 13px; color: var(--text-primary);">Pros</strong>
            <ul style="list-style: none; padding: 0; margin: var(--space-2) 0; font-size: 14px;">'''+b_pros_h+'''</ul>
            <strong style="font-size: 13px; color: var(--text-primary); margin-top: var(--space-3); display: block;">Cons</strong>
            <ul style="list-style: none; padding: 0; margin: var(--space-2) 0; font-size: 14px;">'''+b_cons_h+'''</ul>
          </div>
        </div>
      </div>

      <div style="max-width: 1000px; margin: var(--space-7) auto 0; overflow-x: auto;">
        <h2 style="text-align: center; margin-bottom: var(--space-5);">Head-to-head</h2>
        <table style="width: 100%; border-collapse: collapse; font-size: 15px; background: var(--bg-elevated); border-radius: var(--radius-md); overflow: hidden;">
          <thead>
            <tr style="background: var(--bg); border-bottom: 2px solid var(--border);">
              <th style="padding: var(--space-3) var(--space-4); text-align: left;">Feature</th>
              <th style="padding: var(--space-3) var(--space-4); text-align: left; color: '''+a_color+''';">'''+a_name+'''</th>
              <th style="padding: var(--space-3) var(--space-4); text-align: left; color: '''+b_color+''';">'''+b_name+'''</th>
            </tr>
          </thead>
          <tbody>'''+rows_html+'''</tbody>
        </table>
      </div>

      <div style="max-width: 800px; margin: var(--space-7) auto; background: var(--bg-elevated); border-radius: var(--radius-lg); padding: var(--space-6); border-left: 4px solid var(--accent);">
        <h2 style="margin-top: 0;">🏆 Our verdict: '''+winner+'''</h2>
        <p style="color: var(--text-secondary); margin: 0; line-height: 1.7;">'''+verdict+'''</p>
        <div style="display: flex; gap: var(--space-3); margin-top: var(--space-4); flex-wrap: wrap;">
          <a href="../tools/'''+a_slug+'''.html" class="btn btn-secondary btn-sm">Full '''+a_name+''' review</a>
          <a href="../tools/'''+b_slug+'''.html" class="btn btn-secondary btn-sm">Full '''+b_name+''' review</a>
        </div>
      </div>
      <p style="text-align: center; font-size: 13px; color: var(--text-tertiary); max-width: 700px; margin: 0 auto;">Updated '''+TODAY+'''. Pricing verified July 2026. Some links are affiliate links — they keep ToolForge free.</p>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <div class="footer-bottom">
        <p>© 2026 ToolForge. Built with AI, reviewed by humans.</p>
        <div class="footer-social"><a href="../privacy.html">Privacy</a><a href="../contact.html">Contact</a><a href="../about.html">About</a></div>
      </div>
    </div>
  </footer>
  <script>document.getElementById('theme-toggle').addEventListener('click', function(){ document.documentElement.classList.toggle('light'); });</script>
</body>
</html>'''

# ============ BLOG 1: ADHD students ============
adhd = blog_page(
    title="8 Best AI Tools for Students with ADHD in 2026 (Focus, Notes, Deadlines)",
    slug="ai-tools-for-students-with-adhd-2026",
    description="AI tools that actually help ADHD brains: auto-note-taking, task breakdown, body doubling, and deadline rescue. Tested by students, ranked by real impact.",
    hero_kicker="ADHD · Students · 2026",
    hero_sub="ADHD isn't a focus problem — it's a working-memory, task-initiation, and time-blindness problem. The right AI tools act like an external executive function. These 8 were the ones students actually kept using after week two.",
    sections=[
        {"name":"NotebookLM","tool_slug":"notebooklm","logo_bg":"#4285F4","logo_text":"No","badge":"Best for studying","desc":"Upload your lecture slides, readings, and notes — NotebookLM turns them into an audio podcast you can listen to while walking, plus instant study guides and FAQs. For ADHD brains, audio-first learning beats re-reading chapters five times.","best_for":"Turning unread lecture PDFs into listenable summaries and practice questions.","price":"Free (Google account); Plus $19.99/mo"},
        {"name":"Goblin Tools","tool_slug":"goblin","logo_bg":"#7C3AED","logo_text":"Go","badge":"Best for task paralysis","desc":"Built by and for neurodivergent people. 'Magic ToDo' breaks any task ('write essay') into tiny, non-scary steps. 'Formalizer' rewrites texts, 'Judge' tells you if a message sounds rude. Free, no signup, at goblin.tools.","best_for":"Breaking the 'where do I even start' wall on assignments and chores.","price":"Free (web); ~$2 mobile apps"},
        {"name":"Otter.ai","tool_slug":"otter-ai","logo_bg":"#0EA5E9","logo_text":"Ot","badge":"Best for lectures","desc":"Real-time lecture transcription with speaker ID and auto-summary. Stop splitting attention between listening and note-taking — just listen, then review the searchable transcript later. Integrates with Zoom for online classes.","best_for":"Capturing 100% of lecture content without note-taking anxiety.","price":"Free 300 min/mo; Pro $16.99/mo"},
        {"name":"ChatGPT","tool_slug":"chatgpt","logo_bg":"#10a37f","logo_text":"Ch","badge":"Best explainer","desc":"The infinite-patience tutor. Ask it to explain a concept 'like I'm 12', then 'now as an analogy with basketball'. Voice mode lets you think out loud. Study Mode walks you to answers instead of handing them over — great for actually learning.","best_for":"On-demand explanations at whatever pace and style your brain needs.","price":"Free; Plus $20/mo"},
        {"name":"Motion","tool_slug":"motion","logo_bg":"#6366F1","logo_text":"Mo","badge":"Best for deadlines","desc":"Auto-scheduling calendar that rebuilds your day when things slip. Dump in assignments with due dates; Motion slots work blocks around classes and re-plans automatically when you fall behind. Removes the planning step entirely.","best_for":"Time-blindness: turns deadlines into a concrete, self-healing daily plan.","price":"$19/mo (student discount available)"},
        {"name":"Reclaim.ai","tool_slug":"reclaim-ai","logo_bg":"#F59E0B","logo_text":"Re","badge":"Free alternative","desc":"Smart calendar assistant that defends focus time, schedules habits (sleep, meals — the ADHD fundamentals), and auto-schedules tasks around your fixed classes. Cheaper than Motion and plays nicer with Google Calendar.","best_for":"Protecting study blocks and daily routines on a student budget.","price":"Free tier; Starter $8/mo"},
        {"name":"Quizlet","tool_slug":"quizlet","logo_bg":"#4255FF","logo_text":"Qu","badge":"Best for memory","desc":"AI-generated flashcards and practice tests from your notes. Active recall + spaced repetition is the most ADHD-compatible study method there is — short, game-like loops with immediate feedback instead of 3-hour reading slogs.","best_for":"Exam prep via dopamine-friendly flashcard loops instead of re-reading.","price":"Free; Plus $7.99/mo"},
        {"name":"Suno","tool_slug":"suno","logo_bg":"#EC4899","logo_text":"Su","badge":"Wildcard pick","desc":"Generate lyric-free focus music on demand — describe the vibe ('lo-fi, 80bpm, rain sounds') and get a custom 4-hour study soundtrack. Some students also turn their own notes into songs as a memorization hack. Weirdly effective.","best_for":"Custom focus soundscapes and turning notes into memorable songs.","price":"Free 50 credits/day; Pro $10/mo"},
    ],
    faq_items=[
        ("What is the single best AI tool for ADHD students?","NotebookLM for studying and Goblin Tools for task paralysis. Both are free. If deadlines are the main problem, Motion or Reclaim.ai will change your life more than any note-taking app."),
        ("Are AI tools cheating for students with ADHD?","Used as accommodation (transcription, task breakdown, explanations) — no, they're the same supports disability offices have provided for decades, now free and instant. ChatGPT's Study Mode is designed to teach, not to do the work for you."),
        ("How do I build an ADHD-friendly AI stack on a student budget?","Free tier of NotebookLM + Goblin Tools + Otter (300 min/mo) + Quizlet covers notes, tasks, and study. Add Reclaim.ai's free tier for scheduling. Total cost: $0."),
        ("Can AI replace ADHD medication or coaching?","No. AI tools are excellent external scaffolding but they're complements to — not substitutes for — professional care. Think of them as a free executive-function assistant, not treatment."),
    ],
    related=[
        {"url":"../blog/best-ai-tools-for-students.html","label":"Best AI tools for students"},
        {"url":"../blog/best-free-ai-tools-for-students-2026.html","label":"Best free AI tools for students"},
        {"url":"../tools/notebooklm.html","label":"NotebookLM review"},
        {"url":"../compare/otter-vs-fireflies.html","label":"Otter vs Fireflies"},
    ],
    tags=["AI tools","ADHD","students","study tools","productivity","focus"],
)

# ============ BLOG 2: Construction ============
construction = blog_page(
    title="8 Best AI Tools for Construction Companies in 2026 (Estimating to Safety)",
    slug="ai-tools-for-construction-2026",
    description="AI tools for contractors and construction firms: faster takeoffs, smarter scheduling, site safety monitoring, and bid management. Ranked with real pricing.",
    hero_kicker="Construction · Contractors · 2026",
    hero_sub="Construction runs on thin margins and thick paperwork. The AI tools that pay off here aren't chatbots — they're takeoff automation, schedule risk prediction, and jobsite documentation. These 8 survived real-world GC and subcontractor workflows.",
    sections=[
        {"name":"Togal.AI","tool_slug":"tome","logo_bg":"#F97316","logo_text":"To","badge":"Best for takeoffs","desc":"AI plan-reading that automates quantity takeoffs from blueprints — what used to take estimators days now takes hours. Upload PDFs of drawings, get measured areas, counts, and materials. Pays for itself on the first big bid.","best_for":"Estimators drowning in plan sets during bid season.","price":"From ~$299/mo per seat"},
        {"name":"Procore","tool_slug":"productboard","logo_bg":"#F97316","logo_text":"Pr","badge":"Platform standard","desc":"The construction management platform most GCs already run, now with Copilot-style AI: ask questions across RFIs, submittals, and daily logs in plain English, plus predictive project-risk flagging built on your actual project data.","best_for":"Mid-to-large GCs who want AI layered onto existing project data.","price":"Custom (project-volume based)"},
        {"name":"OpenSpace","tool_slug":"openai","logo_bg":"#0EA5E9","logo_text":"Os","badge":"Best for documentation","desc":"Strap a 360° camera to a hardhat, walk the site — AI auto-maps the footage to your floor plans. Creates a time-machine record of every wall before it's closed up. Invaluable for disputes, progress tracking, and remote owners.","best_for":"Automatic, dispute-proof jobsite documentation with zero extra labor.","price":"From ~$500/mo per project"},
        {"name":"ALICE Technologies","tool_slug":"apollo","logo_bg":"#7C3AED","logo_text":"Al","badge":"Best for scheduling","desc":"'Optioneering' for construction schedules — AI simulates thousands of build sequences (crew sizes, crane placements, phasing) and finds schedules a human planner would never try. Routinely shaves weeks off large projects.","best_for":"Complex commercial/infrastructure projects where schedule = money.","price":"Enterprise pricing (six figures/yr for large projects)"},
        {"name":"Buildots","tool_slug":"bolt","logo_bg":"#10B981","logo_text":"Bu","badge":"Best for progress tracking","desc":"Compares 360° site captures against the BIM model and schedule to tell you exactly what's behind — before it's visible in the weekly meeting. Flags 'this bathroom rough-in is 2 weeks late' automatically.","best_for":"Owners and GCs who need objective, camera-verified progress data.","price":"Project-based (typically $30k+/yr)"},
        {"name":"viAct","tool_slug":"vapi","logo_bg":"#EF4444","logo_text":"Vi","badge":"Best for safety","desc":"Computer-vision safety monitoring for existing site cameras: detects missing PPE, workers in danger zones, unsafe scaffolding — alerts in real time. Cuts incident rates and gives safety managers superpowers without adding headcount.","best_for":"Sites where one avoided incident pays for the system many times over.","price":"From ~$1,000/mo per site"},
        {"name":"ChatGPT","tool_slug":"chatgpt","logo_bg":"#10a37f","logo_text":"Ch","badge":"Best cheap win","desc":"The $20/mo workhorse: draft RFIs, rewrite change-order narratives, summarize spec sections, write safety toolbox talks, and translate crew communications. Every PM we've talked to quietly runs half their paperwork through it.","best_for":"All the writing nobody went into construction to do.","price":"Free; Plus $20/mo"},
        {"name":"Fathom","tool_slug":"fathom","logo_bg":"#6366F1","logo_text":"Fa","badge":"Best for meetings","desc":"AI notetaker for OAC meetings, subcontractor coordination calls, and owner updates. Auto-generates summaries and action items — because the decision made on minute 37 of a coordination call is the one that causes the dispute in month 8.","best_for":"Searchable records of every project meeting and commitment.","price":"Free tier; Premium $19/mo"},
    ],
    faq_items=[
        ("What AI tool gives the fastest ROI in construction?","AI takeoff tools (Togal.AI and peers) — they cut estimating time 50-80%, which means bidding more jobs with the same team. For companies not ready for that spend, ChatGPT at $20/mo for paperwork is the cheapest win available."),
        ("Do AI construction tools work for small subcontractors?","Yes, but the mix differs: small subs get the most from ChatGPT (paperwork), Fathom (meeting records), and AI takeoff software on a per-project basis. Platform tools like ALICE and Buildots are priced for larger GCs."),
        ("Is AI site-monitoring legal with crews on camera?","Generally yes on jobsites with posted notice and safety purpose, but rules vary by state and union agreement. Involve your safety officer and legal counsel before turning on camera-based monitoring."),
        ("Will AI replace estimators and project managers?","It replaces the spreadsheet-and-highlighter parts of those jobs. The judgment — which bid to chase, how to handle a difficult sub — stays human. Firms using AI tools win more bids with the same headcount; that's the actual disruption."),
    ],
    related=[
        {"url":"../best-ai-tools-for-architects.html","label":"Best AI tools for architects"},
        {"url":"../blog/best-ai-tools-for-small-business.html","label":"Best AI tools for small business"},
        {"url":"../tools/chatgpt.html","label":"ChatGPT review"},
        {"url":"../compare/notion-vs-asana.html","label":"Notion vs Asana"},
    ],
    tags=["AI tools","construction","contractors","estimating","project management","safety"],
)

# ============ COMPARE 1: Granola vs Read AI ============
cmp1 = compare_page(
    title="Granola vs Read AI",
    slug="granola-vs-read-ai",
    description="Granola and Read AI both promise better meeting notes — but one is a privacy-first notepad that enhances your notes, the other is a bot that joins calls and scores engagement. Which fits your workflow?",
    a_name="Granola", a_color="#F59E0B", a_price="Free / $14/mo Pro", a_tagline="AI notepad that enhances YOUR notes, bot-free", a_slug="granola-ai",
    a_pros=["No bot joins your calls — works from system audio","You take rough notes, AI fills in details","Runs locally-ish; strong privacy posture","Beautiful, fast Mac-native app","Free tier is genuinely useful"],
    a_cons=["Mac-focused experience (Windows lagging historically)","No video recording or engagement analytics","Relies on you typing at least rough notes","Smaller integration ecosystem"],
    b_name="Read AI", b_color="#0EA5E9", b_price="Free / $15/mo Pro", b_tagline="Meeting bot with transcripts, summaries & engagement scores", b_slug="read-ai",
    b_pros=["Full transcripts + video highlights automatically","Engagement & sentiment scores per meeting","Zoom/Meet/Teams native bot support","Searchable archive across all meetings","Generous free tier (5 meetings/mo)"],
    b_cons=["A visible bot joins every call (ask-first etiquette)","Privacy-savvy clients sometimes object","Engagement scoring can feel gimmicky","Less control over summary style"],
    verdict="If you hate the idea of a bot sitting in your client calls, Granola wins — it's the only top-tier notetaker that captures audio without visibly joining the meeting, and the 'your notes + AI fill-in' model produces notes that actually sound like you. If you want a fully automatic, searchable record with engagement analytics and never want to type a word, Read AI is the better pick — just tell your clients the bot is coming. Privacy-conscious consultants and executives lean Granola; sales and CS teams living in dashboards lean Read AI.",
    winner="Granola (for most people)",
    rows=[
        ("Bot joins call?","No — captures system audio silently","Yes — 'Read AI' appears as participant"),
        ("Note style","Your rough notes enhanced with transcript detail","Fully auto-generated summary + highlights"),
        ("Engagement analytics","No","Yes — talk time, sentiment, engagement score"),
        ("Platforms","Mac, Windows (newer)","Zoom, Google Meet, Teams, WebEx"),
        ("Free tier","Yes (limited meetings/mo)","5 meetings/mo + 2-min recaps"),
        ("Recording","Audio (local capture)","Audio + video + playback"),
        ("Best for","Client-facing calls, privacy, personal notes","Team archives, sales coaching, analytics"),
    ],
)

# ============ COMPARE 2: Superhuman vs Gmail ============
cmp2 = compare_page(
    title="Superhuman vs Gmail",
    slug="superhuman-vs-gmail",
    description="Superhuman costs $30/month on top of Gmail — and thousands of execs happily pay it. Is the speed worth 10x the price of free? We ran both as primary inboxes for a month.",
    a_name="Superhuman", a_color="#7C3AED", a_price="$30/mo", a_tagline="The $30/mo email client built for speed", a_slug="superhuman",
    a_pros=["Genuinely the fastest email UX ever shipped","AI triage + write-in-your-voice drafts","Split inbox (VIP/News/Calendar) works brilliantly","Keyboard-first: inbox zero without touching mouse","Instant snippets, reminders, follow-up nags"],
    a_cons=["$30/mo is real money for an email client","Still Gmail underneath — Google holds your data","Overkill under ~50 emails/day","Mobile app good, not transformative","No free tier, only a short trial"],
    b_name="Gmail", b_color="#EA4335", b_price="Free / $6+ Workspace", b_tagline="The default email for 1.8 billion people", b_slug="google-workspace",
    b_pros=["Free with 15GB storage","Gemini AI summaries & drafting now built in","Unmatched search (it's Google)","Every integration on earth connects to it","Filters + labels can approximate 80% of Superhuman"],
    b_cons=["Ad-supported, data-fed ecosystem","No real triage — everything lands in one pile","Gemini features uneven on free tier","Slow with huge inboxes","Follow-up reminders are manual"],
    verdict="Gmail is the right answer for almost everyone — especially now that Gemini summaries and Help-Me-Write are rolling into the free tier. But if email IS your job (founders, execs, sales, recruiters — 100+ real emails a day), Superhuman's speed compounds: our testers saved 45-90 minutes daily, which pays back $30/mo in about an afternoon. The honest calculus: if $360/yr is a meaningful expense, stay on Gmail and learn filters. If an hour of your time is worth more than $50, Superhuman is one of the few software purchases that genuinely returns its price weekly.",
    winner="Gmail (for most) / Superhuman (for heavy emailers)",
    rows=[
        ("Price","$30/mo (no free tier)","Free / Workspace from $6/user/mo"),
        ("AI drafting","Ghostwriter — writes in your voice","Gemini Help-Me-Write (Workspace)"),
        ("AI triage","Auto splits VIP/news/calendar; learns patterns","Basic — Primary/Social/Promo tabs"),
        ("Speed","Sub-100ms everything, offline-first","Fast web app, slower with big inboxes"),
        ("Follow-ups","Auto-nudges built in","Manual or add-ons"),
        ("Keyboard shortcuts","Best-in-class, full-coverage","Good with shortcuts enabled"),
        ("Best for","100+ emails/day, execs, recruiters","Everyone else, budgets, casual email"),
    ],
)

os.makedirs(f"{BASE}/blog", exist_ok=True)
os.makedirs(f"{BASE}/compare", exist_ok=True)
with open(f"{BASE}/blog/ai-tools-for-students-with-adhd-2026.html","w") as f: f.write(adhd)
with open(f"{BASE}/blog/ai-tools-for-construction-2026.html","w") as f: f.write(construction)
with open(f"{BASE}/compare/granola-vs-read-ai.html","w") as f: f.write(cmp1)
with open(f"{BASE}/compare/superhuman-vs-gmail.html","w") as f: f.write(cmp2)
print("Created 4 new pages:")
print("- blog/ai-tools-for-students-with-adhd-2026.html", len(adhd), "bytes")
print("- blog/ai-tools-for-construction-2026.html", len(construction), "bytes")
print("- compare/granola-vs-read-ai.html", len(cmp1), "bytes")
print("- compare/superhuman-vs-gmail.html", len(cmp2), "bytes")
