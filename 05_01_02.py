import tkinter as tk
from tkinter import simpledialog
import pygame
import math
import random
import sys
import turtle
import json
import os, sys

def resource_path(rel):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)
        return os.path.join(os.path.dirname(_file_), rel)
# ── Fuegos artificiales ───────────────────────────────────────
COLOR_FONDO_FUEGOS = (8, 8, 18)          # ← fondo de los fuegos artificiales

COLORES_LETRAS = [                        # ← colores de letras y chispas
    (255, 80,  80),   # rojo
    (80,  255, 80),   # verde
    (80,  160, 255),  # azul
    (255, 255, 80),   # amarillo
    (255, 150, 80),   # naranja
    (210, 80,  255),  # violeta
    (80,  255, 210),  # turquesa
]

# ── Animación del girasol ────────────────────────────────────
COLOR_FONDO_GIRASOL = "#1a0030"          # ← fondo del girasol
                                         

COLORES_TEXTO_ARCOIRIS = [               # ← letras de "Feliz Cumpleaños"
    "#ff4d4d",  # rojo
    "#ff9900",  # naranja
    "#ffff00",  # amarillo
    "#66ff66",  # verde
    "#00ccff",  # celeste
    "#cc66ff",  # violeta
    "#ff66cc",  # rosa
]

COLOR_SUBTITULO = "white"               # ← color del subtítulo
COLOR_ESTRELLAS = "gold"                # ← color de las estrellas decorativas


# ══════════════════════════════════════════════
#  PASO 1 — Pedir nombre
# ══════════════════════════════════════════════
def get_name():
    root = tk.Tk()
    root.withdraw()
    nombre = simpledialog.askstring("¡Bienvenida! 🌻", "Escribe tu nombre:")
    root.destroy()
    return nombre.strip() if nombre else "Linda"


