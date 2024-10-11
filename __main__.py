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
    
def provar_tableau():
    global ramo, betas, PilhaDeRamos
    
    while True:
       
        expansoes_alfa()

        if checagem_ramo_fechado():
            
            if len(PilhaDeRamos) > 0:
               
                desempilhar()
                
            else:
                print("Sequente válido")
                break
        else:
            beta_expansivel = False
            for i, beta in enumerate(betas):
                if beta:
                    expansoes_beta()
                    beta_expansivel = True
                    break
            
            if not beta_expansivel:
                valoracao()
                break
    print(f'PRINTANDO RAMO APOS TODASSS AS EXPANSÕES {ramo}')
    print(f'PRINTANDO pilhadeRAMOs APOS TODASSS AS EXPANSÕES {PilhaDeRamos}')
    


   
def main():
    ler_arquivo()
    provar_tableau()


if __name__ == '__main__':
    main()