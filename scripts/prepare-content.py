"""One-off import of reviewed source data and supplied assets (not a build dependency)."""
import json,re,shutil,sys
from pathlib import Path
from html import escape
sys.path.insert(0,str(Path('.packaging/content-tools').resolve()))
from PIL import Image,ImageOps
out=Path('content/pages');out.mkdir(parents=True,exist_ok=True)
records=json.loads(Path('content-audit/extracted.json').read_text(encoding='utf-8-sig'))
def record(name): return next(r for r in records if r['file'].endswith('\\'+name))
def paragraphs(text): return ''.join('<p>'+escape(p.strip())+'</p>\n' for p in re.split(r'[\r\v]+',text) if p.strip())
assets=Path('dist/assets/source');assets.mkdir(exist_ok=True)
images=json.loads(Path('content-audit/images.json').read_text())
names={1:'hsaa-logo',3:'contact-football',4:'supporters-team',5:'lester-finch-action',6:'alumni-football',7:'alumni-flyer',8:'history-team',9:'district-group',10:'association-archive',11:'introduction-football',12:'foundation-team',13:'mission-football',14:'schools-goalkeepers',15:'district-huddle',16:'boys-2026',17:'girls-celebration',18:'girls-2026'}
for item in images:
 if item['id'] not in names: continue
 im=ImageOps.exif_transpose(Image.open(item['file'])).convert('RGB');im.thumbnail((1600,1400))
 im.save(assets/(names[item['id']]+'.jpg'),quality=88,optimize=True)
logos={1028:'inner-london',1029:'esfa',1030:'wickers',1031:'gloucester',1039:'kent',1046:'public-digital',1047:'social-matters',1048:'location-location',1049:'swansea',1050:'jersey',1051:'sportinspired',1052:'team-get-involved'}
for ident,name in logos.items(): shutil.copyfile(f'content-audit/supporter-1-{ident}.png',assets/(name+'.png'))
shutil.copyfile('content-audit/foundation-1-1028.png',assets/'foundation-logo.png')
# This deck embeds the Sports Empire logo as a drawing. Crop the supplied render.
im=Image.open('content-audit/deck-14-slide-1.jpg');im.crop((650,560,950,685)).save(assets/'sports-empire.jpg',quality=95)
downloads=Path('dist/downloads');downloads.mkdir(exist_ok=True)
membership=record('HACKNEY DISTRICT ALMUNI NETWORK MEMBERSHIP FORM.doc')
shutil.copyfile(Path('source-content')/membership['file'],downloads/'hsaa-alumni-membership-form.doc')

history=record('Hisotory of Hackney Schools Athletic Association.ppt')
text='\r'.join(s['text'][1] for s in history['slides'])
text=text.replace('The same trophy is still contested today surely making it one of the oldest football trophies still contested.', 'The trophy went on to be contested for more than a century. The school football history records its last playing in 2004–05 and the re-establishment of the school league in 2025–26.')
text=text.replace('who also gave Victoria Park to the people of the impoverished east end of London', 'who also donated the drinking fountain in Victoria Park')
text=text.replace('as the supervised', 'as they supervised').replace('in recent years', 'in the period covered by this account').replace('more recently Jason Matthews', 'Jason Matthews')
(out/'history.html').write_text('<p class="content-note">An account by David LeFevre, drawing on documents by Colm Kerrigan and John Larter MBE. Historical descriptions refer to the period covered by the account.</p>\n'+paragraphs(text),encoding='utf-8')

trophy=record('Lester Finch Trophy Past Winners & Table.doc')
roll=[]
for line in trophy['text'].split('PAST WINNERS TABLE')[0].split('\r'):
 for year,winner in re.findall(r'(\d{4}-\d{2})\s+(.+?)(?=\s+\d{4}-\d{2}|$)',line): roll.append([year,winner.strip()])
roll.sort()
data={'lester_winners':roll,'lester_totals':trophy['tables'][0][1:]}
Path('content/records.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared 17 supplied images, 14 logos, the blank alumni form, history copy and',len(roll),'trophy seasons.')
