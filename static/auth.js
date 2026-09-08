/* Meow OCR — Google sign-in helper (Supabase auth).
   Activates only when window.SUPABASE_CONFIG has a url + anonKey.
   Server session is created via /api/auth (Supabase access token). */
(function () {
    var cfg = window.SUPABASE_CONFIG || {};
    var enabled = !!(cfg.url && cfg.anonKey);
    window.SCAN_AUTH_ENABLED = enabled;

    function currentUser() {
        try { return JSON.parse(localStorage.getItem('scantext_user') || 'null'); } catch (e) { return null; }
    }
    function saveUser(u) {
        if (u) localStorage.setItem('scantext_user', JSON.stringify(u));
        else localStorage.removeItem('scantext_user');
    }

    function refreshUi() {
        var user = currentUser();
        var loginBtn = document.getElementById('google-login-btn');
        var userBadge = document.getElementById('user-badge');
        var logoutBtn = document.getElementById('logout-btn');
        if (!loginBtn) { return; }
        if (user && user.uid) {
            if (loginBtn) loginBtn.style.display = 'none';
            if (userBadge) {
                userBadge.style.display = 'inline-flex';
                var nameEl = document.getElementById('user-name');
                if (nameEl) nameEl.textContent = user.name || user.email || 'Me';
                var av = document.getElementById('user-avatar');
                if (av) { if (user.photo) av.src = user.photo; av.style.display = user.photo ? 'inline-block' : 'none'; }
            }
            if (logoutBtn) logoutBtn.style.display = 'inline-flex';
        } else {
            if (loginBtn && enabled) loginBtn.style.display = 'inline-flex';
            if (userBadge) userBadge.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'none';
        }
    }

    // Seed from server-provided session (if not already saved locally)
    if (window.SCANNER_USER && window.SCANNER_USER.uid && !currentUser()) {
        saveUser(window.SCANNER_USER);
    }

    function supabaseClient() {
        if (!enabled) return null;
        if (!window.__supaClient) {
            if (!(window.supabase && window.supabase.createClient)) return null;
            window.__supaClient = window.supabase.createClient(cfg.url, cfg.anonKey);
        }
        return window.__supaClient;
    }

    function doLogin() {
        var btn = document.getElementById('google-login-btn');
        var client = supabaseClient();
        if (!client) {
            resetBtn();
            alert('Sign-in is being set up.\n\nUntil then you can keep using Meow OCR free — one document per anonymous session.');
            return;
        }
        if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...'; }
        // Preflight: confirm Google auth is actually enabled before redirecting
        fetch(cfg.url + '/auth/v1/settings', { headers: { apikey: cfg.anonKey } })
            .then(function (r) { return r.json(); })
            .then(function (d) {
                var ok = d && d.external && d.external.google === true;
                if (!ok) {
                    resetBtn();
                    alert('Google sign-in is being set up on this site.\n\nUntil then you can keep using Meow OCR free — one document per anonymous session.');
                    return;
                }
                if (btn) btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Redirecting...';
                // Bare origin only (no path/trailing slash) — matches Supabase redirect allowlist exactly
                var redirectTo = window.location.origin;
                return client.auth.signInWithOAuth({
                    provider: 'google',
                    options: { redirectTo: redirectTo }
                });
            })
            .catch(function (err) {
                console.error('Sign-in start error:', err);
                resetBtn();
                alert('Could not start sign-in: ' + (err.message || 'unknown error'));
            });
    }

    function resetBtn() {
        var btn = document.getElementById('google-login-btn');
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fab fa-google"></i> Sign in with Google'; }
    }

    // Completes a fresh OAuth redirect round-trip (or refreshes an existing session)
    function finishLogin() {
        var client = supabaseClient();
        if (!client) return;
        client.auth.getSession().then(function (res) {
            var session = res && res.data && res.data.session;
            if (!session || !session.access_token) return;
            return fetch('/api/auth', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ access_token: session.access_token })
            }).then(function (r) { return r.json(); })
              .then(function (data) {
                if (data && data.ok) {
                    saveUser(data.user);
                    refreshUi();
                    if (typeof window.onScanLogin === 'function') window.onScanLogin(data.user);
                }
              });
        }).catch(function (err) {
            console.error('Sign-in verification error:', err);
        });
    }

    function doLogout() {
        var client = supabaseClient();
        if (client && client.auth.signOut) client.auth.signOut().catch(function () {});
        saveUser(null);
        refreshUi();
        fetch('/api/logout', { method: 'POST' }).catch(function () {});
        if (typeof window.onScanLogout === 'function') window.onScanLogout();
    }

    window.ScanAuth = {
        doLogin: doLogin,
        doLogout: doLogout,
        getUser: currentUser,
        enabled: enabled
    };

    document.addEventListener('DOMContentLoaded', function () {
        refreshUi();
        finishLogin();
        var loginBtn = document.getElementById('google-login-btn');
        var logoutBtn = document.getElementById('logout-btn');
        if (loginBtn) loginBtn.addEventListener('click', function (e) { e.preventDefault(); doLogin(); });
        if (logoutBtn) logoutBtn.addEventListener('click', function (e) { e.preventDefault(); doLogout(); });
    });
})();