#!/usr/bin/env python3
"""Motion QA for a finished video.

Reports:
  - static holds  : runs >= 0.2 s where the whole frame does not change (feels "stiff")
  - abrupt stops  : moving -> dead still within 2 frames (feels like "멈칫")
  - flicker       : seconds with 3+ large luminance jumps (eye strain; keep at 0)

usage: python3 check_motion.py video.mp4
"""
import subprocess, sys, numpy as np

src = sys.argv[1]
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', 'scale=192:108,format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.uint8).reshape(-1, 108, 192).astype(float)
fps = 30
d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
still = d < 0.15

runs, s = [], None
for i, v in enumerate(still):
    if v and s is None: s = i
    if not v and s is not None:
        if i - s >= 6: runs.append((round(s / fps, 2), round((i - s) / fps, 2)))
        s = None
print(f'frames {len(a)}')
print(f'static holds >=0.2s: {len(runs)} (total {sum(r[1] for r in runs):.1f}s) {runs[:15]}')
stops = [round(i / fps, 2) for i in range(2, len(d)) if d[i - 2] > 3 and d[i] < 0.15]
print(f'abrupt stops: {len(stops)} {stops[:20]}')
m = a.mean(axis=(1, 2)); dm = np.abs(np.diff(m))
bad = [(sec, int((dm[sec * fps:(sec + 1) * fps] > 20).sum())) for sec in range(len(dm) // fps + 1)]
bad = [b for b in bad if b[1] >= 4]
print(f'flicker seconds (>=4 big luminance jumps): {bad if bad else "none"}')
