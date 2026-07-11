(function () {
  function encode(value) {
    return encodeURIComponent(value || "");
  }

  function initPropertyShare() {
    var root = document.querySelector(".property-media");
    var container = document.getElementById("property-share-buttons");
    if (!root || !container) return;

    var shareUrl = root.getAttribute("data-share-url") || window.location.href;
    var shareTitle = root.getAttribute("data-share-title") || document.title;
    var shareImage = root.getAttribute("data-share-image") || "";
    var shareText = shareTitle;

    var networks = [
      {
        id: "facebook",
        label: "Facebook",
        className: "bg-[#1877F2] text-white",
        href:
          "https://www.facebook.com/sharer/sharer.php?u=" + encode(shareUrl),
      },
      {
        id: "x",
        label: "X",
        className: "bg-black text-white",
        href:
          "https://twitter.com/intent/tweet?url=" +
          encode(shareUrl) +
          "&text=" +
          encode(shareText),
      },
      {
        id: "linkedin",
        label: "LinkedIn",
        className: "bg-[#0A66C2] text-white",
        href:
          "https://www.linkedin.com/sharing/share-offsite/?url=" +
          encode(shareUrl),
      },
      {
        id: "pinterest",
        label: "Pinterest",
        className: "bg-[#BD081C] text-white",
        href:
          "https://pinterest.com/pin/create/button/?url=" +
          encode(shareUrl) +
          "&media=" +
          encode(shareImage) +
          "&description=" +
          encode(shareText),
      },
      {
        id: "whatsapp",
        label: "WhatsApp",
        className: "bg-[#25D366] text-white",
        href:
          "https://wa.me/?text=" + encode(shareText + " " + shareUrl),
      },
      {
        id: "email",
        label: "Courriel",
        className: "bg-brand-navy text-white",
        href:
          "mailto:?subject=" +
          encode(shareText) +
          "&body=" +
          encode(shareText + "\n\n" + shareUrl),
      },
    ];

    networks.forEach(function (network) {
      var link = document.createElement("a");
      link.href = network.href;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.className =
        "inline-flex items-center rounded-full px-3 py-1.5 text-xs font-semibold transition-opacity hover:opacity-90 " +
        network.className;
      link.textContent = network.label;
      link.setAttribute("data-share", network.id);
      container.appendChild(link);
    });

    var copyBtn = document.createElement("button");
    copyBtn.type = "button";
    copyBtn.className =
      "inline-flex items-center rounded-full border border-gray-300 bg-white px-3 py-1.5 text-xs font-semibold text-brand-navy hover:bg-gray-50";
    copyBtn.textContent = "Copier le lien";
    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText(shareUrl).then(function () {
        copyBtn.textContent = "Lien copié!";
        setTimeout(function () {
          copyBtn.textContent = "Copier le lien";
        }, 1800);
      });
    });
    container.appendChild(copyBtn);

    if (navigator.share) {
      var nativeBtn = document.createElement("button");
      nativeBtn.type = "button";
      nativeBtn.className =
        "inline-flex items-center rounded-full bg-brand-red px-3 py-1.5 text-xs font-semibold text-white hover:bg-brand-navy";
      nativeBtn.textContent = "Partager";
      nativeBtn.addEventListener("click", function () {
        navigator.share({
          title: shareTitle,
          text: shareText,
          url: shareUrl,
        });
      });
      container.appendChild(nativeBtn);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPropertyShare);
  } else {
    initPropertyShare();
  }
})();
