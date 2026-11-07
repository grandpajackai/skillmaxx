/* Shared form UX for every SkillMaxx form. No third-party form backend (FormSubmit kept returning 522).
   <form data-smx-form data-subject="..." [data-issue] data-mail="mailto:...">
   On submit we validate, then show a "send it" panel with:
   - Send by email: mailto:skillmaxx@gilventures.ai with subject + every field prefilled (primary, always works)
   - Copy details: clipboard copy, for webmail users
   - data-issue: Open a prefilled GitHub issue on grandpajackai/skillmaxx (public, needs a GitHub login) */
(function(){
  var TO = 'skillmaxx@gilventures.ai', REPO = 'https://github.com/grandpajackai/skillmaxx/issues/new';
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c] }) }
  document.querySelectorAll('form[data-smx-form]').forEach(function(form){
    var err = form.dataset.err && document.querySelector(form.dataset.err);
    form.removeAttribute('action');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return }
      if (err) err.hidden = true;
      var lines = [], title = '';
      Array.prototype.forEach.call(form.elements, function(el){
        if (!el.name || el.name.charAt(0) === '_' || el.type === 'submit' || !el.value.trim()) return;
        if (!title && el.name === 'name') title = el.value.trim();
        lines.push(el.name.replace(/_/g, ' ') + ': ' + el.value.trim());
      });
      var subject = (form.dataset.subject || 'SkillMaxx form') + (title ? ': ' + title : '');
      var body = lines.join('\n') + '\n\nSent from ' + location.href.split('?')[0];
      var mail = 'mailto:' + TO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var issue = REPO + '?labels=submission&title=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var p = document.createElement('div');
      p.className = 'smx-send'; p.setAttribute('role', 'status');
      p.style.cssText = 'margin-top:14px;padding:16px;border-radius:9px;background:rgba(198,244,50,.08);border:1px solid rgba(198,244,50,.3)';
      p.innerHTML = '<p style="margin:0;color:var(--a);font-weight:600">Almost done: send it to us</p>' +
        '<p class="muted" style="margin:6px 0 12px">Your details are filled in. Pick one way to send them. A human reads every one.</p>' +
        '<div style="display:flex;flex-wrap:wrap;gap:10px">' +
        '<a class="btn" href="' + esc(mail) + '">Send by email</a>' +
        ('issue' in form.dataset ? '<a class="btn ghost" target="_blank" rel="noopener" href="' + esc(issue) + '">Open a GitHub issue</a>' : '') +
        '<button type="button" class="btn ghost" data-copy>Copy details</button>' +
        '<button type="button" class="btn ghost" data-edit>Edit</button></div>' +
        '<p class="muted" data-note style="margin:10px 0 0;font-size:13px">Email app didn\'t open? Copy the details and email them to <a href="mailto:' + TO + '">' + TO + '</a>.</p>';
      p.querySelector('[data-copy]').addEventListener('click', function(){
        var t = 'To: ' + TO + '\nSubject: ' + subject + '\n\n' + body, b = this;
        (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function(){ b.textContent = 'Copied ✓' }, function(){ window.prompt('Copy this and email it to ' + TO, t) });
      });
      p.querySelector('[data-edit]').addEventListener('click', function(){ p.remove(); form.hidden = false });
      var old = form.parentNode.querySelector('.smx-send'); if (old) old.remove();
      form.hidden = true; form.parentNode.insertBefore(p, form.nextSibling);
      p.scrollIntoView({behavior:'smooth', block:'center'});
    });
  });
})();
