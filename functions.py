import os, json

# 1. Pega o caminho da pasta onde ESTE arquivo (functions.py/app.py) está instalado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Junta o caminho da pasta com o nome do arquivo JSON
caminho = os.path.join(BASE_DIR, 'cadastros.json')

def salvar_dados(cadastro):
    '''salvar_dados: Ao chamar a função, ele vai pegar o dicionário informado no parâmetro e mudar ou criar um arquivo .json para armazenar
    as informações do dicionário no arquivo tarefas.json'''
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(cadastro, arquivo, indent=4)


def carregar_dados():
    '''carregar_dados: Ao chamar a função, ele vai puxar como um dicionário as informações contidas no arquivo tarefas.json,
    se não existir, ele retorna que não existe'''
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"admin": "admin"}