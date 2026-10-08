#!/bin/bash
cd "$(dirname "$0")"
rm -rf frames && mkdir -p frames
export NODE_PATH=$(npm root -g)
for w in 0 1 2 3; do node render_part.js mv_template.html frames 60 82.0 $w 4 & done
wait
ls frames | wc -l
