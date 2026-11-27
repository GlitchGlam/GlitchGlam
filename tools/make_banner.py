#!/usr/bin/env python3
"""Generates the GlitchGlam banner SVG: glitch title, shader-like sky, and a magpie that
swoops, loops the loop and leaves a sparkle trail. Everything animates with CSS so that
prefers-reduced-motion is honoured; no JavaScript, nothing loaded from outside the file."""
import math, random

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "banner.svg")
W, H = 1200, 300
CYCLE = 18  # seconds for one flight

# ---------- the flight path: in from the left, dive in front of the letters, climb, loop, second dip, out ----------
PATH = ("M -220 70 C 60 50, 230 212, 400 202 C 520 196, 570 64, 650 62 "
        "C 712 62, 736 128, 690 142 C 640 150, 616 86, 672 66 C 740 44, 860 92, 940 100 "
        "C 1050 112, 1150 150, 1420 110")

# ---------- wing geometry: morph states computed by rotating about the shoulder ----------
SHOULDER = (56.0, 42.0)
FEATHER_TIPS = [(14, 17), (11, 26), (12, 35), (16, 44), (22, 52), (30, 58)]  # mid position

def rot(p, deg, c=SHOULDER):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))

def fan(deg):
    return " ".join(f"M{SHOULDER[0]:.0f} {SHOULDER[1]:.0f} L{rot(t, deg)[0]:.1f} {rot(t, deg)[1]:.1f}" for t in FEATHER_TIPS)

# The wing's arm (the dark shape the feathers grow from): same command structure in every state.
ARM = {
    "up":   "M84 50 C78 30 66 18 52 14 C46 18 44 26 50 34 C58 44 72 54 82 56 Z",
    "mid":  "M84 50 C76 38 62 33 48 34 C43 39 44 47 51 52 C60 59 74 63 82 60 Z",
    "down": "M84 50 C78 58 64 70 50 74 C44 70 44 62 50 58 C58 54 72 52 82 54 Z",
}
ARM_WHITE = {
    "up":   "M84 50 C79 36 70 26 58 22 C58 32 66 44 79 54 L83 52 Z",
    "mid":  "M84 50 C77 41 67 37 58 36 C59 44 66 54 79 60 L83 56 Z",
    "down": "M84 50 C78 54 68 60 58 64 C60 58 66 54 79 56 L83 54 Z",
}
FAN = {"up": fan(-34), "mid": fan(0), "down": fan(30)}

def magpie_symbol():
    rim = "#5a4fa0"
    return f'''
  <!-- The magpie, drawn once and reused for the bird and its afterimages. -->
  <g id="magpie">
    <!-- far wing, behind the body -->
    <g transform="translate(8 -6) rotate(22 78 50)" opacity=".92">
      <g class="far">
        <g stroke-linecap="round" fill="none"><path d="M52 42 L16 24 M52 42 L13 32 M52 42 L15 40 M52 42 L20 48" stroke="#1a1430" stroke-width="5.2"/></g>
        <path d="M82 50 C74 40 62 36 50 36 C46 40 46 46 52 50 C60 56 72 60 80 58 Z" fill="#1a1430"/>
      </g>
    </g>
    <!-- tail: a black fan with a white base -->
    <g class="tail" stroke-linecap="round" fill="none">
      <path d="M50 64 L8 70 M50 66 L9 79 M50 68 L16 88" stroke="{rim}" stroke-width="8.4"/>
      <path d="M50 64 L8 70 M50 66 L9 79 M50 68 L16 88" stroke="#14101f" stroke-width="7"/>
      <path d="M50 64 L35 66 M50 66 L36 70.6 M50 68 L38 75" stroke="#ffffff" stroke-width="7"/>
    </g>
    <!-- body, white back and nape, head -->
    <path d="M36 64 C38 48 58 40 82 42 C100 44 110 54 106 66 C102 78 80 86 58 82 C44 80 35 74 36 64 Z" fill="url(#torso)" stroke="{rim}" stroke-width="1.2"/>
    <path d="M62 44 C72 38 88 38 98 44 C101 46 101 50 98 52 C90 48 76 48 64 52 C59 50 59 46 62 44 Z" fill="#ffffff"/>
    <circle cx="112" cy="46" r="15.5" fill="#14101f" stroke="{rim}" stroke-width="1.2"/>
    <path d="M98 38 C100 31 109 29 115 32 C108 34 103 40 102 49 C98 47 96 42 98 38 Z" fill="#ffffff"/>
    <!-- near wing: the feather fan and the arm morph between up, mid and down -->
    <g class="wing">
      <g stroke-linecap="round" fill="none">
        <path class="fan fan-rim" d="{FAN['mid']}" stroke="{rim}" stroke-width="7.4"/>
        <path class="fan fan-ink" d="{FAN['mid']}" stroke="#14101f" stroke-width="6"/>
        <path class="fan fan-sheen" d="{FAN['mid']}" stroke="url(#sheen)" stroke-width="1.6" opacity=".55"/>
      </g>
      <path class="arm arm-ink" d="{ARM['mid']}" fill="#14101f" stroke="{rim}" stroke-width="1.2"/>
      <path class="arm arm-sheen" d="{ARM['mid']}" fill="url(#sheen)" opacity=".3"/>
      <path class="arm arm-white" d="{ARM_WHITE['mid']}" fill="#ffffff"/>
    </g>
    <!-- bill and eye -->
    <path d="M124 41 C134 41 147 46 152 52 C145 51 134 52 125 54 Z" fill="url(#bill)"/>
    <path d="M125 54 C134 52 144 53 148 55 C140 58 132 58 125 56 Z" fill="#9ea9c1"/>
    <path d="M146 49 L153 52 L148 55 Z" fill="#2b2840"/>
    <circle cx="132" cy="44.5" r="0.9" fill="#6f7a95"/>
    <circle cx="118" cy="43" r="4.8" fill="#7a2e12"/>
    <circle cx="118.6" cy="43" r="2.5" fill="#0d0a14"/>
    <circle cx="119.6" cy="41.9" r="0.9" fill="#ffffff"/>
    <ellipse class="lid" cx="118" cy="43" rx="5.2" ry="5.2" fill="#14101f"/>
  </g>'''

