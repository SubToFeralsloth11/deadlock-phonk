#!/usr/bin/env python3
"""Writes DEADLOCK.json, a Beat Maker project (open it with Beat Maker's "Open" button).

130 BPM, F# Phrygian. Beat Maker patterns are 2 bars (32 sixteenth steps) and a song is
16 pattern slots, so the song is 32 bars, about 59 s:

    A A | B | C D C D | A | B | C D C D C D | A
    intro  build  drop 1  break build  drop 2      outro

A  intro/break/outro: muffled cowbell hook, dark pad, vinyl crackle, shaker
B  build: bright hook, rolling kick, snare roll, riser, half-step gap before the drop
C  drop: impact + crash, punch kick and 808 together, clap+snare, open hats, hook
D  drop variation: Brazilian funk kick/808 pattern, high cowbell layer, rim offbeats
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = 32
_ids = 0


def new_id(tag: str) -> str:
	global _ids
	_ids += 1
	return f"dl{_ids}{tag}"


def drum(sound: str, **o) -> dict:
	return {"id": new_id("d"), "sound": sound, "vol": 0.8, "pitch": 0, "tone": 0, "decay": 1,
		"pan": 0, "rev": 0, "dly": 0, "mute": False, "solo": False, **o}


def synth(inst: str, name: str, **o) -> dict:
	return {"id": new_id("s"), "inst": inst, "name": name, "oct": 4, "vol": 0.7, "tone": 0,
		"pan": 0, "rev": 0.15, "dly": 0, "mute": False, "solo": False, **o}


def grid(s: str) -> list[int]:
	"""'X' = loud hit, 'x' = normal hit, anything else = rest. Short strings repeat."""
	s = s or "."
	return [2 if s[i % len(s)] == "X" else 1 if s[i % len(s)] == "x" else 0 for i in range(STEPS)]


def steps(*on: int, loud: tuple[int, ...] = ()) -> list[int]:
	c = [0] * STEPS
	for s in on:
		c[s] = 2 if s in loud else 1
	return c


def notes(*n) -> list[dict]:
	"""(step, scale row, length in steps); length defaults to 1."""
	return [{"s": s, "r": r, "len": rest[0] if rest else 1} for s, r, *rest in n]


# Rows in F# Phrygian: 0 F#, 1 G, 2 A, 3 B, 4 C#, 5 D, 6 E, 7 F#, 8 G, 9 A, 10 B, 11 C#, 12 D
HOOK = notes(  # 3-3-2 cowbell hook; bar 2 falls back to the low C#
	(0, 7), (3, 7), (6, 7), (8, 8), (10, 7), (12, 5), (14, 4),
	(16, 7), (19, 7), (22, 7), (24, 8), (26, 8), (27, 7), (28, 5), (30, 4))
HOOK_UP = notes(  # same first bar, bar 2 climbs instead
	(0, 7), (3, 7), (6, 7), (8, 8), (10, 7), (12, 5), (14, 4),
	(16, 10), (19, 10), (22, 9), (24, 8), (26, 9), (27, 8), (28, 7), (30, 8))
PAD = notes((0, 0, 15), (0, 2, 15), (0, 4, 15), (16, 1, 15), (16, 3, 15), (16, 5, 15))  # F#m -> G

# Tracks
kick = drum("Punch Kick", vol=0.7, decay=1.0)
clap = drum("Clap", vol=1.5, rev=0.22, tone=0.12)
snare = drum("Snare", vol=0.8, rev=0.12, tone=0.1)
roll = drum("Trap Snare", vol=0.9, rev=0.15)
hat = drum("Closed Hat", vol=1.4, pan=0.18)
hat2 = drum("Closed Hat", vol=1.0, pan=-0.3, pitch=3, decay=1.4)
ohat = drum("Open Hat", vol=0.9, pan=-0.2, rev=0.1)
rim = drum("Rim", vol=0.4, pan=0.35, dly=0.2)
shaker = drum("Shaker", vol=0.5, pan=-0.3)
crackle = drum("Vinyl Crackle", vol=0.55)
riser = drum("Riser", vol=0.55, decay=1.1, rev=0.3)
impact = drum("Impact", vol=0.9, rev=0.25)
crash = drum("Crash", vol=0.32, pan=0.1, rev=0.2)

bell_lo = synth("Phonk Cowbell", "Hook (muffled)", oct=4, vol=0.75, tone=-0.55, rev=0.4, dly=0.3)
bell = synth("Phonk Cowbell", "Hook", oct=4, vol=1.5, pan=-0.12, rev=0.18, dly=0.22)
bell2 = synth("Phonk Cowbell", "Hook (double)", oct=4, vol=1.3, pan=0.12, tone=0.2, rev=0.1)
bell_hi = synth("Phonk Cowbell", "Hook (high)", oct=5, vol=0.45, pan=-0.25, rev=0.25, dly=0.3)
pad = synth("Warm Pad", "Dark pad", oct=3, vol=0.4, rev=0.45)  # intro, break and build only
bass = synth("808 Bass", "808", oct=1, vol=0.65, rev=0)  # F#1 = 46 Hz: the sub carries the drop

intro = {
	"drums": {
		crackle["id"]: grid("x......."),
		shaker["id"]: grid("..x...x...x...x."),
	},
	"notes": {bell_lo["id"]: HOOK, pad["id"]: PAD},
}

build = {
	"drums": {
		kick["id"]: steps(0, 4, 8, 12, 16, 18, 20, 22, 24, 25, 26, 27, 28, 29, loud=(0, 16)),
		roll["id"]: steps(16, 20, 24, 26, 28, 29, loud=(28, 29)),
		hat["id"]: grid("x.x.x.x.x.x.x.x.xxxxxxxxxxxxxx.."),
		riser["id"]: steps(11),
		crackle["id"]: grid("x......."),
	},
	"notes": {bell["id"]: HOOK, bell2["id"]: HOOK, pad["id"]: PAD},
}

drop = {
	"drums": {
		kick["id"]: steps(0, 6, 10, 16, 22, 26, 29, loud=(0, 16)),
		clap["id"]: steps(4, 12, 20, 28, loud=(4, 12, 20, 28)),
		snare["id"]: steps(4, 12, 20, 28),
		hat["id"]: grid("X.XXX.XXX.XXX.XXX.XXX.XXX.XXXXXX"),
		hat2["id"]: grid(".x.x.x.x.x.x.x.x"),
		ohat["id"]: grid("..x...x...x...x."),
		impact["id"]: steps(0),
		crash["id"]: steps(0),
		shaker["id"]: grid(".x.x.x.x.x.x.x.x"),
		crackle["id"]: grid("x......."),
	},
	"notes": {
		bell["id"]: HOOK,
		bell2["id"]: HOOK,
		bass["id"]: notes((0, 0, 5), (6, 0, 3), (10, 0, 5), (16, 1, 5), (22, 1, 3), (26, 0, 2), (29, 7, 3)),
	},
}

drop_b = {
	"drums": {
		kick["id"]: steps(0, 3, 6, 10, 13, 16, 19, 22, 26, 28, 30, loud=(0, 16)),
		clap["id"]: steps(4, 12, 20, 28, loud=(4, 12, 20, 28)),
		snare["id"]: steps(4, 12, 20, 28, 31),
		hat["id"]: grid("X.XXX.XXX.XXX.XX"),
		hat2["id"]: grid(".x.x.x.x.x.x.x.x"),
		ohat["id"]: grid("..x...x...x...x."),
		rim["id"]: grid(".x...x.x.x...x.."),
		shaker["id"]: grid(".x.x.x.x.x.x.x.x"),
		crackle["id"]: grid("x......."),
	},
	"notes": {
		bell["id"]: HOOK_UP,
		bell2["id"]: HOOK_UP,
		bell_hi["id"]: HOOK_UP,  # same rows, one octave up via oct=5 (rows stop at 14)
		bass["id"]: notes((0, 0, 3), (3, 0, 3), (6, 0, 4), (10, 0, 3), (13, 0, 3),
			(16, 5, 3), (19, 5, 3), (22, 4, 4), (26, 2, 2), (28, 1, 2), (30, 1, 2)),
	},
}

A, B, C, D = 0, 1, 2, 3
project = {
	"bpm": 130, "swing": 0, "key": 6, "scale": "Phrygian (dark)", "master": 0.6,
	"mode": "song", "cur": C,
	"fx": {"reverb": 0.3, "size": 2.0, "delay": 0.18, "feedback": 0.3, "div": 3, "drive": 0.25, "filter": 1},
	"song": [A, A, B, C, D, C, D, A, B, C, D, C, D, C, D, A],
	"patterns": [intro, build, drop, drop_b],
	"drums": [kick, clap, snare, roll, hat, hat2, ohat, rim, shaker, crackle, riser, impact, crash],
	"synths": [bell, bell2, bell_lo, bell_hi, pad, bass],
	"sel": bell["id"],
}

if __name__ == "__main__":
	out = ROOT / "DEADLOCK.json"
	out.write_text(json.dumps(project, indent=1))
	print(f"wrote {out}")
