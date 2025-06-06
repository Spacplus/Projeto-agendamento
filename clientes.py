import tkinter as tk
from tkinter import messagebox
from db import conectar
from validations import validar_nome, validar_telefone, validar_email, validar_cpf, formatar_telefone
from logs import registrar_log

def validar_campos(nome, telefone, email, cpf, endereco):
    if not nome or not telefone or not email or not cpf or not endereco:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return False
    if not validar_nome(nome):
        messagebox.showerror("Erro", "Nome inválido")
        return False
    if not validar_telefone(telefone):
        messagebox.showerror("Erro", "Telefone no formato inválido")
        return False
    if not validar_email(email):
        messagebox.showerror("Erro", "Email inválido")
        return False
    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido")
        return False
    return True

def menu_clientes(root, frame_anterior=None):
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

    entry_nome = criar_label_entry("Nome:", 0)
    entry_telefone = criar_label_entry("Telefone:", 1)
    entry_email = criar_label_entry("Email:", 2)
    entry_cpf = criar_label_entry("CPF:", 3)
    entry_endereco = criar_label_entry("Endereço:", 4)

    cliente_em_edicao = None

    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_endereco.delete(0, tk.END)

    def cadastrar():
        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()
        cpf = entry_cpf.get().strip()
        endereco = entry_endereco.get().strip()

        if not validar_campos(nome, telefone, email, cpf, endereco):
            return

        telefone_formatado = formatar_telefone(telefone)

        try:
            conn, cursor = conectar()
            cursor.execute(
                "INSERT INTO clientes (nome, telefone, email, cpf, endereco) VALUES (?, ?, ?, ?, ?)",
                (nome, telefone_formatado, email, cpf, endereco)
            )
            conn.commit()
            conn.close()
            listar()
            limpar_campos()
            registrar_log(f"Cadastro: Cliente '{nome}' cadastrado.")
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao cadastrar", str(e))

    def editar():
        nonlocal cliente_em_edicao
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            dados = lista.get(index).split(" - ")
            cliente_em_edicao = dados[0]
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, dados[1])
            entry_telefone.delete(0, tk.END)
            entry_telefone.insert(0, dados[2])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, dados[3])
            entry_cpf.delete(0, tk.END)
            entry_cpf.insert(0, dados[4])
            entry_endereco.delete(0, tk.END)
            entry_endereco.insert(0, dados[5])
        else:
            messagebox.showerror("Erro", "Selecione um cliente para editar")

    def salvar_alteracao():
        nonlocal cliente_em_edicao
        if not cliente_em_edicao:
            messagebox.showerror("Erro", "Nenhum cliente está sendo editado")
            return

        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()
        cpf = entry_cpf.get().strip()
        endereco = entry_endereco.get().strip()

        if not validar_campos(nome, telefone, email, cpf, endereco):
            return

        telefone_formatado = formatar_telefone(telefone)

        try:
            conn, cursor = conectar()
            cursor.execute(
                "UPDATE clientes SET nome = ?, telefone = ?, email = ?, cpf = ?, endereco = ? WHERE id = ?",
                (nome, telefone_formatado, email, cpf, endereco, cliente_em_edicao)
            )
            conn.commit()
            conn.close()
            registrar_log(f"Edição: Cliente '{nome}' (ID {cliente_em_edicao}) atualizado.")
            cliente_em_edicao = None
            listar()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao salvar alterações", str(e))

    def excluir():
        selecionado = lista.curselection()
        if selecionado:
            index = selecionado[0]
            linha = lista.get(index)
            partes = linha.split(" - ")
            id_cliente = partes[0]
            nome_cliente = partes[1]
            confirmar = messagebox.askyesno("Confirmação", f"Excluir cliente '{nome_cliente}'?")
            if confirmar:
                try:
                    conn, cursor = conectar()
                    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
                    conn.commit()
                    conn.close()
                    listar()
                    limpar_campos()
                    registrar_log(f"Exclusão: Cliente '{nome_cliente}' (ID {id_cliente}) excluído.")
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro ao excluir", str(e))
        else:
            messagebox.showerror("Erro", "Selecione um cliente para excluir")

    def listar():
        lista.delete(0, tk.END)
        try:
            conn, cursor = conectar()
            cursor.execute("SELECT * FROM clientes")
            resultados = cursor.fetchall()
            if not resultados:
                lista.insert(tk.END, "Nenhum cliente encontrado.")
            else:
                for row in resultados:
                    id_, nome, telefone, email, cpf, endereco = row
                    lista.insert(tk.END, f"{id_} - {nome} - {telefone} - {email} - {cpf} - {endereco}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao listar clientes", str(e))

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