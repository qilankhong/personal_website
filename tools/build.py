#!/usr/bin/env python3
"""Builds the static site into the repo folder.

Usage: python3 build.py OUT_DIR [--preview] [--theme classic|field|studio]

Every page shares one header, footer and set of helpers below, so adding
a new project means adding one entry to a page's content.
"""
import sys, os, html

OUT = sys.argv[1]
PREVIEW = "--preview" in sys.argv
THEME = sys.argv[sys.argv.index("--theme") + 1] if "--theme" in sys.argv else "classic"
SITE = "https://www.qilankellandhong.org"
NAME = "Qilan (Kelland) Hong"

FONTS = {
    "classic": "family=Hanken+Grotesk:wght@400;500;600;700",
    "field": "family=Public+Sans:wght@400;500;600;700&family=Young+Serif",
    "studio": "family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Figtree:wght@400;500;600;700",
}

E = html.escape
AC = " aria-current=\"page\""

ICON_EXT = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
            '<path d="M6 3H3v10h10v-3M9 2h5v5M14 2 7 9"/></svg>')
ICON_CHEV = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
             '<path d="m2.5 4.5 3.5 3.5 3.5-3.5"/></svg>')
ICON_MENU = ('<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">'
             '<path d="M2 5h14M2 9h14M2 13h14"/></svg>')


# ---------------------------------------------------------------- helpers
def img(name, alt, caption=None):
    """One photo that opens full-size in the viewer."""
    cap = f"<figcaption>{E(caption)}</figcaption>" if caption else ""
    return (f'<figure><button type="button" data-full="assets/img/{name}.jpg" '
            f'data-caption="{E(caption or alt)}" aria-label="Enlarge photo: {E(alt)}">'
            f'<img src="assets/img/{name}-800.jpg" alt="{E(alt)}" loading="lazy" decoding="async">'
            f"</button>{cap}</figure>")


def gallery(*figs, cls=""):
    return f'<div class="gallery {cls}">{"".join(figs)}</div>'


def links(*pairs):
    items = "".join(f'<a href="{E(u)}" target="_blank" rel="noopener">{E(t)}{ICON_EXT}</a>' for t, u in pairs)
    return f'<div class="links">{items}</div>'


def slides(src, title):
    """Responsive Google Slides embed, plus a link in case the embed is blocked."""
    open_url = src.replace("/pubembed?", "/pub?")
    return (f'<figure class="media"><div class="embed"><iframe src="{E(src)}" title="{E(title)}" '
            f'loading="lazy" allowfullscreen></iframe></div>'
            f'<figcaption>{E(title)} · <a href="{E(open_url)}" target="_blank" rel="noopener">Open the slides in a new tab</a></figcaption></figure>')


def entry(title, meta, body, media="", eid=None):
    idattr = f' id="{eid}"' if eid else ""
    solo = "" if media else " solo"
    m = f'<p class="meta">{meta}</p>' if meta else ""
    right = f"<div>{media}</div>" if media else ""
    return f'<article class="entry{solo}"{idattr}><div><h3>{title}</h3>{m}{body}</div>{right}</article>'


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
            sub = "".join(
                f'<li><a href="{h}"{AC if h == current else ""}>{E(l)}</a></li>'
                for l, h in target)
            out.append(f'<li class="has-sub{" current" if cur else ""}"><button type="button" class="nav-sub-toggle" '
                       f'aria-expanded="false">{E(label)}{ICON_CHEV}</button><ul class="nav-sub">{sub}</ul></li>')
        else:
            ac = ' aria-current="page"' if target == current else ""
            out.append(f'<li><a href="{target}"{ac}>{E(label)}</a></li>')
    return "".join(out)


