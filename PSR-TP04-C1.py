import tkinter as tk
import random

root = tk.Tk()
root.geometry("1000x1000")


matlab = []

for f in range(50):
    fila = [None] * 50
    matlab.append(fila)

for f in range(50):
    for c in range(50):
        matlab[f][c] = random.randint(0, 1)

for e in range(10):
    c = random.randint(0, 49)
    if matlab[0][c] != 0:
        matlab[0][c] = 0

matlbl = []
for f in range(50):
    matlbl.append([None] * 50)

for f in range(50):
    for c in range(50):

        if matlab[f][c] == 1:
            bg = 'white'
            fg = 'black'
        else:
            bg = 'black'
            fg = 'white'

        matlbl[f][c] = tk.Label(
            root,
            text=str(matlab[f][c]),
            bg=bg,
            fg=fg
        )

        matlbl[f][c].place(x=c*20, y=f*20, width=20, height=20)

root.mainloop()