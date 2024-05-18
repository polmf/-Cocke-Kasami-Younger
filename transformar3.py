def transform_rules(non_terminals, terminals, R):
    R = R.copy()  # Crear una copia del diccionario para evitar problemas de modificación durante la iteración
    nuevos_no_terminales = {}  # Diccionario para almacenar nuevos no terminales
    
    for lhs, rule in list(R.items()):
        for rhs in rule:
            if len(rhs) == 2:
                # Verificar si alguno de los símbolos en rhs no es un no terminal
                if rhs[0] not in non_terminals:
                    # Crear un nuevo no terminal
                    nuevo_nt = rhs[0].upper()
                    # Asegurarse de que el nuevo no terminal no existe ya en non_terminals
                    while nuevo_nt in non_terminals:
                        nuevo_nt += "'"
                    # Añadir el nuevo no terminal al diccionario y actualizar las reglas
                    if nuevo_nt not in nuevos_no_terminales:
                        nuevos_no_terminales[nuevo_nt] = [[rhs[0]]]
                    rhs[0] = nuevo_nt
                
                if rhs[1] not in non_terminals:
                    # Crear un nuevo no terminal
                    nuevo_nt = rhs[1].upper()
                    # Asegurarse de que el nuevo no terminal no existe ya en non_terminals
                    while nuevo_nt in non_terminals:
                        nuevo_nt += "'"
                    # Añadir el nuevo no terminal al diccionario y actualizar las reglas
                    if nuevo_nt not in nuevos_no_terminales:
                        nuevos_no_terminales[nuevo_nt] = [[rhs[1]]]
                    rhs[1] = nuevo_nt

    # Añadir los nuevos no terminales a las reglas originales
    R.update(nuevos_no_terminales)

    return R

non_terminals = ['S', 'Z', 'A', 'B', 'C']  # Solo no terminales
terminals = ['a', 'b', 'c', 'd', 'e', 'z']  # Terminales
# Reglas originales
rules = {
    "S": [['A', 'B']],
    "Z": [['C', 'x'], ['z']],
    "A": [['a']],
    "B": [['b']],
    "C": [['c'], ['d'], ['e']],
}

# Transformamos las reglas
new_rules = transform_rules(non_terminals, terminals, rules)

# Mostramos las nuevas reglas
print(new_rules)
