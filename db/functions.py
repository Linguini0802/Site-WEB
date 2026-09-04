# db/functions.py
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

caminho_cadastros = os.path.join(BASE_DIR, 'cadastros.json')
caminho_videos = os.path.join(BASE_DIR, 'videos.json')


def salvar_dados_cadastros(cadastro):
    with open(caminho_cadastros, "w", encoding="utf-8") as arquivo:
        json.dump(cadastro, arquivo, indent=4)


def carregar_dados_cadastros():
    try:
        with open(caminho_cadastros, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {
            "proximo_id": 2, 
            "usuarios": [
                {
                    "id": 1, 
                    "usuario": "admin", 
                    "senha": "admin"
                }
            ]
        }


def salvar_dados_videos(videos):
    with open(caminho_videos, "w", encoding="utf-8") as arquivo:
        json.dump(videos, arquivo, indent=4)


def carregar_dados_videos():
    try:
        with open(caminho_videos, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"proximo_id": 1, "videos": []}


def teste():
    videos = carregar_dados_videos()
    salvar_dados_videos(videos)
    novo_video = {
        "id": videos["proximo_id"],
        "id_usuario": 1,
        "nome_usuario": "a",
        "nome_video": "a",
        "url_video": "https://www.youtube.com/embed/2oIpEQWHqBI?si=6C7F3fRXd-8sba37"
    }
    videos["videos"].append(novo_video)
    salvar_dados_videos(videos)