def page(filename, title, description, body, og_image="headshot"):
    full_title = NAME if filename == "index.html" else f"{title} · {NAME}"
    path = "" if filename == "index.html" else filename[:-5]
    fonts = "&".join(FONTS.values()) if PREVIEW else FONTS[THEME]
    preview_attr = " data-preview" if PREVIEW else ""
    doc = f"""<!DOCTYPE html>
<html lang="en" data-theme="{THEME}">
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
<link rel="icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body{preview_attr}>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">{E(NAME)}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{ICON_MENU}Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Main"><ul class="nav-list">{nav(filename)}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer" id="contact">
  <div class="wrap">
    <div>
      <h2>Contact me</h2>
      <ul class="contact-list">
        <li><a href="mailto:qilan.k.hong@gmail.com">qilan.k.hong@gmail.com</a></li>
        <li><a href="tel:+14159289558">+1 (415) 928-9558</a></li>
        <li>San Gabriel, California</li>
      </ul>
    </div>
    <small>&copy; 2026 {E(NAME)}</small>
  </div>
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


def head(title, lede=None, role=None):
    r = f'<p class="role">{E(role)}</p>' if role else ""
    l = f'<p class="lede">{lede}</p>' if lede else ""
    return f'<header class="page-head wrap">{r}<h1>{E(title)}</h1>{l}</header>'


# ---------------------------------------------------------------- pages
SLIDES_MGMT = ("https://docs.google.com/presentation/d/e/2PACX-1vTe67A3n7HO0X2mjyyBOLw9fHLFjew2IUoqKafi6yZei86SqPlHxgwB_gkpMh_a6k4sWLaTgeFFXKUF"
               "/pubembed?start=false&loop=false&delayms=3000")
SLIDES_VERM = ("https://docs.google.com/presentation/d/e/2PACX-1vQHkLiqwA7VuB54ixppdjmDRJgMeE5eYS1R8ZqAdnL8dCpzvVyZGIUN1m5UR9Pyv_hCopj_hogTLrgt"
               "/pubembed?start=false&loop=false&delayms=3000")


def build_home():
    cards = [
        ("research.html", "research-harvard", "Research", "Consumer behavior, finance and genomics, with three published or in-progress papers."),
        ("awards.html", "award-mun-delegate", "Awards", "Recognition in entrepreneurship, photography, Model UN and hackathons."),
        ("vermighty.html", "verm-upclose", "Vermighty", "A hybrid composting system I designed and built for my school."),
        ("leaf-by-leaf.html", "lbl-workshop-teaching", "Leaf by Leaf", "Hands-on growing workshops that let kids choose what they eat."),
        ("leadership.html", "lead-global-initiatives", "Leadership", "Clubs, councils, festivals and volunteering, on campus and off."),
        ("creative-athletic.html", "ca-dance-stage", "Creative & Athletic", "Badminton, dance, piano and singing."),
    ]
    grid = "".join(
        f'<a class="explore-card" href="{h}"><img src="assets/img/{i}-800.jpg" alt="" loading="lazy">'
        f"<h3>{E(t)}</h3><p>{E(d)}</p></a>" for h, i, t, d in cards)
    body = f"""
<section class="intro wrap">
  <div>
    <h1>Welcome to my portfolio!</h1>
    <p class="lede">I'm Qilan (Kelland) Hong, a senior at Polytechnic School in Pasadena, California.</p>
    <p>I'm fascinated by the hidden systems that shape how people think and decide. My work focuses on consumer behavior, sustainability and design. Explore my research, environmental initiatives, projects and leadership below.</p>
    <div class="btn-row"><a class="btn" href="research.html">See my research</a><a class="btn ghost" href="#contact">Contact me</a></div>
  </div>
  <div class="intro-photo"><img src="assets/img/headshot.jpg" alt="Portrait of Qilan (Kelland) Hong" width="1200" height="1500"></div>
</section>
<section class="explore wrap" aria-labelledby="explore-h">
  <h2 id="explore-h">Explore my work</h2>
  <div class="explore-grid">{grid}</div>
