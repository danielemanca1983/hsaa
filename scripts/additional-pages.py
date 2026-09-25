# Executed by build-pages.py with its shared templates.
import json
CONTENT = Path('content')
def read_fragment(name):
 return (CONTENT / 'pages' / (name + '.html')).read_text(encoding='utf-8-sig')

def table(caption, headings, rows):
 head = ''.join('<th scope="col">' + escape(h) + '</th>' for h in headings)
 body = ''.join('<tr><th scope="row">' + escape(str(r[0])) + '</th>' + ''.join('<td>' + escape(str(c)) + '</td>' for c in r[1:]) + '</tr>' for r in rows)
 return '<div class="table-scroll" role="region" aria-label="' + escape(caption) + '" tabindex="0"><table><caption>' + escape(caption) + '</caption><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div>'

def page(key, title, desc, content):
 PAGE_CONTENT[key] = (title, desc, content)

people = json.loads((CONTENT/'people.json').read_text(encoding='utf-8-sig'))
records = json.loads((CONTENT/'records.json').read_text(encoding='utf-8-sig'))
partners = '<div class="partner-grid">'
for name, logo, url in people['partners']:
 image = '<img src="../assets/source/' + logo + '" alt="" loading="lazy">'
 inside = '<span class="partner-logo-frame">' + image + '</span><span>' + escape(name) + '</span>'
 partners += '<a class="partner" href="' + url + '">' + inside + '</a>' if url and not url.startswith('#') else '<div class="partner">' + inside + '</div>'
partners += '</div>'
replacements = {
 '{{CONTACT}}':section_content('contact', 'Contact Us', 'Contact HSAA for school sport, district football, affiliation and supporting the association.', read_fragment('contact')),
 '{{HISTORY}}':read_fragment('history'),
 '{{PLAYERS}}':table('Former district players and career highlights', ['Player', 'Clubs and international teams'], people['players']),
 '{{ASSOCIATION}}':table('Association and district figures', ['Name', 'Role recorded in the archive'], people['association']),
 '{{PARTNERS}}':partners,
 '{{WINNERS}}':table('Lester Finch Trophy — winners by season', ['Season', 'Winner(s)'], records['lester_winners']),
 '{{TOTALS}}':table('Lester Finch Trophy — supplied past winners totals', ['District', 'Wins in supplied table'], records['lester_totals'])
}
for key,title,desc in [
 ('about','About us','Our mission, history and the people behind school sport in Hackney.'),
 ('schools-football','Schools Football','School competitions, cup histories and affiliation for Hackney primary schools.'),
 ('five-a-side','Five a sides','The Stan Le Brom boys’ trophy and Alan Hutchinson girls’ trophy.'),
 ('nine-a-side','Nine a side League','Boys’ and girls’ school football, and the history of the Hackney Schools Cup.'),
 ('teams','District Football – Boys & Girls','Representing Hackney through district competitions, festivals and tours.'),
 ('contact','Get in touch','Contact HSAA for school sport, representative teams and supporting the association.'),
 ('young-active','Young & Active Hackney 2030','Annual school affiliation and the planned wider sporting programme.'),
 ('contacts-supporters','Schools FA Contacts & HSAA Supporters','The organisations connected with and supporting HSAA.'),
 ('illuminaries','Hackney District & Association Illuminaries','Former players, association figures and the District Players Alumni Network.'),
 ('john-larter-foundation','John Larter MBE Foundation','A development pathway inspired by John’s contribution to grassroots football.'),
 ('district-competitions','District Competitions','The Kay Trophy, John Larter Girls District Trophy and Lester Finch Trophy archive.')]:
 body = read_fragment(key)
 for token,value in replacements.items(): body = body.replace(token,value)
 page(key,title,desc,body)

page('football','Football','School and district football for boys and girls across Hackney.', '<p>HSAA delivers football competitions for Hackney primary schools and oversees the borough’s boys’ and girls’ district teams.</p>')
page('other-sports','HSAA Other Sporting Competitions','The planned sporting programme for 2026–27.', '<p>HSAA plans to run kwik cricket, tag rugby, the Primary Cross Country League and orienteering festivals in 2026–27. Schools must be affiliated to the Young &amp; Active 2030 programme to take part.</p>'+directory(NAVIGATION[3][2])+'<p><a href="orienteering.html">Orienteering festivals</a> are also included in the planned programme.</p><figure><img class="wide-image" src="../assets/source/association-archive.jpg" alt="Two adults looking through papers in a photograph from the HSAA archive" loading="lazy"><figcaption>From the HSAA archive.</figcaption></figure>')
page('information','Information','Contacts, supporters, association connections and district competitions.','')
for key,title in [('cross-country','Cross Country League'),('kwik-cricket','Kwik Cricket'),('tag-touch','Tag Rugby'),('orienteering','Orienteering')]:
 content = '<h2>Planned for 2026–27</h2><p>' + title + ' is included in HSAA’s planned 2026–27 programme for Hackney primary schools.</p><p>Schools must be affiliated to the <a href="young-active.html">Young &amp; Active Hackney 2030 programme</a> to take part.</p><h2>Taking part</h2><p>For entry arrangements, eligible year groups, competition formats, venues and dates, <a href="contact.html">get in touch with HSAA</a>.</p>'
 if key=='orienteering': content=content.replace('Orienteering is included','Orienteering festivals are included')
 if key=='kwik-cricket':
  content += '<section id="boys"><h3>Boys’ participation</h3><p>Contact HSAA for boys’ competition arrangements.</p></section><section id="girls"><h3>Girls’ participation</h3><p>Contact HSAA for girls’ competition arrangements.</p></section>'
 page(key,title,'Part of HSAA’s planned wider sporting programme for Hackney primary schools.',content)

for key,heading,organisation,competitions in [
 ('football-results','Schools Football','School',['Nine a side League — Boys','Nine a side League — Girls']),
 ('district-results','District Football','District',['Kay Trophy','John Larter Girls District Trophy','Lester Finch Trophy'])]:
 options='<option value="">Choose the competition</option>'+''.join(f'<option>{escape(c)}</option>' for c in competitions)
 content='<h2>Report a result</h2><p>Please include the fixture date, both teams and the final score, and select the correct competition.</p>'
 content+='<p>This service is for '+('the boys’ and girls’ Nine a side Leagues.' if organisation=='School' else 'the Inner London Kay Trophy, John Larter Girls District Trophy and Lester Finch Trophy.')+'</p>'
 content+='<p>Complete the form to prepare an email to HSAA. Your email app opens for you to review and send it. Results are not sent or stored by this website.</p>'
 content+=f'<form class="result-form" data-organisation="{organisation}" aria-label="Report a {heading} result"><label>Your name<input name="name" autocomplete="name" required maxlength="120"></label><label>{organisation} submitting the result<input name="school" required maxlength="160"></label><label>Competition<select name="competition" required>{options}</select></label><label>Fixture date<input type="date" name="date" required></label><label>Teams and final score<input name="score" placeholder="Team A 2 – 1 Team B" required maxlength="200"></label><button class="button" type="submit">Prepare results email ↗</button><p class="form-status" role="status"></p></form>'
 content+='<noscript><p>Please email your name, school or district, competition, fixture date, teams and score to <a href="mailto:info@hsaa.org.uk">info@hsaa.org.uk</a>.</p></noscript><h2>Results and tables</h2><p><a href="contact.html">Contact HSAA</a> for the latest results, draws and league tables.</p>'
 page(key,heading+' Results Service','Submit a '+heading.lower()+' result to HSAA.',content)
