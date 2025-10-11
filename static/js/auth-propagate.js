// Propagate user_token across internal navigation and forms so authenticated users
// don't hit unauthorized pages when SECURITY_MODE=enforced.
(function(){
  try {
    const url = new URL(window.location.href);
    const token = url.searchParams.get('user_token') || sessionStorage.getItem('semptify_user_token') || '';
    if (token) {
      sessionStorage.setItem('semptify_user_token', token);
      // Rewrite internal links to include user_token unless they already have it
      const as = document.querySelectorAll('a[href]');
      as.forEach(a => {
        try {
          const href = a.getAttribute('href');
          if (!href) return;
          // Only same-origin relative links
          if (href.startsWith('http:') || href.startsWith('https:') || href.startsWith('#') || href.startsWith('mailto:')) return;
          // Keep static assets untouched
          if (href.startsWith('/static/')) return;
          const u = new URL(href, window.location.origin);
          if (!u.searchParams.get('user_token')) {
            u.searchParams.set('user_token', token);
            a.setAttribute('href', u.pathname + u.search + u.hash);
          }
        } catch {}
      });
      // Ensure forms include user_token hidden input
      const forms = document.querySelectorAll('form');
      forms.forEach(f => {
        if (!f.querySelector('input[name="user_token"]')) {
          const inp = document.createElement('input');
          inp.type = 'hidden';
          inp.name = 'user_token';
          inp.value = token;
          f.appendChild(inp);
        }
      });
    }
  } catch (e) {
    // best-effort; do not break page
    console.warn('auth-propagate failed', e);
  }
})();
