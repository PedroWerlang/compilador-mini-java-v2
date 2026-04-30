import re

# Definição dos tokens usando Expressões Regulares
# A ordem importa! Tokens mais específicos devem vir antes (ex: '==' antes de '=')
TOKEN_REGEX = [
    ('RESERVADA', r'\b(public|class|static|void|main|String|double|if|else|while)\b'),
    ('PRINT', r'System\.out\.println'),
    ('LER_DOUBLE', r'lerDouble'),
    ('NUMERO_REAL', r'\d+(\.\d+)?'), # Aceita números como 10 ou 10.5
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'), # Letras/underscore seguidos de letras/números
    ('OP_RELACIONAL', r'==|!=|>=|<=|>|<'),
    ('ATRIBUICAO', r'='),
    ('OP_ARITMETICO', r'[\+\-\*/]'),
    ('DELIMITADOR', r'[{}()\[\],;]'),
    ('ESPACO', r'[ \t\n\r]+'), # Espaços e quebras de linha
    ('ERRO', r'.'),            # Qualquer outro caractere não reconhecido
]

def analisar_lexico(codigo_fonte):
    tokens_encontrados = []
    
    # Junta todas as regras do regex em uma só
    regex_completa = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_REGEX)
    
    for correspondencia in re.finditer(regex_completa, codigo_fonte):
        tipo_token = correspondencia.lastgroup
        valor_token = correspondencia.group()
        
        if tipo_token == 'ESPACO':
            continue # Ignoramos os espaços em branco
            
        if tipo_token == 'ERRO':
            raise RuntimeError(f"Erro Léxico: Caractere inesperado '{valor_token}'")
            
        tokens_encontrados.append((tipo_token, valor_token))
        
    return tokens_encontrados

if __name__ == '__main__':
    # Abre o arquivo teste.txt que criamos
    with open('teste.txt', 'r') as arquivo:
        codigo_fonte = arquivo.read()
    
    # Chama a função e guarda o resultado na variável 'tokens'
    tokens = analisar_lexico(codigo_fonte)
    
    # Imprime os tokens encontrados (note o recuo/espaço no começo da linha)
    for t in tokens:
        print(t)