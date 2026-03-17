from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Union

class Clase(Enum):
    EJECUTOR = 0
    ECLIPSE = 1
    SOBERANO = 2

class UnidadesDeCombate(metaclass=ABCMeta):
    def __init__(self, id_combate: Union[str, int], clave_transmision: Union[str, int]):
        self.id_combate = str(id_combate)
        self.clave_transmision = clave_transmision
    
    @abstractmethod
    def get_info(self) -> str:
        pass

class Repuesto:
    def __init__(self, nombre: str, proveedor: str, precio: float):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del repuesto debe ser un texto no vacío.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número positivo.")
        
        self.nombre = nombre
        self.proveedor = proveedor
        self.precio = float(precio)

    def __str__(self):
        return f'Nombre: {self.nombre} | Proveedor: {self.proveedor} | Precio: {self.precio}'

class Almacen:
    def __init__(self, nombre: str, catalogo: Dict[Repuesto, int], ubicacion: str):
        self.nombre = nombre
        self.ubicacion = ubicacion
        
        if not isinstance(catalogo, dict):
            raise TypeError("El catálogo debe ser un diccionario.")
        for rep, cant in catalogo.items():
            if not isinstance(rep, Repuesto):
                raise TypeError("Las claves del catálogo deben ser objetos de tipo Repuesto.")
            if not isinstance(cant, int) or cant < 0:
                raise ValueError("Las cantidades en el catálogo deben ser enteros positivos.")
                
        self.catalogo = catalogo

    def quitar_repuesto(self, repuesto: Repuesto, cantidad: int):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a quitar debe ser un entero positivo.")
        if repuesto not in self.catalogo:
            raise KeyError(f"El repuesto '{repuesto.nombre}' no se encuentra en el almacén '{self.nombre}'.")
        if self.catalogo[repuesto] < cantidad:
            raise ValueError(f"Stock insuficiente de '{repuesto.nombre}' en el almacén '{self.nombre}'. Disponibles: {self.catalogo[repuesto]}, solicitados: {cantidad}.")
        
        self.catalogo[repuesto] -= cantidad 

    def adquirir_repuesto(self, repuesto: Repuesto, cantidad: int):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a adquirir debe ser un entero positivo.")
        
        if repuesto in self.catalogo:
            self.catalogo[repuesto] += cantidad
        else:
            self.catalogo[repuesto] = cantidad

    def consultar_stock(self) -> Dict[str, int]:
        return {repuesto.nombre: cantidad for repuesto, cantidad in self.catalogo.items()}

class Nave(UnidadesDeCombate):
    def __init__(self, id_combate: Union[str, int], clave_transmision: Union[str, int], nombre: str, piezas_repuesto: Dict[Repuesto, int]):
        super().__init__(id_combate, clave_transmision)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la nave debe ser un texto no vacío.")
        if not isinstance(piezas_repuesto, dict):
            raise TypeError("Las piezas de repuesto deben ser un diccionario.")
            
        self.nombre = nombre
        self.piezas_repuesto = piezas_repuesto

    def adquirir_repuesto(self, almacen: Almacen, repuesto: Repuesto, cantidad: int):
        if not isinstance(almacen, Almacen):
            raise TypeError("Se debe proporcionar un objeto de tipo Almacen válido.")
        if not isinstance(repuesto, Repuesto):
            raise TypeError("Se debe proporcionar un objeto de tipo Repuesto válido.")
            
        almacen.quitar_repuesto(repuesto, cantidad)
        
        if repuesto in self.piezas_repuesto:
            self.piezas_repuesto[repuesto] += cantidad
        else:
            self.piezas_repuesto[repuesto] = cantidad

class NaveEstelar(Nave):
    def __init__(self, id_combate: Union[str, int], clave_transmision: Union[str, int], nombre: str, piezas_repuesto: Dict[Repuesto, int], tripulacion: List[str], pasaje: int, clase: Clase):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        if not isinstance(tripulacion, list):
            raise TypeError("La tripulación debe ser una lista.")
        if not isinstance(pasaje, int) or pasaje < 0:
            raise ValueError("El pasaje debe ser un entero no negativo.")
        if not isinstance(clase, Clase):
            raise TypeError("La clase debe ser un Enum de tipo Clase.")
            
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def get_info(self) -> str: 
        repuestos_str = [(pieza.nombre, cantidad) for pieza, cantidad in self.piezas_repuesto.items()]
        return f"Nave estelar: {self.nombre} | Clase: {self.clase.name} | Tripulación: {self.tripulacion} | Pasaje: {self.pasaje} | Piezas de repuesto: {repuestos_str}"
    
