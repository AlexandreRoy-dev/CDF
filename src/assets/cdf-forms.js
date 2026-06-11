(function () {
  var allowedOrigins = [
    'https://api.leadconnectorhq.com',
    'https://link.msgsndr.com',
    'https://msgsndr.com'
  ];

  function isAllowedOrigin(origin) {
    return allowedOrigins.some(function (allowed) {
      return origin === allowed || origin.indexOf('leadconnectorhq.com') !== -1;
    });
  }

  function resizeIframe(iframe, height) {
    if (!iframe || !height) return;
    var parsed = parseInt(height, 10);
    if (!parsed || parsed < 200) return;
    iframe.style.height = parsed + 'px';
    iframe.setAttribute('data-height', String(parsed));
  }

  window.addEventListener('message', function (event) {
    if (!isAllowedOrigin(event.origin)) return;

    var data = event.data;
    if (typeof data === 'string') {
      try {
        data = JSON.parse(data);
      } catch (error) {
        return;
      }
    }

    if (!data || typeof data !== 'object') return;

    var height = data.height || data.frameHeight || (data.payload && data.payload.height);
    if (!height) return;

    var iframeId = data.id || data.iframeId || data['data-layout-iframe-id'];
    if (iframeId) {
      var target = document.getElementById(iframeId);
      if (target) resizeIframe(target, height);
      return;
    }

    document.querySelectorAll('.cdf-form-iframe').forEach(function (iframe) {
      resizeIframe(iframe, height);
    });
  });
})();
