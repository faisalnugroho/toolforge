/* ToolForge v3 - Professional Animation & 3D System */

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

// ===== Loading state (hide after first paint) =====
window.addEventListener('load', () => {
  const loader = document.querySelector('.page-loading');
  if (loader) {
    setTimeout(() => loader.classList.add('hidden'), 100);
    setTimeout(() => loader.remove(), 600);
  }
});

// ===== Scroll Reveal =====
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal, .reveal-fade, .reveal-scale, .reveal-left, .reveal-right, .stagger-children').forEach(el => {
  revealObserver.observe(el);
});

// ===== 3D Tilt on cards =====
document.querySelectorAll('.tilt-3d').forEach(card => {
  let rect;
  function updateRect() { rect = card.getBoundingClientRect(); }
  updateRect();
  window.addEventListener('resize', updateRect);
  window.addEventListener('scroll', updateRect, { passive: true });
  
  card.addEventListener('mousemove', (e) => {
    if (!rect) return;
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const xPct = (x / rect.width - 0.5) * 2;
    const yPct = (y / rect.height - 0.5) * 2;
    card.style.transform = `perspective(1200px) rotateY(${xPct * 4}deg) rotateX(${-yPct * 4}deg) translateZ(10px)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
});

// ===== Magnetic buttons =====
document.querySelectorAll('.magnetic').forEach(btn => {
  let rect;
  btn.addEventListener('mousemove', (e) => {
    if (!rect) rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
    rect = null;
  });
});

// ===== Back to Top =====
const backToTop = document.createElement('button');
backToTop.className = 'back-to-top';
backToTop.setAttribute('aria-label', 'Back to top');
backToTop.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>';
document.body.appendChild(backToTop);

window.addEventListener('scroll', () => {
  if (window.scrollY > 600) backToTop.classList.add('visible');
  else backToTop.classList.remove('visible');
}, { passive: true });

backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ===== Reading Progress =====
const article = document.querySelector('article, .article-content, main');
if (article) {
  const progress = document.createElement('div');
  progress.className = 'reading-progress';
  document.body.appendChild(progress);
  window.addEventListener('scroll', () => {
    const r = article.getBoundingClientRect();
    const total = article.offsetHeight;
    const scrolled = Math.max(0, -r.top);
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
      <div class="cookie-banner-text">We use cookies for analytics (Plausible) and preferences. <a href="privacy.html">Privacy policy</a>.</div>
    </div>
    <div class="cookie-banner-actions">
      <button class="primary">Accept</button>
      <button data-action="reject">Reject</button>
    </div>
  `;
  document.body.appendChild(banner);
  setTimeout(() => banner.classList.add('show'), 500);
  banner.querySelector('.primary').addEventListener('click', () => { localStorage.setItem('cookie-consent', 'accepted'); banner.classList.remove('show'); setTimeout(() => banner.remove(), 400); });
  banner.querySelector('[data-action="reject"]').addEventListener('click', () => { localStorage.setItem('cookie-consent', 'rejected'); banner.classList.remove('show'); setTimeout(() => banner.remove(), 400); });
}
showCookieBanner();

// ===== FAQ Accordion =====
document.querySelectorAll('.faq-item').forEach(item => {
  const question = item.querySelector('.faq-question');
  if (question) {
    question.addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      item.parentElement.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  }
});

// ===== Category Filter =====
const filterButtons = document.querySelectorAll('.filter-btn');
const toolCards = document.querySelectorAll('[data-category]');

filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const filter = btn.dataset.filter;
    filterButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    toolCards.forEach((card, i) => {
      const shouldShow = filter === 'all' || card.dataset.category === filter;
      if (shouldShow) {
        card.style.display = '';
        card.style.opacity = '0';
        card.style.transform = 'translateY(10px)';
        setTimeout(() => {
          card.style.transition = 'opacity 0.4s, transform 0.4s';
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        }, i * 20);
      } else {
        card.style.display = 'none';
      }
    });
  });
});

const urlCat = new URLSearchParams(window.location.search).get('cat');
if (urlCat) {
  const targetBtn = document.querySelector(`.filter-btn[data-filter="${urlCat}"]`);
  if (targetBtn) targetBtn.click();
}

