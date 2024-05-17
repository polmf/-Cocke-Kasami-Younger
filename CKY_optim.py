"""
Context Free Grammar: 
We are given a Context Free Grammar G = (V, X, R, S) and a string w, where:

V is a finite set of variables or non-terminal symbols,
X is a finite set of terminal symbols,
R is a finite set of rules,
S is the start symbol, a distinct element of V, and
V and X are assumed to be disjoint sets.
"""

def CKY(non_terminals, terminals, R, init_symbol, w):
    n = len(w)
    
    # Inicializa la tabla CKY
    T = {}
    for i in range(1, n + 1):
        T[(i, i)] = [key for key, value in R.items() if [w[i - 1]] in value]
    
    # Llena la tabla CKY
    for j in range(2, n + 1):
        for i in range(j - 1, 0, -1):
            T[(i, j)] = []
            for k in range(i, j):
                A = T[(i, k)]
                B = T[(k + 1, j)]
                for key, value in R.items():
                    for rule in value:
                        if len(rule) == 2 and rule[0] in A and rule[1] in B:
                            T[(i, j)].append(key)
    
    # Verifica si la palabra es aceptada por la gramática
    if init_symbol in T[(1, n)]:
        print("La palabra '{}' es aceptada por la gramática.".format(w))
        return T
    else:
        print("La palabra '{}' no es aceptada por la gramática.".format(w))
        return T

# Definición de la gramática y símbolo inicial
R = {
    "S": [['a'], ['X', 'A'], ['A', 'X'], ['b']],
    "A": [['R', 'B']],
    "B": [['A', 'X'], ['b'], ['a']],
    "X": [['a']],
    "R": [['X', 'B']]
}
init_symbol = 'S'

# Palabra a reconocer
w = "aabb"

# Ejecución del algoritmo CKY
table = CKY([], [], R, init_symbol, w)


# Imprime la tabla CKY
"""for key, value in table.items():
    print(key, ":", value)"""
