#!/usr/bin/env python3
"""Tile still_*.png files (from render.js stills mode) into 3x3 contact sheets for quick review.

usage: python3 contact_sheet.py <stills_dir>   -> <stills_dir>/sheet_N.png
"""
import glob, os, sys
from PIL import Image, ImageDraw

d = sys.argv[1]
fs = sorted(glob.glob(os.path.join(d, 'still_*.png')), key=lambda f: float(os.path.basename(f)[6:-4]))
for s in range(0, len(fs), 9):
    sheet = Image.new('RGB', (1920, 1080))
    for j, f in enumerate(fs[s:s + 9]):
        im = Image.open(f).resize((640, 360)); dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, 90, 26], fill='black'); dr.text((4, 4), os.path.basename(f)[6:-4], fill='white')
        sheet.paste(im, ((j % 3) * 640, (j // 3) * 360))
    sheet.save(os.path.join(d, f'sheet_{s // 9}.png'))
print('sheets:', (len(fs) + 8) // 9)
