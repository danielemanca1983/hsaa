"""Check publication coverage against the reviewed content records."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from navigation import NAVIGATION
from page_structure import destination, OWNERS

class Content(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.links=[];self.main=False;self.main_text=[];self.nav=False;self.nav_links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='main':self.main=True
  if tag=='nav' and a.get('id')=='main-nav':self.nav=True
  if tag=='a':
   self.links.append(a.get('href',''))
   if self.nav:self.nav_links.append(a.get('href',''))
 def handle_endtag(self,tag):
  if tag=='main':self.main=False
  if tag=='nav':self.nav=False
 def handle_data(self,data):
  if self.main:self.main_text.append(data)

expected = [destination(url) for _, url, _ in NAVIGATION] + ['contact.html']
pages={}
for path in Path('dist').glob('*.html'):
 raw=path.read_text(encoding='utf-8');p=Content();p.feed(raw)
 assert len(p.ids)==len(set(p.ids)),f'Duplicate IDs: {path}'
 assert p.nav_links==expected,f'Navigation mismatch: {path}'
 assert not re.search(r'\{\{|\ufffd|DANIELE|GIFT AID PAGE|gll,com|co,uk|heatholdboys',raw),f'Unresolved source material: {path}'
 pages[path.stem]=' '.join(p.main_text)
assert set(pages) == {'index', 'about', 'contact', 'football', 'other-sports', 'information'}
# The supplied sitemap describes sections within the existing main pages.
sitemap_sections = {
 'index': ['introduction', 'welcome', 'news-ticker-content'],
 'about': ['mission', 'history', 'committee', 'contact'],
 'football': ['schools-football', 'five-a-side', 'nine-a-side', 'teams', 'teams-boys', 'teams-girls', 'football-results'],
 'other-sports': ['cross-country', 'kwik-cricket', 'tag-touch', 'young-active', 'orienteering'],
 'information': ['contacts-supporters', 'illuminaries', 'john-larter-foundation', 'district-competitions', 'district-competitions-kay-trophy', 'district-competitions-john-larter', 'district-competitions-lester-finch', 'district-results'],
}
for parent, sections in sitemap_sections.items():
 parser = Content(); parser.feed(Path('dist', parent + '.html').read_text(encoding='utf-8'))
 for section in sections:
  assert section in parser.ids, f'Sitemap section missing from {parent}: {section}'
assert 'Follow HSAA on social media' in pages['contact']
assert 'info@hsaa.org.uk' in pages['about']
page_count = len(pages)
for child, parent in OWNERS.items():
 raw = Path('dist', parent + '.html').read_text(encoding='utf-8')
 start = raw.index('<section id="' + child + '"')
 parser = Content(); parser.main = True
 # Stop at the next peer section, preserving all nested content.
 next_sections = [raw.find('<section id="' + sibling + '"', start + 1) for sibling, owner in OWNERS.items() if owner == parent]
 end = min([pos for pos in next_sections if pos != -1] or [raw.index('</article>', start)])
 parser.feed(raw[start:end])
 pages[child] = ' '.join(parser.main_text)
people=json.loads(Path('content/people.json').read_text(encoding='utf-8-sig'))
records=json.loads(Path('content/records.json').read_text(encoding='utf-8-sig'))
for name,_ in people['players']+people['association']:assert name in pages['illuminaries'],name
for name,_,_ in people['partners']:assert name in pages['contacts-supporters'],name
for season,winner in records['lester_winners']:
 assert season in pages['district-competitions'] and winner in pages['district-competitions'],season
assert 'info@hsaa.org.uk' in pages['contact']
assert 'Stan Le Brom' in pages['five-a-side'] and 'Alan Hutchinson' in pages['five-a-side']
assert 'Crisp Shield' in pages['teams'] and 'Gills Shield' in pages['teams']
assert 'Eleanor Shield' in pages['schools-football'] and 'Glyn Williams Cup' in pages['schools-football']
assert 'Five a sides' not in pages['football-results'], 'School results must match the supplied nine-a-side scope'
assert 'three-year' in pages['john-larter-foundation']
assert '<base' not in Path('dist/index.html').read_text(encoding='utf-8')
office_files=list(Path('dist').rglob('*.doc'))
assert [p.name for p in office_files]==['hsaa-alumni-membership-form.doc']
assert not list(Path('dist').rglob('*.ppt*'))
print(f'Content checks passed: {page_count} pages; 33 players; 10 association figures; 13 partners; 56 trophy seasons; no unresolved source placeholders.')
