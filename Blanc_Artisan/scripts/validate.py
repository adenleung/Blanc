import json,re
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
root=Path(__file__).resolve().parents[1];dist=root/'dist';s=BeautifulSoup((dist/'index.html').read_text(),'html.parser')
ids=[x['id'] for x in s.select('[id]')];assert len(ids)==len(set(ids)), 'Duplicate IDs'
for el in s.select('[aria-labelledby]'):
 for id in el['aria-labelledby'].split():assert id in ids or id=='productTitle'
for el in s.select('[src]'):
 if not el['src'].startswith('http'):assert (dist/el['src']).is_file(),el['src']
for a in s.select('a[href^="#"]'):
 assert a['href']=='#' or a['href'][1:] in ids,a['href']
p=json.loads((dist/'products.json').read_text());assert len({x['id'] for x in p})==len(p)
for x in p:
 assert x['url'].startswith('https://blancartisan.com/product/')
 assert x['max']>=x['price']>=0
 for image in x['gallery']:
  with Image.open(dist/image) as im:im.verify()
 for v in x['variants']:assert isinstance(v['price'],(int,float)) and v['price']>=0
 for text in [x['description'],x['details']]:assert not re.search(r'\b(?:10AM|11AM|12PM|7PM)\b|\+\$10',text,re.I)
print('PASS: HTML anchors, dialog labels, asset references, catalogue IDs, price ranges, gallery decoding, variant prices and display-policy checks')
print('Products:',len(p),'Published variants:',sum(len(x['variants']) for x in p),'Gallery entries:',sum(len(x['gallery']) for x in p))
def lum(hex):
 rgb=[int(hex[i:i+2],16)/255 for i in (0,2,4)];v=[a/12.92 if a<=.04045 else ((a+.055)/1.055)**2.4 for a in rgb];return .2126*v[0]+.7152*v[1]+.0722*v[2]
for foreground in ['171715','605b54','526048']:
 ratio=(lum('f6f2ec')+.05)/(lum(foreground)+.05);assert ratio>=4.5;print('Contrast',foreground,'on ivory:',round(ratio,2))
