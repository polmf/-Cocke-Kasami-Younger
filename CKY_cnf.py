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
import sys


def parse_grammar(grammar_text):
    """Parse the grammar from a given text.
    
    Args:
        grammar_text (str): Grammar rules in CNF, one per line.
        
    Returns:
        dict: Dictionary representation of the grammar.
    """
    grammar = {}
    for line in grammar_text.strip().split('\n'):
        if '->' in line:
            head, bodies = line.split('->')
            head = head.strip()
            bodies = bodies.strip().split('|')
            
            if head not in grammar:
                grammar[head] = []
            
            for body in bodies:
                if len(body) > 1:
                    llista_bodies = [regla for regla in body.strip()]
                    grammar[head].append(llista_bodies)
                else:
                    grammar[head].append(body.strip().split())
                    
    return grammar

def get_new_non_term(new_non_terms):
    """
    Aquesta funcio rep els no terminals i genera un nou
    
    Parameters:
        new_non_terms (set): Conjunt de no terminals
    
    Returns:
        str: Retorna un nou no terminal
         
    """
        
    available_non_terms = set(string.ascii_uppercase) - new_non_terms
    if not available_non_terms:
        # Si no hi ha no terminals disponibles, es creen de nous
        # Si no hi ha no terminals disponibles, es creen de nous
        new_non_terms = set()
        available_non_terms = set([chr(i) + chr(j) for i in range(65, 91) for j in range(65, 91)]) 
        
    new_non_term = random.choice(list(available_non_terms))
    new_non_terms.add(new_non_term)
    return new_non_term

def simplificar_gramatica(init_symbol, gramatica):
    """
    Aquesta funció s'encarrega d'ordenar la gramàtica i que s'hagi generat tot correctament
    
    Parameters:
        init_symbol (str): Símbol inicial
        gramatica (dict): Diccionari de la gramàtica
        
    Returns:
        dict: Retorna la gramàtica simplificada
    """
    reglas_identicas = {}
    for clave, reglas in list(gramatica.items()):
        reglas_tupla = tuple(tuple(regla) for regla in reglas) # Convertir a tupla per poder comparar
        if reglas_tupla not in reglas_identicas: # Si no s'ha vist abans, es guarda
            reglas_identicas[reglas_tupla] = clave 
        else: # Si ja s'ha vist abans, es reemplaça per la clau existent
            clave_existente = reglas_identicas[reglas_tupla]
            for c, rs in gramatica.items(): # Reemplaçar la clau en totes les regles
                gramatica[c] = [[clave_existente if s == clave else s for s in regla] for regla in rs] 
            del gramatica[clave] # Eliminar la clau actual
    
    # Elimina las claus no utilitzades
    # Elimina las claus no utilitzades
    usados = {init_symbol}
    cambio = True
    while cambio: # Mentre hi hagi canvis
        cambio = False
        for clave, reglas in gramatica.items(): # Recorrer totes les regles
            for regla in reglas: 
                for simbolo in regla: 
                    if simbolo in gramatica and simbolo not in usados: # Si el símbol no s'ha vist abans
                        usados.add(simbolo) # Afegir-lo a la llista de símbols vistos
                        cambio = True
    
    for clave in list(gramatica.keys()):
        if clave not in usados: # Si la clau no s'ha vist abans, eliminar-la
            del gramatica[clave] 

    return gramatica



def transformar(non_terminals, terminals, init_symbol, R):
    """
    Recorre totes les regles i comprova que les unitàries siguin terminals i les binàries no terminals.
    A més, assegura't que les regles només siguin unitàries o binàries.
    
    Parameters:
        non_terminals (set): Conjunt de no terminals
        terminals (set): Conjunt de terminals
        init_symbol (str): Símbol inicial
        R (dict): Diccionari de la gramàtica
        
    Returns:
        dict: Retorna la gramàtica transformada
    """
    
    nova_R = R.copy() # Copiar la gramàtica per no modificar l'original 
    nuevos_no_terminales = {} # Diccionari per guardar els nous no terminals
    new_non_terms = set(non_terminals) # Conjunt de no terminals nous
    
    for lhs, rule in list(nova_R.items()): # Recorrer totes les regles
        new_rhs = [] # Llista per guardar les noves regles
        for rhs in rule: # Recorrer totes les regles de la regla
            
            if len(rhs) == 1 and rhs[0] in non_terminals: # Si la regla és unitària i és un no terminal
                nova_R[lhs].extend(nova_R[rhs[0]]) # Afegir les regles del no terminal a la regla actual
            
            elif len(rhs) == 2: # Si la regla és binària
                if rhs[0] not in non_terminals and rhs[0] in terminals: # Si el primer element és un terminal
                    nuevo_nt = get_new_non_term(new_non_terms) # Generar un nou no terminal
                    nuevos_no_terminales[nuevo_nt] = [[rhs[0]]] # Afegir la nova regla al diccionari
                    rhs[0] = nuevo_nt # Reemplaçar el terminal pel nou no terminal
                    
                if rhs[1] not in non_terminals and rhs[1] in terminals: # Si el segon element és un terminal
                    nuevo_nt = get_new_non_term(new_non_terms) # Generar un nou no terminal
                    nuevos_no_terminales[nuevo_nt] = [[rhs[1]]] # Afegir la nova regla al diccionari
                    rhs[1] = nuevo_nt # Reemplaçar el terminal pel nou no terminal
                new_rhs.append(rhs)
                
            elif len(rhs) > 2: # Si la regla té més de dos elements
                while len(rhs) > 2: # Mentre la regla tingui més de dos elements
                    new_key = get_new_non_term(new_non_terms) # Generar un nou no terminal 
                    nuevos_no_terminales[new_key] = [[rhs[1]] + rhs[2:]] # Afegir la nova regla al diccionari
                    rhs = [rhs[0], new_key] # Reemplaçar la regla per la nova regla
                new_rhs.append(rhs)
                
            else: # Si la regla no és unitària ni binària
                new_rhs.append(rhs) # Afegir la regla a la llista de regles
                
        nova_R[lhs] = new_rhs # Reemplaçar les regles de la clau per les noves regles
     
    nova_R.update(nuevos_no_terminales) # Afegir els nous no terminals a la gramàtica
    
    nova_R = simplificar_gramatica(init_symbol, nova_R) # Simplificar la gramàtica

    return new_non_terms, nova_R