def morph_css():
    # The flap: one keyframe set per morphing path. Browsers without the CSS d property keep the mid shape.
    def kf(name, states):
        return (f"    @keyframes {name} {{ 0%, 100% {{ d: path(\"{states['up']}\"); }} "
                f"50% {{ d: path(\"{states['down']}\"); }} }}")
    return "\n".join([kf("fan-flap", FAN), kf("arm-flap", ARM), kf("white-flap", ARM_WHITE)])

random.seed(7)
PALETTE = ["#ff2e93", "#ffe14d", "#8dff4d", "#27e8ff", "#a259ff", "#ffffff"]

def sparks():
    out = []
    for i in range(14):
        delay = 0.12 + i * 0.07                     # positive: it starts later, so it trails the bird
        colour = PALETTE[i % len(PALETTE)]
        r = 2.2 + random.random() * 2.2
        dx, dy = (random.random() - 0.5) * 18, 6 + random.random() * 22
        twinkle = 0.5 + random.random() * 0.7
        out.append(f'    <g class="spark" style="animation-delay: {delay:.2f}s"><circle r="{r:.1f}" fill="{colour}" '
                   f'style="--dx: {dx:.1f}px; --dy: {dy:.1f}px; animation-duration: {twinkle:.2f}s"/></g>')
    return "\n".join(out)

