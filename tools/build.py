#!/usr/bin/env python3
"""Builds the static site.

Usage: python3 tools/build.py OUT_DIR

All page text and layout lives in this file. Each page is a photo banner
followed by sections laid out on a 12-column grid (text on one side, photo
collage on the other). On phones everything stacks into one column.
"""
import sys, os, html

OUT = sys.argv[1]
SITE = "https://www.qilankellandhong.org"
NAME = "Qilan (Kelland) Hong"
FONTS = "family=Bricolage+Grotesque:opsz,wght@12..96,700&family=DM+Sans:ital,wght@0,300;0,500;0,700;1,300"
E = html.escape
AC = ' aria-current="page"'

ICON_CHEV = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
             '<path d="m2.5 4.5 3.5 3.5 3.5-3.5"/></svg>')
ICON_MENU = ('<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">'
             '<path d="M2 5h14M2 9h14M2 13h14"/></svg>')


# ------------------------------------------------------------- building blocks
def cell(inner, col=None, row=None, cls=""):
    """A grid cell. col/row are CSS grid placements used on desktop only."""
    style = []
    if col: style.append(f"--col:{col}")
    if row: style.append(f"--row:{row}")
    st = f' style="{";".join(style)}"' if style else ""
    return f'<div class="cell {cls}"{st}>{inner}</div>'


def shot(name, alt, cap=None, ar=None):
    """A photo that opens full-size when clicked. ar crops it to an aspect ratio."""
    fill = f' fill" style="--ar:{ar}' if ar else ""
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    plain_cap = html.unescape(cap or "")
    return (f'<figure class="snap"><button type="button" class="shot{fill}" data-full="assets/img/{name}.jpg" '
            f'data-caption="{E(plain_cap)}" aria-label="Enlarge photo: {E(html.unescape(alt))}">'
            f'<img src="assets/img/{name}-800.jpg" alt="{E(html.unescape(alt))}" loading="lazy" decoding="async"></button>{c}</figure>')


def collage(*items, cols="1fr 1fr"):
    """Photos side by side (the column widths come from the original layout)."""
    return f'<div class="collage" style="grid-template-columns:{cols}">{"".join(items)}</div>'


def btn(text, url, external=True):
    ext = ' target="_blank" rel="noopener"' if external else ""
    return f'<p><a class="btn" href="{E(url)}"{ext}>{text}</a></p>'


def slides(src, title):
    open_url = src.replace("/pubembed?", "/pub?")
    return (f'<div class="embed"><iframe src="{E(src)}" title="{E(title)}" loading="lazy" allowfullscreen></iframe></div>'
            f'<p class="embed-link"><a href="{E(open_url)}" target="_blank" rel="noopener">Open the slides in a new tab</a></p>')


RULE = '<hr class="rule">'
_TILT = 0

# Hand-drawn arrows that replace the emoji arrows in captions
_DOWN = ('<svg class="doodle" viewBox="0 0 34 56" aria-hidden="true"><path d="M15 4c-6 10 8 18 3 30-1.5 4-1.5 9-1 16"/>'
         '<path d="M8 42l9 10 9-10"/></svg>')
_UP = _DOWN.replace('class="doodle"', 'class="doodle up"')
ARROWS = [("⬇️⬇️", _DOWN + _DOWN), ("⬇️", _DOWN), ("⬆️", _UP)]


def stat(num, label, href=None):
    """One quick-glance number. num like '600+', '$5,700', 'Top 1%'; digits count up on scroll."""
    import re
    m = re.search(r"[\d,]+(?:\.\d+)?", num)
    data = ""
    if m:
        pre, val, suf = num[:m.start()], m.group(0), num[m.end():]
        data = f' data-to="{val.replace(",", "")}" data-pre="{E(pre)}" data-suf="{E(suf)}" data-comma="{1 if "," in val else 0}"'
    tag, attr = ("a", f' href="{href}"') if href else ("div", "")
    return f'<{tag} class="stat"{attr}><span class="num"{data}>{E(num)}</span><span class="lbl">{label}</span></{tag}>'


def stats(*items):
    return f'<section class="stats" aria-label="At a glance">{"".join(items)}</section>'


