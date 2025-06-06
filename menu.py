from ast import main
import tkinter as tk
import clientes
import servicos
import agendamentos
from logs import registrar_log  

COR_FUNDO = "#e8f5e9"
COR_TEXTO = "#2e7d32"
COR_BOTAO = "#66bb6a"

def mostrar_menu(root, email=None, callback_login=None, frame=None):
    if frame:
        frame.destroy()

    registrar_log(f"Acesso ao menu principal: {email}")

    frame = tk.Frame(root, bg=COR_FUNDO)
    frame.pack(fill="both", expand=True)

    container = tk.Frame(frame, bg=COR_FUNDO)
    container.pack(expand=True)

    tk.Label(container, text="Menu Principal", font=("Helvetica", 18, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(20, 30))

    tk.Button(container, text="Clientes", width=25, bg=COR_BOTAO, fg="white",
              font=("Helvetica", 11), command=lambda: clientes.menu_clientes(root, frame)).pack(pady=5)

    tk.Button(container, text="Serviços", width=25, bg=COR_BOTAO, fg="white",
              font=("Helvetica", 11), command=lambda: servicos.menu_servicos(root, frame)).pack(pady=5)

    tk.Button(container, text="Agendamentos", width=25, bg=COR_BOTAO, fg="white",
              font=("Helvetica", 11), command=lambda: agendamentos.menu_agendamentos(root, frame)).pack(pady=5)

    if email == "administrator@email.com":
        tk.Button(container, text="Relatórios do Sistema", width=25, bg="#388e3c", fg="white",
                  font=("Helvetica", 11), command=lambda: mostrar_logs(root)).pack(pady=5)

    tk.Button(container, text="Sair", width=25, bg="#c62828", fg="white",
              font=("Helvetica", 11), command=lambda: callback_login().py).pack(pady=20)
    

def mostrar_logs(root):
    from logs import mostrar_tela_logs
    mostrar_tela_logs(root)