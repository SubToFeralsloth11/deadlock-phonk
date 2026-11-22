#!/usr/bin/env python3
"""Draws the DEADLOCK thumbnail (1280x720): violet night city, a neon padlock in the sky, a
drifting coupe in silhouette with tyre smoke, and a glitched glowing title. Output: thumbnail.png."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1280, 720
SS = 2  # supersampling for clean edges
IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
rng = random.Random(130)


def lerp(a, b, t):
	return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient_sky() -> Image.Image:
	top, mid, horizon = (6, 0, 14), (40, 2, 40), (150, 8, 30)
	y = np.linspace(0, 1, H)[:, None]
	img = np.zeros((H, W, 3), np.float32)
	for c in range(3):
		upper = top[c] + (mid[c] - top[c]) * np.clip(y / 0.45, 0, 1)
		lower = mid[c] + (horizon[c] - mid[c]) * np.clip((y - 0.45) / 0.3, 0, 1)
		img[..., c] = np.where(y < 0.45, upper, lower)
	return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8).repeat(1, 1))


def radial(size, cx, cy, radius, color, power=2.0) -> Image.Image:
	yy, xx = np.mgrid[0:size[1], 0:size[0]].astype(np.float32)
	d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / radius
	a = np.clip(1 - d, 0, 1) ** power
	img = np.zeros((size[1], size[0], 3), np.float32)
	for c in range(3):
		img[..., c] = color[c] * a
	return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def add(base: Image.Image, layer: Image.Image) -> Image.Image:
	return ImageChops.add(base, layer)


def skyline(horizon: int) -> Image.Image:
	"""Black city silhouette with a few lit windows, as an RGBA layer."""
	layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
	d = ImageDraw.Draw(layer)
	x = -20
	while x < W:
		bw = rng.randint(38, 110)
		bh = rng.choice([rng.randint(40, 120), rng.randint(90, 230)])
		top = horizon - bh
		d.rectangle([x * SS, top * SS, (x + bw) * SS, (horizon + 5) * SS], fill=(8, 2, 12, 255))
		if rng.random() < 0.35:  # antenna
			ax = x + bw // 2
			d.rectangle([ax * SS, (top - rng.randint(15, 45)) * SS, (ax + 2) * SS, top * SS],
				fill=(8, 2, 12, 255))
		for wy in range(top + 8, horizon - 6, 11):
			for wx in range(x + 6, x + bw - 6, 9):
				if rng.random() < 0.09:
					c = rng.choice([(255, 60, 90), (255, 170, 120), (180, 80, 255)])
					d.rectangle([wx * SS, wy * SS, (wx + 3) * SS, (wy + 4) * SS], fill=c + (200,))
		x += bw + rng.randint(-8, 6)
	return layer.resize((W, H), Image.LANCZOS)


def car(ox: int, oy: int, scale: float) -> tuple[Image.Image, Image.Image]:
	"""A low coupe facing right, in silhouette. Returns (body RGBA, light glows RGB)."""
	def p(x, y):
		return ((ox + x * scale) * SS, (oy + y * scale) * SS)

	body = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
	d = ImageDraw.Draw(body)
	dark = (4, 0, 8, 255)
	outline = [(28, 205), (24, 168), (40, 140), (190, 126), (300, 84), (330, 76), (520, 70),
		(560, 74), (650, 96), (770, 140), (930, 152), (972, 170), (982, 200), (970, 214),
		(28, 214)]
	d.polygon([p(*q) for q in outline], fill=dark)
	# Rear wing on two posts.
	d.polygon([p(20, 112), p(150, 108), p(152, 119), p(22, 124)], fill=dark)
	d.rectangle([p(60, 118), p(72, 136)], fill=dark)
	d.rectangle([p(118, 118), p(130, 132)], fill=dark)
	# Side window, faintly lit by the moon.
	d.polygon([p(318, 90), p(512, 80), p(548, 84), p(630, 132), p(336, 134)], fill=(46, 10, 40, 255))
	d.line([p(470, 82), p(482, 134)], fill=dark, width=int(7 * scale * SS))
	# Wheels: arch shadow, tyre, rim spokes catching red light.
	for cx in (205, 800):
		r = 62
		d.ellipse([p(cx - r - 6, 214 - r - 6), p(cx + r + 6, 214 + r + 6)], fill=dark)
		d.ellipse([p(cx - r + 14, 214 - r + 14), p(cx + r - 14, 214 + r - 14)], fill=(30, 6, 18, 255))
		for k in range(10):
			a = k * np.pi / 5 + 0.3
			x2, y2 = cx + np.cos(a) * (r - 18), 214 + np.sin(a) * (r - 18)
			d.line([p(cx, 214), p(x2, y2)], fill=(90, 14, 34, 255), width=int(4 * scale * SS))
		d.ellipse([p(cx - 9, 205), p(cx + 9, 223)], fill=(140, 20, 40, 255))
	body = body.resize((W, H), Image.LANCZOS)

	glow = Image.new("RGB", (W * SS, H * SS), (0, 0, 0))
	g = ImageDraw.Draw(glow)
	g.polygon([p(930, 158), p(970, 170), p(968, 178), p(928, 168)], fill=(255, 245, 230))
	g.rectangle([p(24, 146), p(40, 164)], fill=(255, 20, 50))
	glow = glow.resize((W, H), Image.LANCZOS)
	return body, glow


def smoke(base: Image.Image, x0: int, y0: int) -> Image.Image:
	"""Tyre smoke billowing back from the rear wheel."""
	layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
	d = ImageDraw.Draw(layer)
	for _ in range(420):
		t = rng.random()
		x = x0 - t * 560 + rng.gauss(0, 30)
		y = y0 - t * 150 * rng.random() + rng.gauss(0, 18)
		r = 20 + t * 110 * rng.random()
		shade = rng.randint(110, 190)
		col = (shade, int(shade * 0.75), int(shade * 0.9), int(26 * (1 - t) + 6))
		d.ellipse([x - r, y - r, x + r, y + r], fill=col)
	layer = layer.filter(ImageFilter.GaussianBlur(14))
	return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


def glitch_title(img: Image.Image, text: str, cy: int, size: int) -> Image.Image:
	font = ImageFont.truetype(IMPACT, size)
	tmp = Image.new("L", (W, H), 0)
	td = ImageDraw.Draw(tmp)
	box = td.textbbox((0, 0), text, font=font)
	tw, th = box[2] - box[0], box[3] - box[1]
	x, y = (W - tw) // 2 - box[0], cy - th // 2 - box[1]
	td.text((x, y), text, font=font, fill=255)
	mask = tmp

	# Violet bloom behind the letters.
	bloom = Image.new("RGB", (W, H), (0, 0, 0))
	bloom.paste((150, 30, 255), mask=mask.filter(ImageFilter.GaussianBlur(26)))
	img = add(img, bloom)
	img = add(img, bloom.filter(ImageFilter.GaussianBlur(40)))

	# Chromatic split: cyan left, magenta right, white core.
	for dx, col in ((-7, (0, 230, 255)), (7, (255, 0, 200))):
		layer = Image.new("RGB", (W, H), (0, 0, 0))
		layer.paste(col, mask=ImageChops.offset(mask, dx, 0))
		img = ImageChops.screen(img, layer)
	core = Image.new("RGB", (W, H), (255, 240, 245))
	img.paste(core, mask=mask)

	# Horizontal glitch slices through the title band.
	arr = np.array(img)
	top, bottom = cy - th // 2 - 10, cy + th // 2 + 10
	for _ in range(4):
		y0 = rng.randint(top, bottom - 6)
		hgt = rng.randint(3, 10)
		shift = rng.choice([-1, 1]) * rng.randint(8, 24)
		arr[y0:y0 + hgt] = np.roll(arr[y0:y0 + hgt], shift, axis=1)
	return Image.fromarray(arr)


def small_text(img: Image.Image, text: str, xy, size: int, fill, spacing: int, anchor="la") -> None:
	d = ImageDraw.Draw(img)
	font = ImageFont.truetype(IMPACT, size)
	x, y = xy
	if anchor == "ma":
		total = sum(d.textlength(ch, font=font) + spacing for ch in text) - spacing
		x -= total / 2
	for ch in text:
		d.text((x, y), ch, font=font, fill=fill)
		x += d.textlength(ch, font=font) + spacing


def to_violet(img: Image.Image) -> Image.Image:
	"""Rotates the red scene to violet (hue +275 degrees) so the palette matches the padlock."""
	h, s, v = img.convert("HSV").split()
	h = h.point(lambda x: (x + 196) % 256)
	return Image.merge("HSV", (h, s, v)).convert("RGB")


def padlock(img: Image.Image, cx: int, cy: int) -> Image.Image:
	"""A neon-tube padlock (closed shackle, keyhole) glowing cyan over the city."""
	mask = Image.new("L", (W * SS, H * SS), 0)
	d = ImageDraw.Draw(mask)
	s = SS
	bw, bh, tube = 120, 96, 9
	bx0, by0 = cx - bw // 2, cy - bh // 2 + 30
	d.rounded_rectangle([bx0 * s, by0 * s, (bx0 + bw) * s, (by0 + bh) * s], radius=16 * s,
		outline=255, width=tube * s)
	sw = 76  # shackle: half ellipse plus two legs into the body
	d.arc([(cx - sw // 2) * s, (by0 - 74) * s, (cx + sw // 2) * s, (by0 + 4) * s], 180, 360,
		fill=255, width=tube * s)
	for x in (cx - sw // 2, cx + sw // 2 - tube):
		d.rectangle([x * s, (by0 - 36) * s, (x + tube) * s, by0 * s], fill=255)
	ky = by0 + bh // 2 - 8
	d.ellipse([(cx - 11) * s, (ky - 11) * s, (cx + 11) * s, (ky + 11) * s], fill=255)
	d.polygon([((cx - 7) * s, ky * s), ((cx + 7) * s, ky * s), ((cx + 4) * s, (ky + 28) * s),
		((cx - 4) * s, (ky + 28) * s)], fill=255)
	mask = mask.resize((W, H), Image.LANCZOS)
	for blur, col in ((40, (0, 90, 140)), (14, (0, 200, 255)), (4, (120, 240, 255))):
		glow = Image.new("RGB", (W, H), (0, 0, 0))
		glow.paste(col, mask=mask.filter(ImageFilter.GaussianBlur(blur)))
		img = add(img, glow)
	core = Image.new("RGB", (W, H), (225, 252, 255))
	img.paste(core, mask=mask)
	return img


def main() -> None:
	horizon = 470
	img = gradient_sky()

	# Stars.
	d = ImageDraw.Draw(img)
	for _ in range(260):
		x, y = rng.randint(0, W), rng.randint(0, horizon - 120)
		b = rng.randint(60, 200)
		d.point((x, y), fill=(b, int(b * 0.8), b))

	# Halo where the padlock will hang (drawn red, turned violet by the hue shift below).
	mx, my = 1085, 330
	img = add(img, radial((W, H), mx, my, 410, (150, 10, 40), 2.2))

	# City.
	img = Image.alpha_composite(img.convert("RGBA"), skyline(horizon)).convert("RGB")

	# Wet road: dark, with the moon and city glow smeared into it.
	road = np.array(img).astype(np.float32)
	for y in range(horizon, H):
		t = (y - horizon) / (H - horizon)
		src = max(0, horizon - (y - horizon) * 2)
		road[y] = road[src] * (0.35 - 0.2 * t) + np.array([10, 2, 10]) * (0.8 + t)
	img = Image.fromarray(np.clip(road, 0, 255).astype(np.uint8))
	streak = radial((W, H), mx, horizon + 120, 260, (120, 10, 40), 1.5).resize((W, H))
	img = add(img, streak.filter(ImageFilter.GaussianBlur(20)))
	d = ImageDraw.Draw(img)
	for k in range(14):  # motion streaks on the asphalt
		y = rng.randint(horizon + 20, H - 10)
		x0 = rng.randint(-100, W)
		d.line([(x0, y), (x0 + rng.randint(120, 380), y)], fill=(90, 20, 50), width=rng.randint(1, 3))

	# Car + smoke + lights.
	scale = 0.62
	ox, oy = 330, 520
	img = smoke(img, int(ox + 205 * scale), int(oy + 200 * scale))
	body, lights = car(ox, oy, scale)
	rim = Image.new("RGB", (W, H), (0, 0, 0))
	rim.paste((255, 30, 70), mask=body.split()[3].filter(ImageFilter.GaussianBlur(6)))
	img = add(img, Image.eval(rim, lambda v: v // 2))
	img = Image.alpha_composite(img.convert("RGBA"), body).convert("RGB")
	img = add(img, lights)
	img = add(img, lights.filter(ImageFilter.GaussianBlur(8)))
	img = add(img, lights.filter(ImageFilter.GaussianBlur(30)))
	beam = Image.new("RGB", (W, H), (0, 0, 0))
	bd = ImageDraw.Draw(beam)
	hx, hy = ox + 965 * scale, oy + 166 * scale
	bd.polygon([(hx, hy - 4), (W + 50, hy - 90), (W + 50, hy + 80), (hx, hy + 6)], fill=(90, 80, 75))
	img = add(img, beam.filter(ImageFilter.GaussianBlur(25)))
	tail = Image.new("RGB", (W, H), (0, 0, 0))
	tdr = ImageDraw.Draw(tail)
	tx, ty = ox + 30 * scale, oy + 155 * scale
	tdr.rectangle([tx - 420, ty - 2, tx, ty + 3], fill=(200, 10, 40))
	img = add(img, tail.filter(ImageFilter.GaussianBlur(4)))

	img = to_violet(img)
	img = padlock(img, mx, my)

	# Title + tags.
	img = glitch_title(img, "DEADLOCK", 150, 210)
	small_text(img, "D R I F T   P H O N K", (W // 2, 262), 34, (220, 205, 255), 2, anchor="ma")
	d = ImageDraw.Draw(img)
	d.rectangle([40, 40, 168, 78], fill=(130, 30, 240))
	small_text(img, "130 BPM", (52, 41), 30, (255, 255, 255), 2)
	small_text(img, "NO VOCALS  •  EDIT AUDIO", (W - 40 - 380, 652), 28, (190, 170, 255), 3)

	# Finish: grain, scanlines, vignette.
	arr = np.array(img).astype(np.float32)
	noise = np.random.default_rng(3).normal(0, 9, (H, W, 1))
	arr += noise
	arr[::3] *= 0.9
	yy, xx = np.mgrid[0:H, 0:W]
	v = 1 - 0.55 * np.clip((((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2), 0, 1)
	arr *= v[..., None]
	Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(ROOT / "thumbnail.png", optimize=True)


if __name__ == "__main__":
	main()
