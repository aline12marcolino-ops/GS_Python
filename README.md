# Citizen Assist AI
**Assistente Digital de Orientação ao Cidadão**

## 1. Apresentação
O Citizen Assist AI é um assistente executado no terminal, desenvolvido em Python. Ele orienta cidadãos sobre serviços de saúde, documentação/cidadania e direitos do consumidor, usando exclusivamente uma base de conhecimento em JSON. Cada orientação apresenta resposta, documentos ou informações necessárias, local/canal, fonte, data de verificação e aviso de que o sistema não é um canal oficial.

## 2. Equipe
- Aline Medri Marcolino - RM:569349
- Luís Fernando de Azevedo - RM: 574167
- Rafael Ferreirinha Quaresma  - RM:571949

## 3. Público e problema
**Público-alvo:** cidadãos em geral.

**Problema:** informações sobre serviços públicos e direitos estão distribuídas em diferentes portais e podem ser difíceis de localizar ou compreender. O projeto reúne orientações verificadas em linguagem simples e indica a fonte oficial para consulta.

## 4. ODS relacionados
- **ODS 3 — Saúde e bem-estar:** orientações relacionadas a serviços de saúde.
- **ODS 10 — Redução das desigualdades:** facilita o acesso a informações públicas.
- **ODS 16 — Paz, justiça e instituições eficazes:** divulga canais e informações institucionais.

## 5. Estrutura do projeto
```text
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

## 6. Como executar
Requisito: Python 3 instalado. O projeto utiliza apenas bibliotecas padrão do Python.

No terminal, acesse a pasta `citizen-assist-ai` e execute:

```bash
python main.py
```

## 7. Base de conhecimento
O arquivo `data/base_conhecimento.json` contém **10 orientações em 3 categorias**:
- Saúde;
- Documentação e cidadania;
- Direitos do consumidor.

Cada registro contém os campos obrigatórios: `id`, `categoria`, `titulo`, `palavras_chave`, `resposta`, `documentos`, `onde`, `fonte` e `verificado_em`. Cada orientação possui no mínimo três palavras-chave. As datas de verificação registradas na base são 15/11/2026; a equipe deve conferir novamente os procedimentos e links antes da publicação, pois podem mudar.

## 8. Classes e composição
- **`Orientacao`:** representa um registro do JSON, guarda seus atributos e apresenta a orientação pelo método `exibir()`.
- **`BaseConhecimento`:** carrega o JSON, cria objetos `Orientacao`, lista categorias, filtra por categoria e realiza a busca pontuada.
- **`Assistente`:** conduz a interação, faz perguntas, permite navegação, registra atendimentos, calcula indicadores e exporta CSV.

A composição ocorre porque `Assistente` possui um objeto `BaseConhecimento`, que mantém uma lista de objetos `Orientacao`.

## 9. Regra de busca e confiança
A função `normalizar()` converte o texto para minúsculas, remove acentos e pontuação.

Pontuação aplicada:
- **+3 pontos** para cada palavra-chave da orientação encontrada na pergunta;
- **+1 ponto** para cada palavra da pergunta com quatro ou mais letras que também apareça no título;
- **6 pontos ou mais:** confiança ALTA;
- **3 a 5 pontos:** confiança MÉDIA;
- **menos de 3 pontos:** orientação não encontrada.

O método `buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, ordenada da maior para a menor pontuação. O assistente apresenta a melhor correspondência e até duas alternativas com pontuação mínima de 3.

## 10. Regras de atendimento, privacidade e transparência
- O programa não solicita nome, CPF, telefone ou e-mail.
- Perguntas com oito ou mais dígitos ou com `@` são recusadas e não entram no histórico.
- Entradas vazias, opções fora da faixa e respostas diferentes de `s`/`n` são tratadas sem encerrar o programa.
- A navegação permite voltar com `0` nas telas de categorias e orientações.
- Cada orientação mostra fonte, data de verificação e o aviso: **“este assistente NÃO é um canal oficial.”**
- O sistema não gera respostas fora do conteúdo cadastrado no JSON.

