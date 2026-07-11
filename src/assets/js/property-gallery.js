(function () {
  function byId(id) {
    return document.getElementById(id);
  }

  function initPropertyGallery() {
    var root = document.querySelector(".property-media");
    if (!root) return;

    var uls = root.getAttribute("data-uls");
    var fallback = root.getAttribute("data-fallback-image") || "";
    var main = byId("property-gallery-main");
    var thumbs = byId("property-gallery-thumbs");
    var counter = byId("property-gallery-counter");
    var prevBtn = byId("property-gallery-prev");
    var nextBtn = byId("property-gallery-next");
    if (!main || !thumbs || !counter) return;

    var photos = [];
    var activeIndex = 0;

    function basePath() {
      return "/src/assets/images/proprietes/" + uls + "/";
    }

    function setPhoto(index) {
      if (!photos.length) return;
      activeIndex = (index + photos.length) % photos.length;
      main.src = basePath() + photos[activeIndex];
      main.alt = root.getAttribute("data-share-title") || "Photo de la propriété";
      counter.textContent = activeIndex + 1 + " / " + photos.length;
      thumbs.querySelectorAll("[data-index]").forEach(function (btn) {
        var selected = Number(btn.getAttribute("data-index")) === activeIndex;
        btn.classList.toggle("ring-2", selected);
        btn.classList.toggle("ring-brand-red", selected);
      });
    }

    function renderThumbs() {
      thumbs.innerHTML = "";
      photos.forEach(function (file, index) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.setAttribute("data-index", String(index));
        btn.className =
          "rounded-lg overflow-hidden border border-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-red";
        btn.innerHTML =
          '<img src="' +
          basePath() +
          file +
          '" alt="" class="w-full h-16 object-cover" loading="lazy">';
        btn.addEventListener("click", function () {
          setPhoto(index);
        });
        thumbs.appendChild(btn);
      });
    }

    function useFallback() {
      photos = [];
      if (fallback) {
        main.src = fallback.startsWith("/") ? fallback : "/" + fallback.replace(/^\.?\//, "");
      }
      counter.textContent = photos.length ? "1 / " + photos.length : "1 / 1";
      thumbs.innerHTML =
        '<p class="col-span-full text-sm text-gray-500">Galerie complète bientôt disponible.</p>';
    }

    fetch(basePath() + "manifest.json", { cache: "no-store" })
      .then(function (resp) {
        if (!resp.ok) throw new Error("manifest missing");
        return resp.json();
      })
      .then(function (manifest) {
        photos = Array.isArray(manifest.photos) ? manifest.photos : [];
        if (!photos.length) {
          useFallback();
          return;
        }
        renderThumbs();
        setPhoto(0);
      })
      .catch(function () {
        useFallback();
      });

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        setPhoto(activeIndex - 1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        setPhoto(activeIndex + 1);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPropertyGallery);
  } else {
    initPropertyGallery();
  }
})();
