# Regalo-3 — Animación de Cumpleaños 🌻

Proyecto personal en Python que genera una animación de cumpleaños interactiva combinando **fuegos artificiales** (pygame) y un **girasol dibujado** (turtle), con texto personalizado según el nombre que ingrese la persona.

---

## Descripción general

El programa tiene 4 etapas que se ejecutan en secuencia:

1. **Input del nombre** — una ventana de `tkinter` pide que la persona escriba su nombre.
2. **Fuegos artificiales** — un cohete sube, explota en el centro, y las letras del mensaje `"Feliz Cumpleaños [NOMBRE]"` salen disparadas, flotan y se agrupan para formar el texto final. Implementado con **pygame**.
3. **Texto arcoíris animado** — se dibuja el título `"¡Feliz Cumpleaños, [nombre]!"` letra por letra con colores alternados, estrellas decorativas doradas y un subtítulo. Implementado con **turtle**.
4. **Girasol** — se dibuja un girasol a partir de regiones poligonales definidas en `resources/sunflowers.json`. Cada región tiene un color RGB y una lista de contornos.

---

## Estructura del proyecto

```
Regalo-3/
├── .github/
│   └── workflows/
│       └── build.yml          # Compila automáticamente .exe (Windows) y .app (Mac) en cada push
├── resources/
│   └── sunflowers.json        # Datos del girasol (regiones con color + contornos)
├── src/
│   └── regalo.py              # Script principal
├── requirements.txt           # pygame==2.6.1, pyinstaller==6.11.1
├── README.md
├── CLAUDE.md                  # Este archivo
└── .gitignore
```

---

## Stack técnico

- **Python 3.11**
- **pygame 2.6.1** — animación de fuegos artificiales (rendering 60 FPS, física de partículas).
- **turtle** (stdlib) — dibujo del texto arcoíris y del girasol.
- **tkinter** (stdlib) — ventana de diálogo para pedir el nombre.
- **PyInstaller 6.11.1** — empaquetado a `.exe` / `.app`.
- **GitHub Actions** — compilación automática multiplataforma.

---

## Arquitectura del script principal

El archivo `src/regalo.py` está organizado en bloques claramente separados:

1. **Guía de colores** (constantes al inicio del archivo) — todas las configuraciones de color están centralizadas aquí para facilitar personalización.
2. `resource_path(rel)` — helper que devuelve la ruta correcta de un recurso tanto en modo script como en modo ejecutable. Importante porque el script está en `src/` y los recursos en `resources/`.
3. `get_name()` — abre un `simpledialog.askstring` de tkinter.
4. `run_fireworks(nombre)` — ejecuta la animación pygame con 4 sub-estados: `COHETE`, `EXPLOSION`, `AGRUPAR`, `FINAL`.
5. `dibujar_estrella(t, x, y, size, color)` — helper para dibujar estrellas de 5 puntas con turtle.
6. `texto_arcoiris_animado(screen, nombre)` — dibuja el título animado, estrellas decorativas, línea segmentada y subtítulo.
7. `draw_sunflower(json_file, nombre)` — carga el JSON, normaliza coordenadas, y dibuja cada región con turtle.
8. Bloque `if __name__ == "__main__"` — orquesta las 3 llamadas en secuencia.

---

## Convenciones y patrones

- **Idioma:** el código y comentarios están en **español**. Los nombres de funciones también (`run_fireworks`, `draw_sunflower`, `get_name`).
- **Colores:** se definen como constantes globales en mayúsculas al inicio del archivo (ej. `COLOR_FONDO_FUEGOS`, `COLORES_LETRAS`). Se usan tuplas RGB `(r, g, b)` para pygame y strings hex `"#rrggbb"` o nombres para turtle.
- **Valores del JSON:** los colores del girasol a veces vienen con valores ligeramente fuera del rango 0-255, por lo que deben ser **clampeados** con `min(255, max(0, int(valor)))` antes de convertirlos a hexadecimal.
- **Coordenadas del girasol:** el JSON usa un sistema de coordenadas propio. El código calcula bounding box, centro, escala y offset para centrar el dibujo en la ventana turtle (800×800).
- **No hay tests** — es un proyecto personal de regalo, no hay suite de testing.

