import random
import string

def get_new_non_term(new_non_terms):
    available_non_terms = set(string.ascii_uppercase) - new_non_terms
    if not available_non_terms:
        # Si no hay letras no terminales disponibles, agrega nuevas letras al conjunto
        new_non_terms = set()
        available_non_terms = set(string.ascii_uppercase)
        
    new_non_term = random.choice(list(available_non_terms))
    new_non_terms.add(new_non_term)
    return new_non_term

def simplificar_gramatica(gramatica):
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
    usados = {'S'}
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



def remove_unit_rules(non_terminals, terminals, R):
    R = R.copy()
    claves_para_eliminar = []
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
    
    R = simplificar_gramatica(R)

    return R

non_terminals = ['S', 'F', 'A', 'B', 'C', 'Q']
terminals = ['a', 'b', 'c', 'f', 'q', 'z']

rules = {
    "S": [['A', 'B'], ['F']],
    "F": [['B', 'A', 'Q'], ['C', 'z']],
    "A": [['a']],
    "B": [['b']],
    "C": [['c']],
    "Q": [['q'], ['C']]
}

new_rules = remove_unit_rules(non_terminals, terminals, rules)
print(new_rules)
