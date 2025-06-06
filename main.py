import tkinter as tk
from tkinter import messagebox
from db import criar_tabelas, cadastrar_usuario, validar_login
from logs import registrar_log
from menu import mostrar_menu

criar_tabelas()

# Configurações visuais padrão
BG_COLOR = "#f0f8f5"
FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 14, "bold")
ENTRY_WIDTH = 30

def tela_login():
    limpar_tela()

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="Login", font=TITLE_FONT, bg=BG_COLOR).pack(pady=(10, 20))

    tk.Label(frame, text="Email:", font=FONT, bg=BG_COLOR).pack(anchor='w')
    email_entry = tk.Entry(frame, font=FONT, width=ENTRY_WIDTH)
    email_entry.pack(pady=5)

    tk.Label(frame, text="Senha:", font=FONT, bg=BG_COLOR).pack(anchor='w')
    senha_entry = tk.Entry(frame, show="*", font=FONT, width=ENTRY_WIDTH)
    senha_entry.pack(pady=5)

    def entrar():
        email = email_entry.get()
        senha = senha_entry.get()

        if "@" not in email:
            messagebox.showerror("Erro", "Formato de Email inválido")
            return

        if validar_login(email, senha):
            registrar_log(f"Login realizado com sucesso: {email}")
            limpar_tela()
            mostrar_menu(root, email, tela_login)
        else:
            registrar_log(f"Tentativa de login inválida: {email}")
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    def ir_para_cadastro():
        tela_cadastro()

    botoes = tk.Frame(frame, bg=BG_COLOR)
    botoes.pack(pady=15)

    tk.Button(botoes, text="Fazer Cadastro", command=ir_para_cadastro, width=15, bg="#dfe", font=FONT).grid(row=0, column=0, padx=10)
    tk.Button(botoes, text="Entrar", command=entrar, width=15, bg="#cfc", font=FONT).grid(row=0, column=1, padx=10)

def tela_cadastro():
    limpar_tela()

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(expand=True)

    tk.Label(frame, text="Cadastro", font=TITLE_FONT, bg=BG_COLOR).pack(pady=(10, 20))

    def criar_campo(label_text):
        tk.Label(frame, text=label_text, font=FONT, bg=BG_COLOR).pack(anchor='w')
        entrada = tk.Entry(frame, font=FONT, width=ENTRY_WIDTH)
        entrada.pack(pady=5)
        return entrada

    nome_entry = criar_campo("Nome:")
    cpf_entry = criar_campo("CPF:")
    email_entry = criar_campo("Email:")
    senha_entry = criar_campo("Senha:")
    senha_entry.config(show="*")
    confirmar_entry = criar_campo("Confirmar Senha:")
    confirmar_entry.config(show="*")

    def validar_cpf(tecla):
        return tecla.isdigit() and len(cpf_entry.get()) < 11

    cpf_entry.config(validate="key", validatecommand=(root.register(validar_cpf), '%S'))

    def cadastrar():
        nome = nome_entry.get()
        cpf = cpf_entry.get()
        email = email_entry.get()
        senha = senha_entry.get()
        confirmar = confirmar_entry.get()

        if not email or "@" not in email:
            messagebox.showerror("Erro", "Formato de Email inválido")
            return

        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showerror("Erro", "CPF inválido. Deve conter 11 números.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        sucesso = cadastrar_usuario(nome, cpf, email, senha)
        if sucesso:
            registrar_log(f"Novo usuário cadastrado: {email}")
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
            tela_login()
        else:
            messagebox.showerror("Erro", "Email já cadastrado.")

    tk.Button(frame, text="Cadastrar", command=cadastrar, width=20, bg="#cfc", font=FONT).pack(pady=15)

def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Studio Sublime - Sistema de Agendamentos")
root.configure(bg=BG_COLOR)
root.geometry("1600x900")
root.resizable(True, False)
tela_login()
root.mainloop()