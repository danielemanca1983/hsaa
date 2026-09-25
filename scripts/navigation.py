from html import escape

# (label, destination, children): shared by every page and the footer.
NAVIGATION = [
 ('Home', 'home.html', []),
 ('About us', 'about.html', [
  ('HSAA Mission Statement', 'about.html#mission', []),
  ('History of HSAA', 'about.html#history', []),
  ('HSAA Executive Committee Members', 'about.html#committee', [])]),
 ('Football', 'football.html', [
  ('Schools Football', 'schools-football.html', [
   ('Five a sides', 'five-a-side.html', []),
   ('Nine a side League', 'nine-a-side.html', [])]),
  ('District Football – Boys & Girls', 'teams.html', [
   ('Boys', 'teams.html#boys', []), ('Girls', 'teams.html#girls', [])]),
  ('Results Service', 'football-results.html', [])]),
 ('HSAA Other Sporting Competitions', 'other-sports.html', [
  ('Cross Country League', 'cross-country.html', []),
  ('Kwik Cricket', 'kwik-cricket.html', []),
  ('Tag Rugby', 'tag-touch.html', []),
  ('Young & Active Hackney 2030', 'young-active.html', [])]),
 ('Information', 'information.html', [
  ('Schools FA Contacts & HSAA Supporters', 'contacts-supporters.html', []),
  ('Hackney District & Association Illuminaries', 'illuminaries.html', []),
  ('John Larter MBE Foundation', 'john-larter-foundation.html', []),
  ('District Competitions', 'district-competitions.html', [
   ('Kay Trophy', 'district-competitions.html#kay-trophy', []),
   ('John Larter Girls District Trophy', 'district-competitions.html#john-larter', []),
   ('Lester Finch Trophy', 'district-competitions.html#lester-finch', []),
   ('Results Service', 'district-results.html', [])])])]

def link(label, url, current):
 active = ' aria-current="page"' if url == current + '.html' else ''
 return f'<a href="{url}"{active}>{escape(label)}</a>'

def navigation(current):
 # Sitemap children are content sections within each complete main page.
 return '<ul class="nav-list">' + ''.join(
  '<li>' + link(label, url, current) + '</li>'
  for label, url, _ in NAVIGATION) + '</ul>' + (
   '<div class="mobile-nav-contact"><a class="button" href="contact.html"'
   + (' aria-current="page"' if current == 'contact' else '')
   + '>Get in touch <span aria-hidden="true">&#8599;</span></a></div>')


def footer_links(current):
 return ''.join(link(label, url, current) for label, url, _ in NAVIGATION) + link('Get in touch', 'contact.html', current)

def directory(items):
 return '<ul class="section-directory">' + ''.join(
  f'<li>{link(label, url, "")}{directory(children) if children else ""}</li>'
  for label, url, children in items) + '</ul>'