STATS = {
    "index.html": stats(
        stat("3", "research papers, 2 published", "research.html"),
        stat("Top 1%", "Blue Ocean finalist out of 12,000+ students", "awards.html"),
        stat("600+", "people reached through 20+ Leaf by Leaf workshops", "leaf-by-leaf.html"),
        stat("$5,700", "in grants and fellowship funding", "vermighty.html"),
        stat("2nd", "of 3,000 at the GNEC Hackathon", "awards.html"),
        stat("14", "years of classical piano", "creative-athletic.html")),
    "research.html": stats(
        stat("3", "research papers"), stat("2", "published"),
        stat("~160", "survey participants in Ghana"), stat("99.6%+", "accuracy training CNNs at Harvard")),
    "awards.html": stats(
        stat("Top 1%", "of 12,000+ students from 163 countries"), stat("2nd", "of 3,000 hackathon participants"),
        stat("3", "Scholastic awards out of ~110,000 entrants"), stat("$700", "school grant for Vermighty")),
    "vermighty.html": stats(
        stat("$700", "in funding from the Sabrina Zhang Award"), stat("2", "composting stages: heat first, then worms"),
        stat("Top 100", "global finalist, Blue Ocean Competition")),
    "leaf-by-leaf.html": stats(
        stat("20+", "workshops designed and led"), stat("600+", "people reached"),
        stat("$5,000", "Dragon Kim Foundation funding"), stat("1", "original children’s book, published")),
    "leadership.html": stats(
        stat("600+", "finalist presentations judged for GNEC"), stat("3", "partner countries for Global Voices"),
        stat("7", "leadership and volunteer roles")),
    "creative-athletic.html": stats(
        stat("16", "years of dance"), stat("14", "years of classical piano"),
        stat("2nd", "in girls’ doubles, Montview League 2025"), stat("6", "years of vocal training")),
}


def grid(*cells):
    return f'<div class="grid">{"".join(cells)}</div>'


# ------------------------------------------------------------- page shell
NAV = [
    ("Home", "index.html"),
    ("Research", "research.html"),
    ("Awards", "awards.html"),
    ("Community Impact", [("Vermighty", "vermighty.html"), ("Leaf by Leaf", "leaf-by-leaf.html")]),
    ("Leadership", "leadership.html"),
    ("Creative & Athletic", "creative-athletic.html"),
]


def nav(current):
    out = []
    for label, target in NAV:
        if isinstance(target, list):
            cur = any(h == current for _, h in target)
            sub = "".join(f'<li><a href="{h}"{AC if h == current else ""}>{E(l)}</a></li>' for l, h in target)
            out.append(f'<li class="has-sub{" current" if cur else ""}"><button type="button" class="nav-sub-toggle" '
                       f'aria-expanded="false">{E(label)}{ICON_CHEV}</button><ul class="nav-sub">{sub}</ul></li>')
        else:
            out.append(f'<li><a href="{target}"{AC if target == current else ""}>{E(label)}</a></li>')
    return "".join(out)


def hero(img, title, role=None):
    r = f'<p class="role">{role}</p>' if role else ""
    return (f'<section class="hero"><img src="assets/img/{img}.jpg" alt="" fetchpriority="high">'
            f'<div><h1>{title}</h1>{r}</div></section>')


def page(filename, title, description, body, og_image="headshot", banner=""):
    full_title = NAME if filename == "index.html" else f"{title} · {NAME}"
    path = "" if filename == "index.html" else filename[:-5]
    body_cls = ' class="has-hero"' if banner else ""
    body = body.replace("{{STATS}}", "")
    for emo, svg in ARROWS:
        body = body.replace(emo, svg)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(NAME)}">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fbfff2">
<link rel="icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS}&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body{body_cls}>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="bar">
    <a class="brand" href="index.html">{E(NAME)}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{ICON_MENU}Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Main"><ul class="nav-list">{nav(filename)}</ul></nav>
  </div>
</header>
<main id="main">
{banner}
<div class="page">
{body}
</div>
</main>
<footer class="site-footer" id="contact">
  <h4>Contact Me</h4>
  <p><a href="mailto:qilan.k.hong@gmail.com">qilan.k.hong@gmail.com</a></p>
  <p><a href="tel:+14159289558">+1 (415) 928-9558</a></p>
  <p>San Gabriel, California</p>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(doc)


