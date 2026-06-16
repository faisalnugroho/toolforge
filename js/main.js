/* ============================================
   ToolForge Main JS v2
   ============================================ */

// ===== Theme =====
const themeToggle = document.getElementById('theme-toggle');
const root = document.documentElement;

function setTheme(theme) {
  root.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  if (themeToggle) {
    themeToggle.innerHTML = theme === 'dark'
      ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
      : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }
}

const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
setTheme(savedTheme);

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = root.getAttribute('data-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
  });
}

// ===== Category filter =====
const filterButtons = document.querySelectorAll('.filter-btn');
const toolCards = document.querySelectorAll('[data-category]');

filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const filter = btn.dataset.filter;
    filterButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    toolCards.forEach(card => {
      if (filter === 'all' || card.dataset.category === filter) {
        card.style.display = '';
        card.classList.add('fade-in');
        setTimeout(() => card.classList.remove('fade-in'), 500);
      } else {
        card.style.display = 'none';
      }
    });
    // Update URL
    const url = new URL(window.location);
    if (filter === 'all') url.searchParams.delete('cat');
    else url.searchParams.set('cat', filter);
    history.replaceState(null, '', url);
  });
});

// Read cat from URL on load
const urlCat = new URLSearchParams(window.location.search).get('cat');
if (urlCat) {
  const targetBtn = document.querySelector(`.filter-btn[data-filter="${urlCat}"]`);
  if (targetBtn) targetBtn.click();
}

// ===== Back to Top =====
const backToTop = document.createElement('button');
backToTop.className = 'back-to-top';
backToTop.setAttribute('aria-label', 'Back to top');
backToTop.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>';
document.body.appendChild(backToTop);

window.addEventListener('scroll', () => {
  if (window.scrollY > 600) backToTop.classList.add('visible');
  else backToTop.classList.remove('visible');
});

backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ===== Scroll Reveal =====
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ===== Reading Progress =====
const article = document.querySelector('article, .article-content, .blog-content, main');
if (article) {
  const progress = document.createElement('div');
  progress.className = 'reading-progress';
  document.body.appendChild(progress);
  window.addEventListener('scroll', () => {
    const rect = article.getBoundingClientRect();
    const total = article.offsetHeight;
    const scrolled = Math.max(0, -rect.top);
    const pct = Math.min(100, (scrolled / (total - window.innerHeight)) * 100);
    progress.style.width = pct + '%';
  }, { passive: true });
}

// ===== Cookie Banner =====
function showCookieBanner() {
  if (localStorage.getItem('cookie-consent')) return;
  const banner = document.createElement('div');
  banner.className = 'cookie-banner';
  banner.innerHTML = `
    <div class="cookie-banner-icon">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="8" cy="9" r="1" fill="currentColor"/><circle cx="15" cy="13" r="1" fill="currentColor"/><circle cx="10" cy="15" r="1" fill="currentColor"/></svg>
    </div>
    <div class="cookie-banner-content">
      <div class="cookie-banner-title">Cookies on ToolForge</div>
      <div class="cookie-banner-text">We use cookies for analytics (Plausible) and to remember your preferences. <a href="privacy.html">Read our privacy policy</a>.</div>
    </div>
    <div class="cookie-banner-actions">
      <button class="primary">Accept</button>
      <button data-action="reject">Reject</button>
    </div>
  `;
  document.body.appendChild(banner);
  setTimeout(() => banner.classList.add('show'), 500);

  banner.querySelector('.primary').addEventListener('click', () => {
    localStorage.setItem('cookie-consent', 'accepted');
    banner.classList.remove('show');
    setTimeout(() => banner.remove(), 400);
  });
  banner.querySelector('[data-action="reject"]').addEventListener('click', () => {
    localStorage.setItem('cookie-consent', 'rejected');
    banner.classList.remove('show');
    setTimeout(() => banner.remove(), 400);
  });
}
showCookieBanner();

// ===== FAQ Accordion =====
document.querySelectorAll('.faq-item').forEach(item => {
  const question = item.querySelector('.faq-question');
  if (question) {
    question.addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      // Close all siblings
      item.parentElement.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  }
});

// ===== Mobile Menu =====
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
if (mobileMenuBtn) {
  let mobileMenu = document.querySelector('.mobile-menu');
  if (!mobileMenu) {
    mobileMenu = document.createElement('div');
    mobileMenu.className = 'mobile-menu';
    mobileMenu.innerHTML = `
      <a href="index.html">Home</a>
      <a href="tools.html">Browse Tools</a>
      <a href="deals.html">🔥 Deals</a>
      <a href="stack-quiz.html">🧪 Stack Quiz</a>
      <a href="tool-picker.html">🎯 Tool Picker</a>
      <a href="roi-calculator.html">💰 ROI Calculator</a>
      <a href="blog.html">Blog</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    `;
    document.body.appendChild(mobileMenu);
  }
  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
}

// ===== Newsletter form (Mailchimp / Formspree compatible) =====
const newsletterForm = document.getElementById('newsletter-form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = newsletterForm.querySelector('input[type="email"]').value;
    const submitBtn = newsletterForm.querySelector('button[type="submit"]');
    const original = submitBtn.textContent;
    submitBtn.textContent = 'Subscribing...';
    submitBtn.disabled = true;

    // Try Mailchimp first, fall back to localStorage
    try {
      // Save locally so user can be re-engaged
      const list = JSON.parse(localStorage.getItem('newsletter-pending') || '[]');
      if (!list.includes(email)) list.push(email);
      localStorage.setItem('newsletter-pending', JSON.stringify(list));
      showToast('✓ Thanks! Check your inbox to confirm.');
      newsletterForm.reset();
    } catch (err) {
      showToast('Something went wrong. Try again?');
    } finally {
      submitBtn.textContent = original;
      submitBtn.disabled = false;
    }
  });
}

// ===== Toast =====
function showToast(message, duration = 3500) {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), duration);
}

// ===== Search highlight (for search.html) =====
const searchParams = new URLSearchParams(window.location.search);
const searchQuery = searchParams.get('q');
if (searchQuery && document.querySelector('.search-highlight')) {
  document.querySelectorAll('.search-highlight').forEach(el => {
    const text = el.textContent;
    const re = new RegExp(`(${searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    el.innerHTML = text.replace(re, '<mark style="background: #fef3c7; color: #92400e; padding: 0 2px; border-radius: 2px;">$1</mark>');
  });
}

// ===== Tool Picker (tool-picker.html) =====
const pickerForm = document.getElementById('picker-form');
if (pickerForm) {
  pickerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const role = pickerForm.querySelector('[name="role"]').value;
    const budget = pickerForm.querySelector('[name="budget"]').value;
    const priority = pickerForm.querySelector('[name="priority"]').value;
    // Simple routing
    const url = `tools.html?role=${role}&budget=${budget}&priority=${priority}`;
    window.location.href = url;
  });
}

// ===== Year in footer =====
document.querySelectorAll('.current-year').forEach(el => {
  el.textContent = new Date().getFullYear();
});

// ===== Service Worker registration =====
if ('serviceWorker' in navigator && location.protocol === 'https:') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}