def ghosts():
    return "\n".join(
        f'    <g class="ghost" style="animation-delay: {d:.2f}s; opacity: {o}"><g class="flip"><g transform="scale(0.85) translate(-80 -55)"><use href="#magpie"/></g></g></g>'
        for d, o in [(0.07, 0.38), (0.14, 0.22), (0.21, 0.1)])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">GlitchGlam</title>
  <desc id="d">The word GlitchGlam in big glowing letters that briefly glitch with pink and cyan colour splits. A small magpie swoops in, dives in front of the letters, loops the loop above them and flies out, leaving a trail of sparkles.</desc>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0a0422"/>
      <stop offset="1" stop-color="#26095a"/>
    </linearGradient>
    <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#ff5cc0"/>
      <stop offset="0.5" stop-color="#ffe566"/>
      <stop offset="1"   stop-color="#4df0ff"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop class="sh1" offset="0"  stop-color="#7b2cff"/>
      <stop class="sh2" offset=".5" stop-color="#1d9bff"/>
      <stop class="sh3" offset="1"  stop-color="#19f0a8"/>
    </linearGradient>
    <radialGradient id="torso" cx=".35" cy=".3" r=".85">
      <stop offset="0" stop-color="#3a3060"/><stop offset="1" stop-color="#14101f"/>
    </radialGradient>
    <linearGradient id="bill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#d6deec"/><stop offset=".7" stop-color="#b3bdd2"/><stop offset="1" stop-color="#8f9ab4"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fff" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0V48" fill="none" stroke="#ffffff" stroke-opacity="0.07" stroke-width="1"/>
    </pattern>
    <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.5" fill="#000" fill-opacity="0.22"/>
    </pattern>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>
    <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="11" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="birdglow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
{magpie_symbol()}
  </defs>

  <style>
    text {{ font-family: "Avenir Next", "Trebuchet MS", Verdana, system-ui, sans-serif; }}
    .cy {{ transform: translate(0, 0); }}
    .mg {{ transform: translate(0, 0); }}

    /* Everything on the flight path shares it. The bird turns with the path, so it rolls through the loop. */
    .bird, .ghost, .spark {{
      offset-path: path("{PATH}");
      offset-rotate: auto;
      offset-distance: 58%;
    }}
    .flip {{ transform-box: fill-box; transform-origin: 50% 50%; }}
    .wing {{ transform-origin: 56px 42px; }}
    .far  {{ transform-origin: 78px 50px; }}
    .tail {{ transform-origin: 50px 66px; }}
    .lid  {{ transform-origin: 118px 43px; transform: scaleY(0); }}
    .ghost, .spark {{ visibility: hidden; }}       /* only exist while things move */
    .spark circle {{ transform: translate(var(--dx), var(--dy)); }}

    /* All motion is opt-out: it only runs for people who have not asked for less. */
    @media (prefers-reduced-motion: no-preference) {{
      .b1 {{ animation: d1 13s ease-in-out infinite alternate; }}
      .b2 {{ animation: d2 17s ease-in-out infinite alternate; }}
      .b3 {{ animation: d3 15s ease-in-out infinite alternate; }}
      .cy {{ animation: glc {CYCLE}s steps(1, end) infinite; }}
      .mg {{ animation: glm {CYCLE}s steps(1, end) infinite; }}
      .main {{ animation: glt {CYCLE}s steps(1, end) infinite; }}
      .scan {{ animation: scan 7s linear infinite; }}
      .bird, .ghost, .spark {{ animation: fly {CYCLE}s linear infinite; }}
      .ghost, .spark {{ visibility: visible; }}
      .spark circle {{ animation: twinkle 0.8s ease-in-out infinite alternate; }}
      .bob  {{ animation: bob 1.3s ease-in-out infinite alternate; }}
      .wing {{ animation: bank 0.26s ease-in-out infinite alternate; }}
      .far  {{ animation: bank 0.26s ease-in-out infinite alternate-reverse; }}
      .fan  {{ animation: fan-flap 0.52s ease-in-out infinite; }}
      .arm-ink, .arm-sheen {{ animation: arm-flap 0.52s ease-in-out infinite; }}
      .arm-white {{ animation: white-flap 0.52s ease-in-out infinite; }}
      .tail {{ animation: wag 0.5s ease-in-out infinite alternate; }}
      .lid  {{ animation: blink 4.6s steps(1, end) infinite; }}
      .sh1 {{ animation: shimmer1 2.4s linear infinite; }}
      .sh2 {{ animation: shimmer2 2.4s linear infinite; }}
      .sh3 {{ animation: shimmer3 2.4s linear infinite; }}
      .tw   {{ animation: tw 2.6s ease-in-out infinite; }}
      .tw:nth-of-type(2n) {{ animation-delay: 0.9s; }}
      .tw:nth-of-type(3n) {{ animation-delay: 1.7s; }}
    }}
    @keyframes d1 {{ to {{ transform: translate(200px, 40px); }} }}
    @keyframes d2 {{ to {{ transform: translate(-240px, -30px); }} }}
    @keyframes d3 {{ to {{ transform: translate(140px, -50px); }} }}
    @keyframes scan {{ from {{ transform: translateY(-120px); }} to {{ transform: translateY(330px); }} }}
    @keyframes fly  {{ from {{ offset-distance: 0%; }} to {{ offset-distance: 100%; }} }}
    @keyframes bob  {{ to {{ transform: translateY(8px); }} }}
    @keyframes bank {{ from {{ transform: rotate(-6deg); }} to {{ transform: rotate(6deg); }} }}
    @keyframes wag  {{ from {{ transform: rotate(-4deg); }} to {{ transform: rotate(4deg); }} }}
    @keyframes blink {{ 0%, 92% {{ transform: scaleY(0); }} 94%, 96% {{ transform: scaleY(1); }} 98%, 100% {{ transform: scaleY(0); }} }}
    @keyframes twinkle {{ from {{ opacity: 0.15; transform: translate(var(--dx), var(--dy)) scale(0.6); }} to {{ opacity: 1; transform: translate(var(--dx), var(--dy)) scale(1.3); }} }}
    @keyframes tw   {{ 0%, 100% {{ opacity: 0.25; }} 50% {{ opacity: 1; }} }}
    @keyframes shimmer1 {{ 0% {{ stop-color: #7b2cff; }} 33% {{ stop-color: #19f0a8; }} 66% {{ stop-color: #1d9bff; }} 100% {{ stop-color: #7b2cff; }} }}
    @keyframes shimmer2 {{ 0% {{ stop-color: #1d9bff; }} 33% {{ stop-color: #7b2cff; }} 66% {{ stop-color: #19f0a8; }} 100% {{ stop-color: #1d9bff; }} }}
    @keyframes shimmer3 {{ 0% {{ stop-color: #19f0a8; }} 33% {{ stop-color: #1d9bff; }} 66% {{ stop-color: #7b2cff; }} 100% {{ stop-color: #19f0a8; }} }}
{morph_css()}

    /* The glitch: quiet, then a tear as the bird loops over the letters (about 46% of the flight), and once more near the end. */
    @keyframes glc {{
      0%, 45%  {{ transform: translate(0, 0);     clip-path: inset(0 0 0 0); }}
      46%      {{ transform: translate(-22px, 2px); clip-path: inset(8% 0 62% 0); }}
      47%      {{ transform: translate(18px, -2px); clip-path: inset(58% 0 10% 0); }}
      48%      {{ transform: translate(-12px, 0);  clip-path: inset(30% 0 38% 0); }}
      49%, 86% {{ transform: translate(0, 0);     clip-path: inset(0 0 0 0); }}
      87%      {{ transform: translate(-18px, 2px); clip-path: inset(12% 0 56% 0); }}
      88%      {{ transform: translate(14px, 0);   clip-path: inset(60% 0 8% 0); }}
      89%, 100% {{ transform: translate(0, 0);    clip-path: inset(0 0 0 0); }}
    }}
    @keyframes glm {{
      0%, 45%  {{ transform: translate(0, 0);     clip-path: inset(0 0 0 0); }}
      46%      {{ transform: translate(20px, -2px); clip-path: inset(50% 0 18% 0); }}
      47%      {{ transform: translate(-16px, 2px); clip-path: inset(12% 0 56% 0); }}
      48%      {{ transform: translate(14px, 0);   clip-path: inset(66% 0 4% 0); }}
      49%, 86% {{ transform: translate(0, 0);     clip-path: inset(0 0 0 0); }}
      87%      {{ transform: translate(16px, -2px); clip-path: inset(48% 0 20% 0); }}
      88%      {{ transform: translate(-12px, 0);  clip-path: inset(6% 0 64% 0); }}
      89%, 100% {{ transform: translate(0, 0);    clip-path: inset(0 0 0 0); }}
    }}
    @keyframes glt {{
      0%, 45%, 49%, 86%, 89%, 100% {{ transform: translate(0, 0) skewX(0deg); }}
      46.5% {{ transform: translate(6px, 0) skewX(-7deg); }}
      47.5% {{ transform: translate(-5px, 0) skewX(4deg); }}
      87.5% {{ transform: translate(5px, 0) skewX(-5deg); }}
    }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>

  <g filter="url(#blur)" opacity="0.6">
    <circle class="b1" cx="170"  cy="100" r="130" fill="#ff2e93"/>
    <circle class="b2" cx="1000" cy="290" r="140" fill="#27e8ff"/>
    <circle class="b3" cx="600"  cy="290" r="110" fill="#8dff4d"/>
  </g>

  <g fill="#ffffff">
    <path class="tw" d="M90 46 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z"/>
    <path class="tw" d="M230 246 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3z"/>
    <path class="tw" d="M740 70 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3z"/>
    <path class="tw" d="M1110 230 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z"/>
    <path class="tw" d="M940 252 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3z"/>
    <path class="tw" d="M1030 100 l3 8 8 3 -8 3 -3 8 -3 -8 -8 -3 8 -3z"/>
  </g>

  <!-- CRT feel sits behind the words, so the text stays crisp. -->
  <rect class="scan" x="0" y="0" width="{W}" height="120" fill="url(#sweep)"/>
  <rect width="{W}" height="{H}" fill="url(#lines)"/>

  <!-- The title: a soft glow, then cyan and pink copies that slip out during a glitch, then the real word on top. -->
  <g font-size="156" font-weight="900" letter-spacing="-3" text-anchor="middle">
    <text x="600" y="198" fill="url(#ink)" filter="url(#glow)" opacity="0.55">GlitchGlam</text>
    <text class="cy" x="600" y="198" fill="#27e8ff">GlitchGlam</text>
    <text class="mg" x="600" y="198" fill="#ff2ea6">GlitchGlam</text>
    <text class="main" x="600" y="198" fill="url(#ink)">GlitchGlam</text>
  </g>

  <!-- The sparkle trail: each spark follows the same path a little behind the bird and twinkles. -->
  <g>
{sparks()}
  </g>

  <!-- Afterimages: the same bird, a fraction of a second behind, fading. -->
  <g>
{ghosts()}
  </g>

  <!-- The magpie. Decorative. -->
  <g class="bird" filter="url(#birdglow)">
    <g class="flip">
      <g class="bob">
        <g transform="scale(0.85) translate(-80 -55)"><use href="#magpie"/></g>
      </g>
    </g>
  </g>
</svg>
'''
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT, len(svg), "bytes")
