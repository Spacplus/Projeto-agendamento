from db import conectar
import tkinter as tk

def registrar_log(mensagem):
    try:
        conn, cursor = conectar()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                mensagem TEXT NOT NULL
            )
        """)
        cursor.execute("""
            INSERT INTO logs (data_hora, mensagem)
            VALUES (datetime('now'), ?)
        """, (mensagem,))
        conn.commit()
    except Exception as e:
        print(f"Erro ao registrar log: {e}")
    finally:
        conn.close()

def mostrar_tela_logs(root):
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Relatórios de Logs")
    nova_janela.geometry("500x400")

    tk.Label(nova_janela, text="Relatórios de Logs", font=("Helvetica", 14, "bold")).pack(pady=10)

    texto_logs = tk.Text(nova_janela, wrap="word", height=20)
    texto_logs.pack(padx=10, pady=10, fill="both", expand=True)

    try:
        conn, cursor = conectar()
        cursor.execute("SELECT mensagem, data_hora FROM logs ORDER BY id DESC")
        logs = cursor.fetchall()
    except Exception as e:
        texto_logs.insert("end", f"Erro ao carregar logs: {e}")
        logs = []
    finally:
        conn.close()

    for mensagem, data_hora in logs:
        texto_logs.insert("end", f"[{data_hora}] {mensagem}\n")

    texto_logs.config(state="disabled")
