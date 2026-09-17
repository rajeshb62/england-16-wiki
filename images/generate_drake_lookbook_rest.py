"""Finish remaining lookbook scenes (free-tier credit window)."""
import os, base64, json, urllib.request, time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.hermes/.env'))
KEY = os.environ['OPENROUTER_API_KEY']
OUT = Path(__file__).parent / 'lookbook'
STYLE = ("Style: detailed naturalistic historical reconstruction painting in the manner of late "
         "Victorian marine and narrative history painting, warm period light, muted parchment, sea-green, "
         "tar-black, and crimson accents, accurate Elizabethan sixteenth-century detail, informational and "
         "clear enough for a wiki illustration. No text, no labels, no captions, no borders, no modern objects, "
         "no fantasy elements, no cartoon or anime style.")
SCENES = [
 ("mule-train-ambush.png",
  "Scene: the Panama road, 1573. A royal recua of fifty to seventy laden mules on a narrow forest track, each "
  "mule carrying bales and chests of silver, escorted by Spanish soldiers with advance and rear guard; ahead a "
  "private train of fourteen mules, eight laden with gold and one with jewels, with the Treasurer of Lima and his "
  "daughter riding. Maroon allies and English seamen wait in ambush among the trees at a choke point of the road. "
  "Dappled jungle light, tension before the strike, mules, bells, armed men."),
 ("doughty-communion-port-julian.png",
  "Scene: Port St Julian, Patagonia, 1578. On a bleak shore beside beached ship's boats, a solemn open-air "
  "communion: a chaplain in a white surplice administers the Sacrament at a makeshift table to a condemned "
  "gentleman prisoner, calm and dignified, and to the captain-general himself who kneels beside him as an equal "
  "communicant. After the communion the two sit down together to a simple banquet at the same table, cheerful in "
  "sobriety, crew standing in a respectful ring at a distance, ships of the squadron at anchor in the cold bay "
  "beyond. Grave, ceremonial, reconciliatory mood."),
 ("golden-hind-deptford-knighting.png",
  "Scene: Deptford on the Thames, April 1581. Queen Elizabeth in state visits the Golden Hind moored at Deptford, "
  "a banquet served on board finer than any seen in England since King Henry's time. On the deck, before a vast "
  "concourse crowding the river banks, boats and rigging, the Queen bids the captain kneel and, with a jest on "
  "her lips, hands a gilded sword to a young French nobleman to give the accolade — the dubbing of the master "
  "thief of the unknown world in open defiance of Spain. The ship hung with silk banners: England ancient, red "
  "flags with white cross and gold devices — hawk, globe, pole-star. River pageantry, crowds, state barge."),
]
def gen(prompt, fname):
    body=json.dumps({"model":"google/gemini-2.5-flash-image","messages":[{"role":"user","content":prompt}]})
    req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body.encode(),
      headers={'Authorization':f'Bearer {KEY}','Content-Type':'application/json'})
    r=json.load(urllib.request.urlopen(req, timeout=300))
    imgs=r['choices'][0]['message'].get('images') or []
    if not imgs: raise RuntimeError('no image: '+str(r)[:200])
    (OUT/fname).write_bytes(base64.b64decode(imgs[0]['image_url']['url'].split(',',1)[1]))
    print('OK', fname, (OUT/fname).stat().st_size)
for fname, scene in SCENES:
    if (OUT/fname).exists(): print('skip', fname); continue
    for attempt in range(5):
        try: gen(scene+' '+STYLE, fname); break
        except Exception as e:
            print('retry', fname, attempt, str(e)[:120]); time.sleep(90)
    else: print('FAILED', fname)
print('done')