class EstacionEspacial(Nave):
    def __init__(self, id_combate: Union[str, int], clave_transmision: Union[str, int], nombre: str, piezas_repuesto: Dict[Repuesto, int], tripulacion: List[str], pasaje: int, ubicacion: str):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def get_info(self) -> str: 
        return f"Estación espacial: {self.nombre} | Tripulación: {self.tripulacion} | Ubicación: {self.ubicacion}"
    
class CazaEstelar(Nave):
    def __init__(self, id_combate: Union[str, int], clave_transmision: Union[str, int], nombre: str, piezas_repuesto: Dict[Repuesto, int], dotacion: int):
        super().__init__(id_combate, clave_transmision, nombre, piezas_repuesto)
        if not isinstance(dotacion, int) or dotacion <= 0:
            raise ValueError("La dotación debe ser un entero positivo.")
        self.dotacion = dotacion

    def get_info(self) -> str: 
        return f"Caza estelar: {self.nombre} | Dotación: {self.dotacion}"
    
class Imperio:
    def __init__(self, nombre: str, unidades: List[UnidadesDeCombate], almacenes: List[Almacen]): 
        if not isinstance(unidades, list) or not all(isinstance(u, UnidadesDeCombate) for u in unidades):
            raise TypeError("Las unidades deben ser una lista de UnidadesDeCombate.")
        if not isinstance(almacenes, list) or not all(isinstance(a, Almacen) for a in almacenes):
            raise TypeError("Los almacenes deben ser una lista de objetos Almacen.")
            
        self.nombre = nombre
        self.unidades = unidades
        self.almacenes = almacenes

    def get_unidades(self) -> List[UnidadesDeCombate]:
        return self.unidades
    
    def get_almacenes(self) -> List[Almacen]: 
        return self.almacenes
    
    def set_unidad(self, unidad: UnidadesDeCombate): 
        if not isinstance(unidad, UnidadesDeCombate):
            raise TypeError("Solo se pueden añadir objetos que hereden de UnidadesDeCombate.")
        self.unidades.append(unidad)

    def __str__(self):
        return f'Nombre: {self.nombre} | Unidades: {[unidad.nombre for unidad in self.unidades]} | Almacenes: {[almacen.nombre for almacen in self.almacenes]}'


if __name__ == '__main__':
    
    bolt = Repuesto('bolt', 'paco', 10)
    wing = Repuesto('wing', 'francisco', 50432)

    milenialfalcon = NaveEstelar('1', 1, 'milenial_falcon', {bolt: 3, wing: 1}, ['Lonely Han', 'Chewbacca'], 1, Clase.EJECUTOR)
    deathstar = EstacionEspacial('2', 2, 'death_star', {bolt: 100}, ['Darth Vader', 'Darth Maul', 'Palpatine'], 2, 'espacio')
    xwing = CazaEstelar('3', 3, 'x-wing', {wing: 2}, 3)

    droiddepot = Almacen('Droid Depot', {bolt: 100, wing: 200}, 'Tatooine')

    imperio = Imperio('imperio estelar', [deathstar, xwing], [droiddepot])

    print("--- INFO IMPERIO ---")
    print(imperio)
    imperio.set_unidad(xwing)
    
    print("\n--- INFO NAVE Y ALMACÉN ---")
    print(milenialfalcon.get_info())
    print("Stock inicial Almacén:", droiddepot.consultar_stock())
    
    milenialfalcon.adquirir_repuesto(droiddepot, bolt, 2)
    
    print("\n--- DESPUÉS DE LA COMPRA ---")
    print(milenialfalcon.get_info())
    print("Stock final Almacén:", droiddepot.consultar_stock())

    # 3. Comprobación de errores (Descomenta estas líneas para verlos en acción)
    print("\n--- FORZANDO ERRORES ---")
    milenialfalcon.adquirir_repuesto(droiddepot, bolt, 5000) # Lanzará ValueError: Stock insuficiente
    caza_falso = CazaEstelar('4', 4, 'caza-roto', {wing: 2}, -5) # Lanzará ValueError por dotación negativa
    imperio.set_unidad("TIE Fighter") # Lanzará TypeError: no es un objeto UnidadesDeCombate