# Qilan (Kelland) Hong — personal website

Source for https://www.qilankellandhong.org — a hand-built, responsive static site hosted on GitHub Pages.

## How it's organized
- `*.html` — the pages (generated; edit `tools/build.py`, not these files)
- `assets/css/site.css` — all styling (fonts, colors, grid)
- `assets/js/site.js` — mobile menu, dropdown, photo viewer
- `assets/img/` — photos (full size + `-800` versions for fast loading)
- `assets/media/` — video, audio and PDF
- `tools/build.py` — page content and layout; run `python3 tools/build.py .` to rebuild

`new-page-1.html`, `awards-1.html`, `new-page.html`, `new-page-2.html` and `com.html` forward the old Squarespace addresses to the new pages.
