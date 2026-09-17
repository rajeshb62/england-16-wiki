"""
Drake lookbook — 8 text-to-image assets from Corbett, Drake and the Tudor Navy vol.1
All prompts grounded in specific passages of corbett_drake_tudor_navy_vol1_raw.txt.
Non-map assets only (maps belong to the geography layer).
"""
import os, base64, json, urllib.request
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.hermes/.env'))
KEY = os.environ['OPENROUTER_API_KEY']

OUT = Path(__file__).parent / 'lookbook'
OUT.mkdir(exist_ok=True)

STYLE = ("Style: detailed naturalistic historical reconstruction painting in the manner of late "
         "Victorian marine and narrative history painting, warm period light, muted parchment, sea-green, "
         "tar-black, and crimson accents, accurate Elizabethan sixteenth-century detail, informational and "
         "clear enough for a wiki illustration. No text, no labels, no captions, no borders, no modern objects, "
         "no fantasy elements, no cartoon or anime style.")

SCENES = [
 ("drake-two-oceans-tree.png",
  "Scene: Panama, 1573. In a cleared glade on the highest ridge of the Cordilleras stands a great tree which "
  "local Maroon guides have cut with steps to ascend nearly to the top, where a convenient bower has been made "
  "large enough for ten or twelve men to sit; trees to the south and north have been felled to open out the view. "
  "At the top of the tree, in the bower, a tall English captain in plain seaman's clothes stands beside the Maroon "
  "chief, gazing out over an astonishing vista: on one side the Caribbean/Atlantic, on the far side the fabled "
  "South Sea (Pacific), both oceans visible at once under a fair windy day. Below, a small group of English sailors "
  "climbs the carved steps, faces full of wonder. Tropical ridge landscape, cloud forest, distant silver seas."),
 ("pinnaces-night-approach-nombre-de-dios.png",
  "Scene: night approach to Nombre de Dios, 1572. A line of four small open English pinnaces and a shallop, "
  "muffled oars, packed with armed men (pikes, muskets, calivers, bows, targets, fire-pikes), stealing in deep "
  "silence along the dark shore toward the point of the bay, past a distant Spanish watch-house on the headland "
  "with a faint lantern. High land shadows the anchorage; a tropical night sky, moonlight on low swells, the "
  "sleeping town of Nombre de Dios faintly visible round the point. Tense, hushed atmosphere."),
 ("storming-plaza-nombre-de-dios.png",
  "Scene: dawn assault on the Plaza of Nombre de Dios, 1572. English seamen led by their captain come up the main "
  "street with blazing fire-pikes, drums and trumpets sounding, yelling; a second party enters from the eastward "
  "past the King's Treasure-house, splitting the defence. Spanish soldiers and townsfolk in panic before the "
  "Governor's house; a falling trumpeter in the foreground; push of pike and clubbed muskets in the square. "
  "Spanish colonial town architecture: whitewashed walls, arcaded Plaza, the battery and fort above."),
 ("silver-bars-governors-cellar.png",
  "Scene: interior of the Governor's house at Nombre de Dios, 1572. In a dark stone cellar, English sailors with "
  "torches stand amazed before an enormous piled stack of silver bars — a pile some seventy feet long, ten feet "
  "broad and twelve feet high, each bar a heavy ingot of about thirty-five to forty pounds. Their captain, arm in "
  "a bandage, forbids them to touch a single bar; the men's faces show disbelief and longing. Torchlight on dull "
  "gleaming silver, deep shadow, restrained drama."),
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
 ("cacafuego-capture.png",
  "Scene: off Punta Galera, Peru coast, 1579, night. The small English galleon Golden Hind, having cunningly "
  "trailed empty wine-jars astern to slow herself during the day, now cuts away her drags and runs under the "
  "stern of the great rich Spanish ship Nuestra Señora de la Concepción (the 'Cacafuego'), laying herself alongside "
  "about nine o'clock at night. Moonlight, lanterns, the towering Spanish hull beside the low English ship, "
  "boarding parties at the rails, a volley of small shot over the Spaniard's deck. South Sea swell, dramatic "
  "ship-to-ship composition."),
 ("golden-hind-deptford-knighting.png",
  "Scene: Deptford on the Thames, April 1581. Queen Elizabeth in state visits the Golden Hind moored at Deptford, "
  "a banquet served on board finer than any seen in England since King Henry's time. On the deck, before a vast "
  "concourse crowding the river banks, boats and rigging, the Queen bids the captain kneel and, with a jest on "
  "her lips, hands a gilded sword to a young French nobleman to give the accolade — the dubbing of the master "
  "thief of the unknown world in open defiance of Spain. The ship hung with silk banners: England ancient, red "
  "flags with white cross and gold devices — hawk, globe, pole-star. River pageantry, crowds, state barge."),
]

def gen(prompt, fname):
    body = json.dumps({"model":"google/gemini-2.5-flash-image","messages":[
        {"role":"user","content":prompt}]})
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
        data=body.encode(), headers={'Authorization':f'Bearer {KEY}','Content-Type':'application/json'})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    msg = r['choices'][0]['message']
    imgs = msg.get('images') or []
    if not imgs and isinstance(msg.get('content'), list):
        imgs = [p for p in msg['content'] if p.get('type')=='image_url' for p in [{'image_url':p['image_url']}]]
    if not imgs:
        raise RuntimeError(f'no image in response for {fname}: {str(r)[:300]}')
    b64 = imgs[0]['image_url']['url'].split(',',1)[1]
    (OUT/fname).write_bytes(base64.b64decode(b64))
    print('OK', fname, (OUT/fname).stat().st_size)

for fname, scene in SCENES:
    prompt = scene + ' ' + STYLE
    for attempt in range(3):
        try:
            gen(prompt, fname); break
        except Exception as e:
            print('retry', fname, attempt, str(e)[:200])
    else:
        print('FAILED', fname)
print('done')
