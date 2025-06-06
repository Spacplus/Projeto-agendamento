import re
from datetime import datetime
from tkinter import messagebox

def validar_nome(nome):
    return len(nome.strip().split()) >= 2

def validar_telefone(telefone):
    telefone_limpo = re.sub(r'\D', '', telefone)
    return len(telefone_limpo) in [10, 11]

def formatar_telefone(telefone):
    telefone_limpo = re.sub(r'\D', '', telefone)
    if len(telefone_limpo) == 10:
        return f"({telefone_limpo[:2]}){telefone_limpo[2:6]}-{telefone_limpo[6:]}"
    elif len(telefone_limpo) == 11:
        return f"({telefone_limpo[:2]}){telefone_limpo[2:7]}-{telefone_limpo[7:]}"
    return telefone

def validar_email(email):
    return re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email)

def validar_data(data):
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y")
        return data_formatada.date() >= datetime.now().date()
    except ValueError:
        return False

def validar_hora(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

def validar_campos(nome, telefone, email):
    if not nome or not telefone or not email:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return False
    if not validar_nome(nome):
        messagebox.showerror("Erro", "Informe o nome completo")
        return False
    if not validar_telefone(telefone):
        messagebox.showerror("Erro", "Telefone inválido. Use DDD + número.")
        return False
    if not validar_email(email):
        messagebox.showerror("Erro", "Email inválido")
        return False
    return True

def limpar_campos(*entradas):
    for entrada in entradas:
        entrada.delete(0, "end")

def validar_cpf(cpf):
    cpf_limpo = re.sub(r'\D', '', cpf)  
    return len(cpf_limpo) == 11 and cpf_limpo.isdigit()

def validar_preco(preco):
    try:
        valor = float(preco)
        return valor >= 0
    except ValueError:
        return False

def validar_inteiro_positivo(valor):
    try:
        numero = int(valor)
        return numero > 0
    except ValueError:
        return False

