import re

TOKEN_REGEX = [

    ('RESERVADA', r'\b(public|class|static|void|main|String|double|if|else|while|lerDouble)\b'),
    ('PRINT', r'System\.out\.println'),
    ('NUMERO_REAL', r'\d+(\.\d+)?'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OP_RELACIONAL', r'==|!=|>=|<=|>|<'),
    ('ATRIBUICAO', r'='),
    ('OP_ARITMETICO', r'[\+\-\*/]'),
    ('DELIMITADOR', r'[{}()\[\],;]'),
    ('ESPACO', r'[ \t\n\r]+'),
    ('ERRO', r'.'),
]


def analisar_lexico(codigo_fonte):
    tokens_encontrados = []

    regex_completa = '|'.join(
        f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_REGEX)

    for correspondencia in re.finditer(regex_completa, codigo_fonte):
        tipo_token = correspondencia.lastgroup
        valor_token = correspondencia.group()

        if tipo_token == 'ESPACO':
            continue

        if tipo_token == 'ERRO':
            raise RuntimeError(
                f"Erro Léxico: Caractere inesperado '{valor_token}'")

        tokens_encontrados.append((tipo_token, valor_token))

    return tokens_encontrados


if __name__ == '__main__':
    with open('io/codigo_fonte.txt', 'r') as arquivo:

        codigo_fonte = arquivo.read()

    tokens = analisar_lexico(codigo_fonte)
    for t in tokens:

        print(t)
