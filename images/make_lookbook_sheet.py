from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
OUT=Path(__file__).parent/'lookbook'
names=['drake-two-oceans-tree.png','pinnaces-night-approach-nombre-de-dios.png','storming-plaza-nombre-de-dios.png','silver-bars-governors-cellar.png','cacafuego-capture.png']
caps={'drake-two-oceans-tree.png':'Drake first sees the South Sea from the Maroon tree-bower, Cordilleras 1573',
'pinnaces-night-approach-nombre-de-dios.png':'Night approach by pinnaces to Nombre de Dios, 1572',
'storming-plaza-nombre-de-dios.png':'Storming the Plaza, Nombre de Dios, dawn 1572',
'silver-bars-governors-cellar.png':'360 tons of silver bars in the cellar — Drake forbids touching a bar',
'cacafuego-capture.png':'Golden Hind takes the Cacafuego off Punta Galera, night 1579'}
try: F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',26)
except Exception: F=ImageFont.load_default()
thumbs=[]
for n in names:
    im=Image.open(OUT/n); im.thumbnail((760,400)); thumbs.append((n,im))
rows=(len(thumbs)+1)//2
W,H=1700,140+rows*470
sheet=Image.new('RGB',(W,H),'#f6eddc'); d=ImageDraw.Draw(sheet)
d.text((50,30),'Drake and the Tudor Navy - visual lookbook (Corbett vol.1)',fill='#2f2418',font=F)
for i,(n,im) in enumerate(thumbs):
    x=50+(i%2)*820; y=110+(i//2)*470
    sheet.paste(im,(x,y)); d.rectangle([x,y,x+im.width,y+im.height],outline='#2f2418',width=3)
    d.text((x,y+im.height+8),caps[n],fill='#2f2418',font=F)
sheet.save(OUT/'lookbook-contact-sheet.png')
print('saved',sheet.size)
