"""Gera light.png: máscara de luz radial com alpha em degraus dithered (usada com erase no overlay de escuridão).

Uso: python3 gen_light.py [saida.png]
"""
import os
import sys

from PIL import Image

from pxlib import bay

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "public", "assets", "sprites", "light.png")
SIZE = 256
STEPS = 7


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    c = SIZE / 2
    for y in range(SIZE):
        for x in range(SIZE):
            d = (((x + 0.5 - c) ** 2 + (y + 0.5 - c) ** 2) ** 0.5) / c
            if d >= 1:
                continue
            f = (1 - d) ** 1.6
            level = f * STEPS
            q = int(level) + (1 if (level - int(level)) > bay(x // 2, y // 2) else 0)
            img.putpixel((x, y), (255, 255, 255, min(255, int(q / STEPS * 255))))
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    img.save(OUT)
    print("light ->", OUT)


if __name__ == "__main__":
    main()
