from math import sqrt, floor

def compute_cp(base_a, base_d, base_s, iv_a, iv_d, iv_s, cp_mult):
	return floor((base_a + iv_a) * sqrt(base_d + iv_d) * sqrt(base_s + iv_s) * cp_mult**2 / 10)

CP_MULTIPLIERS = (0.09400000, 0.13513743, 0.16639787, 0.19265092, 0.21573247, 
				  0.23657266, 0.25572005, 0.27353038, 0.29024988, 0.30605738,
				  0.32108760, 0.33544504, 0.34921268, 0.36245775, 0.37523559,
				  0.38759241, 0.39956728, 0.41119355, 0.42250001, 0.43292642,
				  0.44310755, 0.45305996, 0.46279839, 0.47233608, 0.48168495,
				  0.49085580, 0.49985844, 0.50870177, 0.51739395, 0.52594251,
				  0.53435433, 0.54263577, 0.55079269, 0.55883058, 0.56675452,
				  0.57456915, 0.58227891, 0.58988792, 0.59740001, 0.60481881,
				  0.61215729, 0.61939937, 0.62656713, 0.63364453, 0.64065295,
				  0.64757643, 0.65443563, 0.66121481, 0.66793400, 0.67457754,
				  0.68116492, 0.68768065, 0.69414365, 0.70053867, 0.70688421,
				  0.71316500, 0.71939909, 0.72557155, 0.73170000, 0.73474101,
				  0.73776948, 0.74078557, 0.74378943, 0.74678121, 0.74976104,
				  0.75272909, 0.75568551, 0.75863038, 0.76156384, 0.76448607,
				  0.76739717, 0.77029727, 0.77318650, 0.77606496, 0.77893275,
				  0.78179006, 0.78463697, 0.78747358, 0.79030001, 0.79280394,
				  0.79530001, 0.79780392, 0.80030001, 0.80280389, 0.80530001,
				  0.80780387, 0.81030001, 0.81280384, 0.81530001, 0.81780382,
				  0.82030001, 0.82280380, 0.82530001, 0.82780378, 0.83030001,
				  0.83280375, 0.83530001, 0.83780373, 0.84030001, 0.84280371,
				  0.84529999)

with open("base_stats.txt", "r") as f:
	base_stats = f.read().splitlines()

base_stats = [l.split(":") for l in base_stats]
base_stats = dict((a, (int(b), int(c), int(d))) for a,b,c,d in base_stats)

### NAME

while True:
	name = input("Pokémon name: ").strip()
	if not name:
		print("[E] Empty name")
		continue
	matching = [x for x in base_stats.keys() if name.lower() in x.lower()]
	if len(matching) == 0:
		print("[E] Pokémon not found")
		continue
	elif len(matching) > 1:
		print("[E] Multiple Pokémon found:")
		for idx, m in enumerate(matching):
			print(f"{idx+1}: {m}")
		while True:
			try:
				number = int(input("Pick a number from the list above: ").strip())
			except ValueError:
				continue
			if not 1 <= number <= len(matching):
				continue
			chosen = matching[number-1]
			break
		break
	elif len(matching) == 1:
		chosen = matching[0]
		break

name = chosen
base_a, base_d, base_s = base_stats[name]

### CP

while True:
	try:
		cp_read = int(input("CP: ").strip())
	except ValueError:
		continue
	if not 10 <= cp_read <= 5069:
		continue
	break

### WEATHER BOOST

weather_boosted = input("Weather boosted? 'y' for 'yes', anything else for 'no': ").lower().strip() == "y"

if weather_boosted:
	max_cp_multiplier_index = 78
else:
	max_cp_multiplier_index = 68	

### OUTPUT

star_ratios = [0, 0, 0, 0, 0]
for idx, cp_mult in enumerate(CP_MULTIPLIERS[:max_cp_multiplier_index+1]):
	level = (idx/2)+1
	if level != int(level):
		continue # skip "half-levels", as they're not used for wild pokémon
	for iv_a in range(1, 16):
		for iv_d in range(1, 16):
			for iv_s in range(1, 16):
				cp = compute_cp(base_a, base_d, base_s, iv_a, iv_d, iv_s, cp_mult)
				if cp == cp_read:
					total = iv_a + iv_d + iv_s
					if 0 <= total <= 22:
						stars = ""
						star_ratios[0] += 1
					elif 23 <= total <= 29:
						stars = "*"
						star_ratios[1] += 1
					elif 30 <= total <= 36:
						stars = "**"
						star_ratios[2] += 1
					elif 37 <= total <= 44:
						stars = "***"
						star_ratios[3] += 1
					elif total == 45:
						stars = "**** PERFECT"
						star_ratios[4] += 1
					print(f"Level {int(level):02d}, IVS {iv_a:02d}/{iv_d:02d}/{iv_s:02d} {stars}")
print("---")
for idx, star_ratio in enumerate(star_ratios):
	try:
		ratio = floor(star_ratio / sum(star_ratios) * 100)
	except ZeroDivisionError:
		ratio = 0
	print(f"{idx} stars(s): {ratio}%")