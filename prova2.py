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
        return True, T
    else:
        return False, T

non_terminals = ["S", "A", "B"]
terminals = ["a", "b", "c"]
 
# Rules of the grammar
R = {
     "S": [['A', 'B']],
     "A": [['a'], ['c']],
     "B": [['b']],
    }

init_symbol = 'S'

# Palabra a reconocer
w = "abab"

# Ejecución del algoritmo CKY
accepted, table = CKY([], [], R, init_symbol, w)

# Imprime el resultado y la tabla CKY
if accepted:
    print("La palabra '{}' es aceptada por la gramática.".format(w))
else:
    print("La palabra '{}' no es aceptada por la gramática.".format(w))

# Imprime la tabla CKY
"""for key, value in table.items():
    print(key, ":", value)"""
