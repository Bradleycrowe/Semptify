(() => {
  function $(sel, root=document){ return root.querySelector(sel); }
  function $all(sel, root=document){ return Array.from(root.querySelectorAll(sel)); }
  const meta = name => {
    const el = document.querySelector(`meta[name="${name}"]`);
    return el ? (el.getAttribute('content') || '') : '';
  };
  const STORAGE_KEY = 'semptify_help_panel_v2';
  const PAGE_KEY = location.pathname || 'root';
  function loadAll(){
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch { return {}; }
  }
  function saveAll(all){
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(all)); } catch {}
  }
  const allState = loadAll();
  // Back-compat migration from v1 global notes/todo
  if (!allState[PAGE_KEY]) {
    const legacy = (() => { try { return JSON.parse(localStorage.getItem('semptify_help_panel')||'{}'); } catch { return {}; } })();
    if (legacy && (legacy.notes || legacy.todo)) {
      allState[PAGE_KEY] = { notes: legacy.notes || '', todo: legacy.todo || '' };
      saveAll(allState);
    }
  }
  if (!allState[PAGE_KEY]) allState[PAGE_KEY] = { notes: '', todo: '' };
  const state = allState[PAGE_KEY];

  const defaults = {
    read: meta('help:read') || 'Quick overview: This page helps you manage tenant documentation and records.',
    instructions: meta('help:instructions') || 'Use the forms on this page to create or record documents. Save to your Vault.',
    notes: state.notes || meta('help:notes') || '',
    todo: state.todo || meta('help:todo') || ''
  };

  // Styles are defined in app.css to comply with CSP (no inline styles)

  // Create FAB and panel
  const fab = document.createElement('button');
  fab.className = 'help-fab';
  fab.title = 'Read / Instructions / Notes / To-Do';
  fab.textContent = 'R';

  const panel = document.createElement('div');
  panel.className = 'help-panel';
  panel.innerHTML = `
    <div class="help-header">
      <strong>Page Helper</strong>
      <button class="help-close" aria-label="Close">×</button>
    </div>
    <div class="help-tabs">
      <button class="help-tab" data-tab="read">Read</button>
      <button class="help-tab" data-tab="instructions">Instructions</button>
      <button class="help-tab" data-tab="notes">Notes</button>
      <button class="help-tab" data-tab="todo">To-Do</button>
    </div>
    <div class="help-body"></div>
  `;

  document.body.appendChild(fab);
  document.body.appendChild(panel);

  const closeBtn = $('.help-close', panel);
  const tabs = $all('.help-tab', panel);
  const body = $('.help-body', panel);

  function setActive(tab){
    tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
    let html = '';
    if(tab === 'read') html = `<div>${escapeHtml(defaults.read)}</div>`;
    if(tab === 'instructions') html = `<div>${escapeHtml(defaults.instructions)}</div>`;
    if(tab === 'notes') html = `<textarea id="help-notes" placeholder="Your notes...">${escapeHtml(defaults.notes)}</textarea>`;
    if(tab === 'todo') html = `<textarea id="help-todo" placeholder="Your to-do items...">${escapeHtml(defaults.todo)}</textarea>`;
    body.innerHTML = html;
    if(tab === 'notes'){
      const ta = $('#help-notes', body);
      ta.addEventListener('input', () => { state.notes = ta.value; allState[PAGE_KEY] = state; saveAll(allState); });
    }
    if(tab === 'todo'){
      const ta = $('#help-todo', body);
      ta.addEventListener('input', () => { state.todo = ta.value; allState[PAGE_KEY] = state; saveAll(allState); });
    }
  }

  function escapeHtml(s){
    return (s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
  }

  fab.addEventListener('click', () => {
    panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
    panel.style.flexDirection = 'column';
    setActive('read');
  });
  closeBtn.addEventListener('click', () => panel.style.display = 'none');
  tabs.forEach(t => t.addEventListener('click', () => setActive(t.dataset.tab)));
  // Fetch server-configured settings (optional)
  try {
    fetch('/api/help_panel_settings').then(r => r.ok ? r.json() : null).then(cfg => {
      if(!cfg) return;
      if(cfg.enabled === false){
        fab.style.display = 'none';
        panel.style.display = 'none';
        return;
      }
      if(cfg.label){ fab.textContent = (cfg.label + '').slice(0,2); }
      if(cfg.position === 'bl'){
        fab.style.right = 'auto'; fab.style.left = '16px';
        panel.style.right = 'auto'; panel.style.left = '16px';
      }
      // Fallback defaults (only if page meta absent)
      if(!meta('help:read') && cfg.read_default){ defaults.read = cfg.read_default; }
      if(!meta('help:instructions') && cfg.instructions_default){ defaults.instructions = cfg.instructions_default; }
    }).catch(()=>{});
  } catch {}
})();
