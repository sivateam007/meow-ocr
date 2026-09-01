/* Meow Assistant chat widget — talks to /api/chat. The Groq API key is used
   only by the server; this file never sees it. All user/Groq text is added
   with textContent, never innerHTML, so it is XSS-safe. */
(function () {
    'use strict';

    var toggle = document.getElementById('meow-chat-toggle');
    var panel = document.getElementById('meow-chat-panel');
    var closeBtn = document.getElementById('meow-chat-close');
    var form = document.getElementById('meow-chat-form');
    var input = document.getElementById('meow-chat-input');
    var body = document.getElementById('meow-chat-body');
    var chips = document.querySelectorAll('.meow-chip');

    function makeAvatar() {
        var av = document.createElement('span');
        av.className = 'meow-avatar';
        var img = document.createElement('img');
        img.src = window.MEOW_AVATAR || '';
        img.alt = 'Meow Assistant';
        img.loading = 'lazy';
        av.appendChild(img);
        return av;
    }

    function appendMsg(text, who) {
        var row = document.createElement('div');
        row.className = 'meow-row ' + (who === 'bot' ? 'row-bot' : 'row-user');
        if (who === 'bot') row.appendChild(makeAvatar());
        var bubble = document.createElement('div');
        bubble.className = 'meow-msg meow-msg-' + who;
        bubble.textContent = text;
        row.appendChild(bubble);
        body.appendChild(row);
        body.scrollTop = body.scrollHeight;
        return row;
    }

    function showTyping() {
        var row = document.createElement('div');
        row.className = 'meow-row row-bot';
        row.appendChild(makeAvatar());
        var bubble = document.createElement('div');
        bubble.className = 'meow-msg meow-msg-bot meow-typing';
        bubble.innerHTML = '<span></span><span></span><span></span>';
        row.appendChild(bubble);
        body.appendChild(row);
        body.scrollTop = body.scrollHeight;
        return row;
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
            appendMsg(d.reply || 'Sorry, I got distracted by a passing butterfly. Try again? 🐱', 'bot');
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