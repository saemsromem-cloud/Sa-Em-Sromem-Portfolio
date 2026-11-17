// Small progressive enhancements. The site works without JavaScript.
(function () {
  "use strict";
  var root = document.documentElement;

  // Theme toggle (the initial theme is set by a small script in <head>).
  var themeButton = document.querySelector(".theme-toggle");
  function syncThemeLabel() {
    if (!themeButton) return;
    var dark = root.dataset.theme === "dark";
    themeButton.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
  }
  syncThemeLabel();
  if (themeButton) {
    themeButton.addEventListener("click", function () {
      var next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) { /* storage unavailable */ }
      syncThemeLabel();
    });
  }

  // Mobile menu.
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (navToggle && nav) {
    function setMenu(open) {
      nav.classList.toggle("is-open", open);
      navToggle.setAttribute("aria-expanded", String(open));
      navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    navToggle.addEventListener("click", function () { setMenu(!nav.classList.contains("is-open")); });
    nav.addEventListener("click", function (event) { if (event.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (event) { if (event.key === "Escape") setMenu(false); });
  }

  // Highlight the nav link of the section currently in view.
  var links = Array.prototype.slice.call(document.querySelectorAll(".site-nav a[href^='#']"));
  if (links.length && "IntersectionObserver" in window) {
    var byId = {};
    links.forEach(function (link) { byId[link.getAttribute("href").slice(1)] = link; });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) { link.classList.remove("is-current"); link.removeAttribute("aria-current"); });
        var active = byId[entry.target.id];
        if (active) { active.classList.add("is-current"); active.setAttribute("aria-current", "true"); }
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    Object.keys(byId).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) observer.observe(section);
    });
  }
})();
