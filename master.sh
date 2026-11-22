#!/bin/bash
# Masters raw.wav (Beat Maker's "Export WAV" of DEADLOCK.json) into the release files.
# 4x-oversampled limiter so true peak stays at -1 dBFS; lands around -7 LUFS, edit-loud.
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -v error -y -i raw.wav -af "aresample=192000,highpass=f=28,\
equalizer=f=4500:t=q:w=0.8:g=4,treble=g=2:f=9000,volume=4.5dB,\
alimiter=limit=0.88:level=false:attack=0.5:release=50,aresample=48000" \
	-c:a pcm_s24le DEADLOCK.wav
ffmpeg -v error -y -i DEADLOCK.wav -c:a libmp3lame -b:a 320k DEADLOCK.mp3
ffmpeg -nostats -i DEADLOCK.wav -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):'
