#!/bin/bash
# DEADLOCK.mp4: the thumbnail with a violet waveform that moves to the music, and the song as
# 320 kbps AAC. 1280x720, 30 fps, H.264, plays in CapCut, phones and YouTube.
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -v error -y -loop 1 -framerate 30 -i thumbnail.png -i DEADLOCK.wav -filter_complex "
	[1:a]aformat=channel_layouts=mono,showwaves=s=1280x84:mode=cline:rate=30:scale=sqrt:colors=#a04dff,
		format=rgba,colorchannelmixer=aa=0.8[wave];
	[wave]split[w1][w2];[w2]gblur=sigma=6[glow];[glow][w1]blend=all_mode=screen[wv];
	[0:v][wv]overlay=0:470:shortest=1,format=yuv420p[v]" \
	-map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 320k -ar 48000 \
	-shortest -movflags +faststart DEADLOCK.mp4
