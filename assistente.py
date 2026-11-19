import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path


class Assistente:
    """Conduz o atendimento, registra histórico e calcula indicadores."""

    CAMPOS_CSV = [
        "data", "origem", "pergunta", "id_orientacao", "encontrou",
        "ajudou", "tentativas", "tempo_segundos"
    ]

    def __init__(self, nome, base, pasta_dados):
        self.nome = nome
        self.base = base
        self.pasta_dados = Path(pasta_dados)
        self.pasta_dados.mkdir(parents=True, exist_ok=True)
        self.caminho_historico = self.pasta_dados / "historico.json"
        self.caminho_csv = self.pasta_dados / "atendimentos.csv"
        self.historico = {"atendimentos": [], "avaliacoes": []}
        self._carregar_historico()

    def _carregar_historico(self):
        try:
            with self.caminho_historico.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                self.historico = {"atendimentos": dados, "avaliacoes": []}
            elif isinstance(dados, dict):
                self.historico = {
                    "atendimentos": dados.get("atendimentos", []),
                    "avaliacoes": dados.get("avaliacoes", [])
                }
            else:
                raise ValueError("Formato inesperado.")
        except FileNotFoundError:
            self._salvar_historico()
        except (json.JSONDecodeError, ValueError, TypeError) as erro:
            print(f"Aviso: histórico não pôde ser lido ({erro}). Um histórico novo será iniciado.")
            self._salvar_historico()

    def _salvar_historico(self):
        with self.caminho_historico.open("w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)

    @staticmethod
    def contem_dado_pessoal(texto):
        quantidade_digitos = len(re.findall(r"\d", texto))
        return quantidade_digitos >= 8 or "@" in texto

    def _perguntar_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("Entrada inválida. Digite apenas 's' ou 'n'.")

    def _registrar(self, origem, pergunta, orientacao, encontrou,
                   ajudou, tentativas, inicio):
        registro = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1)
        }
        self.historico["atendimentos"].append(registro)
        self._salvar_historico()

    def perguntar(self):
        inicio = time.time()
        pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
        if pergunta == "0":
            return
        if not pergunta:
            print("A pergunta não pode ficar vazia. Tente novamente.")
            return
        if self.contem_dado_pessoal(pergunta):
            print("Atenção: não digite CPF, telefone, e-mail ou outros dados pessoais. Reescreva.")
            return

        tentativas = 1
        resultados = self.base.buscar(pergunta)
        pontos, melhor = resultados[0] if resultados else (0, None)

        if not melhor or pontos < 3:
            print("\nNão encontrei uma orientação com confiança suficiente.")
            print("Tente outras palavras ou navegue pelas categorias.")
            self._registrar("pergunta", pergunta, None, False, False,
                            tentativas, inicio)
            return

        confianca = "ALTA" if pontos >= 6 else "MÉDIA"
        print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
        melhor.exibir()

        alternativas = [(p, o) for p, o in resultados[1:3] if p >= 3]
        if alternativas:
            print("\nOutras orientações que podem ajudar:")
            for pontos_alt, orientacao_alt in alternativas:
                print(f"  - {orientacao_alt.titulo} ({pontos_alt} pontos)")

        ajudou = self._perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
        self._registrar("pergunta", pergunta, melhor, True, ajudou,
                        tentativas, inicio)

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis.")
            return

        while True:
            print("\n=== CATEGORIAS ===")
            for indice, categoria in enumerate(categorias, start=1):
                print(f"{indice}. {categoria}")
            print("0. Voltar")
            escolha = input("Escolha uma categoria: ").strip()

            if escolha == "0":
                return
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(categorias)):
                print("Opção inválida. Escolha um número da lista.")
                continue

            categoria = categorias[int(escolha) - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print(f"\n=== {categoria.upper()} ===")
                for indice, orientacao in enumerate(orientacoes, start=1):
                    print(f"{indice}. {orientacao.titulo}")
                print("0. Voltar")
                opcao = input("Escolha uma orientação: ").strip()

                if opcao == "0":
                    break
                if not opcao.isdigit() or not (1 <= int(opcao) <= len(orientacoes)):
                    print("Opção inválida. Escolha um número da lista.")
                    continue

                orientacao = orientacoes[int(opcao) - 1]
                inicio = time.time()
                orientacao.exibir()
                ajudou = self._perguntar_sim_nao("\nEssa orientação ajudou? (s/n): ")
                self._registrar(
                    "categoria", f"Consulta por categoria: {categoria}",
                    orientacao, True, ajudou, 1, inicio
                )

    def indicadores(self):
        atendimentos = self.historico["atendimentos"]
        total = len(atendimentos)
        if total == 0:
            print("\nAinda não existem atendimentos registrados.")
            return

        encontrados = sum(1 for item in atendimentos if item["encontrou"])
        ajudaram = sum(1 for item in atendimentos if item["ajudou"] is True)
        tempo_medio = sum(item["tempo_segundos"] for item in atendimentos) / total
        tentativas_media = sum(item["tentativas"] for item in atendimentos) / total
        avaliacoes = self.historico["avaliacoes"]
        facilidade = (
            sum(avaliacoes) / len(avaliacoes) if avaliacoes else None
        )
        sem_solucao = [
            item["pergunta"] for item in atendimentos
            if not item["encontrou"] or item["ajudou"] is False
        ]

        print("\n=== INDICADORES ===")
        print(f"Atendimentos registrados: {total}")
        print(f"Respostas encontradas: {encontrados / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {ajudaram / total * 100:.1f}%")
        print(f"Tempo médio por atendimento: {tempo_medio:.1f} segundos")
        print(f"Tentativas médias por atendimento: {tentativas_media:.1f}")
        if facilidade is None:
            print("Facilidade de uso: ainda sem avaliações.")
        else:
            print(f"Facilidade de uso: {facilidade:.1f}/5")
        print("Dúvidas sem solução ou não resolvidas:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(f"  - {duvida}")
        else:
            print("  - Nenhuma registrada.")

    def exportar_csv(self):
        with self.caminho_csv.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=self.CAMPOS_CSV)
            escritor.writeheader()
            escritor.writerows(self.historico["atendimentos"])
        print(f"\nAtendimentos exportados para: {self.caminho_csv}")

    def avaliar_facilidade(self):
        while True:
            nota = input("\nDe 1 a 5, qual foi a facilidade de uso? (0 para pular): ").strip()
            if nota == "0":
                return
            if nota in ("1", "2", "3", "4", "5"):
                self.historico["avaliacoes"].append(int(nota))
                self._salvar_historico()
                print("Avaliação registrada. Obrigado!")
                return
            print("Nota inválida. Digite um número de 1 a 5 ou 0 para pular.")

    def run(self):
        print(f"\nBem-vindo ao {self.nome}!")
        print("Orientações informativas baseadas em fontes oficiais.")
        while True:
            print("\n========== MENU PRINCIPAL ==========")
            print("1. Fazer uma pergunta")
            print("2. Navegar por categorias")
            print("3. Consultar indicadores")
            print("0. Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                break
            elif opcao == "1":
                self.perguntar()
            elif opcao == "2":
                self.navegar()
            elif opcao == "3":
                self.indicadores()
            else:
                print("Opção inválida. Digite 1, 2, 3 ou 0.")

        self.avaliar_facilidade()
        self.exportar_csv()
        print("\nObrigado por utilizar o Citizen Assist AI!")
