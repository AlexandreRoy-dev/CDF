/* Témoins publicitaires (pixel Meta). Rien n'est chargé vers Meta avant un accord. */
(function () {
  if (window.__cdfConsentInit) return;
  window.__cdfConsentInit = true;

  var PIXEL_ID = "1126708586975929";
  var CHOICE_KEY = "cdf_consent";
  var DATE_KEY = "cdf_consent_date";
  var pixelLoaded = false;

  function readChoice() {
    try {
      var value = localStorage.getItem(CHOICE_KEY);
      if (value === "granted" || value === "denied") return value;
    } catch (err) {}
    return null;
  }

  function storeChoice(choice) {
    try {
      localStorage.setItem(CHOICE_KEY, choice);
      localStorage.setItem(DATE_KEY, new Date().toISOString());
    } catch (err) {}
  }

  function clearMetaCookies() {
    ["_fbp", "_fbc"].forEach(function (name) {
      document.cookie = name + "=; Max-Age=0; path=/; SameSite=Lax";
    });
  }

  function loadPixel() {
    if (pixelLoaded || readChoice() !== "granted") return;
    pixelLoaded = true;
    !(function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n;
      n.push = n;
      n.loaded = !0;
      n.version = "2.0";
      n.queue = [];
      t = b.createElement(e);
      t.async = !0;
      t.src = v;
      s = b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t, s);
    })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", PIXEL_ID);
    window.fbq("track", "PageView");
  }

  function hideBanner() {
    var banner = document.getElementById("cdf-consent");
    if (banner) banner.hidden = true;
  }

  function choose(choice) {
    storeChoice(choice);
    hideBanner();
    if (choice === "granted") loadPixel();
    else clearMetaCookies();
  }

  function showBanner() {
    var banner = document.getElementById("cdf-consent");
    if (!banner) return;
    banner.hidden = false;
  }

  function buildBanner() {
    if (document.getElementById("cdf-consent")) return;
    var style = document.createElement("style");
    style.textContent =
      "#cdf-consent{position:fixed;left:0;right:0;bottom:0;z-index:40;background:#000E35;color:#F7F5EE;" +
      "padding:1rem 1rem calc(1rem + env(safe-area-inset-bottom));box-shadow:0 -8px 24px rgba(0,14,53,.28);" +
      "font-family:Inter,system-ui,sans-serif;font-size:.95rem;line-height:1.45}" +
      "#cdf-consent[hidden]{display:none}" +
      "#cdf-consent .cdf-consent-inner{max-width:52rem;margin:0 auto}" +
      "#cdf-consent p{margin:0 0 .85rem}" +
      "#cdf-consent a{color:#F7F5EE;text-underline-offset:2px}" +
      "#cdf-consent .cdf-consent-actions{display:flex;flex-wrap:wrap;gap:.75rem}" +
      "#cdf-consent button{flex:1 1 9rem;min-height:44px;margin:0;padding:.55rem 1rem;border:2px solid #F7F5EE;" +
      "border-radius:.5rem;background:transparent;color:#F7F5EE;font:inherit;font-weight:600;cursor:pointer}" +
      "#cdf-consent button:hover,#cdf-consent button:focus-visible{background:#AA1120;border-color:#AA1120;color:#fff}" +
      "#cdf-consent-manage{color:inherit;text-decoration:underline;text-underline-offset:2px}";
    document.head.appendChild(style);

    var banner = document.createElement("div");
    banner.id = "cdf-consent";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-labelledby", "cdf-consent-title");
    banner.innerHTML =
      '<div class="cdf-consent-inner">' +
      '<p id="cdf-consent-title">Nous utilisons des témoins (cookies) de mesure publicitaire, comme le pixel Meta, pour comprendre l\'utilisation du site et afficher des publicités pertinentes. Ils ne sont activés qu\'avec votre accord.</p>' +
      '<p><a href="/confidentialite.html#pixel-meta">Politique de confidentialité</a></p>' +
      '<div class="cdf-consent-actions">' +
      '<button type="button" data-cdf-choice="granted">Accepter</button>' +
      '<button type="button" data-cdf-choice="denied">Refuser</button>' +
      "</div></div>";
    banner.addEventListener("click", function (event) {
      var button = event.target.closest("button[data-cdf-choice]");
      if (!button) return;
      choose(button.getAttribute("data-cdf-choice"));
    });
    document.body.appendChild(banner);
    if (readChoice()) banner.hidden = true;
  }

  function buildManageLink() {
    if (document.getElementById("cdf-consent-manage")) return;
    var link = document.createElement("a");
    link.id = "cdf-consent-manage";
    link.href = "#gestion-temoins";
    link.textContent = "Gestion des témoins";
    link.addEventListener("click", function (event) {
      event.preventDefault();
      showBanner();
    });
    var holder = document.createElement("p");
    holder.style.cssText = "text-align:center;margin:1rem 0 0;font-size:.85rem;";
    holder.appendChild(link);
    var footer = document.querySelector("footer");
    if (footer) footer.appendChild(holder);
    else document.body.appendChild(holder);
  }

  function onReady() {
    buildBanner();
    buildManageLink();
  }

  if (readChoice() === "granted") loadPixel();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
