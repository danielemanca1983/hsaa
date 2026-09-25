from pathlib import Path
from html import escape
import re
from navigation import NAVIGATION, navigation, footer_links, directory
from page_structure import GROUPS, rewrite_references, section_content
PAGE_CONTENT = {}
D=Path('dist')
sports=[('teams','Borough representative teams','Representing Hackney. Together.','Boys’ and girls’ district football, bringing together young players from primary schools across the borough.'),('cross-country','Cross Country League','Find your stride.','The Primary Cross Country League is part of HSAA’s planned 2026–27 sporting programme.'),('five-a-side','Five a sides','Small teams. Big spirit.','School football competitions for boys and girls across Hackney.'),('nine-a-side','Nine a side League','A new chapter for school football.','Boys’ and girls’ school leagues, bringing friendly rivalry back to the pitch.'),('kwik-cricket','Kwik cricket','Step up to the crease.','Kwik cricket is part of HSAA’s planned 2026–27 programme for Hackney primary schools.'),('tag-touch','Tag Rugby','Move together. Play together.','Tag rugby is part of HSAA’s planned 2026–27 sporting programme.'),('orienteering','Orienteering','Find your way, together.','Orienteering festivals are part of HSAA’s planned 2026–27 programme for Hackney primary schools.')]
children={'teams','five-a-side','nine-a-side','kwik-cricket'}
labels={s[0]:s[1] for s in sports}; labels.update({'home':'Home','contact':'Contact'})
def href(key):return key+'.html'
def navlink(key,label,current):return f'<a href="{href(key)}"'+(' aria-current="page"' if key==current else '')+f'>{label}</a>'
def shell(key,title,desc,body,parent=None):
 nav=navigation(key)
 footer=footer_links(key)
 return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | HSAA</title><meta name="description" content="{escape(desc,quote=True)}"><link rel="icon" href="../assets/logo.jpg"><link rel="stylesheet" href="../css/styles.css"><script src="../js/main.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header><div class="masthead wrap"><a href="home.html" class="brand" aria-label="HSAA home"><img src="../assets/source/hsaa-logo.jpg" alt="Hackney Schools Athletic Association" width="215" height="64"></a><span class="brand-note">HACKNEY SCHOOLS<br><strong>ATHLETICS ASSOCIATION</strong></span><a class="header-contact button" href="contact.html">Get in touch <span aria-hidden="true">↗</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">Menu <span aria-hidden="true">☰</span></button></div><nav class="navigation" id="main-nav" aria-label="Main navigation"><div class="nav-inner wrap">{nav}</div></nav></header>
