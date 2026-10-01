(function () {
  var bar = document.getElementById("cdf-site-notice");
  if (!bar) return;
  var root = document.documentElement;
  var current = "";

  function sync() {
    var height = Math.ceil(bar.getBoundingClientRect().height);
    if (height <= 0) return;
    var next = height + "px";
    if (next === current) return;
    current = next;
    root.style.setProperty("--cdf-notice-h", next);
  }

  sync();

  if (window.ResizeObserver) {
    new ResizeObserver(sync).observe(bar);
  } else {
    window.addEventListener("resize", sync);
  }

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(sync);
  }
})();
