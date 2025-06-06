import tkinter as tk
from tkinter import messagebox
from db import conectar
from validations import validar_nome, validar_preco, validar_inteiro_positivo
from logs import registrar_log

def validar_campos(servico, preco, descricao, duracao, categoria):
    if not servico or not preco or not descricao or not duracao or not categoria:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return False
    if not validar_nome(servico):
        messagebox.showerror("Erro", "Nome do serviço inválido")
        return False
    try:
        preco_float = float(preco)
        if preco_float < 0:
            raise ValueError
    except:
        messagebox.showerror("Erro", "Preço inválido")
        return False
    if not validar_inteiro_positivo(duracao):
        messagebox.showerror("Erro", "Duração deve ser um número inteiro positivo")
        return False
    return True

def menu_servicos(root, frame_anterior=None):
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

    entry_servico = criar_label_entry("Serviço:", 0)
    entry_preco = criar_label_entry("Preço:", 1)
    entry_descricao = criar_label_entry("Descrição:", 2)
    entry_duracao = criar_label_entry("Duração (min):", 3)
    entry_categoria = criar_label_entry("Categoria:", 4)

    servico_em_edicao = None

    def limpar_campos():
        entry_servico.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_duracao.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)

    def cadastrar():
        servico = entry_servico.get().strip()
        preco = entry_preco.get().strip()
        descricao = entry_descricao.get().strip()
        duracao = entry_duracao.get().strip()
        categoria = entry_categoria.get().strip()

        if not validar_campos(servico, preco, descricao, duracao, categoria):
            return

        try:
            conn, cursor = conectar()
            cursor.execute(
                "INSERT INTO servicos (servico, preco, descricao, duracao, categoria) VALUES (?, ?, ?, ?, ?)",
                (servico, preco, descricao, int(duracao), categoria)
            )
            conn.commit()
            conn.close()
            listar()
            limpar_campos()
            registrar_log(f"Cadastro: Serviço '{servico}' cadastrado.")
            messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao cadastrar", str(e))

    def editar():
        nonlocal servico_em_edicao
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            dados = lista.get(index).split(" - ")
            servico_em_edicao = dados[0]
            entry_servico.delete(0, tk.END)
            entry_preco.delete(0, tk.END)
            entry_descricao.delete(0, tk.END)
            entry_duracao.delete(0, tk.END)
            entry_categoria.delete(0, tk.END)

            entry_servico.insert(0, dados[1])
            entry_preco.insert(0, dados[2])
            entry_descricao.insert(0, dados[3])
            entry_duracao.insert(0, dados[4])
            entry_categoria.insert(0, dados[5])
        else:
            messagebox.showerror("Erro", "Selecione um serviço para editar")

    def salvar_alteracao():
        nonlocal servico_em_edicao
        if not servico_em_edicao:
            messagebox.showerror("Erro", "Nenhum serviço está sendo editado")
            return

        servico = entry_servico.get().strip()
        preco = entry_preco.get().strip()
        descricao = entry_descricao.get().strip()
        duracao = entry_duracao.get().strip()
        categoria = entry_categoria.get().strip()

        if not validar_campos(servico, preco, descricao, duracao, categoria):
            return

        try:
            conn, cursor = conectar()
            cursor.execute(
                "UPDATE servicos SET servico = ?, preco = ?, descricao = ?, duracao = ?, categoria = ? WHERE id = ?",
                (servico, preco, descricao, int(duracao), categoria, servico_em_edicao)
            )
            conn.commit()
            conn.close()
            registrar_log(f"Edição: Serviço '{servico}' (ID {servico_em_edicao}) atualizado.")
            servico_em_edicao = None
            listar()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao salvar alterações", str(e))

    def excluir():
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            linha = lista.get(index)
            partes = linha.split(" - ")
            id_servico = partes[0]
            nome_servico = partes[1]
            confirmar = messagebox.askyesno("Confirmação", f"Excluir serviço '{nome_servico}'?")
            if confirmar:
                try:
                    conn, cursor = conectar()
                    cursor.execute("DELETE FROM servicos WHERE id = ?", (id_servico,))
                    conn.commit()
                    conn.close()
                    listar()
                    limpar_campos()
                    registrar_log(f"Exclusão: Serviço '{nome_servico}' (ID {id_servico}) excluído.")
                    messagebox.showinfo("Sucesso", "Serviço excluído com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro ao excluir", str(e))
        else:
            messagebox.showerror("Erro", "Selecione um serviço para excluir")

    def listar():
        lista.delete(0, tk.END)
        try:
            conn, cursor = conectar()
            cursor.execute("SELECT * FROM servicos")
            resultados = cursor.fetchall()
            if not resultados:
                lista.insert(tk.END, "Nenhum serviço encontrado.")
            else:
                for row in resultados:
                    id_, servico, preco, descricao, duracao, categoria = row
                    lista.insert(tk.END, f"{id_} - {servico} - {preco} - {descricao} - {duracao} - {categoria}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao listar serviços", str(e))

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