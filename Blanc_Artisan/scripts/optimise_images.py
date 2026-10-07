from pathlib import Path
from PIL import Image,ImageOps
root=Path(__file__).resolve().parents[1]
for path in (root/'dist/assets').glob('*-detail-*.jpg'):
 with Image.open(path) as source:
  image=ImageOps.exif_transpose(source).convert('RGB');image.thumbnail((1200,1600));image.save(path,'JPEG',quality=88,optimize=True)
print('Gallery optimisation complete')
