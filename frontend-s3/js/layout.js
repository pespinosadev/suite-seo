/* ==========================================================
   layout.js — Shared sidebar + header for Suite SEO
   Usage: await initLayout('pagename')
   Provides: window.logout, window.layoutUser, window.layoutDomains
   ========================================================== */
(function () {
  const _API = 'https://vps-a351882a.vps.ovh.net';

  const _ICONS = {
    dashboard: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    topics:    '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    users:     '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    domains:   '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
  };

  function _e(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function _buildSidebar(page) {
    const items = [
      { id: 'dashboard', label: 'Dashboard',    href: 'dashboard.html' },
      { id: 'topics',    label: 'Temas del día', href: 'topics.html' },
      { id: 'users',     label: 'Usuarios',      href: 'users.html',   admin: true },
      { id: 'domains',   label: 'Dominios',      href: 'domains.html', admin: true },
    ];
    const nav = items.map(item => `
      <a href="${item.href}" class="seo-nav-item${page === item.id ? ' active' : ''}"
         ${item.admin ? `id="nav-${item.id}" style="display:none"` : ''}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke-width="2">${_ICONS[item.id]}</svg>
        <span>${item.label}</span>
      </a>`).join('');
    return `
      <div class="seo-brand">
        <span class="seo-brand-text">
          <span class="brand-top">Suite</span><span class="brand-bot">SEO</span>
        </span>
      </div>
      <nav class="seo-nav">
        <div class="seo-nav-label">Principal</div>
        ${nav}
      </nav>`;
  }

  function _buildHeader() {
    return `
    <div class="seo-header-left">
      <button class="seo-toggle" id="sidebar-toggle" title="Colapsar menú">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>
      <div style="position:relative">
        <button class="seo-modules-btn" id="modules-toggle" title="Dominios">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
          Todos los dominios
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke-width="2.5">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>
        <div class="seo-modules-dropdown" id="modules-menu">
          <a href="domains.html">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
            Todos los dominios
          </a>
          <div id="modules-domain-list"></div>
        </div>
      </div>
    </div>
    <div class="seo-header-right">
      <button class="seo-action" title="Pantalla completa" id="fullscreen-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke-width="2" id="fs-icon-expand">
          <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
        </svg>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke-width="2" id="fs-icon-compress" style="display:none">
          <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/>
        </svg>
      </button>
      <button class="seo-action" title="Modo oscuro" id="theme-toggle">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke-width="2" id="icon-moon">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke-width="2" id="icon-sun" style="display:none">
          <circle cx="12" cy="12" r="5"/>
          <line x1="12" y1="1" x2="12" y2="3"/>
          <line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/>
          <line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
      </button>
      <div class="seo-action" style="width:auto;padding:0 .5rem;pointer-events:none">
        <span class="seo-clock" id="clock">--:--:--</span>
      </div>
      <button class="seo-action" title="Notificaciones" onclick="alert('Sin notificaciones')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke-width="2">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
        </svg>
      </button>
      <div class="seo-sep"></div>
      <div class="seo-user" id="user-trigger">
        <div class="seo-avatar" id="user-avatar">--</div>
        <div class="seo-user-meta">
          <div class="seo-user-name" id="user-name">—</div>
          <div class="seo-user-role" id="user-role">—</div>
        </div>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke-width="2.5"
             style="color:var(--text-muted);stroke:currentColor;margin-left:.1rem">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
        <div class="seo-user-dropdown" id="user-menu">
          <div class="seo-user-dropdown-header">
            <div class="seo-avatar" id="dd-avatar">--</div>
            <div class="name" id="dd-name">—</div>
            <div class="email" id="dd-email">—</div>
          </div>
          <div class="divider"></div>
          <a href="account.html" style="font-weight:600">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2">
              <circle cx="12" cy="8" r="4"/>
              <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
            </svg>
            Mi cuenta
          </a>
          <div class="divider"></div>
          <a href="#" onclick="event.preventDefault();logout()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Cerrar sesión
          </a>
        </div>
      </div>
    </div>`;
  }

  async function _loadHeaderDomains(token) {
    try {
      const res = await fetch(`${_API}/api/domains/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) return [];
      const domains = await res.json();
      window.layoutDomains = domains;
      if (!domains.length) return domains;
      const catLabels = {
        nacionales: 'Nacionales', regionales: 'Regionales',
        deportivos: 'Deportivos', verticales: 'Verticales', revistas: 'Revistas'
      };
      const grouped = {};
      domains.forEach(d => {
        if (!grouped[d.category.name]) grouped[d.category.name] = [];
        grouped[d.category.name].push(d);
      });
      const listEl = document.getElementById('modules-domain-list');
      if (listEl) listEl.innerHTML =
        `<div class="divider" style="margin:.4rem 0"></div>` +
        Object.entries(grouped).map(([cat, doms]) => `
          <div style="padding:.4rem 1rem .15rem;font-size:.65rem;font-weight:700;
            text-transform:uppercase;letter-spacing:.07em;color:var(--text-nav-label)">
            ${_e(catLabels[cat] || cat)}
          </div>
          ${doms.map(d => `
            <a href="${_e(d.full_url)}" target="_blank" rel="noopener">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="2" y1="12" x2="22" y2="12"/>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
              </svg>
              ${_e(d.domain)}
            </a>`).join('')}`).join('');
      return domains;
    } catch (e) { return []; }
  }

  /* ── Public API ── */

  window.logout = function () {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
  };

  window.initLayout = async function (page) {
    const token = localStorage.getItem('token');
    if (!token) { window.location.href = 'login.html'; return null; }

    /* Inject sidebar */
    const sidebar = document.querySelector('aside.seo-sidebar');
    if (sidebar) sidebar.innerHTML = _buildSidebar(page);

    /* Inject header */
    const header = document.querySelector('header.seo-header');
    if (header) header.innerHTML = _buildHeader();

    /* Dark mode */
    if ((localStorage.getItem('seo-theme') || 'light') === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      document.getElementById('icon-moon').style.display = 'none';
      document.getElementById('icon-sun').style.display = '';
    }
    document.getElementById('theme-toggle').addEventListener('click', () => {
      const dark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (dark) {
        document.documentElement.removeAttribute('data-theme');
        document.getElementById('icon-moon').style.display = '';
        document.getElementById('icon-sun').style.display = 'none';
        localStorage.setItem('seo-theme', 'light');
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('icon-moon').style.display = 'none';
        document.getElementById('icon-sun').style.display = '';
        localStorage.setItem('seo-theme', 'dark');
      }
    });

    /* Sidebar toggle */
    if (localStorage.getItem('seo-minimenu')) document.body.classList.add('minimenu');
    document.getElementById('sidebar-toggle').addEventListener('click', () => {
      document.body.classList.toggle('minimenu');
      localStorage.setItem('seo-minimenu', document.body.classList.contains('minimenu') ? '1' : '');
    });

    /* Fullscreen */
    document.getElementById('fullscreen-btn').addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        document.getElementById('fs-icon-expand').style.display = 'none';
        document.getElementById('fs-icon-compress').style.display = '';
      } else {
        document.exitFullscreen();
        document.getElementById('fs-icon-expand').style.display = '';
        document.getElementById('fs-icon-compress').style.display = 'none';
      }
    });

    /* Clock */
    function _tick() {
      const el = document.getElementById('clock');
      if (el) el.textContent = new Date().toLocaleTimeString('es-ES',
        { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }
    _tick(); setInterval(_tick, 1000);

    /* Dropdowns */
    const modulesToggle = document.getElementById('modules-toggle');
    const modulesMenu   = document.getElementById('modules-menu');
    const userTrigger   = document.getElementById('user-trigger');
    const userMenu      = document.getElementById('user-menu');
    modulesToggle.addEventListener('click', e => {
      e.stopPropagation();
      modulesMenu.classList.toggle('show');
      userMenu.classList.remove('show');
    });
    userTrigger.addEventListener('click', e => {
      e.stopPropagation();
      userMenu.classList.toggle('show');
      modulesMenu.classList.remove('show');
    });
    document.addEventListener('click', () => {
      modulesMenu.classList.remove('show');
      userMenu.classList.remove('show');
    });

    /* Load user */
    try {
      const res = await fetch(`${_API}/api/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.status === 401) { window.logout(); return null; }
      const user = await res.json();
      const displayName = [user.first_name, user.last_name].filter(Boolean).join(' ')
                          || user.email.split('@')[0];
      const initials = displayName.slice(0, 2).toUpperCase();
      [document.getElementById('user-avatar'), document.getElementById('dd-avatar')].forEach(el => {
        if (!el) return;
        if (user.avatar) {
          el.style.backgroundImage = `url(${user.avatar})`;
          el.style.backgroundSize  = 'cover';
          el.style.fontSize        = '0';
          el.textContent           = '';
        } else {
          el.textContent = initials;
        }
      });
      document.getElementById('user-name').textContent = displayName;
      document.getElementById('user-role').textContent = user.role.name;
      document.getElementById('dd-name').textContent   = displayName;
      document.getElementById('dd-email').textContent  = user.email;
      if (user.role.name === 'admin') {
        ['nav-users', 'nav-domains'].forEach(id => {
          const el = document.getElementById(id);
          if (el) el.style.display = '';
        });
      }
      window.layoutUser = user;
      await _loadHeaderDomains(token);
      return user;
    } catch (e) {
      console.error('initLayout error:', e);
      return null;
    }
  };
})();
