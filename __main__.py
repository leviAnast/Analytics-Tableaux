from Classes.Tableau import *
import sys
import io

def ler_arquivo():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    arquivo = sys.stdin.read()
    linhas = arquivo.splitlines()
    num_formulas = int(linhas[0].strip())
    antecedentes = [linhas[i].strip() for i in range(1, num_formulas)]
    sequente = linhas[num_formulas].strip()
    return antecedentes, sequente

def inicializar_tableau(antecedentes, sequente):
    return Tableau(antecedentes, sequente)

def provar_tableau(Tableau):
    print(f"Ramo antes da expansao: {Tableau.ramo}")
    print(f"Betas antes da expansão: {Tableau.betas}")

    while True:
        Tableau.expansoes_alfa()

        if any(Tableau.betas):
            Tableau.expansoes_beta()

        if Tableau.checagem_ramo_fechado():
            if len(Tableau.PilhaDeRamos) > 0:
                Tableau.desempilhar()
            else:
                print('Sequente válido')
                break
        else:
            if len(Tableau.PilhaDeRamos) > 0:
                Tableau.desempilhar()
            else:
                Tableau.valoracao()
                break

    print(f"Ramo depois da expansao: {Tableau.ramo}")

def main():
    antecedentes, sequente = ler_arquivo()
    Tableau = inicializar_tableau(antecedentes, sequente)
    Tableau.marcar_vetor_betas()
    provar_tableau(Tableau)

if __name__ == '__main__':
    main()
