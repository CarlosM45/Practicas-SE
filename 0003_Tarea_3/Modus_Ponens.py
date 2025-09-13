# Modus Ponens es una regla de inferencia que sigue la lógica "Si P, entonces Q" donde intenta probarse primero el antecedente para determinar el resultado
# Es decir: "P es verdadero, por lo tanto, Q también lo es"
# Por ejemplo: "Si saco buenas calificaciones, pasaré el semestre. Saqué buenas calificaciones, por ende, pasaré el semestre"

def modus_ponens(P, Q):
    if P:
        print("Q es verdadero")
    else:
        print("No se puede aplicar Modus Ponens dado que P es falso")


P = True
Q = True
modus_ponens(P, Q)
