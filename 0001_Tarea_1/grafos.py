# Clase para los nombres de las acciones
class Accion:
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre


# Clase para los nombres de las salas
class Sala:
    def __init__(self, nombre, acciones):
        self.nombre = nombre
        self.acciones = acciones

    def __str__(self):
        return self.nombre


# Clase para definir las funciones del problema, en este caso regresar si se llegó al objetivo y las acciones resultado
class Problema:
    def __init__(self, sala_inicial, salas_objetivos, acciones, costes=None, heuristicas=None):
        self.sala_inicial = sala_inicial
        self.salas_objetivos = salas_objetivos
        self.acciones = acciones
        self.costes = costes
        self.heuristicas = heuristicas
        self.infinito = 99999
        if not self.costes:
            self.costes = {}
            for sala in self.acciones.keys():
                self.costes[sala] = {}
                for accion in self.acciones[sala].keys():
                    self.costes[sala][accion] = 1
        if not self.heuristicas:
            self.heuristicas = {}
            for sala in self.acciones.keys():
                self.heuristicas[sala] = {}
                for objetivo in self.salas_objetivos:
                    self.heuristicas[sala][objetivo] = self.infinito

    def __str__(self):
        msg = "Sala Inicial: {0} -> Objetivos: {1}"
        return msg.format(self.sala_inicial.nombre, self.salas_objetivos)

    def es_objetivo(self, sala):
        return sala in self.salas_objetivos

    def resultado(self, sala, accion):
        if sala.nombre not in self.acciones.keys():
            return None
        acciones_sala = self.acciones[sala.nombre]
        if accion.nombre not in acciones_sala.keys():
            return None
        return acciones_sala[accion.nombre]
    
    def coste_accion(self, sala, accion):
        if sala.nombre not in self.costes.keys():
            return self.infinito
        costes_sala = self.costes[sala.nombre]
        if accion.nombre not in costes_sala.keys():
            return self.infinito
        return costes_sala[accion.nombre]
    
    def coste_camino(self, nodo):
        total = 0
        while nodo.padre:
            total += self.coste_accion(nodo.padre.sala, nodo.accion)
            nodo = nodo.padre
        return total


# Clase que inicializa los nodos, con la función para expandirlos cuando se exploran
class Nodo:
    def __init__(self, sala, accion=None, acciones=None, padre=None):
        self.sala = sala
        self.accion = accion
        self.acciones = acciones
        self.padre = padre
        self.hijos = []
        self.coste = 0
        self.heuristicas = {}
        self.valores = {}
        self.alfa = 0
        self.beta = 0

    def __str__(self):
        return self.sala.nombre

    def expandir(self, problema):
        self.hijos = []
        if not self.acciones:
            if self.sala.nombre not in problema.acciones.keys():
                return self.hijos
            self.acciones = problema.acciones[self.sala.nombre]
        for accion in self.acciones.keys():
            accion_hijo = Accion(accion)
            nueva_sala = problema.resultado(self.sala, accion_hijo)
            acciones_nuevo = {}
            if nueva_sala.nombre in problema.acciones.keys():
                acciones_nuevo = problema.acciones[nueva_sala.nombre]
            hijo = Nodo(nueva_sala, accion_hijo, acciones_nuevo, self)
            coste = self.padre.coste if self.padre else 0
            coste += problema.coste_accion(self.sala, accion_hijo)
            hijo.coste = coste
            hijo.heuristicas = problema.heuristicas[hijo.sala.nombre]
            hijo.valores = {sala: heuristica+hijo.coste
                            for sala, heuristica
                            in hijo.heuristicas.items()}
            self.hijos.append(hijo)
        return self.hijos
    
    def hijo_mejor(self, problema, metrica='valor', criterio='menor'):
        if not self.hijos:
            return None
        mejor = self.hijos[0]
        for hijo in self.hijos:
            for objetivo in problema.salas_objetivos:
                if metrica == 'valor':
                    valor_hijo = hijo.valores[objetivo.nombre]
                    valor_mejor = mejor.valores[objetivo.nombre]
                    if (criterio == 'menor' and valor_hijo < valor_mejor):
                        mejor = hijo
                    elif (criterio == 'mayor' and valor_hijo > valor_mejor):
                        mejor = hijo
                elif metrica == 'heuristica':
                    heuristica_hijo = hijo.heuristicas[objetivo.nombre]
                    heuristica_mejor = mejor.heuristicas[objetivo.nombre]
                    if (criterio == 'menor' and heuristica_hijo < heuristica_mejor):
                        mejor = hijo
                    elif (criterio == 'mayor' and heuristica_hijo > heuristica_mejor):
                        mejor = hijo
                elif metrica == 'coste':
                    coste_camino_hijo = problema.coste_camino(hijo)
                    coste_camino_mejor = problema.coste_camino(mejor)
                    if (criterio == 'menor' and coste_camino_hijo < coste_camino_mejor):
                        mejor = hijo
                    elif (criterio == 'mayor' and coste_camino_hijo > coste_camino_mejor):
                        mejor = hijo
                elif metrica == 'alfa':
                    if (criterio == 'menor' and hijo.alfa < mejor.alfa):
                        mejor = hijo
                    elif (criterio == 'mayor' and hijo.alfa > mejor.alfa):
                        mejor = hijo
                elif metrica == 'beta':
                    if (criterio == 'menor' and hijo.beta < mejor.beta):
                        mejor = hijo
                    elif (criterio == 'mayor' and hijo.beta > mejor.beta):
                        mejor = hijo
        return mejor


# Declaraciones, comenzando con las acciones
if __name__ == '__main__':
    accN = Accion('adelante')
    accS = Accion('atras')
    accE = Accion('derecha')
    accO = Accion('izquierda')

# Declarar salas que existen con sus posibles acciones
    living = Sala('Sala', [accN, accE])
    corridor = Sala('Pasillo', [accN, accS, accO])
    bedroom = Sala('Cuarto', [accS])
    bathroom = Sala('Baño', [accE])
    kitchen = Sala('Cocina', [accO])

# Declarar qué movimientos llevan a qué salas
    movimientos = {'Sala': {'adelante': corridor,
                            'derecha': kitchen},
                   'Pasillo': {'adelante': bedroom,
                               'atras': living,
                               'izquierda': bathroom},
                   'Cuarto': {'atras': corridor},
                   'Baño': {'derecha': corridor},
                   'Cocina': {'izquierda': living}}
