/* Shared form UX for every SkillMaxx form that posts to FormSubmit.
   <form data-smx-form [data-ajax] data-label="Send" data-err="#id" data-ok="#id" data-mail="mailto:...">
   - instant "Sending…" + disabled button, no double submit
   - "Still sending…" after 6 s; after 20 s stop/flag with a mailto fallback
   - data-ajax: POST to formsubmit.co/ajax, success only on {success:"true"}
   - otherwise: normal POST (reCAPTCHA + _autoresponse + _next), FormSubmit redirects back on success */
(function(){
  document.querySelectorAll('form[data-smx-form]').forEach(function(form){
    var btn = form.querySelector('button[type=submit]'), label = btn.textContent, busy = false; btn.dataset.label = label;
    var err = document.querySelector(form.dataset.err), ok = form.dataset.ok && document.querySelector(form.dataset.ok);
    var mail = form.dataset.mail || 'mailto:skillmaxx@gilventures.ai';
    function reset(){ busy = false; btn.disabled = false; btn.textContent = label }
    function fail(msg){ err.innerHTML = msg + ' You can also <a href="' + mail + '" style="color:inherit;text-decoration:underline">email skillmaxx@gilventures.ai</a> directly.'; err.hidden = false; reset() }
    form.addEventListener('submit', function(e){
      if (busy) { e.preventDefault(); return }
      if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return }
      busy = true; err.hidden = true; btn.disabled = true; btn.textContent = 'Sending…';
      var slow = setTimeout(function(){ if (busy) btn.textContent = 'Still sending…' }, 6000);
      if (!('ajax' in form.dataset)) {
        // Normal POST: the browser navigates to FormSubmit (spam check), then back to our success page.
        setTimeout(function(){ if (busy) fail('This is taking longer than usual. If nothing happens soon, check your connection and try again.') }, 20000);
        return;
      }
      e.preventDefault();
      var ctl = window.AbortController ? new AbortController() : null;
      var kill = setTimeout(function(){ if (ctl) ctl.abort() }, 20000);
      fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {method:'POST', body:new FormData(form), headers:{'Accept':'application/json'}, signal: ctl ? ctl.signal : undefined})
        .then(function(r){ return r.json() })
        .then(function(d){ clearTimeout(slow); clearTimeout(kill);
          if (d && (d.success === true || d.success === 'true')) { form.hidden = true; if (ok) ok.hidden = false; busy = false }
          else fail('We couldn\'t confirm it was received.') })
        .catch(function(x){ clearTimeout(slow); clearTimeout(kill);
          fail(x && x.name === 'AbortError' ? 'No reply after 20 seconds, so we stopped. It may not have been sent. Please try again.' : 'Couldn\'t reach our form service. Check your connection and try again.') });
    });
  });
})();
// Back/forward cache: never leave a button stuck on "Sending…".
window.addEventListener('pageshow', function(){ document.querySelectorAll('form[data-smx-form] button[type=submit][disabled]').forEach(function(b){ b.disabled = false; b.textContent = b.dataset.label || 'Send' }) });
