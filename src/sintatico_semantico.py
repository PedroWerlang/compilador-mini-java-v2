from lexico import analisar_lexico
import os


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.token_atual = self.tokens[self.posicao] if self.tokens else None

        self.tabela_simbolos = {}
        self.codigo_gerado = []
        self.contador_endereco = 0

    def avancar(self):
        """Avança o ponteiro para o próximo token da lista."""
        self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]
        else:
            self.token_atual = None

    def consome(self, tipo_esperado, valor_esperado=None):
        """
        Verifica se o token atual é o esperado. Se for, avança. Se não, dispara um Erro de Sintaxe.
        """
        if self.token_atual is None:
            raise SyntaxError(
                f"Erro Sintático: Fim inesperado do arquivo. Esperava {tipo_esperado}")

        tipo, valor = self.token_atual

        if tipo == tipo_esperado and (valor_esperado is None or valor == valor_esperado):
            self.avancar()
        else:
            detalhe = f" '{valor_esperado}'" if valor_esperado else ""
            raise SyntaxError(
                f"Erro Sintático: Esperava {tipo_esperado}{detalhe}, mas encontrou {tipo} '{valor}'")

    def espiar(self):
        """Devolve o tipo e valor do token atual"""
        if self.token_atual is None:
            return None, None

        return self.token_atual

    def analisar(self):
        """Função principal que dá o pontapé inicial na análise."""
        self.regra_prog()

        if self.token_atual is not None:
            raise SyntaxError(
                f"Erro Sintático: Código extra no final do arquivo.")

        print("✓ Análise Sintática e Semântica concluídas com SUCESSO!")

    def regra_prog(self):
        """ PROG -> public class id { public static void main ( String [ ] id ) { <CMDS> } } """

        self.codigo_gerado.append("INPP")

        self.consome('RESERVADA', 'public')
        self.consome('RESERVADA', 'class')
        self.consome('ID')
        self.consome('DELIMITADOR', '{')
        self.consome('RESERVADA', 'public')
        self.consome('RESERVADA', 'static')
        self.consome('RESERVADA', 'void')
        self.consome('RESERVADA', 'main')
        self.consome('DELIMITADOR', '(')
        self.consome('RESERVADA', 'String')
        self.consome('DELIMITADOR', '[')
        self.consome('DELIMITADOR', ']')
        self.consome('ID')
        self.consome('DELIMITADOR', ')')
        self.consome('DELIMITADOR', '{')
        self.regra_cmds()
        self.consome('DELIMITADOR', '}')
        self.consome('DELIMITADOR', '}')

        self.codigo_gerado.append("PARA")

    def regra_cmds(self):
        """ CMDS -> <CMD><MAIS_CMDS> | <CMD_COND><CMDS> | <DC> | λ """
        tipo, valor = self.espiar()

        if tipo == 'RESERVADA' and valor == 'double':
            self.regra_dc()

        elif tipo == 'RESERVADA' and valor in ['if', 'while']:
            self.regra_cmd_cond()
            self.regra_cmds()

        elif tipo == 'PRINT' or tipo == 'ID':
            self.regra_cmd()
            self.regra_mais_cmds()

        else:
            return

    def regra_dc(self):
        """ DC -> <VAR> <MAIS_CMDS> """
        self.regra_var()
        self.regra_mais_cmds()

    def regra_var(self):
        """ VAR -> <TIPO> <VARS> """
        self.regra_tipo()
        self.regra_vars()

    def regra_tipo(self):
        """ TIPO -> double """
        self.consome('RESERVADA', 'double')

    def regra_vars(self):
        """ VARS -> id <MAIS_VAR> """

        tipo, valor = self.espiar()

        if tipo == 'ID':
            nome_variavel = valor

            if nome_variavel in self.tabela_simbolos:
                raise Exception(
                    f"Erro Semântico: A variável '{nome_variavel}' já foi declarada anteriormente!")
            else:
                self.tabela_simbolos[nome_variavel] = {
                    'tipo': 'double',
                    'end_rel': self.contador_endereco
                }

                self.codigo_gerado.append("ALME 1")
                self.contador_endereco += 1

            self.consome('ID')
            self.regra_mais_var()

        else:
            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado. Esperava um identificador (variável).")
            raise SyntaxError(
                f"Erro Sintático: Esperava um identificador, encontrou '{valor}'")

    def regra_mais_var(self):
        """ MAIS_VAR -> , <VARS> | λ """

        tipo, valor = self.espiar()

        if tipo == 'DELIMITADOR' and valor == ',':
            self.consome('DELIMITADOR', ',')
            self.regra_vars()

        else:
            return

    def regra_mais_cmds(self):
        """ MAIS_CMDS -> ; <CMDS> """
        self.consome('DELIMITADOR', ';')
        self.regra_cmds()

    def regra_cmd_cond(self):
        """ CMD_COND -> if ( <CONDICAO> ) {<CMDS>} <PFALSA> | while ( <CONDICAO> ) {<CMDS>} """

        tipo, valor = self.espiar()

        if tipo == 'RESERVADA' and valor == 'if':
            self.consome('RESERVADA', 'if')
            self.consome('DELIMITADOR', '(')
            self.regra_condicao()
            self.consome('DELIMITADOR', ')')

            idx_dsvf = len(self.codigo_gerado)
            self.codigo_gerado.append("DSVF ?")

            self.consome('DELIMITADOR', '{')
            self.regra_cmds()
            self.consome('DELIMITADOR', '}')

            idx_dsvi = len(self.codigo_gerado)
            self.codigo_gerado.append("DSVI ?")

            linha_else = len(self.codigo_gerado)
            self.codigo_gerado[idx_dsvf] = f"DSVF {linha_else}"

            self.regra_pfalsa()

            linha_fim = len(self.codigo_gerado)
            self.codigo_gerado[idx_dsvi] = f"DSVI {linha_fim}"

        elif tipo == 'RESERVADA' and valor == 'while':
            linha_inicio_while = len(self.codigo_gerado)

            self.consome('RESERVADA', 'while')
            self.consome('DELIMITADOR', '(')
            self.regra_condicao()
            self.consome('DELIMITADOR', ')')

            idx_dsvf = len(self.codigo_gerado)
            self.codigo_gerado.append("DSVF ?")

            self.consome('DELIMITADOR', '{')
            self.regra_cmds()
            self.consome('DELIMITADOR', '}')

            self.codigo_gerado.append(f"DSVI {linha_inicio_while}")

            linha_fim_while = len(self.codigo_gerado)
            self.codigo_gerado[idx_dsvf] = f"DSVF {linha_fim_while}"

        else:
            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado. Esperava 'if' ou 'while'.")
            raise SyntaxError(
                f"Erro Sintático: Esperava 'if' ou 'while', encontrou '{valor}'")

    def regra_cmd(self):
        """ CMD -> System.out.println (<EXPRESSAO>) | id <RESTO_IDENT> """

        tipo, valor = self.espiar()

        if tipo == 'PRINT':
            self.consome('PRINT')
            self.consome('DELIMITADOR', '(')
            self.regra_expressao()
            self.consome('DELIMITADOR', ')')

            self.codigo_gerado.append("IMPR")

        elif tipo == 'ID':
            nome_variavel = valor

            if nome_variavel not in self.tabela_simbolos:
                raise Exception(
                    f"Erro Semântico: A variável '{nome_variavel}' não foi declarada antes de receber um valor!")

            self.consome('ID')
            self.regra_resto_ident()

            endereco = self.tabela_simbolos[nome_variavel]['end_rel']
            self.codigo_gerado.append(f"ARMZ {endereco}")

        else:

            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado. Esperava 'System.out.println' ou um 'id'.")
            raise SyntaxError(
                f"Erro Sintático: Comando inválido. Esperava 'System.out.println' ou variável, encontrou '{valor}'")

    def regra_pfalsa(self):
        """ PFALSA -> else { <CMDS> } | λ """
        tipo, valor = self.espiar()

        if tipo == 'RESERVADA' and valor == 'else':
            self.consome('RESERVADA', 'else')
            self.consome('DELIMITADOR', '{')
            self.regra_cmds()
            self.consome('DELIMITADOR', '}')

        else:
            return

    def regra_resto_ident(self):
        """ RESTO_IDENT -> = <EXP_IDENT> """

        self.consome('ATRIBUICAO', '=')
        self.regra_exp_ident()

    def regra_exp_ident(self):
        """ EXP_IDENT -> <EXPRESSAO> | lerDouble() """

        tipo, valor = self.espiar()

        if tipo == 'RESERVADA' and valor == 'lerDouble':
            self.consome('RESERVADA', 'lerDouble')
            self.consome('DELIMITADOR', '(')
            self.consome('DELIMITADOR', ')')

            self.codigo_gerado.append("LEIT")

        elif tipo in ['NUMERO_REAL', 'ID'] or (tipo == 'DELIMITADOR' and valor == '(') or valor == '-':
            self.regra_expressao()

        else:
            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado após o sinal de '='.")
            raise SyntaxError(
                f"Erro Sintático: Esperava expressão ou 'lerDouble()', encontrou '{valor}'")

    def regra_condicao(self):
        """ CONDICAO -> <EXPRESSAO> <RELACAO> <EXPRESSAO> """

        self.regra_expressao()

        tipo, valor = self.espiar()
        operador = valor

        self.regra_relacao()
        self.regra_expressao()

        mapa_relacao = {
            '==': 'CPIG',
            '!=': 'CDES',
            '<':  'CPME',
            '>':  'CPMA',
            '<=': 'CPMI',
            '>=': 'CMAI'
        }
        if operador in mapa_relacao:
            self.codigo_gerado.append(mapa_relacao[operador])

    def regra_relacao(self):
        """ RELACAO -> == | != | >= | <= | > | < """

        tipo, valor = self.espiar()

        operadores_validos = ['==', '!=', '>=', '<=', '>', '<']

        if valor in operadores_validos:
            self.consome(tipo, valor)

        else:

            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado. Esperava um operador relacional (==, !=, >, <, >=, <=).")
            raise SyntaxError(
                f"Erro Sintático: Esperava operador relacional, encontrou '{valor}'")

    def regra_expressao(self):
        """ EXPRESSAO -> <TERMO> <OUTROS_TERMOS> """

        self.regra_termo()
        self.regra_outros_termos()

    def regra_termo(self):
        """ TERMO -> <OP_UN> <FATOR> <MAIS_FATORES> """

        tipo, valor = self.espiar()
        tem_menos_unario = (valor == '-')

        self.regra_op_un()

        self.regra_fator()

        if tem_menos_unario:
            self.codigo_gerado.append("INVE")

        self.regra_mais_fatores()

    def regra_op_un(self):
        """ OP_UN -> - | λ """

        tipo, valor = self.espiar()

        if valor == '-':
            self.consome(tipo, '-')
        else:
            return

    def regra_fator(self):
        """ FATOR -> id | numero_real | (<EXPRESSAO>) """
        tipo, valor = self.espiar()

        if tipo == 'ID':
            nome_variavel = valor
            if nome_variavel not in self.tabela_simbolos:
                raise Exception(
                    f"Erro Semântico: A variável '{nome_variavel}' não foi declarada antes de ser usada na conta!")

            self.consome('ID')

            endereco = self.tabela_simbolos[nome_variavel]['end_rel']
            self.codigo_gerado.append(f"CRVL {endereco}")

        elif tipo == 'NUMERO_REAL':
            valor_numero = valor
            self.consome('NUMERO_REAL')

            self.codigo_gerado.append(f"CRCT {valor_numero}")

        elif tipo == 'DELIMITADOR' and valor == '(':
            self.consome('DELIMITADOR', '(')
            self.regra_expressao()
            self.consome('DELIMITADOR', ')')

        else:
            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado. Esperava variável, número ou '('.")
            raise SyntaxError(
                f"Erro Sintático: Esperava variável, número ou '(', encontrou '{valor}'")

    def regra_outros_termos(self):
        """ OUTROS_TERMOS -> <OP_AD> <TERMO> <OUTROS_TERMOS> | λ """

        tipo, valor = self.espiar()

        if valor in ['+', '-']:
            operador = valor
            self.regra_op_ad()
            self.regra_termo()

            if operador == '+':
                self.codigo_gerado.append("SOMA")
            else:
                self.codigo_gerado.append("SUBT")

            self.regra_outros_termos()

        else:
            return

    def regra_op_ad(self):
        """ OP_AD -> + | - """

        tipo, valor = self.espiar()

        if valor in ['+', '-']:
            self.consome(tipo, valor)

        else:
            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado. Esperava '+' ou '-'.")
            raise SyntaxError(
                f"Erro Sintático: Esperava '+' ou '-', encontrou '{valor}'")

    def regra_mais_fatores(self):
        """ MAIS_FATORES -> <OP_MUL> <FATOR> <MAIS_FATORES> | λ """

        tipo, valor = self.espiar()

        if valor in ['*', '/']:
            operador = valor
            self.regra_op_mul()
            self.regra_fator()

            if operador == '*':
                self.codigo_gerado.append("MULT")
            else:
                self.codigo_gerado.append("DIVI")

            self.regra_mais_fatores()

        else:
            return

    def regra_op_mul(self):
        """ OP_MUL -> * | / """

        tipo, valor = self.espiar()

        if valor in ['*', '/']:
            self.consome(tipo, valor)

        else:
            if tipo is None:
                raise SyntaxError(
                    "Erro Sintático: Fim inesperado. Esperava '*' ou '/'.")
            raise SyntaxError(
                f"Erro Sintático: Esperava '*' ou '/', encontrou '{valor}'")


if __name__ == '__main__':
    with open('io/codigo_fonte.txt', 'r') as arquivo:
        codigo = arquivo.read()

    print("[Compilador Mini-Java] Iniciando pipeline de compilação...")
    print("✓ Analisador Léxico executado.")
    lista_de_tokens = analisar_lexico(codigo)

    sintatico = AnalisadorSintatico(lista_de_tokens)
    sintatico.analisar()

    print("\n✓ Arquivo 'codigo_objeto.txt' gerado com sucesso na pasta 'io'.")
    print("\n" + "="*45)
    print("      INICIANDO A MÁQUINA VIRTUAL MAQHIPO      ")
    print("="*45 + "\n")
    os.system('python src/maqhipo.py')
