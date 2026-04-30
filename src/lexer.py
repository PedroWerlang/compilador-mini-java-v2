import re

# Definição dos tokens usando Expressões Regulares
# A ordem importa! Tokens mais específicos devem vir antes
TOKEN_REGEX = [
    # Adicionamos o 'lerDouble' na lista de palavras reservadas
    ('RESERVADA', r'\b(public|class|static|void|main|String|double|if|else|while|lerDouble)\b'),
    ('PRINT', r'System\.out\.println'),
    ('NUMERO_REAL', r'\d+(\.\d+)?'),       # Aceita números como 10 ou 10.5
    # Letras/underscore seguidos de letras/números
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OP_RELACIONAL', r'==|!=|>=|<=|>|<'),
    ('ATRIBUICAO', r'='),
    ('OP_ARITMETICO', r'[\+\-\*/]'),
    ('DELIMITADOR', r'[{}()\[\],;]'),
    ('ESPACO', r'[ \t\n\r]+'),             # Espaços e quebras de linha
    # Qualquer outro caractere não reconhecido
    ('ERRO', r'.'),
]


def analisar_lexico(codigo_fonte):
    tokens_encontrados = []

    # Junta todas as regras do regex em uma só
    regex_completa = '|'.join(
        f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_REGEX)

    for correspondencia in re.finditer(regex_completa, codigo_fonte):
        tipo_token = correspondencia.lastgroup
        valor_token = correspondencia.group()

        if tipo_token == 'ESPACO':
            continue  # Ignoramos os espaços em branco

        if tipo_token == 'ERRO':
            raise RuntimeError(
                f"Erro Léxico: Caractere inesperado '{valor_token}'")

        tokens_encontrados.append((tipo_token, valor_token))

    return tokens_encontrados


if __name__ == '__main__':
    with open('testes/teste.txt', 'r') as arquivo:

        codigo_fonte = arquivo.read()

    tokens = analisar_lexico(codigo_fonte)
    for t in tokens:

        print(t)
