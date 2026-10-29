"""Regenera camadas do mapa da Fase 1 e gera public/maps/fase-01/decor.json (posicionamento da decoração).

Determinístico (seed fixa). Uso: python3 gen_world.py   (a partir de V2/tools ou V2)
"""
import json
import math
import os
import random

from pxlib import hsh, nn

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MAP_PATH = os.path.join(ROOT, "public", "maps", "fase-01", "forest.json")
DECOR_PATH = os.path.join(ROOT, "public", "maps", "fase-01", "decor.json")
W, H, T = 50, 32, 32
BRIDGE = (10, 11)
PATH_GIDS = (4, 5, 6, 7)

# colisão (largura, altura) centrada no pé do sprite; arco tem duas colunas
COLLIDERS = {
    "tree_0": (14, 10), "tree_1": (14, 10), "tree_2": (14, 10), "tree_3": (14, 10), "tree_4": (14, 10),
    "tree_big": (18, 12), "pine_0": (12, 8), "pine_1": (12, 8),
    "rock_0": (34, 16), "rock_1": (24, 12), "pillar_broken": (18, 12), "pillar_full": (18, 12),
    "wall_ruin": (56, 14), "stump": (22, 10), "log": (44, 10), "stake_0": (8, 6), "stake_1": (8, 6),
    "barrel": (18, 10), "crystal_0": (24, 10), "crystal_1": (18, 8), "crystal_2": (32, 12), "torch": (14, 8),
}
LIGHTS = {"crystal_0": (78, "cyan"), "crystal_1": (58, "cyan"), "crystal_2": (96, "cyan"), "torch": (118, "warm")}