## 11. Histórico, indicadores e CSV
Cada atendimento válido é armazenado em `data/historico.json` com data, origem (`pergunta` ou `categoria`), pergunta/consulta, ID da orientação, se encontrou, se ajudou, tentativas e tempo em segundos. Perguntas recusadas por possível dado pessoal não são registradas. Ao sair, o sistema solicita uma nota de facilidade de 1 a 5 (ou permite pular com `0`).

O menu de indicadores apresenta:
- percentual de respostas encontradas;
- taxa de atendimentos em que a orientação ajudou;
- tempo médio;
- tentativas médias por atendimento;
- facilidade média (1 a 5), quando houver avaliações;
- dúvidas não encontradas ou que não ajudaram.

Na saída, os atendimentos são exportados para `data/atendimentos.csv` usando `csv.DictWriter`.

## 12. Testes com usuários — preencher com dados reais
O enunciado exige testar o assistente com **pelo menos 3 pessoas de fora da equipe e 10 atendimentos ou mais**. Não registrar nomes, contatos, CPFs ou qualquer dado que identifique participantes.

**Situação deste pacote:** os testes com usuários externos ainda precisam ser realizados e documentados pela equipe. Os testes internos de funcionamento não substituem essa etapa. Não preencher os campos abaixo com estimativas ou resultados inventados.

Após realizar os testes, registrar:
- Participantes externos: [NÚMERO — mínimo 3]
- Atendimentos realizados: [NÚMERO — mínimo 10]
- Respostas encontradas: [PERCENTUAL REAL]
- Taxa de acerto (orientação ajudou): [PERCENTUAL REAL]
- Tempo médio: [VALOR REAL EM SEGUNDOS]
- Tentativas médias por atendimento: [VALOR REAL]
- Facilidade média: [NOTA REAL DE 1 A 5]
- Dúvidas sem solução/não resolvidas: [LISTA ANÔNIMA OU “NENHUMA”]
- Melhoria implementada a partir do teste: [DESCREVER A ALTERAÇÃO REAL, por exemplo uma palavra-chave adicionada ao JSON]

**Como realizar:** distribuir os atendimentos entre pelo menos três pessoas externas, operar o programa com elas, registrar os resultados sem identificação e, ao final, consultar a opção de indicadores. Fazer pelo menos uma melhoria baseada em uma dúvida observada e demonstrá-la no vídeo, alterando uma palavra-chave no JSON e repetindo a pergunta.

## 13. Limitações
- A busca utiliza regras e palavras-chave; não é um modelo generativo de IA.
- O assistente responde somente com os registros existentes no JSON.
- A base é inicial e deve ser revisada e ampliada periodicamente.
- Procedimentos e canais podem variar conforme estado ou município.
- A orientação sobre Procon é específica para São Paulo; pessoas de outros estados devem consultar o Procon local.
- O bloqueio de dados pessoais é uma proteção básica por padrão textual, não uma garantia completa contra o envio de informações sensíveis.

## 14. Integrações com outras disciplinas
Esta versão não utiliza API ou modelo externo. A busca por pontuação e as estruturas de dados exigidas na disciplina foram mantidas como mecanismo principal.

## 15. Entrega e vídeo
- **Repositório público GitHub:** [INSERIR LINK DO REPOSITÓRIO]
- **Vídeo técnico não listado no YouTube (5 a 8 minutos):** [INSERIR LINK DO VÍDEO]

O vídeo deve demonstrar os oito blocos exigidos no enunciado: equipe/público/problema; registro JSON, dicionários e tuplas; classes, atributos, métodos, `self` e composição; normalização e pontuação com exemplo real; execução com os cenários obrigatórios; alteração de palavra-chave no JSON; histórico, CSV e indicadores do teste; uma decisão técnica e uma limitação.

---
**Atenção antes da entrega:** substituir todos os campos entre colchetes, realizar os testes externos exigidos, atualizar o resultado real nesta seção e inserir os links definitivos do GitHub e do vídeo.
