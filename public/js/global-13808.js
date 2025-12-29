(function () {
  const init = () => {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector(".mobile-menu-btn");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (mobileMenuBtn && mobileMenu) {
      mobileMenuBtn.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
      });
    }

    // Counter animation
    const counters = document.querySelectorAll(".counter");
    const speed = 200;

    const animateCounter = (counter) => {
      const target = +counter.getAttribute("data-target");
      const count = +counter.innerText;
      const inc = target / speed;

      if (count < target) {
        counter.innerText = Math.ceil(count + inc);
        setTimeout(() => animateCounter(counter), 10);
      } else {
        counter.innerText = target + "+";
      }
    };

    const observerOptions = {
      threshold: 0.5,
    };

    const counterObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, observerOptions);

    counters.forEach((counter) => {
      counterObserver.observe(counter);
    });

    // Favorite button toggle
    const favoriteBtns = document.querySelectorAll(".favorite-btn");

    favoriteBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const svg = btn.querySelector("svg");
        const isFilled = svg.getAttribute("fill") === "currentColor";

        if (isFilled) {
          svg.setAttribute("fill", "none");
          btn.classList.remove("bg-[#AA1120]", "text-white");
          btn.classList.add("bg-white/90");
        } else {
          svg.setAttribute("fill", "currentColor");
          btn.classList.add("bg-[#AA1120]", "text-white");
          btn.classList.remove("bg-white/90");
        }
      });
    });

    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');

    navLinks.forEach((link) => {
      link.addEventListener("click", (e) => {
        const href = link.getAttribute("href");
        if (href.startsWith("#")) {
          e.preventDefault();
          const target = document.querySelector(href);
          if (target) {
            target.scrollIntoView({
              behavior: "smooth",
              block: "start",
            });
            // Close mobile menu if open
            if (mobileMenu) {
              mobileMenu.classList.add("hidden");
            }
          }
        }
      });
    });

    // Navbar background change on scroll
    const nav = document.querySelector("nav");

    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        nav.classList.add("shadow-xl");
      } else {
        nav.classList.remove("shadow-xl");
      }
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
