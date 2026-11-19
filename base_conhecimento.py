import json
import re
import unicodedata
from pathlib import Path

from orientacao import Orientacao


def normalizar(texto):
    """Deixa o texto em minúsculas, sem acentos e sem pontuação."""
    texto = unicodedata.normalize("NFD", str(texto).lower())
    texto = "".join(caractere for caractere in texto
                    if unicodedata.category(caractere) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    """Carrega, organiza e pesquisa as orientações do arquivo JSON."""

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    def carregar(self):
        try:
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("A raiz do JSON precisa ser uma lista.")
            orientacoes_carregadas = []
            campos = {
                "id", "categoria", "titulo", "palavras_chave", "resposta",
                "documentos", "onde", "fonte", "verificado_em"
            }
            for indice, item in enumerate(dados, start=1):
                if not isinstance(item, dict) or not campos.issubset(item):
                    raise ValueError(f"Registro {indice} incompleto ou inválido.")
                if len(item["palavras_chave"]) < 3:
                    raise ValueError(f"Registro {indice} precisa de 3 palavras-chave.")
                orientacoes_carregadas.append(Orientacao(item))
            self.orientacoes = orientacoes_carregadas
            return True
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {self.caminho}")
        except (json.JSONDecodeError, ValueError, TypeError) as erro:
            print(f"Não foi possível carregar a base de conhecimento: {erro}")
        self.orientacoes = []
        return False

    def categorias(self):
        return sorted({orientacao.categoria for orientacao in self.orientacoes})

    def por_categoria(self, categoria):
        return [orientacao for orientacao in self.orientacoes
                if orientacao.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        titulo_norm = normalizar(orientacao.titulo)
        pontos = 0

        for palavra_chave in orientacao.palavras_chave:
            chave_norm = normalizar(palavra_chave).strip()
            if chave_norm and f" {chave_norm} " in pergunta_norm:
                pontos += 3

        palavras_pergunta = set(pergunta_norm.split())
        palavras_titulo = set(titulo_norm.split())
        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = [
            (self.pontuar(pergunta, orientacao), orientacao)
            for orientacao in self.orientacoes
        ]
        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
