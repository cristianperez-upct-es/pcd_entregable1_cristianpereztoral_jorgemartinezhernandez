from enum import Enum
from abc import ABCMeta, abstractmethod

class Clase(Enum):
    EJECUTOR = 0
    ECLIPSE = 1
    SOBERANO = 2

class UnidadesDeCombate(metaclass=ABCMeta):
    def __init__(self, id_combate, clave_transmision):
        self.id_combate = id_combate
        self.clave_transmision = clave_transmision
    
    @abstractmethod
    def get_info(self):
        pass

class Nave(UnidadesDeCombate):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto):
        super().__init__(id_combate, clave_transmision)
        self.nombre = nombre
        self.piezas_repuesto = piezas_repuesto


class NaveEstelar(Nave):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto, tripulacion, pasaje, clase):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def get_info(self):
        return f"Nave estelar: {self.nombre} | Clase: {self.clase.name} | Tripulación: {self.tripulacion} | Pasaje: {self.pasaje}"
    
class EstacionEspacial(Nave):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def get_info(self):
        return f"Nave estelar: {self.nombre} | Tripulación: {self.tripulacion} | Ubicación: {self.ubicacion}"
    
class CazaEstelar(Nave):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto, dotacion):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        self.dotacion = dotacion

    def get_info(self):
        return f"Nave estelar: {self.nombre} | Dotación: {self.dotacion}"
    
class Imperio:
    def __init__(self, nombre, unidades, almacen):
        self.nombre = nombre
        self.unidades = unidades
        self.almacen = almacen

class Almacen:
    def __init__(self, nombre, catalogo, ubicacion):
        self.nombre = nombre
        self.catalogo = catalogo
        self.ubicacion = ubicacion

class Repuesto:
    def __init__(self, nombre, proveedor, _cantidad, precio):
        self.nombre = nombre
        self.proveedor = proveedor
        self._cantidad = _cantidad
        self.precio = precio