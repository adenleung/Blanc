"""Prepare concise source-backed display copy without conflicting delivery policies."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def prepare(p):
 raw=p.get('sourceDetails',p.get('details',''));rawdesc=p.get('sourceDescription',p.get('description',''))
 p['sourceDetails']=raw;p['sourceDescription']=rawdesc
 p['flowerDescription']='Custom floral arrangement' if p['category']=='Custom' else p['name'].split(' – ')[1] if p['name'].split(' – ')[0].isupper() and len(p['name'].split(' – '))>1 else p['name'].split(' – ')[0]
 lines=[x.strip() for x in raw.split('\n') if x.strip()]
 good=[x for x in lines if len(x)>85 and not re.search(r'\b(?:AM|PM)\b|\$|2019|2020|2021|MMXIX|same.day|whatsapp|delivery.*(?:free|fee|charge|slot)|complimentary',x,re.I)]
 p['description']=good[0] if good else next((x for x in re.split(r'(?<=[.!])\s+',rawdesc) if 'handpicks' in x),'')
 # Only composition and explicitly sourced seasonal substitution notes are rendered.
 composition=[]
 for i,x in enumerate(lines):
  if x.lower()=='composition':
   for line in lines[i+1:i+18]:
    if re.search(r'delivery|about |when to |care |faq|meaning',line,re.I):break
    composition.append(line)
   break
 if not composition:composition=[x for x in lines if re.search(r'^\d+ (?:rose|stalk)|^\*?final composition|^\*?flowers.*substitut',x,re.I)]
 p['details']='\n'.join(dict.fromkeys(composition))
 p['careNotes']=[x for x in lines if len(x)>35 and re.search(r'vase|direct sunlight|trim.*stem|change.*water|substitut|final composition',x,re.I) and not re.search(r'\$|\b(?:AM|PM)\b|whatsapp',x,re.I)][:5]
 p['availability']='Sold out in source snapshot' if p.get('soldOut') else 'Confirm current availability with florist'
 return p
if __name__=='__main__':
 path=ROOT/'dist/products.json';p=[prepare(x) for x in json.loads(path.read_text())];path.write_text(json.dumps(p,ensure_ascii=False,indent=2))
