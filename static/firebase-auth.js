/* ScanText — Google (Firebase) sign-in helper.
   Activates only when window.FIREBASE_CONFIG has valid values.
   Verifies on the server via /api/auth (Firebase REST lookup). */
(function () {
    var cfg = window.FIREBASE_CONFIG || {};
    var enabled = !!(cfg.apiKey && cfg.projectId && cfg.authDomain && cfg.appId);
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

    function doLogin() {
        var btn = document.getElementById('google-login-btn');
        if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...'; }
        firebase.auth().signInWithPopup(new firebase.auth.GoogleAuthProvider())
            .then(function (res) {
                var u = res.user;
                var idToken = _getIdToken(u);
                return idToken.then(function (token) {
                    return fetch('/api/auth', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ idToken: token })
                    });
                }).then(function (r) { return r.json(); });
            })
            .then(function (data) {
                if (data && data.ok) {
                    saveUser(data.user);
                    refreshUi();
                    if (typeof window.onScanLogin === 'function') window.onScanLogin(data.user);
                } else {
                    alert('Could not complete sign-in. Please try again.');
                }
            })
            .catch(function (err) {
                console.error('ScanText login error:', err);
                alert('Sign-in failed: ' + (err.message || 'unknown error'));
            })
            .finally(function () {
                if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fab fa-google"></i> Sign in with Google'; }
            });
    }

    function _getIdToken(u) {
        if (u.getIdToken) {
            return u.getIdToken(true).catch(function () { return u.getIdToken(); });
        }
        return Promise.resolve(null);
    }

    function doLogout() {
        if (firebase && firebase.auth) {
            firebase.auth().signOut().catch(function () {});
        }
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
        var loginBtn = document.getElementById('google-login-btn');
        var logoutBtn = document.getElementById('logout-btn');
        if (loginBtn) loginBtn.addEventListener('click', function (e) { e.preventDefault(); if (!enabled) { alert('Sign-in is being set up.\n\nUntil then you can keep using ScanText free — one document per anonymous session.'); return; } doLogin(); });
        if (logoutBtn) logoutBtn.addEventListener('click', function (e) { e.preventDefault(); doLogout(); });
    });
})();