# ══════════════════════════════════════════════
#  PASO 2 — Fuegos artificiales (pygame)
# ══════════════════════════════════════════════
def run_fireworks(nombre):
    pygame.init()
    W, H = 800, 800
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("🌻 Feliz Cumpleaños 🌻")
    clock = pygame.time.Clock()

    mensaje     = f"Feliz Cumpleaños {nombre.upper()}"
    fuente      = pygame.font.SysFont("Arial", 42, bold=True)
    fuente_hint = pygame.font.SysFont("Arial", 14)

    renders     = [fuente.render(c, True, (255, 255, 255)) for c in mensaje]
    ancho_total = sum(r.get_width() for r in renders)
    x_inicio    = (W - ancho_total) // 2
    y_centro    = H // 2

    targets, x = [], x_inicio
    for r in renders:
        targets.append((x + r.get_width() // 2, y_centro))
        x += r.get_width()

    class Letra:
        def __init__(self, char, color, tx, ty):
            self.char = char; self.color = color
            self.tx = tx; self.ty = ty
            self.x = float(W // 2); self.y = float(H // 2)
            ang = random.uniform(0, 2 * math.pi)
            vel = random.uniform(8, 20)
            self.vx = math.cos(ang) * vel
            self.vy = math.sin(ang) * vel

        def explotar(self):
            self.x += self.vx; self.y += self.vy
            self.vx *= 0.92;   self.vy *= 0.92

        def agrupar(self, p):
            e = 0.05 + p * 0.05
            self.x += (self.tx - self.x) * e
            self.y += (self.ty - self.y) * e

        def dibujar(self, surf):
            r = fuente.render(self.char, True, self.color)
            surf.blit(r, (int(self.x) - r.get_width()//2,
                         int(self.y) - r.get_height()//2))

    letras = [
        Letra(c, COLORES_LETRAS[i % len(COLORES_LETRAS)], tx, ty)
        for i, (c, (tx, ty)) in enumerate(zip(mensaje, targets))
    ]

    chispas = []

    def crear_chispas():
        for _ in range(80):
            ang = random.uniform(0, 2 * math.pi)
            spd = random.uniform(3, 14)
            chispas.append({
                'x': W//2, 'y': H//2,
                'vx': math.cos(ang)*spd, 'vy': math.sin(ang)*spd,
                'color': random.choice(COLORES_LETRAS),
                'vida': 1.0, 'radio': random.randint(2, 4),
            })

    def actualizar_chispas(decay=0.018):
        for s in chispas:
            s['x'] += s['vx']; s['y'] += s['vy']
            s['vx'] *= 0.91;   s['vy'] *= 0.91
            s['vida'] -= decay
        chispas[:] = [s for s in chispas if s['vida'] > 0]

    def dibujar_chispas():
        for s in chispas:
            r, g, b = s['color']; f = s['vida']
            pygame.draw.circle(screen,
                (int(r*f), int(g*f), int(b*f)),
                (int(s['x']), int(s['y'])), s['radio'])

    rastro = []
    T_COHETE, T_EXPLOSION, T_AGRUPAR, T_FINAL = 1600, 700, 2600, 3000
    estado = 'COHETE'
    t0 = pygame.time.get_ticks()
    running = True

    while running:
        clock.tick(60)
        ahora = pygame.time.get_ticks() - t0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and estado == 'FINAL':
                running = False

        screen.fill(COLOR_FONDO_FUEGOS)

        if estado == 'COHETE':
            prog     = min(ahora / T_COHETE, 1.0)
            cohete_y = int(H - 60 - (H - 60 - H//2) * prog)
            rastro.append((W//2 + random.randint(-2, 2), cohete_y + random.randint(2, 12)))
            if len(rastro) > 25: rastro.pop(0)
            for i, (rx, ry) in enumerate(rastro):
                b = int(200 * (i / len(rastro)))
                pygame.draw.circle(screen, (b, b, 180), (rx, ry), max(1, 4*i//len(rastro)))
            pygame.draw.circle(screen, (255, 255, 255), (W//2, cohete_y), 5)
            if prog >= 1.0:
                estado = 'EXPLOSION'; crear_chispas(); t0 = pygame.time.get_ticks()

        elif estado == 'EXPLOSION':
            prog = min(ahora / T_EXPLOSION, 1.0)
            actualizar_chispas(0.015); dibujar_chispas()
            for l in letras: l.explotar(); l.dibujar(screen)
            if prog >= 1.0:
                estado = 'AGRUPAR'; t0 = pygame.time.get_ticks()

        elif estado == 'AGRUPAR':
            prog = min(ahora / T_AGRUPAR, 1.0)
            actualizar_chispas(0.008); dibujar_chispas()
            for l in letras: l.agrupar(prog); l.dibujar(screen)
            if prog >= 1.0:
                estado = 'FINAL'; t0 = pygame.time.get_ticks()

        elif estado == 'FINAL':
            for l in letras: l.dibujar(screen)
            hint = fuente_hint.render(
                "Presiona cualquier tecla para continuar...", True, (120, 120, 120))
            screen.blit(hint, (W//2 - hint.get_width()//2, H - 45))
            if ahora >= T_FINAL: running = False

        pygame.display.flip()

    pygame.quit()


# ══════════════════════════════════════════════
#  PASO 3 — Texto animado arcoíris (turtle)
# ══════════════════════════════════════════════
def dibujar_estrella(t, x, y, size, color):
    """Estrella de 5 puntas rellena."""
    t.penup(); t.goto(x, y); t.pendown()
    t.color(color, color)
    t.begin_fill()
    for _ in range(5):
        t.forward(size); t.right(144)
    t.end_fill()


def texto_arcoiris_animado(screen, nombre):
    """
    Escribe 'Feliz Cumpleaños [nombre]' letra a letra
    con colores alternados + estrellas + subtítulo.
    """
    mensaje = f"¡Feliz Cumpleaños, {nombre}!"

    # ── Estrellas decorativas ──────────────────────────────────────────────────
    st = turtle.Turtle(); st.hideturtle(); st.speed(0); st.penup()
    posiciones = [
        (-360, 330, 9), (360, 330, 7), (-300, 315, 5),
        (300, 318, 6),  (0,   358, 5), (-180, 348, 7),
        (180, 348, 6),  (-90,  328, 4), (90,  328, 4),
    ]
    for ex, ey, sz in posiciones:
        dibujar_estrella(st, ex, ey, sz, COLOR_ESTRELLAS)
    screen.update()

    # ── Letras una a una ───────────────────────────────────────────────────────
    t = turtle.Turtle(); t.hideturtle(); t.speed(0); t.penup()

    # Calcular punto de inicio centrado (aprox 17px por carácter)
    ancho_total = len(mensaje) * 17
    x_actual    = -(ancho_total // 2)
    y_texto     = 305

    t.goto(x_actual, y_texto)
    for i, letra in enumerate(mensaje):
        t.color(COLORES_TEXTO_ARCOIRIS[i % len(COLORES_TEXTO_ARCOIRIS)])
        t.write(letra, font=("Arial", 26, "bold"))
        avance = 12 if letra == " " else 18
        x_actual += avance
        t.goto(x_actual, y_texto)
        screen.update()

    # ── Línea arcoíris debajo del título ──────────────────────────────────────
    linea = turtle.Turtle(); linea.hideturtle(); linea.speed(0); linea.penup()
    linea.pensize(3)
    segmento = (ancho_total + 20) // len(COLORES_TEXTO_ARCOIRIS)
    linea.goto(-(ancho_total // 2) - 10, y_texto - 6)
    linea.pendown()
    for color in COLORES_TEXTO_ARCOIRIS:
        linea.color(color); linea.forward(segmento + 4)
    screen.update()

    # ── Subtítulo ──────────────────────────────────────────────────────────────
    sub = turtle.Turtle(); sub.hideturtle(); sub.penup()
    sub.color(COLOR_SUBTITULO)
    sub.goto(0, 270)
    sub.write("✨   by Antonio   ✨",
              align="center", font=("Arial", 7, "italic"))
    screen.update()


# ══════════════════════════════════════════════
#  PASO 4 — Girasol (turtle)
# ══════════════════════════════════════════════
def draw_sunflower(json_file, nombre):
    screen = turtle.Screen()
    screen.bgcolor(COLOR_FONDO_GIRASOL)
    screen.setup(800, 800)
    screen.title("🌻 Feliz Cumpleaños 🌻")
    screen.tracer(0)

    texto_arcoiris_animado(screen, nombre)

    t = turtle.Turtle(); t.hideturtle(); t.speed(0)

    with open(resource_path(json_file)) as f:
        regions = json.load(f)

    all_points = [(p[0], p[1]) for r in regions for p in r['contour']]
    min_x = min(p[0] for p in all_points); max_x = max(p[0] for p in all_points)
    min_y = min(p[1] for p in all_points); max_y = max(p[1] for p in all_points)

    width    = max_x - min_x; height   = max_y - min_y
    scale    = min(540 / width, 540 / height)
    center_x = (min_x + max_x) / 2; center_y = (min_y + max_y) / 2
    offset_y = -50   
# baja el girasol para no tapar el texto
for region in regions:
    r_val = int(region['color'][0])
    g_val = int(region['color'][1])
    b_val = int(region['color'][2])
# si el color es negro o oscuro
if r_val < 15 and g_val < 15 and b_val < 15:
    color = COLOR_FONDO_GIRASOL
else:
    color = '#{:02x}{:02x}{:02}'.format(r_val, g_val, b_val)
    t.color(color, color)

points = region['contour']
t.begin_fill(); t.penup()
t.goto((points[0][0]-center_x)*scale, (center_y-points[0][1])*scale+offset_y)
       t.pendown()
       for point in points[1:]:
       t.goto((point[0]-center_x)*scale, (center_y-point[1])*scale+offset_y)
t.goto((points[0][0]-center_x)*scale, (center_y-points[0][1])*scale+offset_y)
t.end_fill()
screen.update()

screen.mainloop()


# ══════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════
if __name__ == "__main__":
    nombre = get_name()
    run_fireworks(nombre)
    draw_sunflower("resources/sunflowers.json", nombre)
