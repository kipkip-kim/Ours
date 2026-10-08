#!/usr/bin/env python3
"""Beat grid for a song -> beats.js (window.BEATS) used by the template's beat clock.

Needs librosa (installed in the OpenMontage venv: /home/user/OpenMontage/.venv/bin/python).
usage: python beats.py song.wav beats.js
"""
import sys, json, librosa
import numpy as np

y, sr = librosa.load(sys.argv[1], sr=None, mono=True)
tempo, frames = librosa.beat.beat_track(y=y, sr=sr)
beats = [round(float(t), 3) for t in librosa.frames_to_time(frames, sr=sr)]
open(sys.argv[2], 'w').write('window.BEATS=' + json.dumps(beats) + ';\n')
print(f'tempo {float(np.atleast_1d(tempo)[0]):.1f} BPM, {len(beats)} beats, first {beats[:4]}')
