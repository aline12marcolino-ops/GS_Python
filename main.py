from pathlib import Path

from assistente import Assistente
from base_conhecimento import BaseConhecimento


def main():
    pasta_projeto = Path(__file__).resolve().parent
    pasta_dados = pasta_projeto / "data"
    caminho_json = pasta_dados / "base_conhecimento.json"

    base = BaseConhecimento(caminho_json)
    base.carregar()

    if not base.orientacoes:
        print("\nA base de conhecimento está vazia ou não pôde ser carregada.")
        print("Verifique o arquivo data/base_conhecimento.json antes de continuar.")
        return

    assistente = Assistente("Citizen Assist AI", base, pasta_dados)
    assistente.run()


if __name__ == "__main__":
    main()
