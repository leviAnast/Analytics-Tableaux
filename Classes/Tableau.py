from Classes.SubformulaExtractor import *

class Tableau:
    def __init__(self, antecedentes, sequente):
        self.ramo = [(True, formula) for formula in antecedentes] + [(False, sequente)]
        self.betas = []
        self.PilhaDeRamos = []
        self.checagem_novo_alfa = True

    def expansoes_alfa(self):
        while(self.checagem_novo_alfa):
            self.checagem_novo_alfa = False

            for no in self.ramo.copy():
                if not self.checagem_beta(no) and not self.checagem_atomo(no):
                    marcacao_formula, formula = no
                    conectivo, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)
                    print(f'PRINTANDO FORMULA EXPANDIDA NO MOMENTO: {formula}') #APAGAR DEPOIS
                    alfa1 = subformulas[0]

                    if conectivo != TOKEN_NEG:
                        alfa2 = subformulas[1]
                    else:
                        alfa2 = None

                    if conectivo == TOKEN_AND and marcacao_formula:
                        marcacao_alfa1, marcacao_alfa2 = True, True
                    elif conectivo == TOKEN_OR and not marcacao_formula:
                        marcacao_alfa1, marcacao_alfa2 = False, False
                    elif conectivo == TOKEN_IMPL and not marcacao_formula:
                        marcacao_alfa1, marcacao_alfa2 = True, False
                    elif conectivo == TOKEN_NEG:
                        if marcacao_formula:
                            marcacao_alfa1 = False
                        else:
                            marcacao_alfa1 = True
                    
                    self.ramo.append((marcacao_alfa1, alfa1))
                    self.betas.append(self.checagem_beta((marcacao_alfa1, alfa1)))

                    if conectivo != TOKEN_NEG:
                        self.ramo.append((marcacao_alfa2, alfa2))
                        self.betas.append(self.checagem_beta((marcacao_alfa2, alfa2)))

                    indice_remocao = self.ramo.index(no)
                    self.ramo.pop(indice_remocao)
                    self.betas.pop(indice_remocao)

    def checagem_beta(self, no):
        marcacao, formula = no
        conectivo, _ = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)
            
        if marcacao == True: 
            if conectivo == TOKEN_OR or conectivo == TOKEN_IMPL: 
                return True
                
        if marcacao == False: 
            if conectivo == TOKEN_AND:
                return True
                
        return False

    def expansoes_beta(self):
        for i, beta in enumerate(self.betas):
            if beta == True:
                marcacao_formula, formula = self.ramo[i]
                print(f"PRINTANDO FORMULA EM EXPANSAO BETA: {formula}") #APAGAR DEPOIS
                print(f"PRINTANDO MARCACAO DA FORMULA EM BETA: {marcacao_formula}") #APAGAR DEPOIS
                conectivo, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)
                beta1, beta2 = subformulas
                
                marcacao_expansao1, marcacao_expansao2 = None, None
                    
                if not marcacao_formula:
                    if conectivo == TOKEN_AND:
                        marcacao_expansao1, marcacao_expansao2 = False, False
                elif marcacao_formula:
                    if conectivo == TOKEN_OR:
                        marcacao_expansao1, marcacao_expansao2 = True, True
                    elif conectivo == TOKEN_IMPL:
                            marcacao_expansao1, marcacao_expansao2 = False, True
                    
                self.betas[i] = False
                self.ramo.append((marcacao_expansao1, beta1))
                self.betas.append(self.checagem_beta((marcacao_expansao1, beta1)))
                self.PilhaDeRamos.append([(marcacao_expansao2, beta2), len(self.ramo), self.betas.copy()])

                if not self.checagem_beta((marcacao_expansao1, beta1)):
                    self.checagem_novo_alfa = True

                break

    def marcar_vetor_betas(self):
        self.betas = [False] * len(self.ramo) 
        print(self.betas)
        for i, no in enumerate(self.ramo):
            if self.checagem_beta(no):
                self.betas[i] = True
            else:
                self.betas[i] = False
    
    def desempilhar(self):
        print(f"PRINTANDO PILHA DE RAMOS: {self.PilhaDeRamos}")
        beta2, tamanho_atual_ramo, betas_copia = self.PilhaDeRamos.pop()

        self.betas = betas_copia[:tamanho_atual_ramo]
        self.ramo = self.ramo[:tamanho_atual_ramo]
        self.ramo.append(beta2)
        self.betas.append(self.checagem_beta(beta2))

    def checagem_ramo_fechado(self):
        for i in range(len(self.ramo)):
            marcacao, formula = self.ramo[i]
            
            if self.checagem_atomo(self.ramo[i]):
                if ((not marcacao, formula) in self.ramo) and ((marcacao, formula) in self.ramo):
                    return True
            
            return False
        
    def checagem_atomo(self, no):
        formula = no[1]
        conectivo, _ = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)

        if conectivo == "atom":
            return True
        
        return False
    
    def valoracao(self):
        atomos = {} 

        for i in range(len(self.ramo)):
            marcacao, formula = self.ramo[i]
            if self.checagem_atomo((marcacao, formula)):
                if formula not in atomos:
                    if marcacao:
                        atomos[formula] = True
                    else:
                        atomos[formula] = False

        for formula, marcacao in atomos.items():
            if marcacao == True:
                print(f'T{formula}')
            else:
                print(f'F{formula}')
