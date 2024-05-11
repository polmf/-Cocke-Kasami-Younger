
def cky(gramatica, paraula):
    
    n = len(paraula)
    
    # fer una taula nxn
    T = [[[] for j in range(n+1)] for i in range(n+1)]
    
    T[0][0].append(paraula)
    
    
    for pos in range(n):
        
        for i in range(1,n+1):
            for j in range(1,n+1):
                for lhs, rule in gramatica.items():
                    for rhs in rule:
                        paraula = T[i-1][j-1] 
                        if paraula[pos] == rhs: 
                            T[i][j].append(lhs)
                    
    return T

gramatica = {
    'S':[['A']],
    'A':[['a']]
    }

paraula = 'aa'

taula = cky(gramatica, paraula)

for fila in taula:
    print(fila)