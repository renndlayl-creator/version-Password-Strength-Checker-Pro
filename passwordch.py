import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import string
import re
import csv
import math
from datetime import datetime

historial = []

# ---------------- FUNCIONES ----------------

def calcular_entropia(password):
    if not password:
        return 0

    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[^a-zA-Z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    return round(len(password) * math.log2(charset), 1)


def verificar_password():

    password = entrada.get()

    if not password:
        return

    puntuacion = 0
    consejos = []

    if len(password) >= 12:
        puntuacion += 1
    else:
        consejos.append("Usa al menos 12 caracteres")

    if re.search(r"[A-Z]", password):
        puntuacion += 1
    else:
        consejos.append("Agrega mayúsculas")

    if re.search(r"[a-z]", password):
        puntuacion += 1
    else:
        consejos.append("Agrega minúsculas")

    if re.search(r"\d", password):
        puntuacion += 1
    else:
        consejos.append("Agrega números")

    if re.search(r"[^a-zA-Z0-9]", password):
        puntuacion += 1
    else:
        consejos.append("Agrega símbolos")

    barra["value"] = puntuacion * 20

    if puntuacion <= 2:
        nivel = "Débil"
        resultado.config(text=nivel, fg="#ff5555")

    elif puntuacion <= 4:
        nivel = "Media"
        resultado.config(text=nivel, fg="#ffaa00")

    else:
        nivel = "Fuerte"
        resultado.config(text=nivel, fg="#55ff55")

    if consejos:
        sugerencias.config(text="\n".join(consejos))
    else:
        sugerencias.config(text="Excelente contraseña")

    bits = calcular_entropia(password)

    entropia_label.config(
        text=f"Entropía: {bits} bits"
    )

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    historial.append(
        (fecha, password, nivel)
    )

    actualizar_historial()


def generar_password():

    caracteres = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = "".join(
        random.choice(caracteres)
        for _ in range(16)
    )

    entrada.delete(0, tk.END)
    entrada.insert(0, password)


def actualizar_historial():

    lista.delete(0, tk.END)

    for fecha, pwd, nivel in historial[-20:]:

        lista.insert(
            tk.END,
            f"{fecha} | {nivel} | {pwd}"
        )


def copiar_password():

    ventana.clipboard_clear()
    ventana.clipboard_append(
        entrada.get()
    )

    messagebox.showinfo(
        "Copiado",
        "Contraseña copiada"
    )


def limpiar_historial():

    historial.clear()
    lista.delete(0, tk.END)


def mostrar_ocultar():

    if entrada.cget("show") == "*":
        entrada.config(show="")
    else:
        entrada.config(show="*")


def exportar_csv():

    if not historial:
        messagebox.showinfo(
            "Info",
            "No hay datos para exportar"
        )
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")]
    )

    if not archivo:
        return

    with open(
        archivo,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Fecha",
            "Contraseña",
            "Fortaleza"
        ])

        writer.writerows(historial)

    messagebox.showinfo(
        "Éxito",
        "CSV exportado"
    )

# ---------------- VENTANA ----------------

ventana = tk.Tk()

ventana.title(
    "Password Strength Checker Pro"
)

ventana.geometry("750x700")
ventana.resizable(False, False)

COLOR_BG = "#121212"
COLOR_PANEL = "#1e1e1e"
COLOR_PINK = "#ff4fa3"

ventana.configure(bg=COLOR_BG)

titulo = tk.Label(
    ventana,
    text="Password Strength Checker Pro",
    font=("Segoe UI", 18, "bold"),
    bg=COLOR_BG,
    fg=COLOR_PINK
)

titulo.pack(pady=15)

entrada = tk.Entry(
    ventana,
    width=40,
    font=("Consolas", 12),
    bg=COLOR_PANEL,
    fg="white",
    insertbackground="white",
    show="*"
)

entrada.pack(pady=10)

btn_frame = tk.Frame(
    ventana,
    bg=COLOR_BG
)

btn_frame.pack()

tk.Button(
    btn_frame,
    text="Analizar",
    command=verificar_password,
    bg=COLOR_PINK,
    fg="white"
).grid(row=0, column=0, padx=5)

tk.Button(
    btn_frame,
    text="Generar",
    command=generar_password,
    bg=COLOR_PINK,
    fg="white"
).grid(row=0, column=1, padx=5)

tk.Button(
    btn_frame,
    text="Copiar",
    command=copiar_password,
    bg=COLOR_PINK,
    fg="white"
).grid(row=0, column=2, padx=5)

tk.Button(
    btn_frame,
    text="Mostrar",
    command=mostrar_ocultar,
    bg=COLOR_PINK,
    fg="white"
).grid(row=0, column=3, padx=5)

barra = ttk.Progressbar(
    ventana,
    length=450,
    maximum=100
)

barra.pack(pady=15)

resultado = tk.Label(
    ventana,
    text="",
    font=("Segoe UI", 14, "bold"),
    bg=COLOR_BG
)

resultado.pack()

entropia_label = tk.Label(
    ventana,
    text="Entropía: 0 bits",
    bg=COLOR_BG,
    fg="#ffb6d9",
    font=("Segoe UI", 11)
)

entropia_label.pack()

sugerencias = tk.Label(
    ventana,
    text="",
    bg=COLOR_BG,
    fg="white",
    justify="left"
)

sugerencias.pack(pady=10)

tk.Label(
    ventana,
    text="Historial",
    bg=COLOR_BG,
    fg=COLOR_PINK,
    font=("Segoe UI", 13, "bold")
).pack()

lista = tk.Listbox(
    ventana,
    width=100,
    height=15,
    bg=COLOR_PANEL,
    fg="white"
)

lista.pack(pady=10)

tk.Button(
    ventana,
    text="Limpiar Historial",
    command=limpiar_historial,
    bg=COLOR_PINK,
    fg="white"
).pack(pady=5)

tk.Button(
    ventana,
    text="Exportar CSV",
    command=exportar_csv,
    bg=COLOR_PINK,
    fg="white"
).pack(pady=5)

ventana.mainloop()