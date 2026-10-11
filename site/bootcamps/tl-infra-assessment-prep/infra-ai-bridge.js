/* Interstitium Labs — Infra CBT AI bridge (infra-ai-bridge.js).
   The tl-infra-assessment-prep CBT runs a custom shell whose terminal is
   TLTerm (app.js), not the unified shell's ILBTerminal. The AI learning
   modules (ai-terminal.js et al.) speak the ILBTerminal contract:
     ILBTerminal.onCommand(fn(commandString, fullOutputText))
     ILBTerminal.print(text)
     ILBTerminal.focus()
   This bridge publishes that contract over TLTerm WITHOUT touching the
   CBT's own code: it wraps TLTerm.keydown (the Terminal view's input
   handler), feeds each executed command + its rendered output to the
   registered coach handlers, and routes `ai ...` meta-commands straight
   to the coach so the profile never answers them with "not recognized".
   Lab/scenario terminals built with createTerminal() keep their own
   onCommand checking and are deliberately NOT bridged — assessment
   integrity (labs, mock exam) is untouched.
   Vanilla JS, zero dependencies, ES5-compatible. */
(function () {
  'use strict';

  var handlers = [];

  function notify(cmd, output) {
    for (var i = 0; i < handlers.length; i++) {
      try { handlers[i](cmd, output); } catch (e) { /* coach errors never break the terminal */ }
    }
  }

  window.ILBTerminal = {
    onCommand: function (fn) { if (typeof fn === 'function') handlers.push(fn); },
    print: function (text) { if (window.TLTerm) TLTerm.print(text); },
    focus: function () {
      var inp = document.getElementById('termIn');
      if (inp) inp.focus();
    }
  };

  function wrap() {
    if (!window.TLTerm) { setTimeout(wrap, 300); return; }
    if (TLTerm.__aiBridged) return;
    TLTerm.__aiBridged = true;

    var orig = TLTerm.keydown;
    TLTerm.keydown = function (e) {
      if (!e || e.key !== 'Enter') return orig.call(TLTerm, e);

      var inp = document.getElementById('termIn');
      var cmd = inp ? inp.value : '';

      /* `ai ...` meta-commands belong to the coach, not the shell profile. */
      if (/^\s*ai(\s|$)/i.test(cmd)) {
        TLTerm.print((TLTerm.prompts[TLTerm.profile] || '> ') + ' ' + cmd);
        if (inp) inp.value = '';
        if (cmd.trim()) {
          TLTerm.hist.unshift(cmd);
          TLTerm.hIdx = -1;
        }
        notify(cmd, '');
        if (e.preventDefault) e.preventDefault();
        return;
      }

      /* Normal command: run the original handler, then collect the lines
         it rendered after the command echo and hand them to the coach. */
      var out = document.getElementById('termOut');
      var before = out ? out.childElementCount : 0;
      var ret = orig.call(TLTerm, e);
      if (out) {
        var lines = [];
        for (var i = before + 1; i < out.childElementCount; i++) {
          lines.push(out.children[i].textContent);
        }
        notify(cmd, lines.join('\n'));
      }
      return ret;
    };

    /* Announce the coach (env banner) the first time the Terminal view
       appears: ai-terminal.js listens for ilb:view like on shell pages. */
    var announced = false;
    if (window.MutationObserver && document.body) {
      new MutationObserver(function () {
        if (!announced && document.getElementById('termIn')) {
          announced = true;
          try {
            document.dispatchEvent(new CustomEvent('ilb:view', { detail: 'terminal' }));
          } catch (e) { /* older browsers: banner is cosmetic */ }
        }
      }).observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wrap);
  } else {
    wrap();
  }
})();