def main():
    with open(MAP_PATH) as fh:
        world = json.load(fh)
    layers = {layer["name"]: layer for layer in world["layers"]}
    path = layers["Path"]["data"]
    water = layers["Water"]["data"]
    objects = {o["name"]: o for o in layers["Objects"]["objects"]}

    # --- Path: remove o trecho atrás do santuário e aplica bordas irregulares ---
    for r in range(0, 4):
        for c in range(W):
            path[r * W + c] = 0
    for i, gid in enumerate(path):
        if gid in (17, 18):
            path[i] = 4
    rows = {}
    for r in range(H):
        cols = [c for c in range(W) if path[r * W + c] in PATH_GIDS]
        bridge = any(path[r * W + c] in BRIDGE for c in range(W))
        if cols:
            rows[r] = (min(cols), max(cols))
            if not bridge:
                path[r * W + min(cols)] = 17
                path[r * W + max(cols)] = 18
        elif bridge:
            bcols = [c for c in range(W) if path[r * W + c] in BRIDGE]
            rows[r] = (min(bcols), max(bcols))

    # --- Architecture: remove as ruínas de tiles (substituídas por sprites) ---
    arch = layers["Architecture"]["data"]
    for i in range(len(arch)):
        arch[i] = 0

    water_rows = {r for r in range(H) if any(water[r * W + c] for c in range(W))}

    def is_path(c, r):
        return r in rows and rows[r][0] - 1 <= c <= rows[r][1] + 1

    # --- Ground / GroundDetails ---
    ground = layers["Ground"]["data"]
    details = layers["GroundDetails"]["data"]
    for r in range(H):
        for c in range(W):
            i = r * W + c
            n = nn(c * 32, r * 32, 7, 96) * 0.6 + nn(c * 32, r * 32, 19, 40) * 0.4
            g = 1 if n < 0.4 else 2 if n < 0.6 else 3
            if hsh(c, r, 5) < 0.28:
                g = 25 + int(hsh(c, r, 6) * 4)
            ground[i] = g
            details[i] = 0
            if r in water_rows or is_path(c, r):
                continue
            h = hsh(c, r, 21)
            if h > 0.5:
                continue
            k = hsh(c, r, 22)
            if k < 0.30:
                details[i] = 14 if hsh(c, r, 23) < 0.5 else 29
            elif k < 0.40:
                details[i] = 15 if hsh(c, r, 23) < 0.5 else 30
            elif k < 0.44:
                details[i] = 16
            elif k < 0.54:
                details[i] = (19, 20, 21, 31)[int(hsh(c, r, 24) * 4)]
            elif k < 0.70:
                details[i] = 22 if hsh(c, r, 25) < 0.6 else 32
            elif k < 0.82:
                details[i] = 23
            else:
                details[i] = 24

    # --- Decoração ---
    rng = random.Random(20240611)
    entries = []
    spawn = objects["spawn"]
    points = [(o["x"], o["y"], 58) for n, o in objects.items() if o["type"] == "interaction"]
    points.append((spawn["x"], spawn["y"], 70))
    shrine = (640, 80, 960, 430)

    def near_path(x, y, margin):
        r0, r1 = int((y - margin) // T), int((y + margin) // T)
        for r in range(max(0, r0), min(H - 1, r1) + 1):
            if r in rows:
                if rows[r][0] * T - margin < x < (rows[r][1] + 1) * T + margin:
                    return True
        return False

    def in_water(y, margin=4):
        return any(r * T - margin < y < (r + 1) * T + margin for r in water_rows)

    def ok(x, y, path_margin, keep=48):
        if x < 16 or x > W * T - 16 or y < 24 or y > H * T - 6:
            return False
        if near_path(x, y, path_margin) or in_water(y):
            return False
        if shrine[0] - 24 < x < shrine[2] + 24 and shrine[1] < y < shrine[3] + 24:
            return False
        for px, py, pr in points:
            if math.hypot(x - px, y - py) < pr:
                return False
        for e in entries:
            if math.hypot(x - e["x"], (y - e["y"]) * 1.35) < min(keep, e.get("keep", keep)):
                return False
        return True

    def add(frame, x, y, keep=48, **extra):
        entry = {"f": frame, "x": int(x), "y": int(y), "keep": keep}
        if frame in COLLIDERS:
            entry["c"] = list(COLLIDERS[frame])
        if frame in LIGHTS:
            entry["l"] = list(LIGHTS[frame])
        entry.update(extra)
        entries.append(entry)

    def scatter(frames, count, path_margin, keep, attempts=4000, area=None, weights=None):
        placed = 0
        while placed < count and attempts > 0:
            attempts -= 1
            x, y = rng.uniform(0, W * T), rng.uniform(0, H * T)
            if area and not (area[0] <= x <= area[2] and area[1] <= y <= area[3]):
                continue
            if not ok(x, y, path_margin, keep):
                continue
            frame = rng.choices(frames, weights)[0] if weights else rng.choice(frames)
            add(frame, x, y, keep)
            placed += 1

    # estruturas fixas (ao longo do caminho e em pontos de interesse)
    add("arch", 800, 736, 90, **{"c2": [[-38, 24, 12], [38, 24, 12]]})
    for tx, ty in ((702, 462), (898, 462), (700, 700), (900, 700), (676, 394), (924, 394)):
        add("torch", tx, ty, 40)
    for tx, ty in ((384, 872), (320, 1004), (530, 782)):
        add("torch", tx, ty, 40)
    add("crystal_2", 640, 440, 60)
    add("crystal_0", 960, 470, 60)
    add("crystal_1", 668, 520, 40)
    add("crystal_0", 930, 700, 60)
    add("crystal_1", 470, 800, 50)
    add("crystal_2", 210, 720, 60)
    add("pillar_broken", 650, 790, 50)
    add("pillar_full", 560, 904, 50)
    add("wall_ruin", 940, 780, 60)
    add("wall_ruin", 600, 480, 60)
    add("barrel", 614, 860, 30)
    add("barrel", 600, 874, 30)
    add("stump", 456, 944, 30)
    add("log", 380, 760, 40)
    add("log", 1040, 520, 40)
    add("stake_0", 590, 826, 20)
    add("stake_1", 624, 836, 20)
    add("stake_0", 860, 760, 20)

    # lírios no rio (fora das colisões, só visuais)
    for lx in (120, 210, 330, 470, 560, 1000, 1120, 1260, 1400, 1500):
        add("lily_0" if hsh(lx, 1, 2) < 0.5 else "lily_1", lx, 610 + int(hsh(lx, 2, 3) * 40), 10, nolight=1)

    # floresta
    scatter(["tree_0", "tree_1", "tree_2", "tree_3", "tree_4"], 52, 34, 88, 9000)
    scatter(["tree_big"], 7, 54, 140, 3000)
    scatter(["pine_0", "pine_1"], 14, 36, 80, 3000)
    scatter(["rock_0", "rock_1", "rock_2"], 26, 26, 46, 4000, weights=[2, 3, 3])
    scatter(["bush_0", "bush_1", "bush_flower", "bush_flower_b"], 52, 22, 40, 6000)
    scatter(["fern_0", "fern_1"], 58, 14, 24, 6000)
    scatter(["grass_0", "grass_1"], 54, 8, 22, 6000)
    scatter(["crystal_1"], 3, 40, 150, 2000)

    for e in entries:
        e.pop("keep", None)
        e.pop("nolight", None)
    entries.sort(key=lambda e: (e["y"], e["x"]))
    with open(DECOR_PATH, "w") as fh:
        json.dump(entries, fh, separators=(",", ":"))
    with open(MAP_PATH, "w") as fh:
        json.dump(world, fh, separators=(",", ":"))
    count = {}
    for e in entries:
        count[e["f"]] = count.get(e["f"], 0) + 1
    print("decor:", len(entries), count)


if __name__ == "__main__":
    main()
