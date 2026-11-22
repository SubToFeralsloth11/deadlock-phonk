# DEADLOCK (drift phonk instrumental for edits)

130 BPM, F# Phrygian, 1:02, no vocals. Made in **[Beat Maker](https://github.com/SubToFeralsloth11/beat-maker)**:
every sound is a Beat Maker drum or instrument, and the audio is Beat Maker's own "Export WAV"
of `DEADLOCK.json`. No samples are used.

| File | What |
|---|---|
| `DEADLOCK.wav` | The song, mastered (48 kHz, 24-bit, -6.0 LUFS, true peak -1 dBFS) |
| `DEADLOCK.mp3` | The same at 320 kbps, for phone editing apps (CapCut and similar) |
| `DEADLOCK.mp4` | Video: the thumbnail with a waveform that moves to the music (1280x720, 30 fps, H.264, 320 kbps AAC) |
| `thumbnail.png` | 1280x720 cover |
| `DEADLOCK.json` | The Beat Maker project. Open it in Beat Maker to change the beat. |
| `raw.wav` | Beat Maker's export before mastering |
| `build_project.py` | Writes `DEADLOCK.json` (every pattern, note and knob setting) |
| `master.sh` | Turns `raw.wav` into `DEADLOCK.wav` and `DEADLOCK.mp3` (EQ, oversampled limiter) |
| `make_video.sh` | Makes `DEADLOCK.mp4` from `thumbnail.png` and `DEADLOCK.wav` |
| `make_thumbnail.py` | Draws `thumbnail.png` |

## Cue sheet for editing

Every time lands on a bar line, so cuts placed on them hit the beat. One bar is 1.85 s.

| Time | Section | What happens |
|---|---|---|
| 0:00.0 | Intro | Muffled cowbell hook, dark pad, vinyl crackle, shaker |
| 0:07.4 | Build | Hook opens up, kick rolls faster, snare roll, riser |
| 0:10.9 | **Gap** | Quarter-bar of silence: freeze-frame here |
| **0:11.1** | **DROP 1** | Impact and crash, punch kick with an F#1 808, clap+snare, open hats, doubled hook |
| 0:14.8 | Drop, part B | Brazilian funk kick/808 pattern, high cowbell layer, rim |
| 0:25.9 | Break | Back to the muffled hook and pad |
| 0:29.6 | Build 2 | Same build again |
| 0:33.1 | **Gap** | Freeze-frame here |
| **0:33.3** | **DROP 2** | Three rounds of drop A/B; impact on every A (0:33.3, 0:40.7, 0:48.1) |
| 0:55.4 | Outro | Muffled hook and pad; reverb tail to 1:02 |

## Rebuilding

```sh
python3 build_project.py   # writes DEADLOCK.json
```

Then open Beat Maker, click **Open**, pick `DEADLOCK.json` (it loads in "Play song" mode) and click
**Export WAV**. Save the file as `raw.wav` here, then:

```sh
./master.sh                # DEADLOCK.wav + DEADLOCK.mp3
python3 make_thumbnail.py
./make_video.sh            # DEADLOCK.mp4
```
