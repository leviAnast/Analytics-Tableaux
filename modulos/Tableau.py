from modulos.SubformulaExtractor import *

ramo = [] #Ramo do Tableau
betas = [] #Marca a existência de fórmulas beta dentro do ramo 
PilhaDeRamos = [] #Armazena as expansões beta2 para próximas expansões dentro do ramo
checagem_novo_alfa = True #Marca a existência de fórmula alfa dentro do ramo

marcacoes_expansoes_alfa = { #mapeia as marcações das expansões alfa de acordo com marcacão e concectivo principal da formula que sofre expansão
    (True, TOKEN_AND): (True, True),
    (True, TOKEN_NEG): (False, None),
    (False, TOKEN_OR): (False, False),
    (False, TOKEN_IMPL): (True, False),
    (False, TOKEN_NEG): (True, None)

}
marcacoes_expansoes_beta = { #mapeia as marcações das expansões beta de acordo com marcacão e concectivo principal da formula que sofre expansão
    (False, TOKEN_AND): (False, False),
    (True, TOKEN_OR): (True, True),
    (True, TOKEN_IMPL): (False, True)
}

def expansoes_alfa(): #Realiza as operações de expansão para fórmulas do tipo alfa
    global ramo, checagem_novo_alfa, marcacoes_expansoes_alfa
    while(checagem_novo_alfa):
        checagem_novo_alfa = False

        for no in ramo.copy():
            if not (checagem_beta(no) or checagem_atomo(no)):
                marcacao_no, formula = no
                conectivo, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)
                alfa1 = subformulas[0]

                if conectivo != TOKEN_NEG:
                    alfa2 = subformulas[1]
                else:
                    alfa2 = None

                marcacao_alfa1, marcacao_alfa2 =  marcacoes_expansoes_alfa.get((marcacao_no, conectivo), (None, None))

                ramo.append((marcacao_alfa1, alfa1))
                betas.append(checagem_beta((marcacao_alfa1, alfa1)))

                if alfa2 is not None and marcacao_alfa2 is not None:
                    ramo.append((marcacao_alfa2, alfa2))
                    betas.append(checagem_beta((marcacao_alfa2, alfa2)))
                
                if not (checagem_beta((marcacao_alfa1, alfa1)) and checagem_beta((marcacao_alfa2, alfa2))):
                    checagem_novo_alfa = True

                indice_remocao = ramo.index(no)
                ramo.pop(indice_remocao)
                betas.pop(indice_remocao)


def checagem_beta(no): #verifica se uma formula no ramo do Tableau é do tipo beta
    marcacao, formula = no
    conectivo, _ = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)
            
    if marcacao: 
        if conectivo == TOKEN_OR or conectivo == TOKEN_IMPL: 
            return True       
    if not marcacao: 
        if conectivo == TOKEN_AND:
            return True
            
    return False

def expansoes_beta(): #Realiza as operações de expansão para fórmulas do tipo beta
    global ramo, betas, checagem_novo_alfa, PilhaDeRamos, marcacoes_expansoes_beta
    for i in range(len(betas)):
        if betas[i]:
            marcacao, formula = ramo[i]
            conectivo, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)
            beta1, beta2 = subformulas
            marcacao_expansao1, marcacao_expansao2 = marcacoes_expansoes_beta.get((marcacao, conectivo), (None, None))

            betas[i] = False
            PilhaDeRamos.append([(marcacao_expansao2, beta2), len(ramo), betas.copy()])
            ramo.append((marcacao_expansao1, beta1))
            betas.append(checagem_beta((marcacao_expansao1, beta1)))
            
            if not checagem_beta((marcacao_expansao1, beta1)):
                checagem_novo_alfa = True
            
            break

def desempilhar(): #Caso haja ainda betas2 para expansão, remove eles da pilha e adiciona ao ramo
    global PilhaDeRamos, betas, ramo
    beta2, tamanho_atual_ramo, betas_copia = PilhaDeRamos.pop() 

    ramo = ramo[:tamanho_atual_ramo]
    betas = betas_copia[:tamanho_atual_ramo]
    ramo.append(beta2)
    betas.append(checagem_beta(beta2))

def checagem_ramo_fechado(): #verifica se o ramo está fechado
    global ramo
    aux_atomos = []
    
    for (marcacao, formula) in ramo:
        if checagem_atomo((marcacao, formula)):
            if ((not marcacao, formula) in aux_atomos):
                return True
            
            aux_atomos.append((marcacao, formula))

    return False

def checagem_atomo(no): #Verifica se uma fórmula passa é ou não um átomo
    formula = no[1]
    conectivo, _ = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)

    if conectivo == "atom":
        return True
    
    return False
   
def valoracao(): #Realiza a operação de printar a valoração dos átomos nas situações de não fechamento de todos os ramos do Tableau
    global ramo 
    
    aux_valoracao = []
 
    for (marcacao, formula) in ramo:
        if checagem_atomo((marcacao, formula)) and (marcacao, formula) not in aux_valoracao:
                aux_valoracao.append((marcacao, formula))
    
    for (marcacao, atomo) in aux_valoracao:
        if marcacao:
            print(f'T{atomo}')
        else:
            print(f'F{atomo}')

    