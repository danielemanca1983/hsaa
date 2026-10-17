"""Check that the six complete source pages cover the published content."""
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "content" / "pages"
DIST = ROOT / "dist"
PAGES = ("index", "about", "contact", "football", "other-sports", "information")
EXPECTED_NAV = (
    "index.html", "about.html", "football.html",
    "other-sports.html", "information.html", "contact.html",
)
EXPECTED_PDFS = {
    "cross-country-meet-dates-2026-27.pdf",
    "hsaa-executive-committee-members.pdf",
    "hsaa-five-a-side-draw-2026-27.pdf",
    "john-larter-girls-draw-2026-27.pdf",
    "kay-trophy-draw-2026-27.pdf",
    "lester-finch-draw-and-matches-2026-27.pdf",
}

class Content(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.nav = False
        self.nav_links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "nav" and attrs.get("id") == "main-nav":
            self.nav = True
        if tag == "a" and self.nav:
            self.nav_links.append(attrs.get("href", ""))
    def handle_endtag(self, tag):
        if tag == "nav" and self.nav:
            self.nav = False

def require(text, *needles):
    for needle in needles:
        assert needle in text, f"Missing content: {needle}"

def row_count(text, caption):
    table = text.split("<caption>" + caption + "</caption>", 1)[1].split("</table>", 1)[0]
    body = table.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
    return body.count("<tr>")

assert {p.stem for p in SOURCE.glob("*.html")} == set(PAGES), "Source must have exactly six complete HTML pages"
assert {p.stem for p in DIST.glob("*.html")} == set(PAGES), "Published site must have exactly six HTML pages"
pages = {}
for name in PAGES:
    source = (SOURCE / f"{name}.html").read_bytes()
    published = (DIST / f"{name}.html").read_bytes()
    assert source == published, f"Rebuild needed: {name}.html"
    text = source.decode("utf-8")
    assert not re.search(r"\{\{|\ufffd|DANIELE|GIFT AID PAGE|gll,com|co,uk|heatholdboys", text)
    parsed = Content()
    parsed.feed(text)
    assert len(parsed.ids) == len(set(parsed.ids)), f"Duplicate IDs: {name}.html"
    assert tuple(parsed.nav_links) == EXPECTED_NAV, f"Navigation mismatch: {name}.html"
    pages[name] = (text, set(parsed.ids))

sections = {
    "index": {"introduction", "welcome", "news-ticker-content"},
    "about": {"mission", "history", "committee", "contact"},
    "football": {"schools-football", "five-a-side", "nine-a-side", "teams", "teams-boys", "teams-girls", "football-results"},
    "other-sports": {"cross-country", "kwik-cricket", "tag-touch", "young-active", "orienteering"},
    "information": {"contacts-supporters", "illuminaries", "john-larter-foundation", "district-competitions", "district-competitions-kay-trophy", "district-competitions-john-larter", "district-competitions-lester-finch", "district-results"},
}
for name, expected in sections.items():
    assert expected <= pages[name][1], f"Missing sections in {name}.html: {expected - pages[name][1]}"

home = pages["index"][0]
about = pages["about"][0]
football = pages["football"][0]
other = pages["other-sports"][0]
info = pages["information"][0]
contact = pages["contact"][0]
require(home, "Today we manage the district U-11 boys' and girls' representative teams", "HSAA is committed to providing a fair, inclusive and respectful environment")
require(about, "hsaa-executive-committee-members.pdf", "info@hsaa.org.uk")
require(contact, "Follow HSAA on social media", "info@hsaa.org.uk")
require(football, "Stan Le Brom", "Alan Hutchinson", "Crisp Shield", "Gills Shield", "Glyn Williams Cup", "Eleanor Shield", "hsaa-five-a-side-draw-2026-27.pdf", "kay-trophy-draw-2026-27.pdf", "john-larter-girls-draw-2026-27.pdf", "lester-finch-draw-and-matches-2026-27.pdf")
require(other, "cross-country-meet-dates-2026-27.pdf", "young-active-2030.png")
require(info, "Sonny Perkins", "Wigan Athletic", "Steve Browne", "Mel Capleton", "Aaron Rowe", "Andrew Oluwabori", "Cairo Antoine-Eva", "Phillip Hayfield", "Alan Hutchinson", "Stan Le Brom", "Norman Hamilton", "Liz Prosser", "Jaidon Anthony 11", "Liam Kelly", "three-year", "kay-trophy-draw-2026-27.pdf", "john-larter-girls-draw-2026-27.pdf", "lester-finch-draw-and-matches-2026-27.pdf")
assert row_count(info, "Former district players and career highlights") == 38
assert row_count(info, "Association and district figures") == 15
assert row_count(info, "Lester Finch Trophy — winners by season") == 56
assert len(re.findall(r'<(?:a|div) class="partner"', info)) == 15
assert not list(DIST.rglob("*.ppt*"))
assert [p.name for p in DIST.rglob("*.doc")] == ["hsaa-alumni-membership-form.doc"]
assert {p.name for p in (DIST / "downloads").glob("*.pdf")} == EXPECTED_PDFS
for name in EXPECTED_PDFS:
    assert (DIST / "downloads" / name).read_bytes().startswith(b"%PDF-")
print("Content checks passed: six complete source pages; 38 players; 15 association figures; 15 partners; 56 trophy seasons; six PDF downloads.")
