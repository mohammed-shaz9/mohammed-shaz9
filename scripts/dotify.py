"""Render a photo as a coloured dot-matrix SVG.
Usage: python scripts/dotify.py assets/photo.png -o assets/portrait.svg --cols 64
"""
import argparse
from PIL import Image, ImageOps

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('-o', '--out', default='assets/portrait.svg')
ap.add_argument('--cols', type=int, default=64)
a = ap.parse_args()

im = Image.open(a.src).convert('RGB')
rows = round(a.cols * im.height / im.width)
small = im.resize((a.cols, rows), Image.LANCZOS)
lum = ImageOps.equalize(ImageOps.grayscale(small))
cell = 10
dots = []
for y in range(rows):
    for x in range(a.cols):
        b = lum.getpixel((x, y)) / 255
        r = cell * 0.48 * (0.25 + 0.75 * b)  # bright pixels get bigger dots
        R, G, B = small.getpixel((x, y))
        dots.append(f'<circle cx="{x * cell + cell / 2:.0f}" cy="{y * cell + cell / 2:.0f}" r="{r:.1f}" fill="#{R:02x}{G:02x}{B:02x}"/>')
w, h = a.cols * cell, rows * cell
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="100%" height="100%" rx="24" fill="#0d1117"/>{"".join(dots)}</svg>'
open(a.out, 'w').write(svg)
print(f'{a.out}: {a.cols}x{rows} dots, {len(svg) // 1024} KB')
