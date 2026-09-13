from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.base=None;self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='base':self.base=a.get('href')
  if tag=='h1':self.h1+=1
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if k in a and tag!='base':self.refs.append(a[k])
root=Path('dist').resolve();errors=[];count=0
for path in root.rglob('*.html'):
 p=Page();p.feed(path.read_text(encoding='utf-8'));count+=1
 if p.h1!=1:errors.append(str(path)+': h1 count')
 base=path.parent/p.base if p.base else path.parent
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=(base/unquote(u.path)).resolve() if u.path else path
  if not target.exists():errors.append(str(path)+': missing '+ref)
  elif u.fragment:
   q=Page();q.feed(target.read_text(encoding='utf-8'))
   if u.fragment not in q.ids:errors.append(str(path)+': missing anchor '+ref)
 assert 'main-nav' in p.ids
print(f'Checked {count} HTML files, navigation, local assets and fragment links.')
if errors:raise SystemExit('\n'.join(errors))
print('All checks passed.')
