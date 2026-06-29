# Compilador Mini-Java V2

**Repositório Oficial:** [https://github.com/PedroWerlang/compilador-mini-java-v2](https://github.com/PedroWerlang/compilador-mini-java-v2)

Projeto de construção de um compilador para a linguagem Mini-Java V2, desenvolvido para a disciplina de Projeto de Compiladores da Universidade Federal de Mato Grosso (UFMT) do Instituto de Computação (IC).

## Sobre o Projeto e Status
O objetivo deste trabalho é implementar um compilador completo, passando por todas as fases de análise e gerando código para uma Máquina Hipotética (Máquina à Pilha).

**Fases do Compilador**
- [x] **Analisador Léxico:**
- [x] **Analisador Sintático:**
- [x] **Analisador Semântico:**
- [x] **Geração de Código (Máquina Hipotética):**
- [x] **Execução da Máquina Hipotética:**

---

## Estrutura do Projeto e Arquivos

O projeto está organizado na seguinte estrutura de diretórios:
```text
/
├── io/
│   ├── codigo_fonte.txt         
│   └── codigo_objeto.txt 
├── src/
│   ├── lexico.py         
│   ├── maqhipo.py      
│   └── sintatico_semantico.py 
├── .gitignore
└── README.md
```

### Diretório `/src` (Código-Fonte)
*   **`lexico.py`**: Responsável pela primeira fase da compilação. Ele lê o arquivo-fonte, ignora espaços em branco e comentários, e utiliza Expressões Regulares para quebrar o texto em peças fundamentais (Tokens), classificando-os como palavras reservadas, identificadores, números ou símbolos.
*   **`sintatico_semantico.py`**: É o núcleo do compilador. Ele solicita os tokens ao léxico e os processa usando o método de **Descida Recursiva** (Orientado a Objetos). Ao mesmo tempo em que valida a gramática, ele atua como **Analisador Semântico** (alimentando a Tabela de Símbolos) e como **Gerador de Código**, calculando os pulos lógicos e gravando as instruções finais no arquivo de saída.
*   **`maqhipo.py`**: O interpretador (Máquina Virtual à pilha). Ele atua como o processador do sistema, lendo as instruções geradas pelo compilador e executando as operações matemáticas, lógicas e de memória interativamente no terminal.

### Diretório `/io`
*   **`codigo_fonte.txt`**: Arquivo de entrada. É aqui que você escreve o seu código-fonte na linguagem Mini-Java V2.
*   **`codigo_objeto.txt`**: Arquivo de saída. Gerado automaticamente pelo compilador, contém a lista de instruções (Assembly simulado) prontas para serem lidas pela `maqhipo.py`.

---

## Como Executar

O ciclo de vida do projeto exige que você possua o **Python 3** instalado em sua máquina. O fluxo de uso padrão segue os passos abaixo:

### 1. Preparar o Código-Fonte
Escreva o seu programa em linguagem Mini-Java dentro do arquivo `io/codigo_fonte.txt` e salve.

### 2. Executar a Pipeline Completa
No terminal, na raiz do projeto, execute o script principal. Ele fará a varredura do código, a validação das regras e, em seguida, iniciará a máquina virtual automaticamente:
```bash
python src/sintatico_semantico.py
```
* Se não houver erros de sintaxe ou variáveis não declaradas, o terminal exibirá as mensagens de sucesso, criará o arquivo `codigo_objeto.txt` e a máquina virtual solicitará as entradas de dados, imprimindo os resultados na tela.