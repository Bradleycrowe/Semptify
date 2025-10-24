document.addEventListener('DOMContentLoaded', function() {
  // content module wiring
  (function() {
    const toggleBtns = document.querySelectorAll('.content-toggle-btn');
    const moduleEl = document.getElementById('content-module');
    const runBtn = document.getElementById('module-run');
    const clearBtn = document.getElementById('module-clear');
    const inputEl = document.getElementById('module-input');
    const outputEl = document.getElementById('module-output');
    const statusEl = document.getElementById('module-status');

    function setStatus(s) { if(statusEl) statusEl.textContent = s; }

    toggleBtns.forEach(b => b.addEventListener('click', () => {
      if(!moduleEl) return;
      moduleEl.classList.toggle('hidden');
      setStatus(moduleEl.classList.contains('hidden') ? 'hidden' : 'visible');
    }));

    if(clearBtn) clearBtn.addEventListener('click', () => { inputEl.value = ''; outputEl.textContent = ''; setStatus('cleared'); });

    if(runBtn) runBtn.addEventListener('click', async () => {
      const text = inputEl.value || '';
      setStatus('processing');
      outputEl.textContent = 'Processing...';
      try {
        const resp = await fetch('/api/ai/orchestrate', {
          method: 'POST', headers: {'Content-Type':'application/json'},
          body: JSON.stringify({ requester: 'local-ui', input_refs: [], ais: [{name:'local', role:'assistant'}], strategy:'synthesize', approval_required:false })
        });
        if(resp.ok) {
          const data = await resp.json();
          outputEl.textContent = 'Job queued: ' + (data.job_id || JSON.stringify(data));
          setStatus('queued');
        } else {
          outputEl.textContent = 'Server error, echoing input:\n\n' + text;
          setStatus('errored');
        }
      } catch(e) {
        outputEl.textContent = 'Fallback (no server) - echo:\n\n' + text;
        setStatus('fallback');
      }
    });

    // Control panel handlers
    const ctrlTitle = document.getElementById('ctrl-title');
    const ctrlBody = document.getElementById('ctrl-body');
    const ctrlApply = document.getElementById('ctrl-apply');
    const ctrlReset = document.getElementById('ctrl-reset');
    const pageTitleEl = document.querySelector('.page-title');
    const pageBodyEl = document.querySelector('.page-body');

    if(ctrlApply) ctrlApply.addEventListener('click', () => {
      if(pageTitleEl && ctrlTitle) pageTitleEl.innerHTML = ctrlTitle.value || '';
      if(pageBodyEl && ctrlBody) pageBodyEl.innerHTML = ctrlBody.value || '';
    });
    if(ctrlReset) ctrlReset.addEventListener('click', () => {
      if(pageTitleEl) pageTitleEl.innerHTML = '';
      if(pageBodyEl) pageBodyEl.innerHTML = '';
      if(ctrlTitle) ctrlTitle.value = '';
      if(ctrlBody) ctrlBody.value = '';
    });

    // Footer toggle
    const footerToggle = document.getElementById('footer-toggle');
    const footerExtra = document.getElementById('footer-extra');
    if(footerToggle && footerExtra) footerToggle.addEventListener('click', () => {
      footerExtra.classList.toggle('d-none');
      footerToggle.textContent = footerExtra.classList.contains('d-none') ? 'More' : 'Less';
    });

    // Mobile right sidebar
    const mobileToggle = document.getElementById('mobile-right-toggle');
    const rightSidebar = document.querySelector('.right-sidebar');
    const rightOverlay = document.getElementById('right-overlay');
    if(mobileToggle && rightSidebar && rightOverlay) {
      mobileToggle.addEventListener('click', () => { rightSidebar.classList.add('open'); rightOverlay.classList.add('open'); });
      rightOverlay.addEventListener('click', () => { rightSidebar.classList.remove('open'); rightOverlay.classList.remove('open'); });
    }
  })();
});