---

## Ejecución local

Desde la carpeta raíz del proyecto:
```bash
python src/regalo.py
```

> ⚠️ Debe ejecutarse desde la raíz, no desde dentro de `src/`, para que las rutas relativas a `resources/` funcionen correctamente.

---

## Compilación a ejecutable

### Local (Windows)
```bash
pyinstaller --onefile --windowed --name "FelizCumpleanos" --add-data "resources/sunflowers.json;resources" "src/regalo.py"
```

### Local (macOS / Linux)
```bash
pyinstaller --onefile --windowed --name "FelizCumpleanos" --add-data "resources/sunflowers.json:resources" "src/regalo.py"
```

> ⚠️ **Importante:** el separador en `--add-data` es **`;` en Windows** y **`:` en Mac/Linux**.

### Automática (GitHub Actions)
Cada `git push` a `main` dispara `.github/workflows/build.yml` que compila para Windows y Mac. Los ejecutables se pueden descargar desde la pestaña **Actions** del repositorio como artifacts.

---

## Carga de recursos (JSON del girasol)

Como el programa se compila a `.exe`, el archivo `sunflowers.json` se empaqueta **dentro** del ejecutable con `--add-data`. Para que el código lo encuentre tanto en modo script (`.py`) como en modo ejecutable (`.exe`), debe usarse la función `resource_path()`:

```python
import os, sys

def resource_path(rel):
    """Devuelve la ruta correcta del recurso en dev (.py) o en prod (.exe)."""
    if hasattr(sys, '_MEIPASS'):
        # Modo ejecutable: los recursos están extraídos en la carpeta temporal
        return os.path.join(sys._MEIPASS, rel)
    # Modo script: subir un nivel desde src/ para llegar a resources/
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)
```

Y la apertura del JSON debe ser:
```python
with open(resource_path("resources/sunflowers.json")) as f:
    regions = json.load(f)
```

`sys._MEIPASS` es la carpeta temporal donde PyInstaller extrae los recursos al ejecutar el `.exe`.

---

## Troubleshooting conocido

| Error | Causa | Solución |
|-------|-------|----------|
| `turtle.TurtleGraphicsError: bad color string: #xxxxxx` | Valores del JSON fuera del rango 0-255 | Clampear con `min(255, max(0, int(v)))` |
| `FileNotFoundError: resources/sunflowers.json` al ejecutar `.exe` | Falta `resource_path()` o falta `--add-data` al compilar | Aplicar ambos fixes |
| `FileNotFoundError` al ejecutar `python src/regalo.py` desde dentro de `src/` | `resource_path()` calcula la ruta relativa al archivo | Ejecutar desde la raíz del proyecto |
| Subtítulo invisible en la animación del girasol | Tamaño de fuente muy pequeño (ej. 7) | Subir a mínimo 13 |
| Ventana de consola negra aparece junto con el `.exe` | Falta `--windowed` en PyInstaller | Agregar flag `--windowed` |

---

## Cosas que NO cambiar sin consultar

- La estructura de carpetas `resources/` — si se mueve el JSON, hay que actualizar tanto el código (`resource_path`) como el `build.yml`.
- La ubicación `src/regalo.py` — si se mueve, hay que ajustar `resource_path()` (cuántos niveles sube con `os.path.dirname`) y las rutas en `build.yml`.
- El separador `;` vs `:` en `--add-data` según sistema operativo.
- El orden de ejecución: `get_name()` → `run_fireworks()` → `draw_sunflower()`. pygame y turtle no se llevan bien corriendo al mismo tiempo; deben ejecutarse secuencialmente.

---

## Contexto personal

El proyecto es un regalo de cumpleaños personalizado. El destinatario ingresa su nombre al inicio y la animación se adapta a él/ella. El subtítulo `"✨ by Antonio ✨"` firma el regalo.
