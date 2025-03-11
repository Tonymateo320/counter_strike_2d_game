# Clases para el árbol de comportamiento  Tony Mateo 23-eisn-2-044
class Nodo:
    """Clase base para nodos del árbol de comportamiento"""
    def __init__(self):
        self.padre = None
    
    def ejecutar(self, *args, **kwargs):
        """Ejecuta la lógica del nodo"""
        pass

class Selector(Nodo):
    """
    Nodo Selector (OR): ejecuta hijos hasta que uno tenga éxito
    Devuelve True si alguno de los hijos tiene éxito
    """
    def __init__(self, hijos=None):
        super().__init__()
        self.hijos = hijos or []
        for hijo in self.hijos:
            hijo.padre = self
    
    def ejecutar(self, *args, **kwargs):
        for hijo in self.hijos:
            if hijo.ejecutar(*args, **kwargs):
                return True
        return False

class Secuencia(Nodo):
    """
    Nodo Secuencia (AND): ejecuta hijos hasta que uno falle
    Devuelve True solo si todos los hijos tienen éxito
    """
    def __init__(self, hijos=None):
        super().__init__()
        self.hijos = hijos or []
        for hijo in self.hijos:
            hijo.padre = self
    
    def ejecutar(self, *args, **kwargs):
        for hijo in self.hijos:
            if not hijo.ejecutar(*args, **kwargs):
                return False
        return True

class Hoja(Nodo):
    """
    Nodo Hoja: ejecuta una acción concreta
    La función debe devolver True o False
    """
    def __init__(self, funcion):
        super().__init__()
        self.funcion = funcion
    
    def ejecutar(self, *args, **kwargs):
        return self.funcion(*args, **kwargs)

class Invertidor(Nodo):
    """
    Nodo Invertidor: invierte el resultado del hijo
    True -> False, False -> True
    """
    def __init__(self, hijo):
        super().__init__()
        self.hijo = hijo
        self.hijo.padre = self
    
    def ejecutar(self, *args, **kwargs):
        return not self.hijo.ejecutar(*args, **kwargs)

class Repetidor(Nodo):
    """
    Nodo Repetidor: ejecuta el hijo un número específico de veces
    o hasta que falle
    """
    def __init__(self, hijo, veces=None):
        super().__init__()
        self.hijo = hijo
        self.veces = veces  # None significa repetir indefinidamente  Tony Mateo 23-eisn-2-044
        self.hijo.padre = self
    
    def ejecutar(self, *args, **kwargs):
        if self.veces is None:
            # Repetir indefinidamente hasta fallar  Tony Mateo 23-eisn-2-044
            while self.hijo.ejecutar(*args, **kwargs):
                pass
            return True
        else:
            # Repetir un número específico de veces  Tony Mateo 23-eisn-2-044
            for _ in range(self.veces):
                if not self.hijo.ejecutar(*args, **kwargs):
                    return False
            return True

class Paralelo(Nodo):
    """
    Nodo Paralelo: ejecuta todos los hijos y devuelve True
    si al menos n hijos tienen éxito
    """
    def __init__(self, hijos=None, exitos_requeridos=None):
        super().__init__()
        self.hijos = hijos or []
        # Si exitos_requeridos es None, se requiere que todos tengan éxito  Tony Mateo 23-eisn-2-044
        self.exitos_requeridos = exitos_requeridos if exitos_requeridos is not None else len(self.hijos)
        for hijo in self.hijos:
            hijo.padre = self
    
    def ejecutar(self, *args, **kwargs):
        exitos = sum(1 for hijo in self.hijos if hijo.ejecutar(*args, **kwargs))
        return exitos >= self.exitos_requeridos