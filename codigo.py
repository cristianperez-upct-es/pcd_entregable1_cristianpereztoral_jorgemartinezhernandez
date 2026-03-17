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
    
    @abstractmethod # Añadir al esquema
    def get_info(self):
        pass

class Nave(UnidadesDeCombate):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto):
        super().__init__(id_combate, clave_transmision)
        self.nombre = nombre
        self.piezas_repuesto = piezas_repuesto

    def adquirir_repuesto(self, almacen, repuesto, cantidad):
        almacen.quitar_repuesto(repuesto, cantidad)
        self.piezas_repuesto[repuesto] += cantidad

class NaveEstelar(Nave):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto, tripulacion, pasaje, clase):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def get_info(self): # Añadir al esquema
        return f"Nave estelar: {self.nombre} | Clase: {self.clase.name} | Tripulación: {self.tripulacion} | Pasaje: {self.pasaje} | Piezas de repuesto: {[(pieza.nombre, cantidad) for pieza, cantidad in self.piezas_repuesto.items()]}"
    
class EstacionEspacial(Nave):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto, tripulacion, pasaje, ubicacion):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def get_info(self): # Añadir al esquema
        return f"Nave estelar: {self.nombre} | Tripulación: {self.tripulacion} | Ubicación: {self.ubicacion}"
    
class CazaEstelar(Nave):
    def __init__(self, id_combate, clave_transmision, nombre, piezas_repuesto, dotacion):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        self.dotacion = dotacion

    def get_info(self): # Añadir al esquema
        return f"Nave estelar: {self.nombre} | Dotación: {self.dotacion}"
    
class Imperio:
    def __init__(self, nombre, unidades, almacenes): # Añadir al esquema (almacenes lista) 
        self.nombre = nombre
        self.unidades = unidades
        self.almacenes = almacenes

    def get_unidades(self):
        return self.unidades
    
    def get_almacenes(self): # Añadir al esquema
        return self.almacenes
    
    def set_unidad(self, unidad): # Añadir al esquema los atributos
        self.unidades.append(unidad)

    def __str__(self):
        return f'Nombre: {self.nombre} | Unidades: {[unidad.nombre for unidad in self.unidades]} | Almacenes: {[almacen.nombre for almacen in self.almacenes]}'

class Almacen:
    def __init__(self, nombre, catalogo, ubicacion):
        self.nombre = nombre
        self.catalogo = catalogo
        self.ubicacion = ubicacion

    def quitar_repuesto(self, repuesto, cantidad): # Añadir al esquema
        self.catalogo[repuesto] -= cantidad 

    def adquirir_repuesto(self, repuesto, cantidad):
        self.catalogo[repuesto] += cantidad

    def consultar_stock(self):
        return self.catalogo

class Repuesto:
    def __init__(self, nombre, proveedor, precio): # Añadir al esquema
        self.nombre = nombre
        self.proveedor = proveedor
        self.precio = precio

    def __str__(self):
        return f'Nombre: {self.nombre} | Proveedor: {self.proveedor} |  Precio: {self.precio}'
    
if __name__ == '__main__':
    
    bolt = Repuesto('bolt', 'paco', 10)
    wing = Repuesto('wing', 'francisco', 50432)

    milenialfalcon = NaveEstelar('1', 1, 'milenial_falcon',{bolt:3, wing:1}, ['Lonely Han', 'Chewbacca'], 1, Clase.EJECUTOR)
    deathstar = EstacionEspacial('2', 2, 'death_star', {bolt: 100}, ['Darth Vader', 'Death Moul', 'Palpatin'], 2, 'espacio')
    xwing = CazaEstelar('3', 3, 'x-wing', {wing:2}, 3)

    droiddepot = Almacen('Droid Depot', {bolt: 100, wing:200}, 'Tatooine')

    imperio = Imperio('imperio estelar', [deathstar, xwing], [droiddepot])

    # Imperio
    print(imperio)
    print(imperio.get_unidades())
    print(imperio.get_almacenes())
    imperio.set_unidad(xwing)
    print(imperio.get_unidades())

    # NaveEstelar / Almacén
    print(milenialfalcon.get_info())
    print(droiddepot.consultar_stock())
    milenialfalcon.adquirir_repuesto(droiddepot, bolt, 2)
    print(milenialfalcon.get_info())
    print(droiddepot.consultar_stock())