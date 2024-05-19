# lectura de Gramatica en Forma Normal de Chomsky y algoritmo CYK

"""
Context Free Grammar: 
We are given a Context Free Grammar G = (V, X, R, S) and a string w, where:

V is a finite set of variables or non-terminal symbols,
X is a finite set of terminal symbols,
R is a finite set of rules,
S is the start symbol, a distinct element of V, and
V and X are assumed to be disjoint sets.
"""
import random
import string

non_terminals = ['S', 'F', 'A', 'B', 'C', 'Q']
terminals = ['a', 'b', 'c', 'q', 'z']
 
# Rules of the grammar
R = {
    "S": [['A', 'B', 'C'], ['Q']],
    "F": [['B', 'Q']],
    "A": [['a']],
    "B": [['b']],
    "C": [['c']],
    "Q": [['q']]
}

init_symbol = 'S'

def get_new_non_term(new_non_terms):
    available_non_terms = set(string.ascii_uppercase) - new_non_terms
    if not available_non_terms:
        # Si no hay letras no terminales disponibles, agrega nuevas letras al conjunto
        new_non_terms = set()
        available_non_terms = set(string.ascii_uppercase)
        
    new_non_term = random.choice(list(available_non_terms))
    new_non_terms.add(new_non_term)
    return new_non_term

def simplificar_gramatica(init_symbol, gramatica):
    # Encuentra todas las reglas que son idénticas y unifica
    reglas_identicas = {}
    for clave, reglas in list(gramatica.items()):
        reglas_tupla = tuple(tuple(regla) for regla in reglas)
        if reglas_tupla not in reglas_identicas:
            reglas_identicas[reglas_tupla] = clave
        else:
            clave_existente = reglas_identicas[reglas_tupla]
            for c, rs in gramatica.items():
                gramatica[c] = [[clave_existente if s == clave else s for s in regla] for regla in rs]
            del gramatica[clave]
    
    # Elimina las claves no utilizadas
    usados = {init_symbol}
    cambio = True
    while cambio:
        cambio = False
        for clave, reglas in gramatica.items():
            for regla in reglas:
                for simbolo in regla:
                    if simbolo in gramatica and simbolo not in usados:
                        usados.add(simbolo)
                        cambio = True
    
    for clave in list(gramatica.keys()):
        if clave not in usados:
            del gramatica[clave]

    return gramatica



def transformar(non_terminals, terminals, init_symbol, R):
    R = R.copy()
    nuevos_no_terminales = {}
    new_non_terms = set(non_terminals)
    
    for lhs, rule in list(R.items()):
        new_rhs = []
        for rhs in rule:
            if len(rhs) == 1 and rhs[0] in non_terminals:
                R[lhs].extend(R[rhs[0]])
            elif len(rhs) == 2:
                if rhs[0] not in non_terminals and rhs[0] in terminals:
                    nuevo_nt = get_new_non_term(new_non_terms)
                    nuevos_no_terminales[nuevo_nt] = [[rhs[0]]]
                    rhs[0] = nuevo_nt
                if rhs[1] not in non_terminals and rhs[1] in terminals:
                    nuevo_nt = get_new_non_term(new_non_terms)
                    nuevos_no_terminales[nuevo_nt] = [[rhs[1]]]
                    rhs[1] = nuevo_nt
                new_rhs.append(rhs)
            elif len(rhs) > 2:
                while len(rhs) > 2:
                    new_key = get_new_non_term(new_non_terms)
                    nuevos_no_terminales[new_key] = [[rhs[1]] + rhs[2:]]
                    rhs = [rhs[0], new_key]
                new_rhs.append(rhs)
            else:
                new_rhs.append(rhs)
        R[lhs] = new_rhs
    
    R.update(nuevos_no_terminales)
    
    R = simplificar_gramatica(init_symbol, R)

    return R

def gramatica_CFN(non_terminals, terminals, R):
    
    for lhs, rule in R.items():
        for rhs in rule:
            # If a terminal is found
            if len(rhs) == 1:
                if rhs[0] not in terminals:
                    return False
                
            if len(rhs) == 2:
                if rhs[0] not in non_terminals or rhs[1] not in non_terminals:
                    return False

            if len(rhs) >= 3:
                return False
    
    return True


def CKY(non_terminals, terminals, R, init_symbol, w):
    n = len(w)
    
    gramatica_correcte = gramatica_CFN(non_terminals, terminals, R)

    if not gramatica_correcte:
        R = transformar(non_terminals, terminals, init_symbol, R)
    
    T = {}           
    for j in range(1, n+1):
        i = 1
        while j <= n:
            if i == j:
                val = [key for key, value in R.items() if [w[i-1]] in value]                       
                T[(i, j)] = val
                
            else:
                val = []
                for k in range(i, j):
                    if k+1 <= j:
                        regla_A = T[(i, k)]
                        regla_B = T[(k+1, j)]
                        
                        for key, value in R.items():
                            for regla_a in regla_A:
                                for regla_b in regla_B:
                                    if [regla_a, regla_b] in value:
                                        val.append(key)
                        
                T[(i, j)] = val
                
            i += 1
            j += 1
            
    if init_symbol in T[(1, n)]:
        print("La palabra '{}' es aceptada por la gramática.".format(w))
        return T
    else:
        print("La palabra '{}' no es aceptada por la gramática.".format(w))
        return T

w = 'az'

non_terminals = ['S', 'F', 'A', 'B', 'C', 'Q']
terminals = ['a', 'b', 'c', 'f', 'q', 'z']

R = {
    "S": [['A', 'z'], ['F']],
    "F": [['B', 'A', 'Q'], ['C', 'z']],
    "A": [['a']],
    "B": [['b']],
    "C": [['c']],
    "Q": [['q'], ['C']]
}

table = CKY(non_terminals, terminals, R, init_symbol, w)

# Imprime la tabla CKY
"""for key, value in table.items():
    print(key, ":", value)"""