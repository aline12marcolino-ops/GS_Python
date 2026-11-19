class Orientacao:
    """Representa uma orientação cadastrada na base de conhecimento."""

    def __init__(self, dados):
        self.id = dados["id"]
        self.categoria = dados["categoria"]
        self.titulo = dados["titulo"]
        self.palavras_chave = dados["palavras_chave"]
        self.resposta = dados["resposta"]
        self.documentos = dados["documentos"]
        self.onde = dados["onde"]
        self.fonte = dados["fonte"]
        self.verificado_em = dados["verificado_em"]

    def exibir(self):
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(self.resposta)
        print("\nDocumentos/informações para levar:")
        if self.documentos:
            for documento in self.documentos:
                print(f"  - {documento}")
        else:
            print("  - Não há documento específico indicado nesta orientação.")
        print(f"\nOnde: {self.onde}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("Aviso: este assistente NÃO é um canal oficial.")
