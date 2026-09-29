// ================================================
// DIMSONSGFX — site.js
// Theme, mobile navigation, search, lazy loading,
// go-to-top button, dynamic JSON loader
// ================================================

'use strict';

// ── Theme ──────────────────────────────────────
const THEME_KEY = 'dimsonsgfx-theme';

function getTheme() {
  return localStorage.getItem(THEME_KEY) ||
    (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
}

function applyTheme(theme) {
  document.body.setAttribute('data-theme', theme);
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.getElementById('themeToggle');
  if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  localStorage.setItem(THEME_KEY, theme);
}

// Apply before render to prevent flash
(function() {
  var t = localStorage.getItem('dimsonsgfx-theme') ||
    (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  document.documentElement.setAttribute('data-theme', t);
})();

// ── Mobile side panel ──────────────────────────
function initMobileMenu() {
  const btnMenu   = document.querySelector('.btn-menu');
  const sidePanel = document.querySelector('.side-panel');
  const overlay   = document.querySelector('.close-overlay');
  const btnClose  = document.querySelector('.btn-close');

  if (!btnMenu || !sidePanel) return;

  function openPanel() {
    sidePanel.classList.add('active');
    if (overlay) overlay.classList.add('active');
    if (btnClose) btnClose.classList.add('active');
    document.body.classList.add('opened-menu');
  }
  function closePanel() {
    sidePanel.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    if (btnClose) btnClose.classList.remove('active');
    document.body.classList.remove('opened-menu');
  }

  btnMenu.addEventListener('click', openPanel);
  if (overlay) overlay.addEventListener('click', closePanel);
  if (btnClose) btnClose.addEventListener('click', closePanel);
}

// ── Submenu hover ──────────────────────────────
function initSubmenus() {
  document.querySelectorAll('.submenu > a').forEach(a => {
    a.addEventListener('click', function(e) {
      if (window.innerWidth <= 1220) {
        e.preventDefault();
        const li = this.parentElement;
        li.classList.toggle('open');
      }
    });
  });
}

// ── Search overlay ────────────────────────────
function initSearch() {
  const searchBtn   = document.querySelector('.js-search, .search-btn');
  const searchWrap  = document.querySelector('.search-wrap');
  const searchClose = document.querySelector('.search-close');
  const searchInput = document.querySelector('#story');

  if (!searchBtn || !searchWrap) return;

  searchBtn.addEventListener('click', () => {
    searchWrap.classList.toggle('visible');
    if (searchWrap.classList.contains('visible') && searchInput) {
      searchInput.focus();
    }
  });

  if (searchClose) {
    searchClose.addEventListener('click', () => {
      searchWrap.classList.remove('visible');
    });
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') searchWrap.classList.remove('visible');
  });

  const form = document.getElementById('quicksearch');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const query = (searchInput?.value || '').trim();
      if (!query) return;
      window.location.href = `/search/?q=${encodeURIComponent(query)}`;
    });
  }
}

// ── Go-to-top ─────────────────────────────────
function initGoTop() {
  const btn = document.getElementById('gotop');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.style.display = window.scrollY > 400 ? 'block' : 'none';
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// ── Lazy Load ─────────────────────────────────
function initLazyLoad() {
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) img.src = img.dataset.src;
          img.classList.add('loaded');
          obs.unobserve(img);
        }
      });
    }, { rootMargin: '300px' });
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
      img.addEventListener('load', () => img.classList.add('loaded'));
      if (img.complete) img.classList.add('loaded');
      obs.observe(img);
    });
  } else {
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
      img.classList.add('loaded');
    });
  }
}

// ── Active nav ────────────────────────────────
function markActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.header-menu a, .side-menu a').forEach(a => {
    const href = a.getAttribute('href');
    if (!href) return;
    if (href !== '/' && path.startsWith(href)) {
      a.classList.add('active');
      a.closest('li')?.classList.add('active');
    } else if (href === '/' && (path === '/' || path === '/index.html')) {
      a.classList.add('active');
      a.closest('li')?.classList.add('active');
    }
  });
}

// ── Data loader: works from JSON ───────────────
window.SITE = window.SITE || {};

async function loadWorks() {
  if (window.SITE.works) return window.SITE.works;
  try {
    const r = await fetch('/data/works.json');
    window.SITE.works = await r.json();
    return window.SITE.works;
  } catch(e) {
    console.error('Failed to load works:', e);
    return [];
  }
}

async function loadCategories() {
  if (window.SITE.categories) return window.SITE.categories;
  try {
    const r = await fetch('/data/categories.json');
    window.SITE.categories = await r.json();
    return window.SITE.categories;
  } catch(e) {
    return [];
  }
}

// ── Render short card (no views icon, in English) ──
function renderShortItem(work) {
  const dateStr = formatDate(work.date);
  const imgHtml = work.thumb
    ? `<img src="${esc(work.thumb)}" alt="${esc(work.title)}" loading="lazy" width="400" height="280">`
    : `<div class="no-image-placeholder"><span class="emoji">${work.emoji||'🎨'}</span></div>`;

  return `
<article class="short-item" itemscope itemtype="https://schema.org/CreativeWork">
  <a class="short-link" href="/works/${esc(work.slug)}/">
    <div class="short-img img-resp img-fit">
      ${imgHtml}
      <div class="short-category">${esc(work.categoryLabel||work.category)}</div>
    </div>
    <div class="short-title title anim" itemprop="name">${esc(work.title)}</div>
  </a>
  <div class="short-meta fx-row fx-middle icon-left">
    <div class="short-meta-item fx-1 nowrap"><span class="far fa-calendar-alt" aria-hidden="true"></span><time datetime="${esc(work.date||'')}">${dateStr}</time></div>
  </div>
  <div class="short-text" itemprop="description">${esc((work.description||'').substring(0,140))}${work.description&&work.description.length>140?'…':''}</div>
  <div class="short-bottom fx-row fx-middle">
    <div class="fx-1"></div>
    <a class="short-btn btn" href="/works/${esc(work.slug)}/">View Details</a>
  </div>
</article>`;
}

// ── Helpers ────────────────────────────────────
function formatDate(d) {
  if (!d) return '';
  try {
    return new Date(d).toLocaleDateString('en-US', {
      day: 'numeric', month: 'long', year: 'numeric'
    });
  } catch { return d; }
}

function esc(s) {
  return String(s||'')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Init ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  applyTheme(getTheme());
  initMobileMenu();
  initSubmenus();
  initSearch();
  initGoTop();
  initLazyLoad();
  markActiveNav();

  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
    });
  }
});
