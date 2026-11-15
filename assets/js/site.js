// Navigation, dropdown and photo viewer.
(function () {
  "use strict";

  // ---- Mobile menu ----
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // ---- "Community Impact" dropdown ----
  document.querySelectorAll(".has-sub").forEach(function (item) {
    var btn = item.querySelector(".nav-sub-toggle");
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = item.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (e) {
    document.querySelectorAll(".has-sub.open").forEach(function (item) {
      if (!item.contains(e.target)) {
        item.classList.remove("open");
        item.querySelector(".nav-sub-toggle").setAttribute("aria-expanded", "false");
      }
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    document.querySelectorAll(".has-sub.open").forEach(function (item) {
      item.classList.remove("open");
      item.querySelector(".nav-sub-toggle").setAttribute("aria-expanded", "false");
    });
  });

  // ---- Photo viewer ----
  var shots = Array.prototype.slice.call(document.querySelectorAll("[data-full]"));
  if (shots.length) {
    var box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Photo viewer");
    box.innerHTML =
      '<button class="lb-close" aria-label="Close photo">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous photo">&#8249;</button>' +
      '<img alt=""><p></p>' +
      '<button class="lb-next" aria-label="Next photo">&#8250;</button>';
    document.body.appendChild(box);
    var img = box.querySelector("img");
    var cap = box.querySelector("p");
    var idx = 0;
    var last = null;

    function show(i) {
      idx = (i + shots.length) % shots.length;
      var s = shots[idx];
      img.src = s.getAttribute("data-full");
      img.alt = s.querySelector("img").alt;
      cap.textContent = s.getAttribute("data-caption") || "";
    }
    function close() {
      box.classList.remove("open");
      document.body.style.overflow = "";
      if (last) last.focus();
    }
    shots.forEach(function (s, i) {
      s.addEventListener("click", function () {
        last = s;
        show(i);
        box.classList.add("open");
        document.body.style.overflow = "hidden";
        box.querySelector(".lb-close").focus();
      });
    });
    box.querySelector(".lb-close").addEventListener("click", close);
    box.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    box.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    box.addEventListener("click", function (e) { if (e.target === box) close(); });
    document.addEventListener("keydown", function (e) {
      if (!box.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
  }

  // ---- Quick-glance numbers count up when they scroll into view ----
  var nums = document.querySelectorAll(".stat .num[data-to]");
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (nums.length && "IntersectionObserver" in window && !still) {
    var fmt = function (el, v) {
      var to = el.getAttribute("data-to");
      var dec = to.indexOf(".") > -1 ? to.split(".")[1].length : 0;
      var s = v.toFixed(dec);
      if (el.getAttribute("data-comma") === "1") s = Number(s).toLocaleString("en-US");
      el.textContent = el.getAttribute("data-pre") + s + el.getAttribute("data-suf");
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var el = en.target, end = parseFloat(el.getAttribute("data-to")), t0 = null, dur = 1100;
        if (end < 4) return; // tiny numbers just appear
        var tick = function (t) {
          if (!t0) t0 = t;
          var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
          fmt(el, end * e);
          if (k < 1) requestAnimationFrame(tick);
        };
        fmt(el, 0);
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { io.observe(n); });
  }
  // ---- Gentle fade-in as sections scroll into view ----
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!calm && "IntersectionObserver" in window) {
    var blocks = document.querySelectorAll(".page > .grid, .page > .home-intro, .explore, .page > .collage");
    document.documentElement.classList.add("js-reveal");
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); seen.unobserve(en.target); }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -6% 0px" });
    blocks.forEach(function (b) { b.classList.add("reveal"); seen.observe(b); });
  }
})();
