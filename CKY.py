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

non_terminals = ["NP", "Nom", "Det", "AP", 
                  "Adv", "A"]
terminals = ["book", "orange", "man", 
             "tall", "heavy", 
             "very", "muscular"]
 
# Rules of the grammar
R = {
     "S": [['a'], ['X', 'A'], ['A', 'X'], ['b']],
     "A": [['R', 'B']],
     "B": [['A', 'X'], ['b'], ['a']],
     "X": [['a']],
     "R": [['X', 'B']]
    }

init_symbol = 'S'


def CKY(non_terminals, terminals, R, init_symbol, w):
    n = len(w)
    
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

w = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbb'

table = CKY(non_terminals, terminals, R, init_symbol, w)

# Imprime la tabla CKY
"""for key, value in table.items():
    print(key, ":", value)"""