def gramatica_CFN(non_terminals, terminals, R):
    """
    Recorre totes les regles i comprova que les unitàries siguin terminals i les binàries no terminals.
    A més, assegura que les regles només siguin unitàries o binàries.
    
    Parameters:
        non_terminals (set): Conjunt de no terminals
        terminals (set): Conjunt de terminals
        R (dict): Diccionari de la gramàtica
        
    Returns:
        bool: Retorna True si la gramàtica és correcta, False si no ho és
    """
    
    for lhs, rule in R.items():
        for rhs in rule:
            if len(rhs) == 1: # si trobem una regla unitària
                if rhs[0] not in terminals:
                    return False
                
            if len(rhs) == 2: # si trobem una regla binària
                if rhs[0] not in non_terminals or rhs[1] not in non_terminals:
                    return False

            if len(rhs) >= 3: # si trobem una regla amb més de dos elements
                return False
    
    return True


def CKY(R, w):
    """
    Aquesta funció implementa l'algoritme CKY per determinar si una paraula w pertany al llenguatge generat per una gramàtica G.
    
    Rep com a paràmetres:
    - R: un diccionari que representa la gramàtica en Forma Normal de Chomsky.
    - w: una paraula que volem analitzar.
    
    Retorna:
    - T: una taula que conté les regles de producció que s'han aplicat per generar la paraula w.
    """
    
    n = len(w)
    
    init_symbol = next(iter(R))
    non_terminals = set()
    terminals = set()
    non_terminals.add(init_symbol)

    # Recorrem tota la gramàtica per trobar els no terminals i terminals
    for rules in R.values():
        for rule in rules:
            for symbol in rule:
                if symbol.isupper():
                    non_terminals.add(symbol)
                elif symbol.islower():
                    terminals.add(symbol)
    
    gramatica_correcte = gramatica_CFN(non_terminals, terminals, R)
    
    if not gramatica_correcte:
        print('La gramàtica no està en forma normal de Chomsky')
        while gramatica_correcte == False:
            non_terminals, R = transformar(non_terminals, terminals, init_symbol, R)
            gramatica_correcte = gramatica_CFN(non_terminals, terminals, R)
        print('La gramàtica ha estat corregida. Queda de la següent forma:')
        for keys, rules in R.items():
            print(keys, "->", rules)
    
    else:
        print('La gramàtica és correcta')

    if not gramatica_correcte:
        print('La gramàtica no està en forma normal de Chomsky')
        R = transformar(non_terminals, terminals, init_symbol, R)
        print('La gramàtica ha estat corregida. Queda de la següent forma:')
        for keys, rules in R.items():
            print(keys, "->", rules)
        
    
    T = {}           
    for j in range(1, n+1): # recorrem la paraula
        i = 1
        while j <= n:
            if i == j:
                # si la paraula té una sola lletra, busquem la regla que la conté
                T[(i, j)] = [key for key, value in R.items() if [w[i-1]] in value]                       
                
            else:
                val = []
                for k in range(i, j):
                    regla_A = T[(i, k)] # regles de la part esquerra
                    regla_B = T[(k+1, j)] # regles de la part dreta
                        
                    for key, value in R.items(): # recorrem totes les regles de la gramàtica
                        for regla_a in regla_A: # recorrem les regles de la part esquerra
                            for regla_b in regla_B: # recorrem les regles de la part dreta
                                if [regla_a, regla_b] in value: # si trobem una regla que contingui les dues parts
                                    val.append(key)
                        
                T[(i, j)] = val # afegim les regles a la taula
                
            i += 1
            j += 1
            
    if init_symbol in T[(1, n)]:
        print("La palabra '{}' es aceptada por la gramática.".format(w))
        return R
    else:
        print("La palabra '{}' no es aceptada por la gramática.".format(w))
        return R

# llegim la gramàtica del fitxer de text passada per paràmetre
def main():
    """Funció principal per llegir fitxers d’entrada de gramàtica i paraules i determinar si la paraula es troba en l’idioma."""
    if len(sys.argv) != 2:
        print("Us: python cky.py <grammar_file>")
        sys.exit(1)
    
    grammar_file = sys.argv[1]
    
    # Read grammar from file
    with open(grammar_file, 'r') as f:
        grammar_text = f.read()
    R = parse_grammar(grammar_text)
    
    while True:
        word = input("Introdueix la paraula a analitzar: ")
        
        R, table = CKY(R, str(word))
        
        response = input("Vols continuar? (s/n): ")
        
        if response.lower() != 's':
            break

if __name__ == "__main__":
    main()