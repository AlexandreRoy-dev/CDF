/* Formulaire de contact.
   CDF_GHL_FORM_ID est l'identifiant GoHighLevel (ou l'URL du widget).
   L'iframe charge https://api.leadconnectorhq.com/widget/form/IDENTIFIANT
   et la page charge https://link.msgsndr.com/js/form_embed.js.
   Si l'iframe ou ce script échoue, ou si l'iframe ne charge pas en 5 secondes,
   le formulaire courriel reste affiché. La colonne n'est jamais vide. */
(function () {
  var CDF_GHL_FORM_ID = 'aPBFp2Ved0if0rWkUWTx';
  var CDF_CONTACT_EMAIL = 'p-o.chiasson@remax-quebec.com';
  var LOAD_TIMEOUT_MS = 5000;
  var FALLBACK_SELECTOR = '.cdf-contact-title, .cdf-contact-lead, .cdf-contact-note, .cdf-contact-form, .cdf-contact-direct';

  function formIdFromConfig(value) {
    var raw = String(value || '').trim();
    if (!raw) return '';
    var fromUrl = raw.match(/widget\/form\/([A-Za-z0-9]+)\/?(?:$|[?#])/);
    if (fromUrl) return fromUrl[1];
    if (/^[A-Za-z0-9]+$/.test(raw)) return raw;
    return '';
  }

  function loadScript(src, onload, onerror) {
    var existing = document.querySelector('script[src="' + src + '"]');
    if (existing) {
      if (existing.getAttribute('data-cdf-loaded') === '1') {
        if (onload) onload();
        return;
      }
      if (existing.getAttribute('data-cdf-failed') === '1') {
        if (onerror) onerror();
        return;
      }
      if (onload) existing.addEventListener('load', onload);
      if (onerror) existing.addEventListener('error', onerror);
      return;
    }
    var script = document.createElement('script');
    script.src = src;
    script.async = false;
    script.addEventListener('load', function () {
      script.setAttribute('data-cdf-loaded', '1');
      if (onload) onload();
    });
    script.addEventListener('error', function () {
      script.setAttribute('data-cdf-failed', '1');
      if (onerror) onerror();
    });
    document.body.appendChild(script);
  }

  function emailFor(form) {
    var action = form.getAttribute('action') || '';
    var match = action.match(/^mailto:([^?]+)/i);
    if (match && match[1]) {
      try {
        return decodeURIComponent(match[1]);
      } catch (error) {
        return match[1];
      }
    }
    return CDF_CONTACT_EMAIL;
  }

  function fieldValue(form, name) {
    var el = form.elements[name];
    return el ? String(el.value || '').trim() : '';
  }

  function openMail(href) {
    if (typeof window.CDF_CONTACT_OPEN === 'function') {
      window.CDF_CONTACT_OPEN(href);
      return;
    }
    window.location.href = href;
  }

  function bindFallback(root) {
    var form = root.querySelector('form.cdf-contact-form');
    if (!form || form.getAttribute('data-cdf-bound') === '1') return;
    form.setAttribute('data-cdf-bound', '1');
    var page = form.elements.page;
    if (page) page.value = window.location.href.split('#')[0];

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.classList.add('is-invalid');
        form.reportValidity();
        return;
      }
      var telephone = fieldValue(form, 'telephone');
      var body = [
        'Nom : ' + fieldValue(form, 'nom'),
        'Courriel : ' + fieldValue(form, 'courriel'),
        'Téléphone : ' + (telephone || 'non précisé'),
        'Page : ' + (page && page.value ? page.value : window.location.href.split('#')[0]),
        '',
        fieldValue(form, 'message')
      ].join('\n');
      var href = 'mailto:' + emailFor(form)
        + '?subject=' + encodeURIComponent('Message du site chiassondefrancesco.ca')
        + '&body=' + encodeURIComponent(body);
      openMail(href);
    });
  }

  function setFallbackHidden(root, hidden) {
    var nodes = root.querySelectorAll(FALLBACK_SELECTOR);
    Array.prototype.forEach.call(nodes, function (node) {
      if (hidden) node.setAttribute('hidden', '');
      else node.removeAttribute('hidden');
    });
  }

  function iframeHasForeignDocument(iframe) {
    try {
      var win = iframe.contentWindow;
      if (!win) return false;
      /* Une page lisible (about:blank ou erreur locale) n'est pas le formulaire. */
      void win.location.href;
      return false;
    } catch (error) {
      return true;
    }
  }

  function createIframe(formId, iframeId) {
    var iframe = document.createElement('iframe');
    iframe.className = 'cdf-form-iframe';
    iframe.id = iframeId;
    iframe.title = 'Lead form Site: CDF';
    iframe.setAttribute('data-layout', "{'id':'INLINE'}");
    iframe.setAttribute('data-trigger-type', 'alwaysShow');
    iframe.setAttribute('data-trigger-value', '');
    iframe.setAttribute('data-activation-type', 'alwaysActivated');
    iframe.setAttribute('data-activation-value', '');
    iframe.setAttribute('data-deactivation-type', 'neverDeactivate');
    iframe.setAttribute('data-deactivation-value', '');
    iframe.setAttribute('data-form-name', 'Lead form Site: CDF');
    iframe.setAttribute('data-height', '460');
    iframe.setAttribute('data-layout-iframe-id', iframeId);
    iframe.setAttribute('data-form-id', formId);
    return iframe;
  }

  function showEmbed(root) {
    var embed = root.querySelector('.cdf-form-embed');
    if (embed) embed.classList.remove('cdf-contact-embed-pending');
    var iframe = root.querySelector('.cdf-form-iframe');
    if (iframe) iframe.removeAttribute('tabindex');
    setFallbackHidden(root, true);
    root.setAttribute('data-cdf-state', 'embed');
  }

  function showFallback(root) {
    var embed = root.querySelector('.cdf-form-embed');
    if (embed) embed.remove();
    setFallbackHidden(root, false);
    bindFallback(root);
    root.setAttribute('data-cdf-state', 'fallback');
  }

  function mountEmbed(root, formId, index) {
    var settled = false;
    var iframeLoaded = false;
    var scriptLoaded = false;
    var iframeId = index === 0 ? 'inline-' + formId : 'inline-' + formId + '-' + (index + 1);
    var embed = document.createElement('div');
    var iframe = createIframe(formId, iframeId);
    var timer;

    embed.className = 'cdf-form-embed cdf-contact-embed-pending';
    iframe.setAttribute('tabindex', '-1');
    embed.appendChild(iframe);
    root.insertBefore(embed, root.firstChild);
    root.setAttribute('data-cdf-state', 'pending');
    bindFallback(root);

    function fail() {
      if (settled) return;
      settled = true;
      window.clearTimeout(timer);
      showFallback(root);
    }

    function succeed() {
      if (settled || !iframeLoaded || !scriptLoaded) return;
      settled = true;
      window.clearTimeout(timer);
      showEmbed(root);
    }

    iframe.addEventListener('error', fail);
    iframe.addEventListener('load', function () {
      if (!iframeHasForeignDocument(iframe)) return;
      iframeLoaded = true;
      succeed();
    });

    timer = window.setTimeout(function () {
      if (!iframeLoaded || !scriptLoaded) fail();
    }, LOAD_TIMEOUT_MS);

    iframe.src = 'https://api.leadconnectorhq.com/widget/form/' + formId;

    loadScript('https://link.msgsndr.com/js/form_embed.js', function () {
      scriptLoaded = true;
      succeed();
    }, fail);

    loadScript('/src/assets/cdf-forms.js');
  }

  function boot() {
    var formId = formIdFromConfig(CDF_GHL_FORM_ID);
    var slots = document.querySelectorAll('[data-cdf-contact]');
    Array.prototype.forEach.call(slots, function (root, index) {
      if (formId) mountEmbed(root, formId, index);
      else {
        bindFallback(root);
        root.setAttribute('data-cdf-state', 'fallback');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
