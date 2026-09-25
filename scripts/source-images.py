import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('.packaging/content-tools').resolve()))
from PIL import Image,ImageOps,ImageDraw
files=[p for p in Path('source-content').rglob('*') if p.suffix.lower() in ['.jpg','.jpeg','.png']]
out=Path('content-audit');out.mkdir(exist_ok=True)
manifest=[]
for i,p in enumerate(files):
 im=ImageOps.exif_transpose(Image.open(p)); original=im.size;im.thumbnail((1400,1100));im.convert('RGB').save(out/f'image-{i+1}.jpg')
 manifest.append({'id':i+1,'file':str(p),'dimensions':original})
for start in range(0,len(files),8):
 canvas=Image.new('RGB',(1200,900),'white');d=ImageDraw.Draw(canvas)
 for j,p in enumerate(files[start:start+8]):
  im=Image.open(out/f'image-{start+j+1}.jpg');im.thumbnail((290,380));x=(j%4)*300;y=(j//4)*450
  canvas.paste(im,(x,y+40));d.text((x+5,y+5),f'{start+j+1}: {p.name[:33]}',fill='black')
 canvas.save(out/f'contact-sheet-{start//8+1}.jpg')
(out/'images.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Prepared',len(files),'source images for inspection.')
