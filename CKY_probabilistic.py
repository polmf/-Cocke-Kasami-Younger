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


#######################################
################ CKY ##################
#######################################
 
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

"""#w = 'aabb'

#table = CKY(non_terminals, terminals, R, init_symbol, w)

# Imprime la tabla CKY
for key, value in table.items():
    print(key, ":", value)"""



#######################################
########## CKY PROBABILISTIC ##########
#######################################

R_probabilistic = {
     "S": [(['NP', 'VP'], 0.5), (['NP', 'Vi'], 0.5)],
     "NP": [(['DT', 'NN'], 0.4), (['NP', 'PP'], 0.6)],
     "PP": [(['IN', 'NP'], 1.0)],
     "VP": [(['Vt', 'NP'], 0.4), (['VP', 'PP'], 0.1), (['Vi', 'PP'], 0.5)],
     "Vi": [(['sleeps'], 1.0)],
     "Vt": [(['saw'], 1.0)],
     "DT": [(['the'], 1.0)],
     "NN": [(['man'], 0.7), (['telescope'], 0.1), (['woman'], 0.2)],
     "IN": [(['with'], 0.5), (['in'], 0.5)]
    }

def CKY_prob(R, init_symbol, w):
    n = len(w)
    
    T = {}           
    for j in range(1, n+1):
        i = 1
        while j <= n:
            if i == j:
                
                val = [(key, regla[1]) for key, value in R.items() for regla in value if w[i-1] in regla[0]]                              
                
                T[(i, j)] = max(val, key=lambda x: x[1]) if val else []
                
            else:
                val = []
                for k in range(i, j):
                    if k+1 <= j:
                        regla_A = T[(i, k)]
                        regla_B = T[(k+1, j)]
                        
                        for key, value in R.items():
                            for regla in value:
                                if regla_A and regla_B and [regla_A[0], regla_B[0]] == regla[0]:
                                    probabilitat = regla[1] * regla_A[1] * regla_B[1]
                                    val.append((key, probabilitat))
                        
                T[(i, j)] = max(val, key=lambda x: x[1]) if val else []
            
            i += 1
            j += 1
            
    if init_symbol in T[(1, n)]:
        print("La palabra '{}' es aceptada por la gramática.".format(w))
        return T
    else:
        print("La palabra '{}' no es aceptada por la gramática.".format(w))
        return T

w = 'the woman saw the man with the telescope'.split()
    
table = CKY_prob(R_probabilistic, init_symbol, w)
    
for key, value in table.items():
    print(key, ":", value)