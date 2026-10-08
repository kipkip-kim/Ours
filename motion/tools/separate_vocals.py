#!/usr/bin/env python3
"""Isolate the vocal track from a song with the UVR MDX-Net "Voc_FT" ONNX model (CPU, onnxruntime).

Model: https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR-MDX-NET-Voc_FT.onnx
Needs: numpy, librosa, soundfile, onnxruntime (pip; no torch / Hugging Face needed).
usage: python separate_vocals.py song.wav model.onnx vocals.wav
"""
import sys, numpy as np, librosa, soundfile as sf, onnxruntime as ort

N_FFT, HOP, DIM_F, DIM_T, SR, COMP = 6144, 1024, 3072, 256, 44100, 1.021
L = HOP * (DIM_T - 1)                       # samples per model window -> exactly DIM_T stft frames
STEP = L // 2

src, model, out = sys.argv[1:4]
y, _ = librosa.load(src, sr=SR, mono=False)
if y.ndim == 1: y = np.stack([y, y])
n = y.shape[1]
pad = np.pad(y, ((0, 0), (L, L + STEP)))
sess = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
acc = np.zeros_like(pad); wsum = np.zeros(pad.shape[1])
fade = np.hanning(L)
for s in range(0, pad.shape[1] - L + 1, STEP):
    x = pad[:, s:s + L]
    spec = librosa.stft(x, n_fft=N_FFT, hop_length=HOP, window='hann', center=True)[:, :DIM_F]  # (2, F, T)
    inp = np.stack([spec[0].real, spec[0].imag, spec[1].real, spec[1].imag])[None].astype(np.float32)
    o = sess.run(None, {'input': inp})[0][0]
    vs = np.zeros((2, N_FFT // 2 + 1, DIM_T), np.complex64)
    vs[0, :DIM_F] = o[0] + 1j * o[1]; vs[1, :DIM_F] = o[2] + 1j * o[3]
    v = librosa.istft(vs, hop_length=HOP, window='hann', center=True, length=L)
    acc[:, s:s + L] += v * fade; wsum[s:s + L] += fade
v = (acc / np.maximum(wsum, 1e-8))[:, L:L + n] * COMP
sf.write(out, v.T, SR)
print('wrote', out, v.shape[1] / SR, 's')
