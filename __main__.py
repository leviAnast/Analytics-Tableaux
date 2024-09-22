# << alunos integrantes da equipe: >>
# Francisco Levi Souza Anastácio 538536
# Andreza Honório Magalhães 515185

from modulos.Tableau import *
import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ler_arquivo(): #Leitura do arquivo, armazenamento das fórmulas marcadas no ramo, e marcação inicial do vetor de betas
    global ramo, betas
    arquivo = sys.stdin.read()
    linhas = arquivo.splitlines()
    num_formulas = int(linhas[0].strip())
    antecedentes = [linhas[i].strip() for i in range(1, num_formulas)]
    sequente = linhas[num_formulas].strip()
    
    for formula in antecedentes:
        ramo.append((True, formula))
   
    ramo.append((False, sequente))
    
    for no in ramo:
        betas.append(checagem_beta(no))
    
def provar_tableau():# prova as formulas presentes no ramo
    global ramo, betas, PilhaDeRamos
    
    while True:
        expansoes_alfa() #expande os alfas

        if checagem_ramo_fechado(): #ramo fechou
            if len(PilhaDeRamos) > 0: #caso a pilha não esteja vazia
                desempilhar()
            else: #caso não haja mais elementos na pilha
                print("Sequente válido")
                break
        else: #se o ramo não fechou
            if any(betas): #verifica se há algum beta e se sim, expande
                expansoes_beta()
            else: #caso não haja betas para expansão, imprime valoração
                valoracao()
                break

   
def main():
    ler_arquivo()
    provar_tableau()


if __name__ == '__main__':
    main()