#!/bin/bash
# usage: bash render_all.sh <outDir> [workers] — whole song at 60fps as near-lossless segments, then joined
cd "$(dirname "$0")"
OUT=${1:-render}; NW=${2:-4}
mkdir -p "$OUT"
export NODE_PATH=$(npm root -g)
for w in $(seq 0 $((NW-1))); do node render_seg.js no_exit.html "$OUT/seg_$w.mp4" 60 213.4 $w $NW & done
wait
: > "$OUT/list.txt"; for w in $(seq 0 $((NW-1))); do echo "file 'seg_$w.mp4'" >> "$OUT/list.txt"; done
ffmpeg -loglevel error -y -f concat -safe 0 -i "$OUT/list.txt" -c copy "$OUT/master60.mp4"
ffprobe -v error -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$OUT/master60.mp4"
