
## Tomando el ejemplo de la clase, convertir la salida de texto en una salida gráfica, donde la pista esté representada por un vector,
## en la que compitan tres animales representados por una imagen y su nombre y se vayan desplazando sobre la pista. Al finalizar mostrar el podio.

import threading
import random
import time
import tkinter as tk

PASOS = 50
ANCHO_PISTA = 600

animales = ["Liebre", "Tortuga", "Puma"]

class Animal(threading.Thread):
    def __init__(self, nombre, callback_paso, callback_fin):
        super().__init__(name=nombre)
        self.callback_paso = callback_paso
        self.callback_fin = callback_fin

    def run(self):
        for _ in range(PASOS):
            time.sleep(random.uniform(0.05, 0.3))
            self.callback_paso(self.name)
        self.callback_fin(self.name)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Carrera de Animales")
        self.resizable(False, False)
        self.podio = []
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Carrera de Animales", font=("Arial", 14, "bold")).pack(pady=10)

        self.letras = {}

        for nombre in animales:
            fila = tk.Frame(self)
            fila.pack(fill="x", padx=20, pady=4)

            tk.Label(fila, text=nombre, width=10, anchor="w").pack(side="left")

            canvas = tk.Canvas(fila, width=ANCHO_PISTA, height=30,
                                highlightthickness=1, highlightbackground="black", bg="white")
            canvas.pack(side="left")

            
            letra = canvas.create_text(0, 15, text=nombre[0], anchor="w", font=("Arial", 14, "bold"))
            self.letras[nombre] = (canvas, letra)

        self.btn = tk.Button(self, text="Iniciar", command=self._iniciar)
        self.btn.pack(pady=10)

    def _iniciar(self):
        self.btn.config(state="disabled")
        self.podio = []

        for nombre, (canvas, letra) in self.letras.items():
            canvas.coords(letra, 0, 15)

        hilos = [Animal(n, self._actualizar, self._fin) for n in animales]
        for h in hilos:
            h.start()

        def esperar():
            for h in hilos:
                h.join()
            self.after(0, self._mostrar_podio)

        threading.Thread(target=esperar, daemon=True).start()

    def _actualizar(self, nombre):
        def _draw():
            canvas, letra = self.letras[nombre]
            x = canvas.coords(letra)[0] + (ANCHO_PISTA / PASOS)
            canvas.coords(letra, x, 15)
        self.after(0, _draw)

    def _fin(self, nombre):
        self.podio.append(nombre)

    def _mostrar_podio(self):
        win = tk.Toplevel(self)
        win.title("Podio")

        tk.Label(win, text="Podio Final").pack(pady=8)

        puestos = ["1ro", "2do", "3ro"]
        for i, nombre in enumerate(self.podio):
            tk.Label(win, text=f"{puestos[i]}: {nombre}").pack()

        tk.Button(win, text="Cerrar", command=lambda: [win.destroy(), self.btn.config(state="normal")]).pack(pady=8)


if __name__ == "__main__":
    App().mainloop()