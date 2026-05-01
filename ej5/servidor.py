import socket
import threading
from tkinter import *
from tkinter import messagebox
from functools import partial

HOST = '0.0.0.0'
PORT = 9999

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((HOST, PORT))
server_sock.listen(1)

conn = None          
mi_turno = [True]   

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
    global conn
    if not mi_turno[0]:
        messagebox.showwarning('Espera', 'No es tu turno')
        return
    if btn_tablero[f][c].cget('state') == 'disabled':
        messagebox.showerror('Error', 'Casilla ocupada')
        return

    btn_tablero[f][c].configure(text='X', state='disabled', fg='#e74c3c')
    num_tablero[f][c] = 'X'
    mi_turno[0] = False
    lbl_turno.configure(text='Turno: O (esperando...)')

    conn.sendall(f'{f},{c}'.encode())

    if verifica_jugada(num_tablero, 'X'):
        deshabilitar_todo()
        messagebox.showinfo('GANADOR', '¡Ganaste! (X)')
        return
    if tablero_lleno():
        messagebox.showinfo('Empate', '¡Empate!')

def recibir_jugadas():
    global conn
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            f, c = map(int, data.split(','))
            app.after(0, lambda f=f, c=c: aplicar_jugada_remota(f, c))
        except:
            break

def aplicar_jugada_remota(f, c):
    btn_tablero[f][c].configure(text='O', state='disabled', fg='#3498db')
    num_tablero[f][c] = 'O'
    mi_turno[0] = True
    lbl_turno.configure(text='Turno: X (vos)')

    if verifica_jugada(num_tablero, 'O'):
        deshabilitar_todo()
        messagebox.showinfo('PERDISTE', 'Ganó O')
        return
    if tablero_lleno():
        messagebox.showinfo('Empate', '¡Empate!')

def esperar_conexion():
    global conn
    lbl_estado.configure(text='Esperando cliente...')
    conn, addr = server_sock.accept()
    lbl_estado.configure(text=f'Conectado: {addr[0]}')
    lbl_turno.configure(text='Turno: X (vos)')
    for f in range(3):
        for c in range(3):
            btn_tablero[f][c].configure(state='normal')
    threading.Thread(target=recibir_jugadas, daemon=True).start()

app = Tk()
app.title('Ta-Te-Ti  —  Servidor (X)')
app.geometry('400x480')
app.configure(bg='#1a1a2e')
app.resizable(False, False)

Label(app, text='TA-TE-TI', font=('Courier', 22, 'bold'),
      bg='#1a1a2e', fg='#e94560').pack(pady=(16, 2))

Label(app, text='Sos el jugador  X', font=('Courier', 11),
      bg='#1a1a2e', fg='#a0a0c0').pack()

lbl_estado = Label(app, text=f'Escuchando en puerto {PORT}...',
                   font=('Courier', 10), bg='#1a1a2e', fg='#f5a623')
lbl_estado.pack(pady=4)

lbl_turno = Label(app, text='—', font=('Courier', 11, 'bold'),
                  bg='#1a1a2e', fg='#ffffff')
lbl_turno.pack(pady=2)

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
                     state='disabled',
                     command=partial(clk_tablero, f, c))
        btn.grid(row=f, column=c, padx=4, pady=4, ipadx=10, ipady=10)
        btn_tablero[f][c] = btn

threading.Thread(target=esperar_conexion, daemon=True).start()

app.mainloop()