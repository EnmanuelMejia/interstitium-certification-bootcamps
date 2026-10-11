/* Interstitium Labs — Unified AI Client (ai-client.js).
   Shared client for the /api/ai/ endpoint family. Used by Noah, the shell,
   CBTs, and any other consumer. One backend, multiple consumers.
   Vanilla JS, zero dependencies, ES5-compatible.
   Exposes window.AIClient. */
(function () {
  'use strict';

  var BASE = '';

  function baseUrl() {
    if (BASE) return BASE;
    /* Same-origin by default; the endpoints live on the flagship worker. */
    try {
      BASE = (window.location && window.location.origin) || 'https://interstitiumlabs.dev';
    } catch (e) {
      BASE = 'https://interstitiumlabs.dev';
    }
    return BASE;
  }

  function post(path, body, timeoutMs) {
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timer = null;
    if (controller) {
      timer = setTimeout(function () { controller.abort(); }, timeoutMs || 25000);
    }
    return fetch(baseUrl() + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: controller ? controller.signal : undefined,
    }).then(function (res) {
      return res.json().then(function (data) { return { ok: res.ok, status: res.status, data: data }; });
    }).then(function (out) {
      if (timer) clearTimeout(timer);
      return out;
    }).catch(function (err) {
      if (timer) clearTimeout(timer);
      return { ok: false, status: 0, data: null, error: err };
    });
  }

  /* Intelligent routing: taskType picks the best model automatically. */
  function route(taskType, messages, opts) {
    opts = opts || {};
    return post('/api/ai/route', {
      taskType: taskType,
      messages: messages,
      system: opts.system,
      max_tokens: opts.maxTokens,
      temperature: opts.temperature,
    }).then(function (out) {
      if (out.ok && out.data && out.data.reply) return out.data;
      throw new Error((out.data && out.data.error) || 'AI route failed');
    });
  }

  /* Direct chat with explicit model. */
  function chat(model, messages, opts) {
    opts = opts || {};
    return post('/api/ai/chat', {
      model: model,
      messages: messages,
      max_tokens: opts.maxTokens,
      temperature: opts.temperature,
    }).then(function (out) {
      if (out.ok && out.data && out.data.reply) return out.data;
      throw new Error((out.data && out.data.error) || 'AI chat failed');
    });
  }

  /* Multi-step agent execution. */
  function agent(agentId, input, context, opts) {
    opts = opts || {};
    return post('/api/ai/agent', {
      agent: agentId,
      input: input,
      context: context || {},
      maxSteps: opts.maxSteps || 3,
    }).then(function (out) {
      if (out.ok && out.data && out.data.answer) return out.data;
      throw new Error((out.data && out.data.error) || 'Agent failed');
    });
  }

  /* Dynamic labs: scenario generation, evaluation, hints, questions. */
  function dynamic(action, payload) {
    payload = payload || {};
    payload.action = action;
    return post('/api/noah/dynamic', payload, 30000).then(function (out) {
      if (out.ok && out.data && out.data.ok) return out.data;
      throw new Error((out.data && out.data.error) || 'Dynamic AI failed');
    });
  }

  /* Transcription (Parakeet ASR): base64 audio -> text.
     Backend prefers self-hosted NVIDIA Parakeet (parakeet-tdt-0.6b-v3,
     EN+ES auto-detect) when configured; otherwise Workers AI Whisper.
     opts: { language: 'en'|'es'|'auto', timestamps: bool }.
     Resolves { text, language, backend, model, words? }. */
  function transcribe(audioBase64, opts) {
    opts = opts || {};
    return post('/api/ai/transcribe', {
      audio: audioBase64,
      language: opts.language || 'auto',
      timestamps: !!opts.timestamps,
    }, 60000).then(function (out) {
      if (out.ok && out.data && out.data.ok) return out.data;
      throw new Error((out.data && out.data.error) || 'Transcription failed');
    });
  }

  /* Convenience: detect task type from text. */
  function detectTaskType(text) {
    var t = String(text || '').toLowerCase();
    if (/```|function |class |def |import |const |let |var |debug|error:|stack trace/i.test(text)) return 'code';
    if (/\b(solve|equation|integral|derivative|theorem|proof)\b/i.test(t)) return 'math';
    if (text.length < 100 && /^(what is|define|who is|when|where)\b/i.test(t)) return 'fast';
    return 'chat';
  }

  /* List available models and agents. Cached. */
  var modelsCache = null;
  function models() {
    if (modelsCache) return Promise.resolve(modelsCache);
    return fetch(baseUrl() + '/api/ai/models')
      .then(function (r) { return r.json(); })
      .then(function (data) { modelsCache = data; return data; })
      .catch(function () { return { ok: false, models: [], agents: [] }; });
  }

  window.AIClient = {
    route: route,
    chat: chat,
    agent: agent,
    dynamic: dynamic,
    transcribe: transcribe,
    models: models,
    detectTaskType: detectTaskType,
    /* Task-type shortcuts */
    tutor: function (messages, opts) { return route('tutor', messages, opts); },
    code: function (messages, opts) { return route('code', messages, opts); },
    fast: function (messages, opts) { return route('fast', messages, opts); },
  };
})();
// deploy 20261011T022918Z
// deploy 20261011T023002Z
// deploy 20261011T023034Z
// deploy 20261011T023300Z
// deploy 20261011T023544Z
