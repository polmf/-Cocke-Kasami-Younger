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

non_terminals = ["S", "A", "B"]
terminals = ["a", "b", "c"]
 
# Rules of the grammar
R = {
     "S": [['A', 'B'], ],
     "A": [['S'], ['a']],
     "B": [['b']],
    }

init_symbol = 'S'

def transformar(non_termionals, terminals, R):
    
    
    
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
        R = transformar(non_terminals, terminals, R)
    
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

w = 'abab'

table = CKY(non_terminals, terminals, R, init_symbol, w)

# Imprime la tabla CKY
"""for key, value in table.items():
    print(key, ":", value)"""