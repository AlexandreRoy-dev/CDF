window.dataLayer = window.dataLayer || [];
function gtag() {
  dataLayer.push(arguments);
}
gtag('js', new Date());
gtag('config', 'G-VBQPR5ZNV0');

window.cdfTrackLead = function (source) {
  if (typeof gtag !== 'function') return;
  gtag('event', 'generate_lead', {
    lead_source: source || 'website'
  });
};

document.addEventListener('click', function (event) {
  var link = event.target && event.target.closest ? event.target.closest('a[href^="tel:"]') : null;
  if (!link || typeof gtag !== 'function') return;
  gtag('event', 'click_to_call', {
    link_url: link.getAttribute('href')
  });
});
