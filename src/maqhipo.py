C = []
D = [0.0] * 1000
i = 0
s = -1


def carregar_codigo(caminho_arquivo):
    global C
    C = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split()
            comando = partes[0]
            parametro = partes[1] if len(partes) > 1 else None

            C.append((comando, parametro))


def executar():
    global C, D, i, s

    while True:
        if i < 0 or i >= len(C):
            print("Erro: Ponteiro de instrução fora dos limites.")
            break

        comando, param = C[i]

        i += 1

        if comando == 'INPP':
            s = -1

        elif comando == 'PARA':
            break

        elif comando == 'CRCT':
            s += 1
            D[s] = float(param)

        elif comando == 'CRVL':
            s += 1
            n = int(param)
            D[s] = D[n]

        elif comando == 'ARMZ':
            n = int(param)
            D[n] = D[s]
            s -= 1

        elif comando == 'ALME':
            m = int(param)
            s += m

        elif comando == 'SOMA':
            D[s - 1] = D[s - 1] + D[s]
            s -= 1

        elif comando == 'SUBT':
            D[s - 1] = D[s - 1] - D[s]
            s -= 1

        elif comando == 'MULT':
            D[s - 1] = D[s - 1] * D[s]
            s -= 1

        elif comando == 'DIVI':
            if D[s] == 0.0:
                print(
                    f"\nNão é possível dividir por 0 na intrução {i}.")
                print("FIm do Código.")
                break

            D[s - 1] = D[s - 1] / D[s]
            s -= 1

        elif comando == 'INVE':
            D[s] = -D[s]

        # Não será utilizado essas intruções pois a gramática da linguagem não incluí as seguintes operações &&, || e !

        # elif comando == 'CONJ':
        #     if D[s - 1] == 1.0 and D[s] == 1.0:
        #         D[s - 1] = 1.0
        #     else:
        #         D[s - 1] = 0.0
        #     s -= 1
        #
        # elif comando == 'DISJ':
        #     if D[s - 1] == 1.0 or D[s] == 1.0:
        #         D[s - 1] = 1.0
        #     else:
        #         D[s - 1] = 0.0
        #     s -= 1
        #
        # elif comando == 'NEGA':
        #     D[s] = 1.0 - D[s]

        elif comando == 'CPME':
            D[s - 1] = 1.0 if (D[s - 1] < D[s]) else 0.0
            s -= 1

        elif comando == 'CPMA':
            D[s - 1] = 1.0 if (D[s - 1] > D[s]) else 0.0
            s -= 1

        elif comando == 'CPIG':
            D[s - 1] = 1.0 if (D[s - 1] == D[s]) else 0.0
            s -= 1

        elif comando == 'CDES':
            D[s - 1] = 1.0 if (D[s - 1] != D[s]) else 0.0
            s -= 1

        elif comando == 'CPMI':
            D[s - 1] = 1.0 if (D[s - 1] <= D[s]) else 0.0
            s -= 1

        elif comando == 'CMAI':
            D[s - 1] = 1.0 if (D[s - 1] >= D[s]) else 0.0
            s -= 1

        elif comando == 'DSVI':
            i = int(param)

        elif comando == 'DSVF':
            if D[s] == 0.0:
                i = int(param)
            s -= 1

        elif comando == 'LEIT':
            s += 1
            valor = float(input("Entrada de dados (lerDouble): "))
            D[s] = valor

        elif comando == 'IMPR':
            print(f">> Saída: {D[s]}")
            s -= 1

        else:
            print(f"Erro: Comando desconhecido '{comando}' na linha {i}")
            break


if __name__ == '__main__':
    carregar_codigo('io/codigo_objeto.txt')
    executar()