</section>"""
    page("index.html", "Home",
         "Qilan (Kelland) Hong, a senior at Polytechnic School in Pasadena, California: research, awards, community impact, leadership and creative work.",
         body)


def build_research():
    body = head("Research", "Studies in consumer behavior, financial markets and genomics, plus the technical training behind them.")
    body += '<div class="wrap">'
    body += entry(
        "Hybrid Consumer Identity in Ghanaian Fashion: Coexistence of Sustainable and Fast-Fashion Consumption Among Young Adults",
        "<strong>Johns Hopkins University</strong> (Pioneer Research Institute) · Summer–Fall 2026",
        "<p>Working with a Johns Hopkins professor, I'm running a cross-sectional study that pairs a literature review with an online survey. It asks whether young Ghanaian consumers form a “hybrid” identity that blends sustainable and fast-fashion clothing. The question grew out of my interest in fashion sustainability and my internship with Unkara Fashion Collective, a textile sustainability nonprofit.</p>"
        + links(("Read it here", "https://docs.google.com/document/d/1C-m4gjO5XDZR9Du6J9tVdPWnFCYGEW_X/edit?usp=sharing&ouid=107115511025543877695&rtpof=true&sd=true")),
        gallery(img("research-ghana-survey", "Survey charts from the Ghanaian fashion study", "Snapshot of primary survey data from ~160 participants."), cls="one natural"))
    body += entry(
        "Understanding Sectoral Responses to Tariff Uncertainty via a High-Dimensional Mediation Analysis",
        "<strong>Penn State University</strong> (Prof. Runze Li) · 2025–present · Published",
        "<p>I studied how financial fundamentals mediate the link between a company's sector and its stock-market performance during the 2025 tariff periods. Using high-dimensional mediation analysis, I identified which financial variables explain why sectors responded to the shock differently.</p>"
        + links(("Read it on arXiv", "https://doi.org/10.48550/arXiv.2609.33881")))
    body += entry(
        "Environmental and Genetic Influences in Alcohol Use Disorder",
        "<strong>National Human Genome Research Institute</strong> (Genomics: Insight) · 2026 · Published",
        "<p>I co-wrote this paper with four others on how environmental and biological factors shape alcohol use and addiction. I synthesized research on machine-learning models that predict relapse and treatment outcomes, and discussed how environmental variables interact with genetic susceptibility.</p>"
        + links(("Read it on Genomics Insight", "https://www.unlockinglifescode.org/genomics-insights/environmental-and-genetic-influences-alcohol-use-disorder")),
        gallery(img("research-genomics", "Presenting the genomics research to an audience"), cls="one"))
    body += '</div><section class="section wrap"><h2>Technical &amp; research preparation</h2>'
    body += entry(
        "Mathematical Elements of AI",
        "<strong>Harvard University</strong> Pre-College Program · Summer 2025",
        "<p>A four-week program on the mathematics behind neural networks: multivariable calculus and linear algebra. I implemented gradient descent and backpropagation from scratch and trained CNNs on MNIST and CIFAR, reaching over 99.6% classification accuracy. My final project was a computer-vision model that recognizes playing cards, built into a working Blackjack game.</p>",
        gallery(img("research-harvard", "Harvard Pre-College class group photo"),
                img("research-harvard-training", "Laptop screen showing the card classifier training", "Training the card classifier.")))
    body += '</section><section class="section wrap"><h2>Other research-related programs</h2>'
    body += entry(
        "Wharton Global Youth Program: MGMT 0001",
        "<strong>Wharton School</strong> · Fall 2025",
        "<p>Business-strategy case studies, including Trader Joe's and Gong Cha. For the final project, my team analyzed why Uber's expansion into China failed and proposed a localized “Build + Borrow” strategy.</p>"
        + links(("About the course", "https://globalyouth.wharton.upenn.edu/programs-courses/mgmt-0001-principles-of-management/")),
        slides(SLIDES_MGMT, "WGYP MGMT 0001 final project")
        + gallery(img("research-wharton-class", "Video-call grid of the MGMT 0001 class", "WGYP MGMT 0001 class photo."), cls="one"))
    body += entry(
        "Los Angeles Behavioral Economics Laboratory",
        "Trainee · 2025–present",
        "<p>Training in behavioral and experimental methods, with work spanning AI, housing and the environment.</p>"
        + links(("LABEL training program", "https://label-laboratory.org/label-training-program/")))
    body += entry(
        "World Assembly of Youth",
        "Research Intern · 2024–2025",
        "<p>Wrote five research papers of 10+ pages each on education, poverty, ICT access, leisure and juvenile delinquency, each tied to the UN Sustainable Development Goals.</p>"
        + links(("World Assembly of Youth", "https://www.way.org.my/")))
    body += entry(
        "USC Data Analytics Pre-College",
        "<strong>University of Southern California</strong> · Summer 2024",
        "<p>A statistical analysis course. My final project applied k-means clustering to a dataset of 2,000+ students using Python, Pandas and Tableau.</p>"
        + links(("About the program", "https://precollege.usc.edu/summer-programs/analytics-the-power-of-data-for-businesses/")))
    body += "</section>"
    page("research.html", "Research",
         "Research by Qilan (Kelland) Hong on sustainable fashion in Ghana, sector responses to tariff uncertainty, and genetic influences in alcohol use disorder.",
         body, "research-harvard")


def build_awards():
    body = head("Awards & honors")
    body += '<div class="wrap">'
    body += entry(
        "Sabrina Zhang Award",
        "<strong>Polytechnic School</strong> · Grade 11",
        '<p class="stat">$700 grant</p><p>The award funded <a href="vermighty.html">Vermighty</a>, my two-chamber composting system, taking it from sketches to a campus prototype used for testing and curriculum integration.</p>',
        gallery(img("verm-hero", "Building the Vermighty composting system on campus"), cls="one"))
    body += entry(
        "Top 100 Finalist, Blue Ocean Student Entrepreneur Competition",
        "<strong>Blue Ocean Student Entrepreneurs Corp</strong> · Grade 10",
        '<p class="stat">Top 1% of 12,000+ students from 163 countries</p><p>Named a global Top 100 finalist for Vermighty.</p>'
        + links(("Watch the pitch", "https://www.youtube.com/watch?v=ykseSfgmh6g&t=30s"), ("View the certificate", "assets/media/blue-ocean-certificate.pdf")),
        gallery(img("award-blue-ocean-cert", "Blue Ocean Competition Top 100 finalist certificate"), cls="one natural"))
    body += entry(
        "Scholastic Art &amp; Writing Awards, Photography",
        "<strong>Alliance for Young Artists &amp; Writers</strong> · Grade 11",
        '<p class="stat">Two Silver Keys and an Honorable Mention, out of ~110,000 entrants</p><p>Recognized for three photographs: <em>Above the Noise</em>, <em>The Crowd and the Sea</em> and <em>Stones That Remember</em>.</p>',
        gallery(img("award-above-the-noise", "Above the Noise: a fiery orange sky over a dark silhouette", "Above the Noise"),
                img("award-crowd-and-sea", "The Crowd and the Sea: waves at sunset with people on the rocks", "The Crowd and the Sea"),
                img("award-stones-that-remember", "Stones That Remember: a narrow cobblestone lane between old brick houses", "Stones That Remember"),
                cls="three"))
    body += entry(
        "Outstanding Delegate, Northwood High School Model UN",
        "<strong>Northwood High School MUNC</strong> · Grade 11",
        "<p>Represented Al Gore on a committee on energy consumption and climate policy, and earned Outstanding Delegate for research, speeches and negotiation.</p>",
        gallery(img("award-mun-delegate", "Receiving the Outstanding Delegate certificate on stage"),
                img("award-mun-group", "Polytechnic Model UN delegation group photo")))
    body += entry(
        "2nd Place, GNEC Hackathon",
        "<strong>Global NGO Executive Committee</strong> · Grade 10",
        '<p class="stat">2nd of 3,000 participants</p><p>Built TarantulaX, a solar-powered reverse-osmosis drone. I later joined GNEC as a partnerships coordinator and judge.</p>'
        + links(("See TarantulaX on Devpost", "https://devpost.com/software/tarantulax")),
        gallery(img("award-drone", "Line drawing of the TarantulaX drone design", "Drone design"), cls="one natural"))
    body += "</div>"
    page("awards.html", "Awards",
         "Awards and honors of Qilan (Kelland) Hong: Sabrina Zhang Award, Blue Ocean Top 100, Scholastic Art & Writing Awards, Model UN and GNEC Hackathon.",
         body, "award-mun-delegate")


def build_vermighty():
    body = head("Vermighty",
                "A hybrid thermophilic and vermicomposting system I designed, engineered and built. It tests whether heat-based and worm-based composting can work in sequence at micro-scale: heat speeds up decomposition first, then worms improve the compost's quality.",
                "Founder · 2025–present")
    body += '<div class="wrap"><figure class="hero-figure">' + gallery(img("verm-upclose", "The finished Vermighty composting bin in its frame"), cls="one") + "</figure>"
    body += entry("Early design sketches", "",
                  "<p>Vermighty started as sketches and a 3D model before I built the campus prototype.</p>",
                  slides(SLIDES_VERM, "Early Vermighty design sketches")
                  + gallery(img("verm-model", "Technical drawing of the Vermighty model", "Vermighty model drawing."), cls="one natural"))
    body += entry("Testing and presentations", "",
                  "<p>Vermighty is being tested on my high school campus, funded by $700 from the Sabrina Zhang Award. I presented it at Terrapalooza, Poly's Earth Day festival.</p>",
                  gallery(img("verm-terrapalooza-1", "Presenting Vermighty at Terrapalooza", "Presenting Vermighty at Terrapalooza"),
                          img("verm-terrapalooza-2", "Title slide: Vermighty, Rethinking Food Systems"),
                          img("verm-assembling", "Assembling Vermighty on campus", "Assembling Vermighty on campus"),
                          img("verm-hero", "Collage of Vermighty under construction")))
    body += entry("A small circular system", "",
                  "<p>I partner with Epicurean, the school's food service, to collect leftover food for compost testing. The finished compost goes to the Poly Planters club for its garden beds, closing the loop on campus.</p>",
                  gallery(img("verm-leftovers", "School food leftovers ready for composting", "School leftovers Vermighty used"),
                          img("verm-location", "Vermighty under its canopy on campus", "Location of Vermighty"),
                          img("verm-garden-beds", "Poly Planters garden beds", "Location of Poly Planters garden beds"),
                          cls="three"))
    body += entry("Long-term goal", "",
                  "<p>I want Vermighty built into the school curriculum so other students can run and develop it. I'm working toward this through an Independent Study with a teacher, focused on curriculum development and long-term implementation.</p>")
    body += "</div>"
    page("vermighty.html", "Vermighty",
         "Vermighty: a hybrid thermophilic and vermicomposting system designed and built by Qilan (Kelland) Hong at Polytechnic School.",
         body, "verm-upclose")


def build_lbl():
    body = head("Leaf by Leaf",
                "I co-founded Leaf by Leaf after noticing that children are told which foods are healthy without much say in the choice. Our workshops have kids plant and care for food themselves, then decide whether to eat what they grew.",
                "Co-Founder · 2026–present")
    body += '<div class="wrap">'
    body += '<p>' + links(("Visit the Leaf by Leaf website", "https://www.leaf-by-leaf.org/home")) + "</p>"
    body += entry("Workshops", "",
                  '<p class="stat">20+ workshops · 600+ people reached</p>'
                  "<p>I've designed and led workshops at schools, youth centers, a rescue mission, a children's museum and community events, in person and virtually.</p>",
                  gallery(img("lbl-workshop-teaching", "Teaching a Leaf by Leaf workshop in a middle-school classroom"),
                          img("lbl-workshop-class", "A class of students posing with their growing kits"),
                          img("lbl-virtual", "Leading a virtual workshop from a laptop", "Leading hands-on workshops, in person and virtually!"),
                          img("lbl-workshop-collage", "Students raising hands during a workshop")))
    body += entry("Our children's book and growing kits", "",
                  "<p>We wrote and published an original children's book and created take-home growing kits that extend the workshops. We've donated many of both.</p>"
                  + links(("Leaf by Leaf on Amazon", "https://www.amazon.com/Leaf-Qilan-Hong/dp/B0H8BXJ7BD")),
                  gallery(img("lbl-book", "Cover of the Leaf by Leaf children's book", "Our original children's book!"),
                          img("lbl-books-kids", "Kids reading the Leaf by Leaf book outdoors"),
                          img("lbl-hero", "Stacks of take-home growing kits", "Donated take-home growing kits!"),
                          img("lbl-donations", "Book donations to community partners", "Book donations!")))
    body += entry("Recognition", "",
                  "<p>We were named Dragon Kim Foundation Fellows, with $5,000 in funding, and were featured on CBS News.</p>"
                  + links(("Watch the CBS News segment", "https://www.youtube.com/watch?v=zIxP-wy2kek")),
                  gallery(img("lbl-dragon-kim", "Receiving Dragon Kim Foundation Fellow medals", "Dragon Kim Foundation Fellows"),
                          img("lbl-cbs", "Stills from the CBS News segment", "Featured on CBS News")))
    body += "</div>"
    page("leaf-by-leaf.html", "Leaf by Leaf",
         "Leaf by Leaf, co-founded by Qilan (Kelland) Hong: 20+ hands-on growing workshops reaching 600+ people, an original children's book and take-home kits.",
         body, "lbl-workshop-teaching")


def build_leadership():
    body = head("Leadership & volunteering")
    body += '<div class="wrap">'
    body += entry("Terrapalooza", "Programming Committee Member &amp; Presenter · <strong>Polytechnic School</strong> · 2025–present",
                  "<p>Terrapalooza is Poly's Earth Day festival. On the programming committee I design climate-education workshops and speaker events. At the 2026 festival I presented a climate constitution to peers and faculty that draws on behavioral economics, intergenerational equity and environmental design policy, and shared the story behind Vermighty.</p>",
                  gallery(img("lead-climate-treaty", "Presenting the climate constitution at Terrapalooza"), cls="one"))
    body += entry("Poly Global Voices Club", "Head of Operations · 2025–present",
                  "<p>Global Voices is a student-led club connecting high schoolers worldwide to discuss global issues. I run communications and coordinate with partner schools in Australia, Singapore and Finland. I've helped host a school event with visiting professor Dr. Steven Lamy, presented research on the Fukushima wastewater release and co-organized a school-wide clothing swap.</p>",
                  gallery(img("lead-clothing-swap", "Organizers at the school-wide clothing swap", "School-wide clothing swap"),
                          img("lead-global-initiatives", "Students with Dr. Steven Lamy at a Global Initiatives event", "Global Initiatives Program event")))
    body += entry("GNEC Hackathon", "Partnerships Coordinator &amp; Judge · <strong>Global NGO Executive Committee</strong> · 2024–present",
                  "<p>After placing second in the 2024 hackathon, I stayed on as an intern. The role began with social-media graphics and grew into leading partner and sponsor outreach, designing marketing and branding, moderating opening and closing ceremonies and judging. I've judged over 600 finalist presentations, and I built an automated certificate-distribution system to replace a manual process.</p>")
    body += entry("The Huntington", "Museum Education &amp; Gardening Volunteer · 2025–present",
                  "<p>I lead hands-on cultural learning for visitors in the Chinese Garden's Flowery Brush Library and help run sustainability-focused events such as the Huntington's plant sale.</p>",
                  gallery(img("lead-huntington", "Volunteering at a calligraphy table in the Huntington's Chinese Garden"), cls="one"))
    body += entry("Boys &amp; Girls Club of Pasadena", "Volunteer · 2025–present",
                  "<p>I volunteer weekly with after-school enrichment and leisure activities, and I've brought Leaf by Leaf workshops to several Boys &amp; Girls Club locations.</p>")
    body += entry("Global Scholar", "<strong>Polytechnic School</strong> · 2026–present",
                  "<p>As a Global Scholar I attend speaker events with diplomats and policy experts, take part in cross-cultural exchanges and write a blog analyzing international affairs, from geopolitical conflicts to global environmental policy. I also serve as a Global Ambassador, helping organize events and discussions that build global awareness on campus.</p>"
                  + links(("Visit my blog", "https://kellandhgip.squarespace.com")))
    body += entry("Judiciary Council", "<strong>Polytechnic School</strong> · 2025–present",
                  "<p>Elected and interviewed onto the Judiciary Council. On the Policy and Student Voice subcommittee, I review student conduct cases on behalf of the student body.</p>")
    body += "</div>"
    page("leadership.html", "Leadership",
         "Leadership and volunteering by Qilan (Kelland) Hong: Terrapalooza, Global Voices, GNEC, The Huntington, Boys & Girls Club, Global Scholar and Judiciary Council.",
         body, "lead-global-initiatives")


def build_creative():
    body = head("Creative & athletic")
    body += '<div class="wrap">'
    body += entry("Badminton", "Varsity · <strong>Polytechnic School</strong> · 2025–present",
                  "<p>I've loved playing badminton with my family since I was young, and playing with close friends on a school team was a dream come true. I play mixed and girls' doubles, and placed second in girls' doubles in the Montview League in 2025.</p>",
                  gallery(img("ca-badminton", "Playing badminton in the school gym"), cls="one"))
    body += entry("Dance", "2010–present",
                  "<p>I've been dancing since I was two, starting with ballet. At nine, I performed with San Francisco Ballet despite being a year below the program's minimum age. Moving between schools, cities and countries, I explored K-pop, jazz and hip-hop. Today I mainly dance hip-hop. Below is a piece I co-choreographed for my school's dance show.</p>",
                  '<figure class="media"><video class="player" controls preload="metadata" playsinline poster="assets/img/ca-dance-video-poster.jpg">'
                  '<source src="assets/media/dance-show.mp4" type="video/mp4">Your browser can’t play this video.</video>'
                  "<figcaption>A piece I co-choreographed for the school dance show.</figcaption></figure>"
                  + gallery(img("ca-dance-stage", "Mid-kick on stage under purple lights"),
                            img("ca-dance-show", "The full dance ensemble on stage"),
                            img("ca-dance-collage", "Dance rehearsal and performance collage"), cls="three"))
    body += entry("Piano", "2012–present",
                  "<p>Piano has always been an outlet for expression and relaxation. I've played classical piano for 14 years and won awards in multiple competitions.</p>"
                  + links(("Watch a chamber music piece I played", "https://www.youtube.com/watch?v=4skXd9GU03w")),
                  gallery(img("ca-piano", "Performing on a grand piano"),
                          img("ca-piano-competition", "At a European international music competition")))
    body += entry("Singing", "2020–present",
                  "<p>I've always loved singing and began formal lessons in 2020. Since then I've worked on vocal technique, interpretation and performance across contemporary and musical-theatre repertoire. Here's a professionally recorded cover.</p>",
                  '<div class="audio-card"><div class="title">Someone You Loved <span>· cover of Lewis Capaldi</span></div>'
                  '<audio controls preload="none" src="assets/media/someone-you-loved-cover.mp3"></audio></div>')
    body += "</div>"
    page("creative-athletic.html", "Creative & Athletic",
         "Badminton, dance, piano and singing: the creative and athletic side of Qilan (Kelland) Hong.",
         body, "ca-dance-stage")


def build_404():
    page("404.html", "Page not found", "This page doesn't exist.",
         head("Page not found", 'This page doesn\'t exist or has moved. <a href="index.html">Go to the homepage</a>.'))


os.makedirs(OUT, exist_ok=True)
build_home(); build_research(); build_awards(); build_vermighty(); build_lbl()
build_leadership(); build_creative(); build_404()
# Old Squarespace addresses keep working
redirect("new-page-1.html", "research.html")
redirect("awards-1.html", "awards.html")
redirect("new-page.html", "leadership.html")
redirect("new-page-2.html", "creative-athletic.html")
redirect("com.html", "index.html")
print("built", OUT, "preview" if PREVIEW else THEME)
