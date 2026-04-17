# 🌻 Regalo-3 — Animación de Cumpleaños

Una animación de cumpleaños personalizada hecha en Python. Combina fuegos artificiales animados con un girasol dibujado punto por punto, todo adaptado al nombre de la persona homenajeada.

---

## ✨ ¿Qué hace?

1. **Pide el nombre** de la persona al iniciar.
2. **Lanza fuegos artificiales** 🎆 — un cohete sube, explota en el centro y las letras del mensaje *"Feliz Cumpleaños [NOMBRE]"* salen disparadas, flotan y se agrupan formando el título.
3. **Dibuja un girasol** 🌻 con un título arcoíris animado letra por letra, estrellas doradas decorativas y un subtítulo personalizado.

---

## 🛠️ Tecnologías

- **Python 3.11**
- **pygame** — para los fuegos artificiales
- **turtle** — para el texto arcoíris y el girasol
- **tkinter** — para la ventana de ingreso del nombre
- **PyInstaller** — para generar los ejecutables
- **GitHub Actions** — compilación automática multiplataforma

---

## 📁 Estructura del proyecto

```
Regalo-3/
├── .github/
│   └── workflows/
│       └── build.yml          # Compila automáticamente .exe y .app
├── resources/
│   └── sunflowers.json        # Datos del girasol (regiones + colores)
├── src/
│   └── regalo.py              # Script principal
├── requirements.txt           # Dependencias
├── README.md
├── CLAUDE.md
└── .gitignore
```

---

## 🚀 Cómo ejecutar

### Opción 1 — Descargar el ejecutable (recomendado)

Ve a la pestaña **Actions** del repositorio, abre el último build exitoso y descarga el artifact correspondiente a tu sistema operativo:
- `FelizCumpleanos-Windows` → `.exe`
- `FelizCumpleanos-Mac` → `.app`

### Opción 2 — Ejecutar desde código

```bash
# Clonar el repositorio
git clone https://github.com/Anthonysc08/Regalo-3.git
cd Regalo-3

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar (desde la raíz del proyecto)
python src/regalo.py
```

> ⚠️ Ejecútalo desde la carpeta raíz `Regalo-3/`, no desde dentro de `src/`.

---

## 📦 Compilar manualmente a ejecutable

### Windows
```bash
pyinstaller --onefile --windowed --name "FelizCumpleanos" --add-data "resources/sunflowers.json;resources" "src/regalo.py"
```

### macOS / Linux
```bash
pyinstaller --onefile --windowed --name "FelizCumpleanos" --add-data "resources/sunflowers.json:resources" "src/regalo.py"
```

> ⚠️ El separador en `--add-data` es `;` en Windows y `:` en Mac/Linux.

El ejecutable se genera en la carpeta `dist/`.

---

## 🎨 Personalización

Todos los colores están centralizados al inicio de `src/regalo.py` en la sección **"GUÍA DE COLORES"**. Puedes modificar:

- Fondo de los fuegos artificiales
- Colores de las letras y chispas
- Fondo del girasol
- Colores del texto arcoíris
- Color de las estrellas y subtítulo

---

## 👤 Autor

Hecho con cariño por **Antonio** 🌻

---

## 📄 Licencia

Proyecto personal de uso libre.
