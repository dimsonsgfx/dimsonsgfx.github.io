// ================================================
// DIMSONSGFX — site.js
// Статический аналог libs.js из шаблона DLE
// Тема, мобильное меню, поиск, ленивая загрузка,
// кнопка наверх, загрузка данных из JSON
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
  // Already handled by CSS :hover, but add mobile tap
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

  // JS search (client-side, searches works.json)
  const form = document.getElementById('quicksearch');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const query = (searchInput?.value || '').trim().toLowerCase();
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
    // Fallback
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

// ── Render short card (like shortstory.tpl) ────
function renderShortItem(work) {
  const dateStr = formatDate(work.date);
  const imgHtml = work.thumb
    ? `<img src="${esc(work.thumb)}" alt="${esc(work.title)}" loading="lazy" width="400" height="280">`
    : `<div class="no-image-placeholder"><span class="emoji">${work.emoji||'🎨'}</span></div>`;

  return `
<div class="short-item">
  <a class="short-link" href="/works/${esc(work.slug)}/">
    <div class="short-img img-resp img-fit">
      ${imgHtml}
      <div class="short-category">${esc(work.categoryLabel||work.category)}</div>
    </div>
    <div class="short-title title anim">${esc(work.title)}</div>
  </a>
  <div class="short-meta fx-row fx-middle icon-left">
    <div class="short-meta-item fx-1 nowrap"><span class="far fa-calendar-alt"></span>${dateStr}</div>
    <div class="short-meta-item"><span class="far fa-eye"></span>${work.views||0}</div>
  </div>
  <div class="short-text">${esc((work.description||'').substring(0,140))}${work.description&&work.description.length>140?'…':''}</div>
  <div class="short-bottom fx-row fx-middle icon-left">
    <div class="fx-1"></div>
    <a class="short-btn btn" href="/works/${esc(work.slug)}/">Подробнее</a>
  </div>
</div>`;
}

// ── Render top-item (sidebar) ──────────────────
function renderTopItem(work) {
  const imgHtml = work.thumb
    ? `<img src="${esc(work.thumb)}" alt="${esc(work.title)}" loading="lazy" width="60" height="60">`
    : `<div style="width:60px;height:60px;background:#e8eaed;display:flex;align-items:center;justify-content:center;font-size:1.5rem;">${work.emoji||'🎨'}</div>`;
  return `
<a class="top-item fx-row" href="/works/${esc(work.slug)}/">
  <div class="top-item-img img-box">${imgHtml}</div>
  <div class="top-item-text fx-1">${esc(work.title)}</div>
</a>`;
}

// ── Render thumb item (related/editor's pick) ──
function renderThumbItem(work) {
  const imgHtml = work.thumb
    ? `<img src="${esc(work.thumb)}" alt="${esc(work.title)}" loading="lazy" width="200" height="120">`
    : `<div style="height:120px;background:#e8eaed;display:flex;align-items:center;justify-content:center;font-size:2rem;">${work.emoji||'🎨'}</div>`;
  return `
<a class="thumb-item" href="/works/${esc(work.slug)}/">
  <div class="thumb-item-img img-wide">${imgHtml}</div>
  <div class="thumb-item-cat">${esc(work.categoryLabel||work.category)}</div>
  <div class="thumb-item-title">${esc(work.title)}</div>
</a>`;
}

// ── Helpers ────────────────────────────────────
function formatDate(d) {
  if (!d) return '';
  try {
    return new Date(d).toLocaleDateString('ru-RU', {
      day: 'numeric', month: 'long', year: 'numeric'
    });
  } catch { return d; }
}

function esc(s) {
  return String(s||'')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function pluralRu(n, f1, f2, f5) {
  n = Math.abs(n) % 100;
  const n1 = n % 10;
  if (n > 10 && n < 20) return f5;
  if (n1 > 1 && n1 < 5) return f2;
  if (n1 === 1) return f1;
  return f5;
}

// ── Populate sidebars ─────────────────────────
async function populateSidebars(opts = {}) {
  const works = await loadWorks();
  if (!works.length) return;

  const sorted = [...works].sort((a, b) => new Date(b.date) - new Date(a.date));
  const catFilter = opts.category || null;

  // Editor's pick (Выбор редакции) — первые 3
  const editorPick = document.getElementById('sidebar-editor-pick');
  if (editorPick) {
    editorPick.innerHTML = sorted.slice(0, 3).map(renderThumbItem).join('');
  }

  // Top week (Топ за неделю / Популярное) — первые 5-6
  document.querySelectorAll('[data-sidebar="top"]').forEach(el => {
    const limit = parseInt(el.dataset.limit || '6');
    el.innerHTML = sorted.slice(0, limit).map(renderTopItem).join('');
  });

  // Recommend (Рекомендуем)
  const recommend = document.getElementById('sidebar-recommend');
  if (recommend) {
    const recs = catFilter
      ? works.filter(w => w.category === catFilter).slice(0, 5)
      : sorted.slice(3, 8);
    recommend.innerHTML = recs.map(renderThumbItem).join('');
  }

  initLazyLoad();
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

  populateSidebars();

  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
    });
  }
});
