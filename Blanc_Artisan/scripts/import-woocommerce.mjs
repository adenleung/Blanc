/** Owner-authorised catalogue import. Never run with secret values in command arguments. */
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import path from 'node:path';
const origin=process.env.WOO_ORIGIN,key=process.env.WOO_CONSUMER_KEY,secret=process.env.WOO_CONSUMER_SECRET;
if(!origin||!key||!secret)throw Error('Set WOO_ORIGIN, WOO_CONSUMER_KEY and WOO_CONSUMER_SECRET in your local environment.');
const base=new URL(origin);if(base.protocol!=='https:')throw Error('WooCommerce requires HTTPS.');
const source=JSON.parse(await readFile('public/products.json','utf8')),collectedAt=new Date().toISOString();
async function api(route){const url=new URL('/wp-json/wc/v3/'+route,base);const r=await fetch(url,{headers:{Authorization:'Basic '+Buffer.from(key+':'+secret).toString('base64')},redirect:'error'});if(!r.ok)throw Error('WooCommerce import request failed ('+r.status+').');return r.json();}
async function all(route){let rows=[];for(let n=1;n<=100;n++){const page=await api(route+(route.includes('?')?'&':'?')+'per_page=100&page='+n);rows.push(...page);if(page.length<100)break;if(n===100)throw Error('Catalogue exceeds importer safety limit.');}return rows;}
const text=s=>String(s||'').replace(/<[^>]*>/g,' ').replace(/&amp;/g,'&').replace(/&nbsp;/g,' ').replace(/\s+/g,' ').trim();
await mkdir('public/assets/imported',{recursive:true});
async function image(im,id,index){const url=new URL(im.src);if(url.protocol!=='https:')throw Error('Non-HTTPS image rejected.');const r=await fetch(url,{redirect:'error'});if(!r.ok)throw Error('Official image download failed.');const type=r.headers.get('content-type')?.split(';')[0];const extension={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[type];if(!extension)throw Error('Unsupported official image type.');if(Number(r.headers.get('content-length'))>15000000)throw Error('Image too large.');const bytes=Buffer.from(await r.arrayBuffer());if(bytes.length>15000000)throw Error('Image too large.');const file=`assets/imported/${id}-${index}.${extension}`;await writeFile(path.join('public',file),bytes);return file;}
const products=[],inventory=[],warnings=[];
for(const p of await all('products?status=publish')){
 if(!['simple','variable'].includes(p.type)){warnings.push('Unsupported product type '+p.id+': '+p.type);continue;}
 const previous=source.find(x=>new URL(x.url).pathname===new URL(p.permalink).pathname),id=previous?.id??1000000+p.id;
 const variations=p.type==='variable'?await all('products/'+p.id+'/variations'):[];
 const options=Object.fromEntries((p.attributes||[]).filter(a=>a.variation).map(a=>[a.name,a.options]));
 const variants=variations.filter(v=>v.status==='publish'&&v.price!==''&&!v.virtual).map(v=>({wooVariantId:v.id,price:Number(v.price),inStock:v.stock_status==='instock',attributes:Object.fromEntries(v.attributes.map(a=>['attribute_'+a.name,a.option]))}));
 if(p.type==='variable'&&!variants.length){warnings.push('No complete variants for '+p.id);continue;}
 const gallery=[];for(const [i,im]of (p.images||[]).entries())gallery.push(await image(im,id,i));
 if(!gallery.length){warnings.push('Missing image for '+p.id);continue;}
 const prices=variants.length?variants.map(v=>v.price):[Number(p.price)];if(!prices.every(Number.isFinite)||p.price===''){warnings.push('Missing price for '+p.id);continue;}
 const product={...previous,id,wooProductId:p.id,name:p.name,url:p.permalink,category:p.categories?.[0]?.name||'Flowers',price:Math.min(...prices),max:Math.max(...prices),image:gallery[0],gallery,description:text(p.short_description||p.description),details:text(p.description),flowerDescription:previous?.flowerDescription||text(p.short_description),options,variants,inStock:p.stock_status==='instock',careNotes:previous?.careNotes||[],source:{url:p.permalink,collectedAt,method:'owner-authorised WooCommerce REST v3'},leadDays:null,sameDay:null};
 products.push(product);
 if(p.type==='simple'&&p.manage_stock&&Number.isInteger(p.stock_quantity))inventory.push({id:id+':simple',available:Math.max(0,p.stock_quantity)});
 variants.forEach((v,i)=>{const official=variations.find(x=>x.id===v.wooVariantId);if(official.manage_stock&&Number.isInteger(official.stock_quantity))inventory.push({id:id+':'+i,available:Math.max(0,official.stock_quantity)});else warnings.push('Owner stock capacity required: '+id+':'+i);});
 if(p.type==='simple'&&!p.manage_stock)warnings.push('Owner stock capacity required: '+id+':simple');
}
await mkdir('data',{recursive:true});
await writeFile('data/owner-import.json',JSON.stringify({delivery:{approved:false,policiesApproved:false,cutoff:null,baseFee:null,blackoutDates:[],excludedPrefixes:[],surcharges:[],policies:{delivery:'',substitution:'',refunds:'',privacy:'',terms:''}},products,inventory,slots:[]},null,2));
await writeFile('data/import-report.json',JSON.stringify({collectedAt,source:base.origin,products:products.length,warnings},null,2));
console.log(`Imported ${products.length} products into data/owner-import.json. Review ${warnings.length} warnings; fill owner delivery and stock data before approval. Nothing has been published or activated.`);
