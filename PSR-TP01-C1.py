import threading
import time
import random
import queue
import tkinter as tk
from tkinter import scrolledtext

class Repositor(threading.Thread):
    def __init__(self, estante, nombre, log):
        super().__init__(name=nombre)
        self.estante = estante
        self.log = log

    def run(self):
        for i in range(1, 6):
            time.sleep(random.uniform(0.1, 0.5))
            producto = f"Caja-{i} de {self.name}"
            self.estante.put(producto)
            self.log(f"[{self.name}] Colocó: {producto}. (Disponibles: {self.estante.qsize()})")

class Consumidor(threading.Thread):
    def __init__(self, estante, nombre, log):
        super().__init__(name=nombre)
        self.estante = estante
        self.log = log

    def run(self):
        for _ in range(5):
            time.sleep(random.uniform(0.3, 0.9))
            producto = self.estante.get()
            self.log(f"[{self.name}] Retiró y compró: {producto}.")
            self.estante.task_done()

def iniciar():
    btn.config(state="disabled")
    txt.delete("1.0", "end")

    estante = queue.Queue(maxsize=5)

    def log(msg):
        txt.after(0, lambda: txt.insert("end", msg + "\n") or txt.see("end"))

    log("Abriendo el supermercado...")

    r1 = Repositor(estante, "Repositor-A", log)
    c1 = Consumidor(estante, "Cliente-X", log)

    r1.start()
    c1.start()

    def esperar():
        r1.join()
        c1.join()
        log("Supermercado cerrado.")
        btn.after(0, lambda: btn.config(state="normal"))

    threading.Thread(target=esperar, daemon=True).start()

root = tk.Tk()
root.title("Supermercado")

btn = tk.Button(root, text="Abrir Supermercado", command=iniciar)
btn.pack(pady=5)

txt = scrolledtext.ScrolledText(root, width=60, height=20)
txt.pack()

root.mainloop()