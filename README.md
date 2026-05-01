# Compilador Mini-Java

Projeto de construção de um compilador para a linguagem Mini-Java V2, desenvolvido para a disciplina de Projeto de Compiladores da Universidade Federal de Mato Grosso (UFMT) do Instituto de Computação (IC).

## 🎯 Sobre o Projeto e Status
O objetivo deste trabalho é implementar um compilador completo, passando por todas as fases de análise e gerando código para uma Máquina Hipotética.

**Fases do Compilador:**
- [x] **Analisador Léxico:** Concluído (Tokenização com classificação via Regex)
- [x] **Analisador Sintático:** Concluído (Análise Descendente Recursiva e tratamento de erros)
- [ ] **Analisador Semântico:** Pendente
- [ ] **Geração de Código (Máquina Hipotética):** Pendente
- [ ] **Execução da Máquina Hipotética:** Pendente

## 📁 Estrutura do Projeto
```text
/
├── src/
│   ├── lexico.py         # Lógica de varredura e geração de tokens
│   └── sintatico.py      # Lógica de validação gramatical e recursão
├── teste/
│   ├── teste.txt         # Arquivo de entrada com o código-fonte Mini-Java
│   └── codigo_objeto.txt # Arquivo de saída gerado com o código da Máquina Hipotética
└── README.md