def redirect(old, new):
    with open(os.path.join(OUT, old), "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Moved</title><link rel="canonical" href="{SITE}/{new[:-5]}">
<meta http-equiv="refresh" content="0; url={new}"><meta name="robots" content="noindex">
</head><body><p>This page has moved to <a href="{new}">{new}</a>.</p></body></html>
""")


# ------------------------------------------------------------- pages
SLIDES_MGMT = ("https://docs.google.com/presentation/d/e/2PACX-1vTe67A3n7HO0X2mjyyBOLw9fHLFjew2IUoqKafi6yZei86SqPlHxgwB_gkpMh_a6k4sWLaTgeFFXKUF"
               "/pubembed?start=false&loop=false&delayms=3000")
SLIDES_VERM = ("https://docs.google.com/presentation/d/e/2PACX-1vQHkLiqwA7VuB54ixppdjmDRJgMeE5eYS1R8ZqAdnL8dCpzvVyZGIUN1m5UR9Pyv_hCopj_hogTLrgt"
               "/pubembed?start=false&loop=false&delayms=3000")


def build_home():
    cards = [("research.html", "research-genomics", "Research"), ("awards.html", "award-mun-delegate", "Awards"),
             ("vermighty.html", "verm-terrapalooza-1", "Vermighty"), ("leaf-by-leaf.html", "lbl-workshop-teaching", "Leaf by Leaf"),
             ("leadership.html", "lead-global-initiatives", "Leadership"), ("creative-athletic.html", "ca-dance-stage", "Creative &amp; Athletic")]
    grid_html = "".join(f'<a class="explore-card" href="{h}"><img src="assets/img/{i}-800.jpg" alt="" loading="lazy"><span>{t}</span></a>'
                        for h, i, t in cards)
    body = '<div class="home-intro">' + grid(
        cell("<h2>Welcome to my portfolio!</h2>"
             "<p>My name is Qilan (Kelland) Hong, and I am currently a senior at Polytechnic School in Pasadena, California.</p>"
             "<p>I am fascinated by the hidden systems that shape how people think and make decisions. Across much of my work, I explore the intersection of consumer behavior, sustainability, and design, often questioning how small changes can lead to larger social or environmental impact.</p>"
             "<p>Feel free to explore this page to learn more about my research, environmental initiatives, projects, leadership, and more. I hope it gives you a glimpse into the questions that drive my curiosity and the ways I’ve tried to turn those questions into action.</p>"
             '<div class="btn-row"><p><a class="btn" href="assets/media/qilan-hong-resume.pdf" target="_blank" rel="noopener">View my resume</a></p>'
             '<p><a class="btn ghost" href="research.html">Explore my work</a></p></div>',
             "1 / 8", "1"),
        cell('<div class="home-photo"><img src="assets/img/headshot.jpg" alt="Portrait of Qilan (Kelland) Hong" width="1200" height="1500"></div>',
             "9 / -1", "1"),
    ) + "</div>"
    body += "{{STATS}}"
    body += f'<section class="explore" aria-label="Explore my work"><div class="explore-grid">{grid_html}</div></section>'
    page("index.html", "Home",
         "Qilan (Kelland) Hong, a senior at Polytechnic School in Pasadena, California, exploring consumer behavior, sustainability, and design.",
         body)


def build_research():
    p1 = ("<h4>Hybrid Consumer Identity in Ghanaian Fashion: The Coexistence of Sustainable and Fast-Fashion Consumption Among Young Adults</h4>"
          "<p class=\"meta\">Johns Hopkins University (Pioneer Research Institute) · Summer to Fall 2026</p>"
          "<p>In the Pioneer Research Institute, I worked with a Johns Hopkins University professor to produce a cross-sectional study combining a literature review and online survey to investigate the existence of a hybrid consumer in Ghana that integrates both sustainable and fast-fashion clothing into their identity. With a personal interest in the sustainability of fashion and interning for a textile sustainability nonprofit, Unkara Fashion Collective, I directly drew on my own experiences and questions about the tension between ethical values and everyday consumer choices when developing my research topic.</p>"
          + shot("research-ghana-survey", "Survey charts from the Ghanaian fashion study", "Snapshot of primary survey data from ~160 participants")
          + btn("Read it here!", "https://docs.google.com/document/d/1C-m4gjO5XDZR9Du6J9tVdPWnFCYGEW_X/edit?usp=sharing&ouid=107115511025543877695&rtpof=true&sd=true"))
    p2 = ("<h4>Understanding Sectoral Responses to Tariff Uncertainty via a High-Dimensional Mediation Analysis</h4>"
          "<p class=\"meta\">Penn State University (Prof. Runze Li) · 2025 - Present · <em>published</em></p>"
          "<p>Driven by my interest in how large-scale environmental and economic changes alter market behavior, I worked with Dr. Runze Li to produce a primary study examining how financial fundamentals mediated the relationship between company sector and stock-market performance during major tariff-affected periods in 2025. I utilized high-dimensional mediation analysis to identify which financial variables helped explain differences in sector-level shock responses.</p>"
          + btn("Read it on arXiv", "https://doi.org/10.48550/arXiv.2609.33881"))
    p3 = ("<h4>Environmental and Genetic Influences in Alcohol Use Disorder</h4>"
          "<p class=\"meta\">National Human Genome Research Institute (Genomics: Insight) · 2026 · <em>published</em></p>"
          "<p>Growing up in a health-conscious household, I was highly curious about how environmental and societal factors can influence one's health. This led me to work with four others to write a paper investigating how environmental and biological factors influence alcohol use and addiction. I synthesized the research on machine-learning models used to predict things like relapse and treatment outcomes, and wrote about how environmental variables interact with susceptibility from genetics.</p>"
          + btn("Read it on Genomics Insight (NHGRI)", "https://www.unlockinglifescode.org/genomics-insights/environmental-and-genetic-influences-alcohol-use-disorder"))
    body = grid(cell(p1, "1 / 5"), cell(p2, "5 / 9"), cell(p3, "9 / -1"), RULE)
    body += grid(
        cell("<h4>Technical &amp; Research Preparation</h4>"
             "<p><strong>Mathematical Elements of AI</strong></p>"
             "<p class=\"meta\">Harvard University (Pre-College Program) · Summer 2025</p>"
             "<p>Four weeks exploring the mathematics behind neural networks through multivariable calculus and linear algebra. I implemented gradient descent and backpropagation from scratch before training CNNs on MNIST and CIFAR, reaching 99.6%+ classification accuracy. For my final project, I trained a computer-vision model to identify playing cards and integrated it into a functioning Blackjack game.</p>",
             "1 / 6"),
        cell(collage(shot("research-harvard", "Harvard Pre-College class group photo", ar="1 / 1"),
                     shot("research-harvard-training", "Laptop showing the card classifier training", "Training the card classifier", ar="2 / 3"),
                     cols="1.8fr 1fr"), "7 / -1"),
        RULE)
    body += grid(
        cell("<h4>Other research-related programs</h4>"
             '<ul class="programs">'
             '<li><p><a href="https://globalyouth.wharton.upenn.edu/programs-courses/mgmt-0001-principles-of-management/" target="_blank" rel="noopener"><strong>Wharton Global Youth Program, MGMT 0001</strong></a>: Principles of Management (Fall 2025). Analyzed business strategy through case studies including Trader Joe’s and Gong Cha; final project examined Uber’s failed China expansion and proposed a localized “Build + Borrow” strategy.</p></li>'
             '<li><p><a href="https://label-laboratory.org/label-training-program/" target="_blank" rel="noopener"><strong>Los Angeles Behavioral Economics Laboratory</strong></a>: trainee, (2025-Present). Training in behavioral and experimental research methodology across topics including AI, housing, and the environment.</p></li>'
             '<li><p><a href="https://www.way.org.my/" target="_blank" rel="noopener"><strong>World Assembly of Youth</strong></a>, research intern (2024-2025). Wrote five 10+ page research papers on education, poverty, ICT access, leisure, and juvenile delinquency to support WAY’s youth-development work, connecting each to the UN Sustainable Development Goals.</p></li>'
             '<li><p><a href="https://precollege.usc.edu/summer-programs/analytics-the-power-of-data-for-businesses/" target="_blank" rel="noopener"><strong>USC Data Analytics Pre-College</strong></a> (Summer 2024). Studied statistical analysis and completed a final project using k-means clustering on a 2,000+ student dataset with Python, Pandas, and Tableau.</p></li>'
             "</ul>", "1 / 7"),
        cell(slides(SLIDES_MGMT, "WGYP MGMT 0001 Final Project") + '<p class="cap">WGYP MGMT 0001 Final Project</p>'
             + '<div style="margin-top:1.2rem">' + shot("research-wharton-class", "Video-call grid of the MGMT 0001 class", "WGYP MGMT 0001 Class Photo") + "</div>",
             "8 / -1"))
    page("research.html", "Research",
         "Research by Qilan (Kelland) Hong on sustainable fashion in Ghana, sector responses to tariff uncertainty, and genetic influences in alcohol use disorder.",
         body, "research-genomics", hero("research-genomics", "Research"))


def award(title, meta, text, extra, media, media_col="7 / -1"):
    return grid(cell(f"<h4>{title}</h4><p class=\"meta\">{meta}</p><p>{text}</p>{extra}", "1 / 7"),
                cell(media, media_col), RULE)


def build_awards():
    body = award("Recipient, Sabrina Zhang Award", "Polytechnic School · Grade 11",
                 '$700 school grant to fund <a href="vermighty.html">Vermighty</a>, turning a set of sketches into a two-chamber composting system now situated on campus for testing and school curriculum integration.',
                 "", shot("verm-hero", "Building the Vermighty composting system", ar="16 / 9"), "8 / -1")
    body += award("Top 100 Finalist (Top 1%), Blue Ocean Student Entrepreneur Competition", "Blue Ocean Student Entrepreneurs Corp · Grade 10",
                  "Selected as a Top 100 Global Finalist from 12,000+ student participants across 163 countries for Vermighty.",
                  btn("Watch the pitch here!", "https://www.youtube.com/watch?v=ykseSfgmh6g&t=30s"),
                  shot("award-blue-ocean-cert", "Blue Ocean Competition Top 100 finalist certificate"), "9 / -1")
    body += award("Award-Winning Photographer, Scholastic Art &amp; Writing Awards", "Alliance for Young Artists &amp; Writers · Grade 11",
                  "Two Silver Keys and an Honorable Mention in Photography, out of roughly 110,000 entrants. The pieces were <em>Above the Noise</em>, <em>The Crowd and the Sea</em>, and <em>Stones That Remember</em>.",
                  "",
                  collage(shot("award-above-the-noise", "Above the Noise: a fiery orange sky over a dark silhouette", "Above the Noise", ar="1 / 1"),
                          shot("award-crowd-and-sea", "The Crowd and the Sea: waves at sunset", "The Crowd and the Sea", ar="4 / 5"),
                          shot("award-stones-that-remember", "Stones That Remember: a cobblestone lane between old brick houses", "Stones That Remember", ar="2 / 3"),
                          cols="1fr 1fr 1fr"))
    body += award("Outstanding Delegate, Northwood High School Model UN Conference", "Grade 11",
                  "Represented Al Gore in a committee on energy consumption and climate policy, earning Outstanding Delegate for my research, speeches, and negotiation.",
                  "",
                  collage(shot("award-mun-delegate", "Receiving the Outstanding Delegate award on stage", ar="4 / 3"),
                          shot("award-mun-group", "Polytechnic Model UN delegation", ar="4 / 3")))
    body += grid(cell("<h4>2nd Place, GNEC Hackathon</h4><p class=\"meta\">Global NGO Executive Committee · Grade 10</p>"
                      "<p>Selected out of 3,000 participants for \"TarantulaX,\" a solar-powered reverse osmosis drone. I've since stayed on with GNEC as a partnerships coordinator and a judge.</p>"
                      + btn("Check out TarantulaX!", "https://devpost.com/software/tarantulax"), "1 / 7"),
                 cell(shot("award-drone", "Line drawing of the TarantulaX drone", "Drone Design"), "8 / 11"))
    page("awards.html", "Awards",
         "Awards and honors of Qilan (Kelland) Hong: Sabrina Zhang Award, Blue Ocean Top 100, Scholastic Art & Writing Awards, Model UN and GNEC Hackathon.",
         body, "award-mun-delegate", hero("award-mun-delegate", "Awards &amp; Honors"))


def build_vermighty():
    body = grid(cell('<p class="statement">Vermighty is a <u>hybrid thermophilic and vermicomposting system</u> I designed, engineered, and built to test whether the two processes can work sequentially at a micro-scale. The system uses heat first for faster decomposition, then worms to improve compost quality.</p>'))
    body += '<div class="spacer"></div>'
    body += grid(
        cell('<p class="cap">Early Vermighty Design Sketches ⬇️⬇️</p>', "6 / -1", "1", "center"),
        cell(shot("verm-model", "Technical drawing of the Vermighty model"), "1 / 6", "2"),
        cell(slides(SLIDES_VERM, "Early Vermighty Design Sketches"), "6 / -1", "2"),
        RULE)
    left = ("<p>I’m currently testing Vermighty on my high school campus with <strong>$700 in funding</strong> from the Sabrina Zhang Award, and I’ve <strong>presented the project</strong> at our Earth Day event, Terrapalooza.</p>"
            + collage(shot("verm-terrapalooza-1", "Presenting Vermighty at Terrapalooza", ar="8 / 7"),
                      shot("verm-terrapalooza-2", "Title slide: Vermighty, Rethinking Food Systems", ar="8 / 7"))
            + '<p class="cap">Presenting Vermighty at Terrapalooza ⬆️</p>'
            + '<div class="spacer sm"></div>'
            + collage(shot("verm-assembling", "Assembling Vermighty on campus", ar="4 / 3"),
                      shot("verm-upclose", "Vermighty set up in its frame on campus", ar="4 / 3"))
            + '<p class="cap">Assembling Vermighty on Campus ⬆️</p>')
    right = ("<p>I’m also <strong>partnering with Epicurean</strong>, our school food service, to collect leftover food for compost testing. Once the compost is ready, I <strong>give it to our school’s Poly Planters club</strong> to use in their garden beds, creating a <strong>small circular system</strong> on campus.</p>"
             + collage('<div style="padding-top:2.2rem">' + shot("verm-leftovers", "School food leftovers used for compost", ar="3 / 4")
                       + '<p class="cap" style="text-align:center">School leftovers Vermighty used</p></div>',
                       '<div>' + shot("verm-location", "Vermighty’s spot on campus", ar="4 / 3")
                       + '<p class="cap">Location of Vermighty to ⬇️⬇️</p>'
                       + '<div style="margin-left:12%">' + shot("verm-garden-beds", "The Poly Planters garden beds", ar="4 / 3")
                       + '<p class="cap" style="text-align:center">⬆️ Location of Poly Planters garden beds</p></div></div>',
                       cols="1fr 1.75fr"))
    body += grid(cell(left, "1 / 7", "1"), '<div class="vrule" style="--col:7 / 8;--row:1"></div>', cell(right, "8 / -1", "1"))
    body += '<hr class="rule short">'
    body += grid(cell("<p>My long-term goal is to<strong> build Vermighty into the school curriculum</strong> so other students can continue running and developing it beyond my own involvement. I’m currently working toward that goal through an <strong>Independent Study</strong> with a teacher focused on developing Vermighty’s curriculum and long-term implementation.</p>",
                      "4 / 10", None, "center"))
    page("vermighty.html", "Vermighty",
         "Vermighty: a hybrid thermophilic and vermicomposting system designed, engineered, and built by Qilan (Kelland) Hong.",
         body, "verm-terrapalooza-1", hero("verm-hero", "Vermighty", "Founder · 2025 - present"))


def build_lbl():
    body = grid(cell('<p class="statement">I co-founded Leaf by Leaf after noticing that children were often told what foods were healthy without being given much ownership over those choices. I developed our hands-on approach around <u>planting, caring for, and ultimately choosing whether to try food they grew themselves</u>.</p>', "1 / 12"),
                cell(btn("Visit Leaf by Leaf’s website here to learn more about my work!", "https://www.leaf-by-leaf.org/home"), "1 / -1", None, "center"))
    body += '<div class="spacer"></div>'
    left = ("<p>I designed and led <strong>20+ workshops</strong> across schools, youth centers, a rescue mission, a children’s museum, and community events, <strong>reaching 600+ people</strong>.</p>"
            + collage(shot("lbl-workshop-class", "A class posing with their Leaf by Leaf growing kits", ar="4 / 5"),
                      shot("lbl-virtual", "Leading a virtual workshop from a laptop", ar="4 / 5"))
            + '<p class="cap">Leading hands-on workshops, in-person and virtually!</p>'
            + '<div class="spacer sm"></div>'
            + collage(shot("lbl-workshop-teaching", "Teaching a workshop in a middle-school classroom", ar="3 / 4"),
                      shot("lbl-workshop-collage", "Students raising hands during a workshop", ar="3 / 4")))
    right = ("<p>I co-wrote and published our <strong>original children’s book</strong> and developed <strong>take-home growing kits </strong>to extend the experience beyond each workshop. We have donated many of both.</p>"
             + collage('<div>' + shot("lbl-book", "Cover of the Leaf by Leaf children’s book", "Our original CHILDREN’S BOOK!", ar="6 / 5")
                       + btn("Check out Leaf by Leaf on AMAZON here", "https://www.amazon.com/Leaf-Qilan-Hong/dp/B0H8BXJ7BD")
                       + shot("lbl-books-kids", "Kids holding Leaf by Leaf books outdoors", "Donated take-home growing kits!", ar="6 / 5") + "</div>",
                       shot("lbl-donations", "Book donations to community partners", "Book donations!", ar="3 / 5"),
                       cols="1.25fr 1fr")
)
    body += grid(cell(left, "1 / 6"), cell(right, "7 / -1"), RULE)
    body += grid(cell("<h4>Recognition</h4>", "1 / -1", None, "center"),
                 cell(shot("lbl-dragon-kim", "Receiving Dragon Kim Foundation Fellow medals", ar="4 / 3")
                      + '<p class="cap">Recognized as Dragon Kim Foundation Fellows with $5,000 in funding</p>', "2 / 6"),
                 cell(shot("lbl-cbs", "Stills from the CBS News segment", ar="16 / 10")
                      + '<p class="cap">Featured in CBS News</p>'
                      + '<p><a href="https://www.youtube.com/watch?v=zIxP-wy2kek" target="_blank" rel="noopener"><strong>Full News Snippet Here!</strong></a></p>', "7 / 12"))
    page("leaf-by-leaf.html", "Leaf by Leaf",
         "Leaf by Leaf, co-founded by Qilan (Kelland) Hong: 20+ hands-on growing workshops reaching 600+ people, an original children’s book and take-home growing kits.",
         body, "lbl-workshop-teaching", hero("lbl-hero", "Leaf by Leaf", "Co-Founder · 2025 - Present"))


def build_leadership():
    def entry(title, meta, text, media=None, extra=""):
        cells = [cell(f"<h4>{title}</h4><p class=\"meta\">{meta}</p>{text}{extra}", "1 / 8" if media else "1 / 10")]
        if media: cells.append(cell(media, "8 / -1"))
        cells.append(RULE)
        return grid(*cells)

    body = entry("Terrapalooza", "Programming Committee Member &amp; Presenter, Polytechnic School · 2025 – present",
                 "<p>Terrapalooza is Poly’s Earth Day festival. Working on the programming committee, I design climate education workshops and speaker events. </p>"
                 "<p>I also present! In 2026’s Terrapalooza, I presented a <strong>climate constitution</strong> I wrote to peers and faculty, which connected behavioral economics, intergenerational equity, and environmental design policy into one framework. I also told the story behind <strong><a href=\"vermighty.html\">Vermighty</a></strong>.</p>",
                 shot("lead-climate-treaty", "Presenting the climate constitution at Terrapalooza", ar="6 / 5"))
    body += entry("Poly Global Voices Club", "Head of Operations · 2025 – present",
                  "<p>Global Voices is a student-led international club connecting high schoolers around the world to share varying views on global issues. For Global Voices, I handle the communications and operational coordination across our many partners spanning Australia, Singapore, and Finland. I’ve assisted in <strong>hosting a school event </strong>with a visiting professor (Dr. Steven Lamy), <strong>presented research</strong> on the Fukushima wastewater release, and <strong>co-organized a school-wide clothing swap</strong>.</p>",
                  collage(shot("lead-clothing-swap", "The school-wide clothing swap", ar="6 / 5"),
                          shot("lead-global-initiatives", "With Dr. Steven Lamy at a Global Initiatives event", ar="6 / 5")))
    body += entry("GNEC Hackathon", "Partnerships Coordinator &amp; Judge, Global NGO Executive Committee · 2024 – present",
                  "<p>After coming second in this hackathon in 2024, I stayed as an intern. I started as <strong>creating promotional graphics </strong>for social media. Now, I<strong> lead partner and sponsor outreach,</strong> continuing to design marketing and branding materials, <strong>moderate hackathon events</strong> such as opening/closing ceremonies, and <strong>judge</strong> (600+ finalist presentations up to date). I also have <strong>built an automated certificate distribution system </strong>after noticing the manual inefficiency.</p>")
    body += entry("Global Scholar", "Polytechnic School · 2025 - present",
                  "<p>As a Global Scholar at Polytechnic School, I attend <strong>speaker events</strong> with <strong>diplomats</strong> and <strong>policy experts</strong>, participate in cross-cultural exchanges, and write a <strong>blog</strong> analyzing international affairs, from geopolitical conflicts to global environmental policies. I also serve as a Global Ambassador, helping <strong>organize events and discussions</strong> that foster global awareness on campus.</p>",
                  extra=btn("Visit my blog here!", "https://kellandhgip.squarespace.com/"))
    body += entry("Judiciary Council", "Polytechnic School · 2025 - present",
                  "<p>I was elected and interviewed into the Judiciary Council, where I focus in the Policy and Student Voice subcommittee on reviewing student conduct cases to represent the student body.</p>")
    body += grid(
        cell("<h4>Volunteering</h4>"
             "<p><strong>The Huntington</strong></p><p class=\"meta\">Museum Education &amp; Gardening Volunteer · 2026 – present</p>"
             "<p>At the Huntington, I lead hands-on cultural learning in the Chinese Garden’s Flowery Brush Library for public visitors and help facilitate sustainability-focused events such as the Huntington’s plant sale. </p>"
             "<p class=\"gap\"><strong>Boys &amp; Girls Club (Pasadena)</strong></p><p class=\"meta\">Volunteer · 2025 – present</p>"
             "<p>I volunteer weekly at the Boys and Girls Club to assist with after-school enrichment and leisure activities. I have also brought my own advocacy work–<a href=\"leaf-by-leaf.html\">Leaf by Leaf</a>–to multiple Boys and Girls Clubs locations.</p>",
             "1 / 7"),
        cell(collage(shot("lead-huntington", "Volunteering at the Huntington’s Chinese Garden", "The Huntington", ar="4 / 5"),
                     shot("lbl-workshop-collage", "A Leaf by Leaf workshop with Boys and Girls Club kids", "Boys &amp; Girls Club", ar="4 / 5")),
             "7 / -1"))
    page("leadership.html", "Leadership",
         "Leadership and volunteering by Qilan (Kelland) Hong: Terrapalooza, Global Voices, GNEC, Global Scholar, Judiciary Council, The Huntington and Boys & Girls Club.",
         body, "lead-global-initiatives", hero("lead-global-initiatives", "Leadership and Volunteering"))


def build_creative():
    def entry(title, meta, text, media, extra=""):
        return grid(cell(f"<h3>{title}</h3><p class=\"meta\">{meta}</p>{text}{extra}", "1 / 7"), cell(media, "7 / -1"), RULE)

    body = entry("Badminton", "Polytechnic School · Varsity · 2025 - present",
                 "<p>I’ve loved playing badminton with my family since I was young, and being able to play with close friends on a school team was a dream come true. I play mixed and girls doubles, and placed second in girls’ doubles in the Montview League in 2025.</p>",
                 collage(shot("ca-badminton", "Playing badminton in the school gym", ar="4 / 5"),
                         shot("ca-badminton-team", "The Polytechnic badminton team with their medals", ar="7 / 6"), cols="1fr 1.4fr"))
    body += entry("Dance", "2010 - present",
                  "<p>I’ve been dancing since I was two, starting with ballet. At nine, I performed with San Francisco Ballet despite being a year below the program’s minimum age. As I moved between schools, cities, and countries, I explored styles including K-pop, jazz, and hip-hop. Today, I primarily dance hip-hop. Below is a piece I co-choreographed for my school’s dance show.</p>"
                  '<p class="cap">⬇️⬇️</p>'
                  '<video class="player" controls preload="metadata" playsinline poster="assets/img/ca-dance-video-poster.jpg">'
                  '<source src="assets/media/dance-show.mp4" type="video/mp4">Your browser can’t play this video.</video>',
                  collage(shot("ca-dance-collage", "Dance rehearsal and performance collage", ar="4 / 5"),
                          shot("ca-dance-stage", "Mid-kick on stage under purple lights", ar="4 / 5")))
    body += entry("Piano", "2012 - present",
                  "<p>I’ve always seen piano as an outlet of expression and relaxation. I’ve played classical piano for 14 years now, and competed in multiple competitions with awards. </p>",
                  collage(shot("ca-piano", "Performing on a grand piano", ar="4 / 3"),
                          shot("ca-piano-competition", "At an international music competition", ar="4 / 3")),
                  btn("Check out a chamber music piece I played here!", "https://www.youtube.com/watch?v=4skXd9GU03w"))
    body += grid(cell("<h3>Singing/Vocal</h3><p class=\"meta\">2020 - present</p>"
                      "<p>I’ve always loved singing, but formally began taking lessons in 2020. Since then, I’ve worked on vocal technique, interpretation, and performance through a mix of contemporary and musical theatre repertoire. I have included one professionally recorded cover I did here.</p>", "1 / 7"),
                 cell('<div class="audio-card"><div class="t">Someone You Loved Cover</div><div class="a">Lewis Capaldi</div>'
                      '<audio controls preload="none" src="assets/media/someone-you-loved-cover.mp3"></audio></div>', "8 / 12"))
    page("creative-athletic.html", "Creative & Athletic",
         "Badminton, dance, piano and singing: the creative and athletic side of Qilan (Kelland) Hong.",
         body, "ca-dance-stage", hero("ca-dance-show", "Creative &amp; Athletic"))


def build_404():
    page("404.html", "Page not found", "This page doesn't exist.",
         '<h2>Page not found</h2><p>This page doesn’t exist or has moved.</p>' + btn("Go to the homepage", "index.html", external=False))


os.makedirs(OUT, exist_ok=True)
build_home(); build_research(); build_awards(); build_vermighty(); build_lbl()
build_leadership(); build_creative(); build_404()
# Old Squarespace addresses keep working
redirect("new-page-1.html", "research.html")
redirect("awards-1.html", "awards.html")
redirect("new-page.html", "leadership.html")
redirect("new-page-2.html", "creative-athletic.html")
redirect("com.html", "index.html")
print("built", OUT)