<main id="main">{body}</main><footer><div class="wrap footer-grid"><div><img src="../assets/source/hsaa-logo.jpg" alt="HSAA" width="215" height="64" loading="lazy"><p>Sport. Opportunity. Community.<br>For the children of Hackney.</p><a href="mailto:info@hsaa.org.uk">info@hsaa.org.uk ↗</a></div><div><h2>Explore HSAA</h2><div class="footer-links">{footer}</div></div><div><h2>Boys &amp; girls</h2><div class="footer-links">{''.join(f'<a href="{s}.html#{g}">{labels[s]} — {g}</a>' for s in ['teams','five-a-side','nine-a-side','kwik-cricket'] for g in ['boys','girls'])}</div></div></div><div class="wrap footer-bottom">© HSAA · Hackney Schools Athletics Association <a href="#main">Back to top ↑</a></div></footer></body></html>'''
def cards(items):return '<div class="sport-grid">'+''.join(f'<a class="sport-card" href="{s}.html"><span class="card-number">0{i+1} / {"FOOTBALL" if s in ["teams","five-a-side","nine-a-side"] else "SCHOOL SPORT"}</span><h3>{l}</h3><p>{d}</p><span class="card-arrow" aria-hidden="true">↗</span></a>' for i,(s,l,h,d) in enumerate(items))+'</div>'
def contactbox(subject='school sport'):return f'<aside class="enquiry"><span class="eyebrow">GET INVOLVED</span><h2>Bring your school<br>into the action.</h2><p>For {subject} enquiries, entry information and the latest arrangements, get in touch with HSAA.</p><a class="button" href="contact.html">Contact HSAA <span aria-hidden="true">↗</span></a></aside>'
def intro(key,title,heading,desc,parent=None):return f'<div class="wrap page-intro"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="home.html">Home</a><span>/</span>'+ (f'<a href="{parent}.html">{labels[parent]}</a><span>/</span>' if parent else '')+f'<span>{title}</span></nav><span class="eyebrow">HACKNEY SCHOOLS SPORT</span><h1>{heading}</h1><p class="lead">{desc}</p></div>'
home='''<section class="news-ticker" aria-label="Latest HSAA news"><div class="wrap ticker-inner"><h2 class="ticker-label">LATEST NEWS</h2><div class="ticker-window" id="news-ticker-content"><div class="ticker-track"><ul class="ticker-items"><li>2026: Hackney girls win the Southern Counties Cup</li><li>2026–27: Kwik cricket, tag rugby, cross country and orienteering planned</li><li>School sport enquiries: info@hsaa.org.uk</li></ul></div></div></div></section><section class="hero wrap" id="introduction"><div class="hero-copy"><span class="eyebrow">OUR SCHOOLS. OUR BOROUGH. OUR FUTURE.</span><h1>Every child.<br>Every chance.<br><em>Through sport.</em></h1><p>Welcome to the Hackney Schools Athletic Association (HSAA) website — where every Hackney primary school child’s potential takes centre stage. We believe sport is more than just a game; it’s a powerful tool for teamwork, discipline, and confidence. Through the exciting competitions, skill-building programmes, and community events we deliver, we endeavour to nurture a love for physical activity while fostering values that last a lifetime. Together, we’re shaping healthy, happy, and resilient children &amp; young people.</p><p>This is an information point for Hackney Primary Schools Sport and we also hope this is a resource which can assist in promoting opportunities for Hackney Primary Schools to access. Enjoy!</p><div class="actions"><a class="button" href="#sports">Explore our sports <span aria-hidden="true">↗</span></a></div><div class="hero-footnote"><span class="small-mark" aria-hidden="true">✳</span> Rooted in Hackney. Open to possibility.</div></div><figure class="hero-photo"><img src="../assets/football-action.jpg" alt="Hackney girls playing football in front of the goal" width="1990" height="1508" fetchpriority="high"><figcaption><span>MORE THAN A GAME</span><strong>A place to belong.</strong></figcaption></figure></section><section class="values wrap" aria-label="Our values"><div><span>01</span><strong>Opportunity for every child</strong></div><div><span>02</span><strong>Teamwork that lasts</strong></div><div><span>03</span><strong>Proud to represent Hackney</strong></div></section><section class="section wrap" id="sports"><div class="section-heading"><div><span class="eyebrow">FIND YOUR GAME</span><h2>A borough full of possibility.</h2></div><p>From the football pitch to the cross-country course, discover sport for Hackney’s primary schools.</p></div>'''+cards([item for item in sports if item[0] != 'orienteering'] + [('young-active', 'Young & Active Hackney 2030', '', 'Affiliation and participation in the wider school sport programme.')])+'''</section><section class="feature wrap"><img src="../assets/team-celebration.jpg" alt="Hackney players celebrating together with a trophy" width="884" height="1024" loading="lazy"><div><span class="eyebrow">ONE BOROUGH. A SHARED PRIDE.</span><h2>Local talent.<br>Lasting memories.</h2><p>Our boys’ and girls’ district teams give young footballers the opportunity to represent Hackney, meet players from other schools and compete beyond the borough.</p><p>The girls won the Southern Counties Cup in 2026, following the boys’ success in 2024.</p><a class="text-link" href="teams.html">Discover our representative teams →</a></div></section><section class="section wrap mission"><span class="eyebrow">WHY WE DO IT</span><h2>More than the final score.</h2><p>We believe sport is a powerful way to build teamwork, discipline and confidence. HSAA provides extra-curricular sporting opportunities and encourages healthy rivalry between schools and districts, underpinned by equal opportunities, child protection and safeguarding.</p><a class="text-link" href="contact.html">Be part of HSAA →</a></section>'''
home=home.replace('<section class="section wrap" id="sports">', Path('content/pages/home-welcome.html').read_text(encoding='utf-8-sig')+'<section class="section wrap" id="sports">')
PAGE_CONTENT['home'] = ('Home', 'School sport, competitions and borough representative teams for Hackney primary schools.', home)
exec((Path(__file__).parent/'additional-pages.py').read_text(encoding='utf-8-sig'))
for key, children in GROUPS.items():
 title, desc, content = PAGE_CONTENT[key]
 if key == 'home':
  body = content
 else:
  body = intro(key, title, title, desc)
  body += '<div class="wrap content-layout"><article class="article">' + content
  for child in children:
   child_title, child_desc, child_content = PAGE_CONTENT[child]
   body += section_content(child, child_title, child_desc, child_content)
  body += '</article>'
  if key == 'contact':
   body += '<aside class="enquiry"><span class="eyebrow">EMAIL HSAA</span><h2>Start a conversation</h2><p>For school sport, district teams, affiliation or supporting the association, send us an email.</p><a class="button" href="mailto:info@hsaa.org.uk">Email HSAA &rarr;</a></aside></div>'
  else:
   body += '<aside class="enquiry"><span class="eyebrow">CONTACT HSAA</span><h2>How can we help?</h2><p>For participation, competition information, affiliation or supporting HSAA, get in touch.</p><a class="button" href="contact.html">Contact HSAA &rarr;</a></aside></div>'
 filename = 'index' if key == 'home' else key
 if key == 'information':
  # Read Information sequentially, without same-page section jump links.
  body = rewrite_references(body)
  body = re.sub(r'<a\b[^>]*href="(?:information\.html)?#[^"]*"[^>]*>(.*?)</a>', r'\1', body, flags=re.S)
 (D / (filename + '.html')).write_text(rewrite_references(shell(key, title, desc, body)), encoding='utf-8')
# Remove only known legacy generated pages, after the complete pages are written.
for key in PAGE_CONTENT:
 legacy = D / 'html' / (key + '.html')
 if legacy.exists(): legacy.unlink()
legacy_dir = D / 'html'
if legacy_dir.exists() and not any(legacy_dir.iterdir()): legacy_dir.rmdir()
print(f'Created {len(GROUPS)} complete pages in dist/.')
