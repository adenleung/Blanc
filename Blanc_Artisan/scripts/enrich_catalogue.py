"""Recollect public source fields; no credentials, orders or inferred variants."""
import json,datetime,urllib.request,concurrent.futures,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist';DATE=datetime.datetime.now(datetime.timezone.utc).isoformat();products=json.loads((DIST/'products.json').read_text());report=[]
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (catalogue snapshot)'})
 return urllib.request.urlopen(req,timeout=40).read()
def collect(p):
 try:
  soup=BeautifulSoup(fetch(p['url']),'html.parser');p['collectedAt']=DATE;p['source']=p['url']
  desc=soup.select_one('.woocommerce-product-details__short-description');long=soup.select_one('#tab-description')
  p['description']=desc.get_text(' ',strip=True) if desc else ''
  p['details']=long.get_text('\n',strip=True) if long else ''
  p['sourceDetails']=p['details'];p['sourceDescription']=p['description']
  p['options']={}
  for select in soup.select('.variations select'):
   vals=[o.get_text(' ',strip=True) for o in select.select('option') if o.get('value')]
   if vals:p['options'][select.get('name','Option').replace('attribute_','').replace('pa_','').replace('-',' ').title()]=vals
  form=soup.select_one('form.variations_form');raw=form.get('data-product_variations') if form else None
  variants=json.loads(raw) if raw and raw!='false' else []
  p['variants']=[{'attributes':v.get('attributes',{}),'price':v.get('display_price'),'inStock':v.get('is_in_stock'),'image':v.get('image',{}).get('src')} for v in variants if isinstance(v,dict) and isinstance(v.get('display_price'),(int,float))]
  p['occasions']=[];p['occasionSources']={}
  for a in soup.select('.posted_in a'):
   name=a.get_text(' ',strip=True)
   if any(w in name.lower() for w in ['birthday','anniversary','proposal','graduation','wedding','bridal']):p['occasions'].append(name);p['occasionSources'][name]=a.get('href')
  stock=soup.select_one('.stock');p['availability']=stock.get_text(' ',strip=True) if stock else 'Confirm with florist';p['soldOut']=bool(stock and 'out-of-stock' in stock.get('class',[]))
  gallery=[]
  for a in soup.select('.woocommerce-product-gallery__image a'):
   url=a.get('href');
   if url and url.startswith('http') and url not in gallery:gallery.append(url)
  p['gallery']=[p['image']]
  for n,url in enumerate(gallery[:3]):
   path=f"assets/{p['id']}-detail-{n}.jpg"
   try:(DIST/path).write_bytes(fetch(url));p['gallery'].append(path)
   except Exception:pass
  report.append({'url':p['url'],'status':'collected','options':len(p['options']),'variants':len(p['variants'])})
 except Exception as e:
  p.setdefault('collectedAt','2026-10-07');p.setdefault('description','');p.setdefault('options',{});p.setdefault('variants',[]);p.setdefault('occasions',[]);p.setdefault('gallery',[p['image']]);p['availability']='Confirm with florist';report.append({'url':p['url'],'status':'failed','reason':str(e)})
 return p
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:products=list(pool.map(collect,products))
from prepare_catalogue import prepare
products=[prepare(p) for p in products]
(DIST/'products.json').write_text(json.dumps(products,ensure_ascii=False,indent=2));(ROOT/'COLLECTION_REPORT.json').write_text(json.dumps(report,indent=2));print('Collected',sum(x['status']=='collected' for x in report),'of',len(products))
# Category metadata and suitable editorial imagery are source backed.
features={}
for key,url in [('money','https://blancartisan.com/money-bouquet-singapore/'),('wedding','https://blancartisan.com/product/white-tulip-bridal-bouquet-singapore/')]:
 try:
  soup=BeautifulSoup(fetch(url),'html.parser');im=soup.select_one('.woocommerce-product-gallery__image img') or soup.select_one('li.product img')
  if im:
   remote=im.get('data-src') or im.get('src');path=f'assets/{key}.jpg';(DIST/path).write_bytes(fetch(remote));features[key]={'url':url,'image':path,'source':remote,'collectedAt':DATE}
 except Exception as e:print(key,str(e))
features['occasions']={'birthday':'https://blancartisan.com/birthday-bouquet-delivery-singapore/','anniversary':'https://blancartisan.com/anniversary-bouquet-delivery-singapore/','graduation':'https://blancartisan.com/graduation-bouquet-delivery-singapore/'}
features['occasionSource']='https://blancartisan.com/'
(DIST/'features.json').write_text(json.dumps(features,indent=2))
