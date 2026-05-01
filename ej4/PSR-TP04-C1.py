import tkinter as tk
import random
import threading
import time
from collections import deque

FILAS = 15
COLS = 15
CELDA = 40

def generar_laberinto(filas, cols):
    maze = [[random.choice([0, 0, 1]) for _ in range(cols)] for _ in range(filas)]
    maze[0][0] = 0          # entrada 1
    maze[0][cols - 1] = 0   # entrada 2
    maze[filas - 1][cols // 2] = 0  # salida
    return maze

COLORES_JUGADOR = ["#e74c3c", "#3498db"]
SALIDA = (FILAS - 1, COLS // 2)
ENTRADAS = [(0, 0), (0, COLS - 1)]

class Jugador(threading.Thread):
    def __init__(self, jugador_id, maze, canvas, entrada):
        super().__init__()
        self.jugador_id = jugador_id
        self.maze = maze
        self.canvas = canvas
        self.entrada = entrada
        self.color = COLORES_JUGADOR[jugador_id]
        self.daemon = True

    def run(self):
        self.bfs(self.entrada)

    def bfs(self, inicio):
        visitado = set()
        cola = deque()
        cola.append((inicio, [inicio]))
        visitado.add(inicio)

        while cola:
            (r, c), camino = cola.popleft()

            self.pintar(r, c)
            time.sleep(0.05)

            if (r, c) == SALIDA:
                for (pr, pc) in camino:
                    self.pintar(pr, pc, final=True)
                return

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < FILAS and 0 <= nc < COLS:
                    if (nr, nc) not in visitado and self.maze[nr][nc] == 0:
                        visitado.add((nr, nc))
                        cola.append(((nr, nc), camino + [(nr, nc)]))

    def pintar(self, r, c, final=False):
        x1 = c * CELDA + 2
        y1 = r * CELDA + 2
        x2 = x1 + CELDA - 4
        y2 = y1 + CELDA - 4
        color = self.color if not final else ("yellow" if self.jugador_id == 0 else "cyan")
        self.canvas.after(0, lambda x1=x1,y1=y1,x2=x2,y2=y2,col=color:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=col, outline=""))


def dibujar_laberinto(canvas, maze):
    for r in range(FILAS):
        for c in range(COLS):
            x1, y1 = c * CELDA, r * CELDA
            x2, y2 = x1 + CELDA, y1 + CELDA
            color = "#2c3e50" if maze[r][c] == 1 else "#ecf0f1"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#bdc3c7")

    for i, (r, c) in enumerate(ENTRADAS):
        x1, y1 = c * CELDA + 2, r * CELDA + 2
        canvas.create_rectangle(x1, y1, x1+CELDA-4, y1+CELDA-4,
                                 fill=COLORES_JUGADOR[i], outline="")

    r, c = SALIDA
    x1, y1 = c * CELDA + 2, r * CELDA + 2
    canvas.create_rectangle(x1, y1, x1+CELDA-4, y1+CELDA-4, fill="#2ecc71", outline="")
    canvas.create_text(c*CELDA + CELDA//2, r*CELDA + CELDA//2,
                       text="S", fill="white", font=("Arial", 12, "bold"))


def iniciar(canvas, maze):
    jugadores = [Jugador(i, maze, canvas, ENTRADAS[i]) for i in range(2)]
    for j in jugadores:
        j.start()


def main():
    maze = generar_laberinto(FILAS, COLS)

    ventana = tk.Tk()
    ventana.title("Laberinto con Threads")
    ventana.resizable(False, False)

    ancho = COLS * CELDA
    alto  = FILAS * CELDA

    canvas = tk.Canvas(ventana, width=ancho, height=alto, bg="#ecf0f1")
    canvas.pack()

    frame = tk.Frame(ventana)
    frame.pack(pady=4)
    tk.Label(frame, text="■ Jugador 1", fg="#e74c3c", font=("Arial", 11)).pack(side="left", padx=10)
    tk.Label(frame, text="■ Jugador 2", fg="#3498db", font=("Arial", 11)).pack(side="left", padx=10)
    tk.Label(frame, text="■ Salida",    fg="#2ecc71", font=("Arial", 11)).pack(side="left", padx=10)

    dibujar_laberinto(canvas, maze)

    btn = tk.Button(ventana, text="Iniciar busqueda",
                    command=lambda: iniciar(canvas, maze),
                    font=("Arial", 11), bg="#3498db", fg="white",
                    relief="flat", padx=10, pady=4)
    btn.pack(pady=6)

    ventana.mainloop()

if __name__ == "__main__":
    main()