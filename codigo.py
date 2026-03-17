from enum import Enum # Importamos Enum para poder crear Clase, para especificar la clase de nave
from abc import ABCMeta, abstractmethod # Importamos las librerías necesarias para poder hacer la clase y el método abstractos
from typing import Dict, List, Union # Importamos Dict, List, y Union para, al establecer los atributos en los métodos, poder especificar los datos esperados

# Creamos la clase 'Clase' como una enumeración para poder guardar los tipos de nave
class Clase(Enum):
    EJECUTOR = 0
    ECLIPSE = 1
    SOBERANO = 2

# Establecemos una clase general, que le dará el método get_info a todas las naves.
class UnidadesDeCombate(metaclass=ABCMeta):
    def __init__(self, id_combate: Union[str, int], clave_transmision: Union[str, int]): # Gracias a Union, nos aseguramos de que se puedan usar tanto strings como enteros
        self.id_combate = str(id_combate) # Una vez dentro, lo guardamos todo en una string, por si nos han pasado un entero
        self.clave_transmision = clave_transmision
    
    @abstractmethod
    def get_info(self) -> str:
        pass

# Repuesto debemos establecerlo al principio, porque las demás clases tienen que establecerlo como input en sus atributos
class Repuesto:
    def __init__(self, nombre: str, proveedor: str, precio: float):
        # Hacemos una comprobación de que el nombre y el precio introducidos son válidos
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
    def __init__(self, nombre: str, catalogo: Dict[Repuesto, int], ubicacion: str): # Gracias a Dict, decimos que catalogo será un diccionario con una instancia de Repuesto como clave, y un entero como valor
        self.nombre = nombre
        self.ubicacion = ubicacion
        
        # Comprobamos que los elementos introducidos dentro de catalogo sean válidos
        if not isinstance(catalogo, dict):
            raise TypeError("El catálogo debe ser un diccionario.") # Nos aseguramos de que efectivamente es un catálogo
        for rep, cant in catalogo.items(): # Sacamos por separado la clave y el valor para comprobar que son del tipo esperado
            if not isinstance(rep, Repuesto):
                raise TypeError("Las claves del catálogo deben ser objetos de tipo Repuesto.")
            if not isinstance(cant, int) or cant < 0:
                raise ValueError("Las cantidades en el catálogo deben ser enteros positivos.")
                
        self.catalogo = catalogo

    def quitar_repuesto(self, repuesto: Repuesto, cantidad: int):
        # Comprobamos que cantidad es un entero y que la cantidad es positiva
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a quitar debe ser un entero positivo.")
        # Nos aseguramos de que el repuesto que queremos quitar existe
        if repuesto not in self.catalogo:
            raise KeyError(f"El repuesto '{repuesto.nombre}' no se encuentra en el almacén '{self.nombre}'.")
        # Nos aseguramos de que el repuesto que queremos no está agotado
        if self.catalogo[repuesto] < cantidad:
            raise ValueError(f"Stock insuficiente de '{repuesto.nombre}' en el almacén '{self.nombre}'. Disponibles: {self.catalogo[repuesto]}, solicitados: {cantidad}.")
        
        self.catalogo[repuesto] -= cantidad # Si pasa los filtros previos, quitamos de la cantidad del repuesto lo que se haya introducido

    def adquirir_repuesto(self, repuesto: Repuesto, cantidad: int):
        # Comprobamos que la cantidad es positiva y un entero
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad a adquirir debe ser un entero positivo.")
        
        # Comprobamos si ya existe en el catálogo, si existe, añadimos la cantidad, si no, lo creamos con la cantidad
        if repuesto in self.catalogo:
            self.catalogo[repuesto] += cantidad
        else:
            self.catalogo[repuesto] = cantidad

    # Como vamos a devolver el nombre, no el objeto, la clave será una string
    def consultar_stock(self) -> Dict[str, int]:
        return {repuesto.nombre: cantidad for repuesto, cantidad in self.catalogo.items()}

