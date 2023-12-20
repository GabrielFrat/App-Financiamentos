import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from main import functions
import matplotlib.pyplot as plt
from tkinter import ttk
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class app:

    def ide(self):
        # starting
        root = tk.Tk()
        root.geometry("1380x720")
        root.configure(background="grey")
        root.title("Renda Variável")
        funcoes = functions()
        # construct ide
        # Create an object of tkinter ImageTk
        #img = ImageTk.PhotoImage(Image.open(r"C:\Users\gabri\OneDrive - XP Investimentos\Settima - BI\Python Scripts\4. Renda Variavel\Settima-Financiamentos\Imgs\settimaLogo.png").resize((300, 80)))
        #message = tk.Label(root, image=img, background="grey")
        #message.pack(anchor=tk.W)
        # Create a Label Widget to display the text or Image

    

        def terceira_sexta_feira_um_ano():
            hoje = datetime.today()
            datas_terceira_sexta = []

            for i in range(12): 

                novo_mes = (hoje.month + i - 1) % 12 + 1
                novo_ano = hoje.year + (hoje.month + i - 1) // 12

                primeiro_dia_do_mes = datetime(novo_ano, novo_mes, 1)
                dia_da_semana_primeiro_dia = primeiro_dia_do_mes.weekday()

                dias_para_terceira_sexta = (4 - dia_da_semana_primeiro_dia + 7) % 7 + 14

                terceira_sexta_feira = primeiro_dia_do_mes + timedelta(days=dias_para_terceira_sexta)

                datas_terceira_sexta.append(terceira_sexta_feira.date())

            return datas_terceira_sexta


        def configurar_scrollbar_y(*args):
            df_tree.yview(*args)

        def configurar_scrollbar_x(*args):
            df_tree.xview(*args)

        def clear_all():
            for item in df_tree.get_children():
                df_tree.delete(item)


        def execute():
            #try:
            cont = 0
            ativo = text_box.get()

            qtde = text_boxqtde.get()

            vencimento = text_Cbox.get()

            pm = text_PM.get()
            corretagem = text_corretagem.get()

            valor, cotacao = funcoes.get_option(ativo, qtde, vencimento, corretagem, pm)


            label_corretagem = Label(root, text="Cotação:", font="arial 16", background="grey")
            #label_qtde.pack(anchor=tk.W, padx=20, pady=10)
            label_corretagem.place(x=825, y=100)

            label_corretagem = Label(root, text=cotacao, font="arial 16", background="grey")
            #label_qtde.pack(anchor=tk.W, padx=20, pady=10)
            label_corretagem.place(x=825, y=130)
            
            df_tree["column"] = list(valor.columns)
            df_tree["show"] = "headings"

            for column in df_tree['column']:
                
                df_tree.column(str(column), anchor=CENTER, minwidth=10, width=120)
                df_tree.heading(column, text=column)
                

                #df_tree.columnconfigure(column, width=25)

            df_tree.tag_configure('oddrow', background="white")
            df_tree.tag_configure('evenrow', background="lightblue")
            df_rows = valor.to_numpy().tolist()
            my_tag="normal"
            for row in df_rows:
                df_tree.insert(parent="", index="end", values=row)

            
            funcoes.plotar_grafico(ativo, root, vencimento)
            
            
            #except:
            #   tk.messagebox.showwarning("Aviso", "Algo inesperado aconteceu. Se o erro persistir envie um email para gabriel.fratucci@settimainvest.com\n - Varifique o campo do ativo")

            


        label_ativo = Label(root, text="Ativo:", font="arial 16", background="grey")
        #label_ativo.pack(anchor=tk.W, padx=20, pady=10)
        label_ativo.place(x=25, y=100)
        
        text_box = tk.Entry(root, font="arial 18")
        #text_box.pack(anchor=tk.W, padx=20)
        text_box.place(x=25, y=130, width=150)
        

        label_qtde = Label(root, text="Quantidade:", font="arial 16", background="grey")
        #label_qtde.pack(anchor=tk.W, padx=20, pady=10)
        label_qtde.place(x=225, y=100)

        text_boxqtde = tk.Entry(root, font="arial 18")
        #text_boxqtde.pack(anchor=tk.W, padx=20)
        text_boxqtde.place(x=225, y=130, width=150)

        label_qtde = Label(root, text="Vencimento:", font="arial 16", background="grey")
        #label_qtde.pack(anchor=tk.W, padx=20, pady=10)
        label_qtde.place(x=425, y=100)
        listaMeses = terceira_sexta_feira_um_ano()
        text_Cbox = ttk.Combobox(root, font="arial 18", state="readonly", values=listaMeses)
        #text_boxqtde.pack(anchor=tk.W, padx=20)
        text_Cbox.place(x=425, y=130, width=150)

        label_corretagem = Label(root, text="Corretagem:", font="arial 16", background="grey")
        #label_qtde.pack(anchor=tk.W, padx=20, pady=10)
        label_corretagem.place(x=625, y=100)

        text_corretagem= tk.Entry(root, font="arial 18")
        #text_boxqtde.pack(anchor=tk.W, padx=20)
        text_corretagem.place(x=625, y=130, width=150)

        label_PM = Label(root, text="Preço Médio:", font="arial 16", background="grey")
        #label_qtde.pack(anchor=tk.W, padx=20, pady=10)
        label_PM.place(x=950, y=100)

        text_PM= tk.Entry(root, font="arial 18")
        #text_boxqtde.pack(anchor=tk.W, padx=20)
        text_PM.place(x=950, y=130, width=150)


        
        B = Button(root, text="Cotar Financiamento", fg="black", font="arial 12 bold", relief="raised", borderwidth=2, command=execute)
        B.place(x=25,y=180)
        #B.pack(anchor=tk.W, padx=20, pady=10)

        B = Button(root, text="Limpar Tabela", fg="black", font="arial 12 bold", relief="raised", borderwidth=2, command=clear_all)
        B.place(x=225,y=180)
        #B.pack(anchor=tk.W, padx=20, pady=10)

        df_tree = ttk.Treeview(root)
        df_tree.place(x=25, y=260, width=1800, height=350)
        scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=configurar_scrollbar_y)
        scrollbar_y.place(x=1825, y=260, height=350)

        scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=configurar_scrollbar_x)
        scrollbar_x.place(x=25, y=610, width=1800)

        style = ttk.Style()
        
        
        root.mainloop()

reading = app()
reading.ide()
