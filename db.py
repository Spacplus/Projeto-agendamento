import sqlite3
from datetime import datetime

def conectar():
    conn = sqlite3.connect("clinica.db")
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    conn, cursor = conectar()
    
    #Tabela de clientes 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL,
            cpf TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
    ''')
    
    #Tabela de serviços 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servico TEXT NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT,
            duracao INTEGER,  -- duração em minutos, por exemplo
            categoria TEXT
        )
    ''')

    #Tabela de agendamentos 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            servico_id INTEGER,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (servico_id) REFERENCES servicos(id)
        )
    ''')

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    # Criação automática do usuário administrador
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", ("administrator@email.com",))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO usuarios (nome, cpf, email, senha)
            VALUES (?, ?, ?, ?)
        ''', ("Administrador", "00000000000", "administrator@email.com", "0000"))
        print("Usuário administrador criado automaticamente.")

    # Tabela de logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            data_hora TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def cadastrar_usuario(nome, cpf, email, senha):
    conn, cursor = conectar()
    try:
        cursor.execute("INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)",
                       (nome, cpf, email, senha))
        conn.commit()
        registrar_log(f"Cadastro de novo usuário: {email}")
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validar_login(email, senha):
    conn, cursor = conectar()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

def registrar_log(mensagem):
    """Registra logs simples com mensagem única."""
    conn, cursor = conectar()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        cursor.execute("INSERT INTO logs (mensagem, data_hora) VALUES (?, ?)", (mensagem, data_hora))
        conn.commit()
    except Exception as e:
        print(f"Erro ao registrar log: {e}")
    finally:
        conn.close()
