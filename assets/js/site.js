// Navigation, photo viewer and (preview only) style picker.
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

  // ---- Style picker: only on preview builds (body has data-preview) ----
  if (document.body.hasAttribute("data-preview")) {
    var themes = [
      ["classic", "Classic", "White and clean, closest to your current site"],
      ["field", "Field Notes", "Soft sage paper and a serif, for the sustainability work"],
      ["studio", "Studio", "Bold type and cobalt blue, more modern"]
    ];
    var saved = null;
    try { saved = localStorage.getItem("qkh-theme"); } catch (e) {}
    if (saved) document.documentElement.setAttribute("data-theme", saved);

    var panel = document.createElement("div");
    panel.className = "style-picker";
    panel.innerHTML = "<p>Preview a style</p><div class='opts'></div><button class='hide'>Hide this panel</button>";
    var opts = panel.querySelector(".opts");
    themes.forEach(function (t) {
      var b = document.createElement("button");
      b.innerHTML = t[1] + "<span>" + t[2] + "</span>";
      b.setAttribute("aria-pressed", String(document.documentElement.getAttribute("data-theme") === t[0]));
      b.addEventListener("click", function () {
        document.documentElement.setAttribute("data-theme", t[0]);
        try { localStorage.setItem("qkh-theme", t[0]); } catch (e) {}
        opts.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
      });
      opts.appendChild(b);
    });
    panel.querySelector(".hide").addEventListener("click", function () { panel.remove(); });
    document.body.appendChild(panel);
  }
})();
