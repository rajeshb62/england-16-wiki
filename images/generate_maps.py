"""
Generate purpose-drawn maps for the England 16th Century knowledge base.
Run from the wiki/images/ directory: python3 generate_maps.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.lines as mlines
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature
import warnings
warnings.filterwarnings('ignore')

# ── Shared style constants ──────────────────────────────────────────────────
OCEAN      = '#c8ddf0'
LAND       = '#e8e0d0'
BORDER     = '#b0a898'
COAST      = '#8a9aaa'
ROUTE_A    = '#c0392b'   # red/Spanish
ROUTE_B    = '#d4860a'   # gold/Drake
ROUTE_C    = '#1a6b4a'   # teal
ROUTE_D    = '#2c5f8a'   # blue
NODE_COL   = '#8B1A1A'   # dark red dots
INTEL_COL  = '#e67e22'   # amber intel nodes
LABEL_COL  = '#1a1a2e'
SHADOW     = dict(path_effects=[pe.withStroke(linewidth=2.5, foreground='white')])
DPI        = 200


def add_title_box(ax, title, subtitle=None):
    """Add a styled title box in the upper-left corner."""
    txt = title if subtitle is None else f"{title}\n{subtitle}"
    ax.text(0.02, 0.98, txt, transform=ax.transAxes,
            fontsize=9, fontweight='bold', color='#1a1a2e',
            va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='#999', alpha=0.88))


def label(ax, lon, lat, text, transform, offset=(4, 4), fontsize=7.5,
          ha='left', va='bottom', bold=False):
    weight = 'bold' if bold else 'normal'
    ax.text(lon + offset[0] * 0.01 * (ax.get_xlim()[1] - ax.get_xlim()[0]),
            lat + offset[1] * 0.01 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
            text, transform=transform, fontsize=fontsize, color=LABEL_COL,
            ha=ha, va=va, fontweight=weight, **SHADOW)


def dot(ax, lon, lat, transform, color=NODE_COL, size=40, zorder=5, marker='o'):
    ax.scatter([lon], [lat], transform=transform, color=color,
               s=size, zorder=zorder, marker=marker, edgecolors='white', linewidths=0.6)


def arrow_route(ax, lons, lats, transform, color, lw=1.8, alpha=0.85,
                n_arrows=3, head_width=0.4, zorder=4):
    """Draw a route with periodic directional arrows."""
    ax.plot(lons, lats, transform=transform, color=color, lw=lw,
            alpha=alpha, zorder=zorder, solid_capstyle='round')
    # Place arrows at evenly-spaced intervals along the path
    total = len(lons)
    step = max(1, total // (n_arrows + 1))
    for i in range(step, total - step, step):
        dx = lons[i+1] - lons[i-1]
        dy = lats[i+1] - lats[i-1]
        ax.annotate('', xy=(lons[i] + dx*0.01, lats[i] + dy*0.01),
                    xytext=(lons[i] - dx*0.01, lats[i] - dy*0.01),
                    transform=transform,
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                   mutation_scale=12),
                    zorder=zorder + 1)


# ═══════════════════════════════════════════════════════════════════════════
# MAP 1 — Spanish Armada Route (1588)
# ═══════════════════════════════════════════════════════════════════════════
def map_armada():
    fig = plt.figure(figsize=(10, 9))
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent([-22, 16, 34, 64], crs=proj)

    ax.add_feature(cfeature.OCEAN.with_scale('50m'), color=OCEAN)
    ax.add_feature(cfeature.LAND.with_scale('50m'), color=LAND, edgecolor=COAST, lw=0.5)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), edgecolor=BORDER, lw=0.5)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor=COAST, lw=0.6)

    # ── Armada outbound route (red) ──
    # Lisbon → A Coruña (restocking) → English Channel → Calais → Gravelines
    outbound_lons = [-9.1, -11, -13, -12, -10, -8.5, -6, -4, -2, -0.5, 1.5, 2.5]
    outbound_lats = [38.7, 42,  45,  47,  48,  49,  50, 50.5, 50.4, 50.5, 50.9, 51.0]
    ax.plot(outbound_lons, outbound_lats, transform=proj,
            color=ROUTE_A, lw=2.2, alpha=0.9, zorder=4, solid_capstyle='round')
    # A Coruña to Channel leg
    for i in range(1, len(outbound_lons)-1, 3):
        dx = outbound_lons[i+1] - outbound_lons[i-1]
        dy = outbound_lats[i+1] - outbound_lats[i-1]
        ax.annotate('', xy=(outbound_lons[i]+dx*0.3, outbound_lats[i]+dy*0.3),
                    xytext=(outbound_lons[i]-dx*0.3, outbound_lats[i]-dy*0.3),
                    arrowprops=dict(arrowstyle='->', color=ROUTE_A, lw=1.5, mutation_scale=12),
                    zorder=5)

    # ── Armada return route (dashed orange) — north of Scotland, west of Ireland ──
    return_lons = [2.5, 2.0, 1.0, -1.0, -3.0, -5.0, -7.0, -9.0, -10.5,
                   -12.0, -14.0, -15.5, -14.0, -12.0, -9.5, -8.0, -7.0, -8.5, -8.8]
    return_lats = [51.0, 52.5, 54.0, 55.5, 57.0, 58.5, 60.0, 61.5, 62.5,
                   61.0, 59.0, 56.5, 54.0, 52.0, 50.0, 47.5, 44.5, 41.0, 38.7]
    ax.plot(return_lons, return_lats, transform=proj,
            color='#e67e22', lw=1.8, alpha=0.85, zorder=4,
            linestyle='--', dashes=(6, 3))
    # Arrow on return
    mid = len(return_lons) // 2
    ax.annotate('', xy=(return_lons[mid+1], return_lats[mid+1]),
                xytext=(return_lons[mid-1], return_lats[mid-1]),
                arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.5, mutation_scale=12),
                zorder=5)

    # ── Parma's army embarkation zone ──
    ax.plot([2.6, 3.2], [51.0, 51.2], transform=proj,
            color='#8B008B', lw=2, zorder=4, linestyle=':')

    # ── Key cities ──
    cities = {
        'Lisbon':       (-9.1,  38.7),
        'A Coruña':     (-8.4,  43.35),
        'Plymouth':     (-4.14, 50.37),
        'Calais':       (1.85,  50.95),
        'Gravelines':   (2.13,  51.01),
        'Dunkirk\n(Parma)': (2.38, 51.04),
        'London':       (-0.12, 51.5),
        'Edinburgh':    (-3.2,  55.95),
        'Dublin':       (-6.26, 53.33),
    }
    for name, (lon, lat) in cities.items():
        dot(ax, lon, lat, proj, color=NODE_COL, size=25)
        offset_x = 0.4 if lon < 0 else -0.4
        ha = 'left' if lon < -2 else 'right'
        ax.text(lon + offset_x, lat + 0.3, name, transform=proj,
                fontsize=6.8, color=LABEL_COL, ha=ha, va='bottom', **SHADOW)

    # ── Battle markers ──
    # Gravelines — main battle
    ax.scatter([2.13], [51.01], transform=proj, marker='*',
               color='#c0392b', s=120, zorder=6, edgecolors='white', lw=0.5)
    ax.text(2.13, 51.3, 'Battle of Gravelines\n29 July 1588', transform=proj,
            fontsize=6.5, color='#c0392b', ha='center', va='bottom',
            fontweight='bold', **SHADOW)

    # Calais — fireship attack
    ax.scatter([1.85], [51.25], transform=proj, marker='D',
               color='#e67e22', s=50, zorder=6, edgecolors='white', lw=0.5)
    ax.text(1.4, 51.5, 'Fireships\n7 Aug 1588', transform=proj,
            fontsize=6.3, color='#e67e22', ha='center', **SHADOW)

    # ── Legend ──
    leg_elements = [
        mlines.Line2D([], [], color=ROUTE_A, lw=2, label='Armada outbound route'),
        mlines.Line2D([], [], color='#e67e22', lw=1.8, ls='--', label='Armada return (survivors)'),
        mlines.Line2D([], [], color='#8B008B', lw=2, ls=':', label="Parma's embarkation zone"),
        plt.scatter([], [], marker='*', color='#c0392b', s=80, label='Battle'),
        plt.scatter([], [], marker='D', color='#e67e22', s=40, label='Fireship attack'),
    ]
    ax.legend(handles=leg_elements[:5], loc='lower left', fontsize=6.5,
              framealpha=0.9, edgecolor='#aaa', fancybox=True)

    add_title_box(ax, 'The Spanish Armada, 1588',
                  'Route · Engagements · Return')
    fig.tight_layout(pad=0.3)
    fig.savefig('armada-route.png', dpi=DPI, bbox_inches='tight',
                facecolor='#f5f2ed')
    plt.close(fig)
    print('armada-route.png done')


# ═══════════════════════════════════════════════════════════════════════════
# MAP 2 — Drake's Circumnavigation (1577–80)
# ═══════════════════════════════════════════════════════════════════════════
def map_circumnavigation():
    fig = plt.figure(figsize=(14, 7))
    proj = ccrs.Robinson()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_global()

    ax.add_feature(cfeature.OCEAN.with_scale('110m'), color=OCEAN)
    ax.add_feature(cfeature.LAND.with_scale('110m'), color=LAND, edgecolor=COAST, lw=0.4)
    ax.add_feature(cfeature.COASTLINE.with_scale('110m'), edgecolor=COAST, lw=0.4)

    geo = ccrs.PlateCarree()

    # Route: Plymouth → Cape Verde → Brazil coast → Strait of Magellan →
    #        Pacific → Ecuador (Cacafuego) → California → Moluccas → Java →
    #        Cape of Good Hope → Sierra Leone → Plymouth
    route_lons = [
        -4.1,    # Plymouth
        -17.5,   # Cape Verde
        -35.0, -40.0, -50.0, -55.0,  # South America coast southward
        -65.0, -68.5, -68.0,          # Magellan Strait approach
        -75.0, -80.5, -78.0,          # Pacific, Cacafuego off Ecuador
        -90.0, -100.0, -110.0, -120.0, -122.5,  # Pacific north to California
        -130.0, -145.0, -160.0, -175.0, 175.0,   # Across Pacific
        130.0, 127.5, 124.0, 120.0,    # Moluccas, Java
        105.0, 95.0, 80.0, 60.0,       # Indian Ocean
        32.0, 18.5,                    # Cape of Good Hope area
        -3.0, -10.0, -13.0,            # West Africa (Sierra Leone)
        -4.1,                          # Plymouth return
    ]
    route_lats = [
        50.4,   # Plymouth
        16.0,   # Cape Verde
        -5.0, -15.0, -30.0, -45.0,    # South America
        -50.0, -52.0, -54.0,           # Magellan
        -55.0, -5.0, 0.0,              # Pacific, Cacafuego ~0°S/80°W
        5.0, 10.0, 15.0, 25.0, 38.0,  # Pacific north
        40.0, 38.0, 30.0, 20.0, 10.0, # Across Pacific
        5.0, -4.0, -2.0, -8.0,         # Moluccas
        -12.0, -15.0, -20.0, -28.0,    # Indian Ocean
        -34.5, -34.0,                   # Cape of Good Hope
        5.0, 8.0, 8.5,                  # West Africa
        50.4,                           # Plymouth
    ]

    ax.plot(route_lons, route_lats, transform=geo,
            color=ROUTE_B, lw=2.0, alpha=0.9, zorder=4)

    # Arrows at key points
    arrow_pts = [1, 5, 9, 13, 18, 22, 26, 30, 33]
    for i in arrow_pts:
        if i < len(route_lons) - 1:
            ax.annotate('', xy=(route_lons[i+1], route_lats[i+1]),
                        xytext=(route_lons[i], route_lats[i]),
                        transform=geo,
                        arrowprops=dict(arrowstyle='->', color=ROUTE_B,
                                       lw=1.5, mutation_scale=11),
                        zorder=5)

    # Key event dots and labels
    events = {
        'Plymouth\n(Dec 1577 / Sep 1580)': (-4.1, 50.4),
        'Cape Verde\n(Jan 1578)':            (-17.5, 16.0),
        'Strait of Magellan\n(Aug 1578)':    (-68.5, -53.0),
        '*Cacafuego* captured\n(Mar 1579)':  (-80.5, -5.0),
        '"New Albion"\nCalifornia (Jun 1579)':(-122.5, 38.0),
        'Moluccas\n(Nov 1579)':              (127.5, -4.0),
        'Cape of Good Hope\n(Jun 1580)':     (18.5, -34.0),
    }
    for name, (lon, lat) in events.items():
        dot(ax, lon, lat, geo, color=ROUTE_B, size=35, zorder=6)
        ha = 'left'
        va = 'bottom'
        if lon < -100:
            ha = 'center'
            va = 'top'
        elif lon > 100:
            ha = 'left'
        ax.text(lon, lat + 3, name, transform=geo,
                fontsize=6.2, color=LABEL_COL, ha=ha, va='bottom',
                style='italic' if '*' in name else 'normal',
                **SHADOW)

    # Drake's Golden Hind label mid-Pacific
    ax.text(-150, -2, "GOLDEN HIND\n1577–1580", transform=geo,
            fontsize=8, color=ROUTE_B, ha='center', va='center',
            alpha=0.6, style='italic')

    add_title_box(ax, "Drake's Circumnavigation, 1577–1580",
                  "First English voyage around the world · Golden Hind")
    fig.tight_layout(pad=0.3)
    fig.savefig('circumnavigation-1577-1580.png', dpi=DPI, bbox_inches='tight',
                facecolor='#f5f2ed')
    plt.close(fig)
    print('circumnavigation-1577-1580.png done')


# ═══════════════════════════════════════════════════════════════════════════
# MAP 3 — Drake's Caribbean Operations
# ═══════════════════════════════════════════════════════════════════════════
def map_caribbean():
    fig = plt.figure(figsize=(12, 8))
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent([-95, -55, 5, 32], crs=proj)

    ax.add_feature(cfeature.OCEAN.with_scale('50m'), color=OCEAN)
    ax.add_feature(cfeature.LAND.with_scale('50m'), color=LAND, edgecolor=COAST, lw=0.5)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor=COAST, lw=0.6)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), edgecolor=BORDER, lw=0.4)

    # ── 1572-73 voyage (gold): Nombre de Dios, Isthmus overland, mule train ──
    v72_lons = [-4.1, -17.0, -60.0, -65.0, -69.5, -77.5, -79.5]
    v72_lats = [50.4,  16.0,  14.0,  12.0,  10.5,   9.5,   8.9]
    ax.plot(v72_lons[:3] + [-72], v72_lats[:3] + [10],
            transform=proj, color=ROUTE_B, lw=1.8, alpha=0.8, zorder=3,
            linestyle='--', dashes=(6,3))
    ax.plot([-77.5, -79.5], [9.5, 8.9], transform=proj,
            color=ROUTE_B, lw=2.0, alpha=0.9, zorder=4)

    # Overland isthmus crossing (dashed through jungle)
    ax.plot([-79.5, -79.0, -78.0, -77.2, -79.5],
            [8.9,  8.8,   8.9,   8.97,  9.0],
            transform=proj, color=ROUTE_B, lw=1.5, alpha=0.7,
            linestyle=':', zorder=4)
    ax.text(-78.5, 9.2, 'Isthmus crossing\n(overland, with Maroons)', transform=proj,
            fontsize=6.2, color=ROUTE_B, ha='center', **SHADOW)

    # ── 1585 Indies Voyage (teal): San Domingo, Cartagena ──
    v85_lons = [-4.1, -17.0, -70.0, -69.9, -75.5, -80.0, -82.0, -4.1]
    v85_lats = [50.4,  16.0,  19.5,  18.5,  10.4,   9.0,  10.5, 50.4]
    ax.plot(v85_lons, v85_lats, transform=proj,
            color=ROUTE_C, lw=1.8, alpha=0.85, zorder=4)
    ax.annotate('', xy=(v85_lons[3], v85_lats[3]),
                xytext=(v85_lons[2], v85_lats[2]),
                arrowprops=dict(arrowstyle='->', color=ROUTE_C, lw=1.5, mutation_scale=11),
                zorder=5)

    # ── San Juan de Ulúa (1568) ──
    ax.scatter([-96.1], [19.2], transform=proj, marker='X',
               color='#8B0000', s=80, zorder=6, edgecolors='white', lw=0.5)
    ax.text(-96.1, 19.7, 'San Juan de Ulúa\n(1568 — Spanish betrayal)', transform=proj,
            fontsize=6.3, color='#8B0000', ha='center', **SHADOW)

    # ── Key locations ──
    places = {
        'Nombre de Dios\n(1572–73 raid)':  (-79.5, 8.9),
        'Panama City':                      (-79.5, 8.97),
        'Cartagena\n(1585)':               (-75.5, 10.4),
        'San Domingo\n(1585)':             (-69.9, 18.5),
        'Havana':                           (-82.3, 23.1),
        'Jamaica':                          (-77.3, 18.1),
        'Hispaniola':                       (-70.0, 19.0),
    }
    for name, (lon, lat) in places.items():
        col = NODE_COL
        if '1572' in name or '1585' in name:
            col = '#c0392b'
        dot(ax, lon, lat, proj, color=col, size=28)
        ax.text(lon + 0.5, lat + 0.4, name, transform=proj,
                fontsize=6.3, color=LABEL_COL, ha='left', va='bottom', **SHADOW)

    # Drake's Pacific tree
    ax.text(-79.0, 8.6, '★ Drake saw Pacific\nfrom tree (1573)', transform=proj,
            fontsize=6.2, color=ROUTE_B, ha='left', style='italic', **SHADOW)

    # Maroon territory label
    ax.text(-80.5, 8.3, 'Maroon territory\n(cimarrones)', transform=proj,
            fontsize=6.0, color='#5d4037', ha='left', style='italic', alpha=0.8)

    # Legend
    leg = [
        mlines.Line2D([], [], color=ROUTE_B, lw=2, ls='--',
                      label="1572–73: Nombre de Dios raid"),
        mlines.Line2D([], [], color=ROUTE_C, lw=2,
                      label="1585: Indies Voyage (San Domingo, Cartagena)"),
        plt.scatter([], [], marker='X', color='#8B0000', s=60,
                    label="1568: San Juan de Ulúa (founding grievance)"),
    ]
    ax.legend(handles=leg, loc='lower right', fontsize=6.5,
              framealpha=0.9, edgecolor='#aaa', fancybox=True)

    add_title_box(ax, "Drake's Caribbean Operations",
                  "1568 · 1572–73 · 1585")
    fig.tight_layout(pad=0.3)
    fig.savefig('drake-caribbean.png', dpi=DPI, bbox_inches='tight',
                facecolor='#f5f2ed')
    plt.close(fig)
    print('drake-caribbean.png done')


# ═══════════════════════════════════════════════════════════════════════════
# MAP 4 — Walsingham's Intelligence Network
# ═══════════════════════════════════════════════════════════════════════════
def map_intelligence():
    fig = plt.figure(figsize=(11, 9))
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent([-15, 40, 34, 62], crs=proj)

    ax.add_feature(cfeature.OCEAN.with_scale('50m'), color=OCEAN)
    ax.add_feature(cfeature.LAND.with_scale('50m'), color=LAND, edgecolor=COAST, lw=0.5)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), edgecolor=BORDER, lw=0.5)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor=COAST, lw=0.6)

    london = (-0.12, 51.5)

    # Agent nodes: (lon, lat, label, type)
    # type: 'hq', 'embassy', 'agent', 'seminary', 'hostile'
    nodes = [
        (london[0], london[1], 'London\n(HQ)', 'hq'),
        (2.35,   48.85, 'Paris\n(embassy 1570–73)', 'embassy'),
        (-3.70,  40.42, 'Madrid', 'agent'),
        (-9.14,  38.72, 'Lisbon\n(fleet assembly)', 'agent'),
        (-6.26,  36.52, 'Cadiz\n(naval intelligence)', 'agent'),
        (4.34,   50.85, 'Brussels', 'agent'),
        (4.90,   52.37, 'Amsterdam', 'agent'),
        (2.55,   51.04, 'Gravelines\n/ Dunkirk\n(Parma)', 'hostile'),
        (3.06,   50.63, 'Douai\n(seminary, to 1578)', 'seminary'),
        (4.03,   49.25, 'Rheims\n(seminary, from 1578)', 'seminary'),
        (12.48,  41.90, 'Rome\n(English College)', 'seminary'),
        (8.55,   47.37, 'Zurich', 'agent'),
        (7.59,   47.56, 'Basel\n(exile, 1568)', 'agent'),
        (7.75,   48.58, 'Strasbourg\n(exile, 1568)', 'agent'),
        (-1.10,  43.30, 'Huguenot\nheartland\n(La Rochelle\narea)', 'agent'),
        (2.35,   43.60, 'Toulouse\n(Huguenot south)', 'agent'),
        (16.37,  48.21, 'Vienna\n(Habsburg)', 'hostile'),
        (13.40,  52.52, 'Berlin\n(Protestant contacts)', 'agent'),
    ]

    colors = {
        'hq':       '#1a1a8c',
        'embassy':  '#2c5f8a',
        'agent':    INTEL_COL,
        'seminary': '#8B1A1A',
        'hostile':  '#6d1f6d',
    }
    sizes = {'hq': 120, 'embassy': 70, 'agent': 40, 'seminary': 50, 'hostile': 40}
    markers = {'hq': '*', 'embassy': 's', 'agent': 'o', 'seminary': '^', 'hostile': 'X'}

    # Draw spokes from London to each node
    for lon, lat, label_txt, ntype in nodes:
        if ntype == 'hq':
            continue
        col = colors[ntype]
        ax.plot([london[0], lon], [london[1], lat], transform=proj,
                color=col, lw=0.9, alpha=0.45, zorder=3, linestyle=':')

    # Draw nodes
    for lon, lat, label_txt, ntype in nodes:
        col = colors[ntype]
        sz = sizes[ntype]
        mk = markers[ntype]
        ax.scatter([lon], [lat], transform=proj, color=col, s=sz, zorder=5,
                   marker=mk, edgecolors='white', linewidths=0.6)
        ha = 'left'
        offset_x = 0.5
        if lon > 15:
            ha = 'left'
        if lon < -5:
            ha = 'right'
            offset_x = -0.5
        ax.text(lon + offset_x, lat + 0.4, label_txt, transform=proj,
                fontsize=6.2, color=LABEL_COL, ha=ha, va='bottom', **SHADOW)

    # St Bartholomew's Day Massacre annotation
    ax.text(2.35, 47.5, "Walsingham witnesses\nSt Bartholomew's Massacre\nfrom English embassy, 1572",
            transform=proj, fontsize=6.2, color='#8B0000', ha='center',
            style='italic', **SHADOW)

    # Legend
    leg = [
        mlines.Line2D([], [], marker='*', color='w', mfc=colors['hq'], ms=10,
                      label='HQ (London / Seething Lane)'),
        mlines.Line2D([], [], marker='s', color='w', mfc=colors['embassy'], ms=8,
                      label='Embassy / diplomatic post'),
        mlines.Line2D([], [], marker='o', color='w', mfc=colors['agent'], ms=7,
                      label='Agent / resident network'),
        mlines.Line2D([], [], marker='^', color='w', mfc=colors['seminary'], ms=8,
                      label='Catholic seminary (infiltrated)'),
        mlines.Line2D([], [], marker='X', color='w', mfc=colors['hostile'], ms=8,
                      label='Hostile power / threat node'),
    ]
    ax.legend(handles=leg, loc='lower left', fontsize=6.5,
              framealpha=0.9, edgecolor='#aaa', fancybox=True)

    add_title_box(ax, "Walsingham's Intelligence Network, c.1573–1590",
                  "~15 countries · financed from personal fortune")
    fig.tight_layout(pad=0.3)
    fig.savefig('walsingham-intelligence-network.png', dpi=DPI,
                bbox_inches='tight', facecolor='#f5f2ed')
    plt.close(fig)
    print('walsingham-intelligence-network.png done')


# ═══════════════════════════════════════════════════════════════════════════
# MAP 5 — Elizabethan London (schematic)
# ═══════════════════════════════════════════════════════════════════════════
def map_london():
    """Schematic map of Elizabethan London — theatres, Stationers', Tower."""
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 75)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#f5f2ed')
    ax.set_facecolor('#f5f2ed')

    # ── Thames ──
    from matplotlib.patches import Polygon as MPoly
    from matplotlib.collections import PatchCollection
    # Thames as a wide blue band running roughly E-W through the middle
    thames_upper = [(10, 34), (20, 32), (30, 30), (40, 29), (50, 29),
                    (60, 30), (70, 30), (80, 31), (90, 32)]
    thames_lower = [(10, 28), (20, 26), (30, 24), (40, 23), (50, 23),
                    (60, 24), (70, 24), (80, 25), (90, 26)]
    thames_x = [p[0] for p in thames_upper] + [p[0] for p in reversed(thames_lower)]
    thames_y = [p[1] for p in thames_upper] + [p[1] for p in reversed(thames_lower)]
    thames_poly = plt.Polygon(list(zip(thames_x, thames_y)),
                              facecolor='#c8ddf0', edgecolor='#8ab0cc', lw=1.5)
    ax.add_patch(thames_poly)
    ax.text(50, 26, 'River Thames', fontsize=9, color='#4a7aaa',
            ha='center', va='center', style='italic', alpha=0.8)

    # London Bridge
    ax.plot([55, 55], [23, 32], color='#8a7060', lw=4, zorder=4)
    ax.text(55, 21, 'London\nBridge', fontsize=6.5, ha='center',
            va='top', color='#5a4030')

    # ── North bank — City of London outline ──
    city_x = [32, 32, 70, 70, 32]
    city_y = [32, 55, 55, 32, 32]
    city_poly = plt.Polygon(list(zip(city_x, city_y)),
                            facecolor='#e0d8c8', edgecolor='#8a7a6a', lw=1.5,
                            linestyle='--', alpha=0.6)
    ax.add_patch(city_poly)
    ax.text(51, 53, 'City of London', fontsize=7.5, color='#5a4030',
            ha='center', style='italic', alpha=0.7)

    # City walls label
    ax.text(70.5, 43, 'City Walls', fontsize=6, color='#8a7a6a',
            ha='left', rotation=-90, alpha=0.7)

    # ── KEY INSTITUTIONS — North Bank ──
    # St Paul's / Stationers' precinct
    ax.scatter([45], [42], color='#8B1A1A', s=120, zorder=6,
               marker='s', edgecolors='white', lw=0.8)
    ax.text(45, 43.5, "St Paul's Churchyard\n(Stationers' Company precinct)\nLicensing · printing · bookselling",
            fontsize=6.5, ha='center', va='bottom', color='#8B1A1A',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#8B1A1A', alpha=0.85))

    # Tower of London (east end)
    ax.add_patch(plt.Rectangle((66, 34), 6, 6, color='#5a4030',
                                ec='#3a2010', lw=1.5, zorder=5))
    ax.text(69, 33.5, 'Tower of London', fontsize=6.5, ha='center',
            va='top', color='#3a2010', fontweight='bold')
    ax.text(69, 32.5, '(More, Fisher, Anne Boleyn,\nCromwell — all imprisoned here)',
            fontsize=5.8, ha='center', va='top', color='#5a4030', style='italic')

    # Whitehall Palace (west)
    ax.add_patch(plt.Rectangle((13, 34), 8, 7, color='#c8b560',
                                ec='#a89040', lw=1.5, zorder=5, alpha=0.8))
    ax.text(17, 33.5, 'Whitehall\nPalace', fontsize=6.5, ha='center',
            va='top', color='#7a6020', fontweight='bold')

    # Aldgate / East gate
    ax.text(70, 43, '→ Aldgate', fontsize=6, color='#5a4030', ha='left')

    # ── SHOREDITCH (north of city) — The Theatre & Curtain ──
    ax.scatter([48, 52], [63, 63], color='#1a6b4a', s=80, zorder=6,
               marker='D', edgecolors='white', lw=0.6)
    ax.text(50, 65, 'Shoreditch\nThe Theatre (1576)   The Curtain (1577)',
            fontsize=6.8, ha='center', va='bottom', color='#1a6b4a',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#1a6b4a', alpha=0.85))
    # Arrow from Shoreditch down to city
    ax.annotate('', xy=(50, 55), xytext=(50, 63),
                arrowprops=dict(arrowstyle='->', color='#1a6b4a',
                               lw=1, mutation_scale=10, linestyle='dashed'))

    # ── BANKSIDE (south bank) ──
    # Rose, Globe, Swan
    bankside_theatres = [
        (42, 20, 'Rose (1587)'),
        (48, 19, 'Globe (1599)'),
        (38, 21, 'Swan (c.1595)'),
    ]
    for x, y, name in bankside_theatres:
        ax.scatter([x], [y], color='#2c5f8a', s=80, zorder=6,
                   marker='D', edgecolors='white', lw=0.6)
        ax.text(x, y - 1.5, name, fontsize=6.2, ha='center',
                va='top', color='#2c5f8a', **SHADOW)

    ax.text(43, 15, 'Bankside (Southwark)\nCommercial theatre district',
            fontsize=7, ha='center', va='top', color='#2c5f8a',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2c5f8a', alpha=0.85))

    # Paris Garden (bear-baiting, west of theatres)
    ax.scatter([33], [21], color='#888', s=50, zorder=5,
               marker='o', edgecolors='white', lw=0.5)
    ax.text(33, 19, 'Paris Garden\n(bear-baiting)', fontsize=5.8,
            ha='center', va='top', color='#666', style='italic')

    # ── LEGEND ──
    leg = [
        mlines.Line2D([], [], marker='s', color='w', mfc='#8B1A1A', ms=9,
                      label='Stationers\' Company precinct'),
        mlines.Line2D([], [], marker='D', color='w', mfc='#1a6b4a', ms=8,
                      label='North bank theatres (Shoreditch)'),
        mlines.Line2D([], [], marker='D', color='w', mfc='#2c5f8a', ms=8,
                      label='South bank theatres (Bankside)'),
        mpatches.Patch(facecolor='#c8b560', edgecolor='#a89040',
                       label='Royal palace'),
        mpatches.Patch(facecolor='#5a4030', edgecolor='#3a2010',
                       label='Tower of London'),
    ]
    ax.legend(handles=leg, loc='upper right', fontsize=6.5,
              framealpha=0.9, edgecolor='#aaa', fancybox=True)

    # Compass rose (simple)
    ax.text(92, 68, 'N', fontsize=10, ha='center', va='center', fontweight='bold', color='#333')
    ax.annotate('', xy=(92, 70), xytext=(92, 65),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5, mutation_scale=10))

    ax.set_title("Elizabethan London — Theatres, Stationers' Precinct, and the Tower",
                 fontsize=10, fontweight='bold', color='#1a1a2e', pad=8)
    ax.text(50, 1, 'Schematic — not to scale', fontsize=6, ha='center',
            color='#888', style='italic')

    fig.tight_layout(pad=0.5)
    fig.savefig('elizabethan-london.png', dpi=DPI, bbox_inches='tight',
                facecolor='#f5f2ed')
    plt.close(fig)
    print('elizabethan-london.png done')


# ═══════════════════════════════════════════════════════════════════════════
# MAP 6 — Dissolution of Monasteries & Pilgrimage of Grace
# ═══════════════════════════════════════════════════════════════════════════
def map_dissolution():
    fig = plt.figure(figsize=(9, 12))
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent([-6.5, 2.2, 49.8, 56.5], crs=proj)

    ax.add_feature(cfeature.OCEAN.with_scale('50m'), color=OCEAN)
    ax.add_feature(cfeature.LAND.with_scale('50m'), color=LAND, edgecolor=COAST, lw=0.5)
    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), edgecolor=COAST, lw=0.7)

    # Shade the Pilgrimage of Grace region (northern England, roughly)
    # North of a line from Humber to Mersey, below Scotland
    from matplotlib.patches import Polygon as MPoly
    pog_lons = [-3.5, -3.0, -2.0, -1.0, 0.0, 0.5,
                 0.3, -0.5, -1.5, -2.5, -3.5, -4.5, -5.0, -5.5, -5.0, -4.0, -3.5]
    pog_lats = [55.0, 55.2, 55.1, 54.9, 54.5, 53.8,
                 53.7, 53.6, 53.5, 53.7, 53.8, 54.0, 54.3, 54.7, 55.0, 55.0, 55.0]
    ax.fill(pog_lons, pog_lats, transform=proj,
            color='#e74c3c', alpha=0.12, zorder=3)
    ax.plot(pog_lons + [pog_lons[0]], pog_lats + [pog_lats[0]],
            transform=proj, color='#c0392b', lw=1.2, alpha=0.4,
            linestyle='--', zorder=4)
    ax.text(-2.5, 54.5, 'Pilgrimage of Grace\nOct 1536 — northern rising\n(tens of thousands mobilised)',
            transform=proj, fontsize=7, color='#c0392b', ha='center',
            style='italic', **SHADOW)

    # ── Monasteries / abbeys ──
    # Pilgrimage-associated (northern)
    northern_abbeys = [
        ('Jervaulx\n(abbot hanged)', -1.80, 54.26),
        ('Barlings\n(abbot hanged)', -0.35, 53.27),
        ('Whalley\n(abbot hanged)', -2.40, 53.82),
        ('Sawley\n(restored, then\nsuppressed)', -2.35, 53.93),
        ('Fountains', -1.68, 54.12),
        ('Rievaulx', -1.12, 54.27),
        ('Furness', -3.18, 54.20),
        ('Bridlington', -0.19, 54.08),
    ]

    # Greater abbeys — south (second wave, attainder)
    southern_abbeys = [
        ('Glastonbury\n(abbot hanged)', -2.71, 51.14),
        ('Reading\n(abbot hanged)', -0.97, 51.45),
        ('Colchester\n(abbot hanged)', 0.90,  51.89),
        ('Waltham', -0.03, 51.68),
        ('Westminster', -0.13, 51.50),
        ('Bath', -2.36, 51.38),
        ('Tintern', -2.68, 51.70),
    ]

    for name, lon, lat in northern_abbeys:
        dot(ax, lon, lat, proj, color='#c0392b', size=40, zorder=6, marker='^')
        ax.text(lon + 0.15, lat + 0.05, name, transform=proj,
                fontsize=5.8, color='#8B0000', ha='left', **SHADOW)

    for name, lon, lat in southern_abbeys:
        dot(ax, lon, lat, proj, color='#8B4513', size=35, zorder=6, marker='^')
        ax.text(lon + 0.15, lat + 0.05, name, transform=proj,
                fontsize=5.8, color='#5a3010', ha='left', **SHADOW)

    # Key cities
    cities = {
        'London': (-0.12, 51.50),
        'York':   (-1.08, 53.96),
        'Lincoln':(-0.54, 53.23),
        'Durham': (-1.57, 54.78),
        'Exeter': (-3.53, 50.72),
        'Bristol':(-2.59, 51.45),
        'Norwich':(1.30,  52.63),
        'Chester':(-2.89, 53.19),
    }
    for name, (lon, lat) in cities.items():
        ax.scatter([lon], [lat], transform=proj, color='#333', s=25, zorder=5,
                   marker='o', edgecolors='white', lw=0.5)
        ax.text(lon + 0.15, lat + 0.1, name, transform=proj,
                fontsize=6.5, color='#1a1a2e', **SHADOW)

    # Legend
    leg = [
        mlines.Line2D([], [], marker='^', color='w', mfc='#c0392b', ms=9,
                      label='Northern abbeys — Pilgrimage-linked\n(abbots hanged at own gates)'),
        mlines.Line2D([], [], marker='^', color='w', mfc='#8B4513', ms=8,
                      label='Greater abbeys — dissolved by\nattainder / surrender (2nd wave)'),
        mpatches.Patch(facecolor='#e74c3c', alpha=0.3, edgecolor='#c0392b', ls='--',
                       label='Pilgrimage of Grace uprising zone\n(Oct 1536 — Jan 1537)'),
    ]
    ax.legend(handles=leg, loc='lower left', fontsize=6.5,
              framealpha=0.9, edgecolor='#aaa', fancybox=True)

    add_title_box(ax, 'Dissolution of the Monasteries, 1536–40',
                  'Key houses · Pilgrimage of Grace · Abbots executed')
    fig.tight_layout(pad=0.3)
    fig.savefig('england-dissolution-monasteries.png', dpi=DPI,
                bbox_inches='tight', facecolor='#f5f2ed')
    plt.close(fig)
    print('england-dissolution-monasteries.png done')


# ── Run all ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import os
    # Run from the script's own directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    map_armada()
    map_circumnavigation()
    map_caribbean()
    map_intelligence()
    map_london()
    map_dissolution()
    print('\nAll maps generated.')
