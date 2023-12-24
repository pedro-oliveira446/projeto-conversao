import tkinter as tk
import tkinter.ttk as ttk

class TabelaTransformador(tk.Frame):

    def __init__(self, master=None, dados=None):
        super().__init__(master)
        
        self.dados = dados

        self.cria_tabela()

    def cria_tabela(self):
        self.tabela = ttk.Treeview(self)
        self.tabela["columns"] = ["Dado", "Valor"]
        self.tabela.column("#0", width=0, stretch=False)
        self.tabela.column("Dado", width=100)
        self.tabela.column("Valor", width=200)

        self.tabela.heading("Dado", text="Dado")
        self.tabela.heading("Valor", text="Valor")
        
        for dado, valor in self.dados.items():
            self.tabela.insert("", "end", values=(dado, valor))

        self.tabela.pack()