/* Meow Assistant chat widget — talks to /api/chat. The Groq API key is used
   only by the server; this file never sees it. */
(function () {
    'use strict';

    var toggle = document.getElementById('meow-chat-toggle');
    var panel = document.getElementById('meow-chat-panel');
    var closeBtn = document.getElementById('meow-chat-close');
    var form = document.getElementById('meow-chat-form');
    var input = document.getElementById('meow-chat-input');
    var body = document.getElementById('meow-chat-body');
    var chips = document.querySelectorAll('.meow-chip');

    function appendMsg(text, who) {
        var wrap = document.createElement('div');
        wrap.className = 'meow-msg meow-msg-' + who;
        wrap.textContent = text;
        body.appendChild(wrap);
        body.scrollTop = body.scrollHeight;
        return wrap;
    }

    function showTyping() {
        var wrap = document.createElement('div');
        wrap.className = 'meow-msg meow-msg-bot meow-typing';
        wrap.innerHTML = '<span></span><span></span><span></span>';
        body.appendChild(wrap);
        body.scrollTop = body.scrollHeight;
        return wrap;
    }

    function send(text) {
        if (!text) return;
        appendMsg(text, 'user');
        var typing = showTyping();
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(function (r) { return r.json(); })
        .then(function (d) {
            typing.remove();
            appendMsg(d.reply || 'Sorry, I got distracted by a passing butterfly. Try again? 🦋', 'bot');
        })
        .catch(function () {
            typing.remove();
            appendMsg('Oops, the connection hiccuped. Try again in a moment? 🐱', 'bot');
        });
    }

    if (!toggle || !panel) return;

    toggle.addEventListener('click', function () {
        panel.classList.toggle('open');
        toggle.classList.toggle('open');
        if (panel.classList.contains('open')) input.focus();
    });

    closeBtn.addEventListener('click', function () {
        panel.classList.remove('open');
        toggle.classList.remove('open');
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var value = input.value.trim();
        input.value = '';
        if (value) send(value);
    });

    chips.forEach(function (chip) {
        chip.addEventListener('click', function () {
            send(chip.getAttribute('data-q'));
        });
    });
})();