# Nave ya heredará de UnidadesDeCombate, aunque ella no necesita implementar el método get_info() ya que no va a existir 
# una instancia de la clase propiamente sino de las que heredan de ella, pero estas si que necesitarán el método get_info()
class Nave(UnidadesDeCombate):
    def __init__(self, id_combate: Union[str, int], clave_transmision: Union[str, int], nombre: str, piezas_repuesto: Dict[Repuesto, int]):
        super().__init__(id_combate, clave_transmision) # Pasamos los atributos necesarios a la clase padre
        # Comprobamos que nombre sea una string y que no esté vacía 
        if not isinstance(nombre, str) or not nombre.strip(): # Intentamos hacerle el .strip() para que no devuelva nada si está vacía
            raise ValueError("El nombre de la nave debe ser un texto no vacío.")
        # Comprobamos que piezas de repuesto sea un directorio
        if not isinstance(piezas_repuesto, dict):
            raise TypeError("Las piezas de repuesto deben ser un diccionario.")
            
        self.nombre = nombre
        self.piezas_repuesto = piezas_repuesto

    def adquirir_repuesto(self, almacen: Almacen, repuesto: Repuesto, cantidad: int):
        # Comprobamos que el almacén sea instancia de Almacen y el repuesto sea instancia de Repuesto
        if not isinstance(almacen, Almacen):
            raise TypeError("Se debe proporcionar un objeto de tipo Almacen válido.")
        if not isinstance(repuesto, Repuesto):
            raise TypeError("Se debe proporcionar un objeto de tipo Repuesto válido.")
            
        almacen.quitar_repuesto(repuesto, cantidad) # Cada vez que una nave adquiere un repuesto de un almacén, este lo pierde
        
        # Comprobamos si ya disponíamos de ese repuesto para aumentar la cantidad, o si es uno nuevo, lo añadimos al diccionario
        if repuesto in self.piezas_repuesto:
            self.piezas_repuesto[repuesto] += cantidad
        else:
            self.piezas_repuesto[repuesto] = cantidad

class NaveEstelar(Nave): # Hereda de Nave, que a su vez hereda de UnidadesDeCombate, lo que nos da acceso a get_info()
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
        repuestos_str = [(pieza.nombre, cantidad) for pieza, cantidad in self.piezas_repuesto.items()] # Primero, hacemos una lista de tuplas con los atributos de las instancias que nos interesan
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
        # Como unidades y almacenes son listas, debemos iterar internamente para comprobar que todos los elementos son los correctos
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
    print("=== INICIALIZACIÓN DE DATOS ===")
    # Creación de Repuestos y testeo de su método __str__
    motor = Repuesto('Motor Iónico', 'Sienar', 15000.5)
    laser = Repuesto('Cañón Láser', 'Kuat', 5000)
    escudo = Repuesto('Deflector', 'Corellia', 12000.75)
    
    print("Repuestos creados:")
    print(f" - {motor}")
    print(f" - {laser}")

    # Creación de Almacén y testeo de sus métodos
    almacen_imperial = Almacen('Base Starkiller', {motor: 10, laser: 50}, 'Ilum')
    print(f"\nStock inicial Almacén: {almacen_imperial.consultar_stock()}")
    
    # Probamos a adquirir un repuesto que ya existe (Suma cantidad)
    almacen_imperial.adquirir_repuesto(motor, 5)
    # Probamos a adquirir un repuesto nuevo en el almacén (Crea entrada)
    almacen_imperial.adquirir_repuesto(escudo, 20)
    
    print(f"Stock Almacén tras adquisiciones: {almacen_imperial.consultar_stock()}")

    # Creación de Naves (Hijas de UnidadesDeCombate)
    destructor = NaveEstelar('ID-001', 111, 'Devastador', {motor: 2}, ['Darth Vader', 'Almirante Piett'], 5000, Clase.EJECUTOR)
    estacion = EstacionEspacial('ID-002', 222, 'Estrella de la Muerte', {laser: 100}, ['Gran Moff Tarkin'], 10000, 'Órbita de Endor')
    tie_fighter = CazaEstelar('ID-003', 333, 'TIE Avanzado', {laser: 2}, 1)

    print("\n=== MÉTODOS GET_INFO() ===")
    print(destructor.get_info())
    print(estacion.get_info())
    print(tie_fighter.get_info())

    # Transacciones (Naves adquiriendo repuestos de Almacenes)
    print("\n=== COMPRAS DE PARTES ===")
    # Tie fighter compra láseres (ya tenía láseres en su diccionario)
    tie_fighter.adquirir_repuesto(almacen_imperial, laser, 4)
    # Tie fighter compra un escudo (no tenía escudos, se crea la clave en su diccionario)
    tie_fighter.adquirir_repuesto(almacen_imperial, escudo, 1)
    
    print(tie_fighter.get_info())
    print(f"Stock Almacén tras venta a TIE Fighter: {almacen_imperial.consultar_stock()}")

    # Gestión del Imperio Galáctico
    print("\n=== MÉTODOS DE IMPERIO ===")
    imperio = Imperio('Imperio Galáctico', [destructor, estacion], [almacen_imperial])
    print(imperio) # Test de su __str__
    
    imperio.set_unidad(tie_fighter) # Añadimos unidad nueva
    
    print("\nLista de unidades:")
    for u in imperio.get_unidades():
        print(f" -> {u.nombre}")
        
    print("Lista de almacenes:")
    for a in imperio.get_almacenes():
        print(f" -> {a.nombre}")