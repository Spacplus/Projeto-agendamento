import tkinter as tk
from db import conectar

def mostrar_logs(root):
    janela_logs = tk.Toplevel(root)
    janela_logs.title("Relatórios do Sistema")
    janela_logs.geometry("600x400")

    frame = tk.Frame(janela_logs)
    frame.pack(fill="both", expand=True)

    texto = tk.Text(frame, wrap="word")
    texto.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(texto)
    scrollbar.pack(side="right", fill="y")
    texto.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=texto.yview)

    try:
        conn, cursor = conectar()
        cursor.execute("SELECT data_hora, mensagem FROM logs ORDER BY id DESC")
        logs = cursor.fetchall()
        for data_hora, mensagem in logs:
            texto.insert("end", f"{data_hora} - {mensagem}\n")
    except Exception as e:
        texto.insert("end", f"Erro ao carregar logs: {e}")
    finally:
        conn.close()