// ===== Newsletter =====
const newsletterForm = document.getElementById('newsletter-form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', async (e) => {
    const submitBtn = newsletterForm.querySelector('button[type="submit"]');
    const original = submitBtn.textContent;
    submitBtn.textContent = 'Subscribing...';
    submitBtn.disabled = true;
    setTimeout(() => {
      submitBtn.textContent = original;
      submitBtn.disabled = false;
    }, 2000);
  });
}

// ===== Search highlight =====
const searchQuery = new URLSearchParams(window.location.search).get('q');
if (searchQuery && document.querySelector('.search-highlight')) {
  document.querySelectorAll('.search-highlight').forEach(el => {
    const text = el.textContent;
    const re = new RegExp(`(${searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    el.innerHTML = text.replace(re, '<mark style="background: #fef3c7; color: #92400e; padding: 0 2px; border-radius: 2px;">$1</mark>');
  });
}

// ===== Lazy load images =====
if ('IntersectionObserver' in window) {
  const imgObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.classList.add('loaded');
          imgObserver.unobserve(img);
        }
      }
    });
  });
  document.querySelectorAll('img.lazy').forEach(img => imgObserver.observe(img));
}

// ===== Year =====
document.querySelectorAll('.current-year').forEach(el => el.textContent = new Date().getFullYear());

// ===== Parallax on hero orbs (mouse-based) =====
const heroScene = document.querySelector('.hero-3d-scene');
if (heroScene) {
  let mouseX = 0, mouseY = 0;
  let targetX = 0, targetY = 0;
  
  document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });
  
  function animateOrbs() {
    targetX += (mouseX - targetX) * 0.05;
    targetY += (mouseY - targetY) * 0.05;
    heroScene.querySelectorAll('.orb').forEach((orb, i) => {
      const speed = (i + 1) * 8;
      orb.style.transform = `translate(${targetX * speed}px, ${targetY * speed}px)`;
    });
    requestAnimationFrame(animateOrbs);
  }
  animateOrbs();
}

// ===== Lightweight 3D Hero Scene (CSS 3D + canvas particles) =====
const hero3d = document.querySelector('[data-3d-hero]');
if (hero3d) {
  // Create a 3D canvas scene with floating particles
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position: absolute; inset: 0; pointer-events: none; width: 100%; height: 100%; z-index: 0;';
  hero3d.appendChild(canvas);
  
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animFrame;
  
  function resize() {
    canvas.width = hero3d.offsetWidth;
    canvas.height = hero3d.offsetHeight;
    initParticles();
  }
  
  function initParticles() {
    particles = [];
    const count = Math.min(60, Math.floor((canvas.width * canvas.height) / 25000));
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 2 + 0.5,
        alpha: Math.random() * 0.5 + 0.2
      });
    }
  }
  
  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const color = getComputedStyle(root).getPropertyValue('--accent').trim() || '#5e6ad2';
    
    particles.forEach((p, i) => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;
      
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.globalAlpha = p.alpha;
      ctx.fill();
      
      // Connect nearby
      for (let j = i + 1; j < particles.length; j++) {
        const dx = p.x - particles[j].x;
        const dy = p.y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = color;
          ctx.globalAlpha = (1 - dist / 120) * 0.15;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    });
    ctx.globalAlpha = 1;
    animFrame = requestAnimationFrame(drawParticles);
  }
  
  resize();
  drawParticles();
  window.addEventListener('resize', resize);
  
  // Pause when not visible
  const visObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        if (!animFrame) drawParticles();
      } else {
        cancelAnimationFrame(animFrame);
        animFrame = null;
      }
    });
  });
  visObserver.observe(hero3d);
}

// ===== Animated counter for stats =====
function animateCounter(el) {
  const target = parseFloat(el.dataset.count || el.textContent);
  const duration = 1500;
  const start = performance.now();
  const isFloat = target % 1 !== 0;
  
  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(1, elapsed / duration);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = target * eased;
    el.textContent = isFloat ? current.toFixed(2) : Math.floor(current).toLocaleString();
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

const statObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      if (!el.dataset.count) {
        // Extract number from text
        const match = el.textContent.match(/[\d.]+/);
        if (match) el.dataset.count = match[0];
      }
      animateCounter(el);
      statObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-value').forEach(el => statObserver.observe(el));

// ===== Service worker =====
if ('serviceWorker' in navigator && location.protocol === 'https:') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}
