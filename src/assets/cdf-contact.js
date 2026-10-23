/* Formulaire de contact.
   Une seule ligne à modifier : CDF_GHL_FORM_ID, juste sous ce commentaire.
   Collez l'identifiant nu (exemple Abc123), ou l'URL complète
   https://api.leadconnectorhq.com/widget/form/Abc123.
   Le script charge alors l'iframe et https://link.msgsndr.com/js/form_embed.js.
   Laissez les guillemets vides pour garder le formulaire courriel. */
(function () {
  var CDF_GHL_FORM_ID = '';
  var CDF_CONTACT_EMAIL = 'p-o.chiasson@remax-quebec.com';

  function formIdFromConfig(value) {
    var raw = String(value || '').trim();
    if (!raw) return '';
    var fromUrl = raw.match(/widget\/form\/([A-Za-z0-9]+)\/?(?:$|[?#])/);
    if (fromUrl) return fromUrl[1];
    if (/^[A-Za-z0-9]+$/.test(raw)) return raw;
    return '';
  }

  function loadScript(src) {
    if (document.querySelector('script[src="' + src + '"]')) return;
    var script = document.createElement('script');
    script.src = src;
    script.async = false;
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

  function embedForm(root, formId, index) {
    var iframeId = 'cdf-ghl-' + formId + '-' + index;
    root.innerHTML = ''
      + '<div class="cdf-form-embed">'
      + '<iframe'
      + ' src="https://api.leadconnectorhq.com/widget/form/' + formId + '"'
      + ' class="cdf-form-iframe"'
      + ' id="' + iframeId + '"'
      + ' title="Formulaire de contact, Équipe Chiasson De Francesco"'
      + ' loading="lazy"'
      + ' data-layout="{\'id\':\'INLINE\'}"'
      + ' data-trigger-type="alwaysShow"'
      + ' data-trigger-value=""'
      + ' data-activation-type="alwaysActivated"'
      + ' data-activation-value=""'
      + ' data-deactivation-type="neverDeactivate"'
      + ' data-deactivation-value=""'
      + ' data-form-name="Contact Équipe Chiasson De Francesco"'
      + ' data-height="640"'
      + ' data-layout-iframe-id="' + iframeId + '"'
      + ' data-form-id="' + formId + '"'
      + '></iframe>'
      + '</div>';
    loadScript('/src/assets/cdf-forms.js');
    loadScript('https://link.msgsndr.com/js/form_embed.js');
  }

  function boot() {
    var formId = formIdFromConfig(CDF_GHL_FORM_ID);
    var slots = document.querySelectorAll('[data-cdf-contact]');
    Array.prototype.forEach.call(slots, function (root, index) {
      if (formId) embedForm(root, formId, index);
      else bindFallback(root);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
