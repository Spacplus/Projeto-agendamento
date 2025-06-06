import tkinter as tk
from tkinter import messagebox
from db import conectar
from datetime import datetime

def menu_agendamentos(root, frame_anterior):
    if frame_anterior:
        frame_anterior.destroy()

    # Cores do tema
    verde_claro = "#d0f0c0"
    verde_escuro = "#006400"
    branco = "#ffffff"
    cinza = "#f0f0f0"

    frame = tk.Frame(root, bg=verde_claro)
    frame.pack(fill="both", expand=True)

    container = tk.Frame(frame, bg=verde_claro)
    container.place(relx=0.5, rely=0.05, anchor="n")

    def criar_label_entry(texto, linha):
        tk.Label(container, text=texto, bg=verde_claro, fg="black", font=("Arial", 11, "bold")).grid(row=linha, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(container, font=("Arial", 11), bg=branco)
        entrada.grid(row=linha, column=1, padx=10, pady=5)
        return entrada

    entry_id_cliente = criar_label_entry("ID Cliente:", 0)
    entry_id_servico = criar_label_entry("ID Serviço:", 1)
    entry_data = criar_label_entry("Data (DD/MM/AAAA):", 2)
    entry_hora = criar_label_entry("Horário (HH:MM):", 3)
    entry_observacoes = criar_label_entry("Observações:", 4)

    agendamento_em_edicao = None
    ids_clientes = {}
    ids_servicos = {}

    # Mesma lógica nas funções abaixo — apenas aparência alterada nas Listbox e botões

    def cadastrar():
        id_cliente = entry_id_cliente.get()
        id_servico = entry_id_servico.get()
        data = entry_data.get()
        hora = entry_hora.get()
        observacoes = entry_observacoes.get()

        if id_cliente and id_servico and data and hora:
            try:
                data_convertida = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                conn, cursor = conectar()
                cursor.execute(
                    "INSERT INTO agendamentos (cliente_id, servico_id, data, hora, observacoes) VALUES (?, ?, ?, ?, ?)",
                    (id_cliente, id_servico, data_convertida, hora, observacoes)
                )
                conn.commit()
                conn.close()
                listar()
                entry_id_cliente.delete(0, tk.END)
                entry_id_servico.delete(0, tk.END)
                entry_data.delete(0, tk.END)
                entry_hora.delete(0, tk.END)
                entry_observacoes.delete(0, tk.END)
                messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao cadastrar", str(e))
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")

    def editar():
        nonlocal agendamento_em_edicao, ids_clientes, ids_servicos
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            linha = lista.get(index)

            try:
                partes = linha.split(" - ")
                agendamento_em_edicao = int(partes[0])

                dados = partes[1].split(", ")
                cliente = dados[0].replace("Cliente: ", "")
                servico = dados[1].replace("Serviço: ", "")
                data = dados[2].replace("Data: ", "")
                hora = dados[3].replace("Horário: ", "")
                obs = dados[4].replace("Observações: ", "")

                entry_id_cliente.delete(0, tk.END)
                entry_id_cliente.insert(0, ids_clientes.get(cliente, cliente))
                entry_id_servico.delete(0, tk.END)
                entry_id_servico.insert(0, ids_servicos.get(servico, servico))
                entry_data.delete(0, tk.END)
                entry_data.insert(0, data)
                entry_hora.delete(0, tk.END)
                entry_hora.insert(0, hora)
                entry_observacoes.delete(0, tk.END)
                entry_observacoes.insert(0, obs)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao obter os dados do agendamento: {str(e)}")
        else:
            messagebox.showerror("Erro", "Selecione um agendamento para editar.")

    def salvar_alteracao():
        nonlocal agendamento_em_edicao
        id_cliente = entry_id_cliente.get()
        id_servico = entry_id_servico.get()
        data = entry_data.get()
        hora = entry_hora.get()
        observacoes = entry_observacoes.get()

        if agendamento_em_edicao is None:
            messagebox.showwarning("Aviso", "Nenhum agendamento em edição.")
            return

        if id_cliente and id_servico and data and hora:
            try:
                data_convertida = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")

                conn, cursor = conectar()

                cursor.execute("SELECT id FROM clientes WHERE id = ?", (id_cliente,))
                if cursor.fetchone() is None:
                    messagebox.showerror("Erro", f"Cliente com ID {id_cliente} não encontrado.")
                    conn.close()
                    return

                cursor.execute("SELECT id FROM servicos WHERE id = ?", (id_servico,))
                if cursor.fetchone() is None:
                    messagebox.showerror("Erro", f"Serviço com ID {id_servico} não encontrado.")
                    conn.close()
                    return

                cursor.execute("""UPDATE agendamentos 
                    SET cliente_id = ?, servico_id = ?, data = ?, hora = ?, observacoes = ?
                    WHERE id = ?""",
                    (id_cliente, id_servico, data_convertida, hora, observacoes, agendamento_em_edicao))

                conn.commit()
                conn.close()
                listar()

                entry_id_cliente.delete(0, tk.END)
                entry_id_servico.delete(0, tk.END)
                entry_data.delete(0, tk.END)
                entry_hora.delete(0, tk.END)
                entry_observacoes.delete(0, tk.END)

                agendamento_em_edicao = None
                messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro ao salvar alterações", str(e))
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")

    def excluir():
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            id_agendamento = lista.get(index).split(" - ")[0]

            confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este agendamento?")
            if confirmar:
                try:
                    conn, cursor = conectar()
                    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (id_agendamento,))
                    conn.commit()
                    conn.close()
                    listar()
                    entry_id_cliente.delete(0, tk.END)
                    entry_id_servico.delete(0, tk.END)
                    entry_data.delete(0, tk.END)
                    entry_hora.delete(0, tk.END)
                    entry_observacoes.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Erro ao excluir", str(e))
        else:
            messagebox.showerror("Erro", "Selecione um agendamento para excluir")

    def listar():
        nonlocal ids_clientes, ids_servicos
        lista.delete(0, tk.END)
        ids_clientes = {}
        ids_servicos = {}
        conn = None
        try:
            conn, cursor = conectar()
            cursor.execute("""
                SELECT a.id, c.id, c.nome, s.id, s.servico, a.data, a.hora, a.observacoes
                FROM agendamentos a
                JOIN clientes c ON a.cliente_id = c.id
                JOIN servicos s ON a.servico_id = s.id
            """)
            resultados = cursor.fetchall()
            if not resultados:
                lista.insert(tk.END, "Nenhum agendamento encontrado.")
            else:
                for row in resultados:
                    ag_id, cli_id, cli_nome, srv_id, srv_nome, data, hora, obs = row
                    ids_clientes[cli_nome] = cli_id
                    ids_servicos[srv_nome] = srv_id
                    data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                    texto = f"{ag_id} - Cliente: {cli_nome}, Serviço: {srv_nome}, Data: {data_formatada}, Horário: {hora}, Observações: {obs}"
                    lista.insert(tk.END, texto)
        except Exception as e:
            messagebox.showerror("Erro ao listar agendamentos", str(e))
        finally:
            if conn:
                conn.close()

    botoes_frame = tk.Frame(frame, bg=verde_claro)
    botoes_frame.place(relx=0.5, rely=0.43, anchor="n")

    def botao(texto, comando, coluna):
        tk.Button(botoes_frame, text=texto, command=comando, width=18, bg=verde_escuro, fg="white",
                  font=("Arial", 10, "bold"), relief="raised", bd=2).grid(row=0, column=coluna, padx=5, pady=5)

    botao("Cadastrar", cadastrar, 0)
    botao("Editar", editar, 1)
    botao("Salvar Alterações", salvar_alteracao, 2)
    botao("Excluir", excluir, 3)

    lista = tk.Listbox(frame, width=120, height=10, bg=branco, fg="black", font=("Arial", 10))
    lista.place(relx=0.5, rely=0.6, anchor="n")

    def voltar():
        from menu import mostrar_menu
        frame.destroy()
        mostrar_menu(root)

    tk.Button(frame, text="Voltar ao Menu", command=voltar, bg=cinza, font=("Arial", 10, "bold")).place(relx=0.5, rely=0.95, anchor="s")

    listar()