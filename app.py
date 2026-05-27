import tkinter as tk
from tkinter import filedialog
from tkinter import font
from column_read import filtrar_arquivo
import csv
import threading

input_file = ""  # global

def thread_arquivo():
    thread = threading.Thread(target=selecionar_arquivo)
    thread.start()

# função para ler arquivos armazenados no computador
def selecionar_arquivo():
    global input_file

    input = filedialog.askopenfilename(
        title="Selecione um arquivo csv",
        filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
    )
    
    # se o arquivo for legivel pelo código:
    if input:
        input_file = input
        try:
            with open(input, newline='', encoding='latin-1') as arquivo:
                leitor = csv.reader(arquivo, delimiter=";")
                linhas = sum(1 for _ in leitor)

            label_arquivo.config(text=f"Arquivo:\n{input}")
            label_dados.config(text=f"Linhas: {linhas}")
        except Exception as e:
            label_arquivo.config(text=f"Erro: {e}") 

def rodar_filtro():
    thread = threading.Thread(target=executar_filtro)
    thread.start()

# função para filtrar dados do arquivo base
def executar_filtro():
    if not input_file:
        label_resultado.config(text="Selecione um arquivo primeiro!")
        return

    label_resultado.config(text="Aguarde, o programa está filtrando seus dados...")
    palavras = entrada_palavras.get()
    
    key_words = [
        p.strip().upper()
        for p in palavras.split(",")
        if p.strip()
    ]

    total, filtrado = filtrar_arquivo(
        input_file,
        "Condomínios.xlsx",
        key_words
    )

    label_resultado.config(
        text=f"Filtro realizado com sucesso!\nFiltrados: {filtrado}\nArquivo salvo como Condomínios.xlsx"
    )

# GUI
janela = tk.Tk()
janela.title("CSV Filter")
janela.resizable(False, False)
janela.geometry("500x350")

titulo_label = tk.Label(
    janela, 
    text="Filtro de dados da Receita Federal", 
    font=("Arial", 20, "bold")
)
titulo_label.pack(pady=5)

botao_abrir = tk.Button(janela, text="Escolher CSV", command=thread_arquivo)
botao_abrir.pack(pady=5)

label_arquivo = tk.Label(janela, text="Nenhum arquivo")
label_arquivo.pack()

label_dados = tk.Label(janela)
label_dados.pack()

# campo de palavras-chave
label_palavras_chave = tk.Label(janela, text="Insira as palavras chave desejadas para filtrar. Separar por ,")
label_palavras_chave.pack(pady=10)
entrada_palavras = tk.Entry(janela, width=50)
entrada_palavras.pack(pady=5)
entrada_palavras.insert(0, "")

# botão de filtro
botao_filtrar = tk.Button(janela, text="Filtrar", command=rodar_filtro)
botao_filtrar.pack(pady=5)

# resultado
label_resultado = tk.Label(janela, text="")
label_resultado.pack()

janela.mainloop()