from lexico import analisar_lexico


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.token_atual = self.tokens[self.posicao] if self.tokens else None

    def avancar(self):
        """Avança o ponteiro para o próximo token da lista."""
        self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]
        else:
            self.token_atual = None

    def consome(self, tipo_esperado, valor_esperado=None):
        """
        Verifica se o token atual é o esperado.
        Se for, avança. Se não, dispara um Erro de Sintaxe.
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
        """Devolve o tipo e valor do token atual com segurança, sem risco de dar erro no Python."""
        if self.token_atual is None:
            return None, None

        return self.token_atual

    def analisar(self):
        """Função principal que dá o pontapé inicial na análise."""
        print("Iniciando análise sintática...")
        self.regra_prog()

        if self.token_atual is not None:
            raise SyntaxError(
                f"Erro Sintático: Código extra no final do arquivo.")

        print("Análise sintática concluída com SUCESSO!")

    def regra_prog(self):
        """ PROG -> public class id { public static void main ( String [ ] id ) { <CMDS> } } """

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
        self.consome('ID')
        self.regra_mais_var()

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
            self.consome('DELIMITADOR', '{')
            self.regra_cmds()
            self.consome('DELIMITADOR', '}')
            self.regra_pfalsa()

        elif tipo == 'RESERVADA' and valor == 'while':
            self.consome('RESERVADA', 'while')
            self.consome('DELIMITADOR', '(')
            self.regra_condicao()
            self.consome('DELIMITADOR', ')')
            self.consome('DELIMITADOR', '{')
            self.regra_cmds()
            self.consome('DELIMITADOR', '}')

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

        elif tipo == 'ID':
            self.consome('ID')
            self.regra_resto_ident()

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
        self.regra_relacao()
        self.regra_expressao()

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

        self.regra_op_un()
        self.regra_fator()
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
            self.consome('ID')

        elif tipo == 'NUMERO_REAL':
            self.consome('NUMERO_REAL')

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
            self.regra_op_ad()
            self.regra_termo()
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
            self.regra_op_mul()
            self.regra_fator()
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
    with open('testes/teste.txt', 'r') as arquivo:
        codigo = arquivo.read()
    print("Executando Léxico...")
    lista_de_tokens = analisar_lexico(codigo)

    sintatico = AnalisadorSintatico(lista_de_tokens)
    sintatico.analisar()
