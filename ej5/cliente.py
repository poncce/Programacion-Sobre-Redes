import socket
import threading
from tkinter import *
from tkinter import messagebox
from functools import partial

HOST = '127.0.0.1'   
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

mi_turno = [False]   

btn_tablero = [[None]*3 for _ in range(3)]
num_tablero = [[None]*3 for _ in range(3)]

def verifica_jugada(mat, jugador):
    fils = mat
    cols = [[mat[f][c] for f in range(3)] for c in range(3)]
    dia1 = [mat[i][i] for i in range(3)]
    dia2 = [mat[i][2-i] for i in range(3)]
    ganadora = fils + cols + [dia1, dia2]
    return [jugador]*3 in ganadora

def tablero_lleno():
    return all(num_tablero[f][c] is not None for f in range(3) for c in range(3))

def deshabilitar_todo():
    for f in range(3):
        for c in range(3):
            btn_tablero[f][c].configure(state='disabled')

def clk_tablero(f, c):
    if not mi_turno[0]:
        messagebox.showwarning('Espera', 'No es tu turno')
        return
    if btn_tablero[f][c].cget('state') == 'disabled':
        messagebox.showerror('Error', 'Casilla ocupada')
        return

    btn_tablero[f][c].configure(text='O', state='disabled', fg='#3498db')
    num_tablero[f][c] = 'O'
    mi_turno[0] = False
    lbl_turno.configure(text='Turno: X (esperando...)')

    sock.sendall(f'{f},{c}'.encode())

    if verifica_jugada(num_tablero, 'O'):
        deshabilitar_todo()
        messagebox.showinfo('GANADOR', '¡Ganaste! (O)')
        return
    if tablero_lleno():
        messagebox.showinfo('Empate', '¡Empate!')

def recibir_jugadas():
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            f, c = map(int, data.split(','))
            app.after(0, lambda f=f, c=c: aplicar_jugada_remota(f, c))
        except:
            break

def aplicar_jugada_remota(f, c):
    btn_tablero[f][c].configure(text='X', state='disabled', fg='#e74c3c')
    num_tablero[f][c] = 'X'
    mi_turno[0] = True
    lbl_turno.configure(text='Turno: O (vos)')

    if verifica_jugada(num_tablero, 'X'):
        deshabilitar_todo()
        messagebox.showinfo('PERDISTE', 'Ganó X')
        return
    if tablero_lleno():
        messagebox.showinfo('Empate', '¡Empate!')

app = Tk()
app.title('Ta-Te-Ti  —  Cliente (O)')
app.geometry('400x480')
app.configure(bg='#1a1a2e')
app.resizable(False, False)

Label(app, text='TA-TE-TI', font=('Courier', 22, 'bold'),
      bg='#1a1a2e', fg='#e94560').pack(pady=(16, 2))

Label(app, text='Sos el jugador  O', font=('Courier', 11),
      bg='#1a1a2e', fg='#a0a0c0').pack()

lbl_turno = Label(app, text='Turno: X (esperando...)', font=('Courier', 11, 'bold'),
                  bg='#1a1a2e', fg='#ffffff')
lbl_turno.pack(pady=8)

frame = Frame(app, bg='#1a1a2e')
frame.pack(pady=10)

for f in range(3):
    for c in range(3):
        btn = Button(frame, text='', font=('Courier', 28, 'bold'),
                     width=3, height=1,
                     bg='#16213e', fg='white',
                     activebackground='#0f3460',
                     disabledforeground='white',
                     relief='flat', bd=0,
                     command=partial(clk_tablero, f, c))
        btn.grid(row=f, column=c, padx=4, pady=4, ipadx=10, ipady=10)
        btn_tablero[f][c] = btn

threading.Thread(target=recibir_jugadas, daemon=True).start()

app.mainloop()