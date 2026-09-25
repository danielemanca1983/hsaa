"""The published pages and the sections each owns."""
import re
from html import escape
from urllib.parse import urlsplit

GROUPS = {
 'home': [],
 'about': [],
 'contact': [],
 'football': ['schools-football', 'five-a-side', 'nine-a-side', 'teams', 'football-results'],
 'other-sports': ['cross-country', 'kwik-cricket', 'tag-touch', 'orienteering', 'young-active'],
 'information': ['contacts-supporters', 'illuminaries', 'john-larter-foundation', 'district-competitions', 'district-results'],
}
OWNERS = {child: parent for parent, children in GROUPS.items() for child in children}

def destination(value):
 parsed = urlsplit(value)
 if parsed.scheme or parsed.netloc or not parsed.path.endswith('.html'):
  return value
 key = parsed.path.removesuffix('.html')
 if key == 'home': return 'index.html' + ('#' + parsed.fragment if parsed.fragment else '')
 if key not in OWNERS: return value
 anchor = key + ('-' + parsed.fragment if parsed.fragment else '')
 return OWNERS[key] + '.html#' + anchor

def rewrite_references(markup):
 def replace(match):
  attr, value = match.groups()
  if value.startswith('../'): value = value[3:]
  return f'{attr}="{destination(value)}"'
 return re.sub(r'(href|src)="([^"\n]+)"', replace, markup)

def section_content(key, title, desc, content):
 # Prefix child IDs so repeated boys/girls sections remain unique.
 content = re.sub(r'id="([^"]+)"', lambda m: f'id="{key}-{m[1]}"', content)
 content = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{key}-{m[1]}"', content)
 # Child headings sit below the section title in the complete page.
 content = re.sub(r'(<\/?h)([2-5])(?=[\s>])', lambda m: m[1] + str(int(m[2]) + 1), content)
 return f'<section id="{key}" class="gender-section"><h2>{escape(title)}</h2><p class="lead">{escape(desc)}</p>{content}</section>'
