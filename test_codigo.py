import pytest
from codigo import Clase, Repuesto, Almacen, Nave, NaveEstelar, EstacionEspacial, CazaEstelar, Imperio


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def motor():
    return Repuesto('Motor Iónico', 'Sienar', 15000.5)

@pytest.fixture
def laser():
    return Repuesto('Cañón Láser', 'Kuat', 5000)

@pytest.fixture
def escudo():
    return Repuesto('Deflector', 'Corellia', 12000.75)

@pytest.fixture
def almacen(motor, laser):
    return Almacen('Base Starkiller', {motor: 10, laser: 50}, 'Ilum')

@pytest.fixture
def nave_estelar(motor):
    return NaveEstelar('ID-001', 111, 'Devastador', {motor: 2},
                       ['Darth Vader', 'Almirante Piett'], 5000, Clase.EJECUTOR)

@pytest.fixture
def estacion(laser):
    return EstacionEspacial('ID-002', 222, 'Estrella de la Muerte', {laser: 100},
                            ['Gran Moff Tarkin'], 10000, 'Órbita de Endor')

@pytest.fixture
def caza(laser):
    return CazaEstelar('ID-003', 333, 'TIE Avanzado', {laser: 2}, 1)

@pytest.fixture
def imperio(nave_estelar, estacion, almacen):
    return Imperio('Imperio Galáctico', [nave_estelar, estacion], [almacen])


# ─── Repuesto ─────────────────────────────────────────────────────────────────

class TestRepuesto:
    def test_creacion_correcta(self, motor):
        assert motor.nombre == 'Motor Iónico'
        assert motor.proveedor == 'Sienar'
        assert motor.precio == 15000.5

    def test_precio_se_convierte_a_float(self):
        r = Repuesto('Pieza', 'Proveedor', 100)
        assert isinstance(r.precio, float)

    def test_nombre_vacio_lanza_error(self):
        with pytest.raises(ValueError):
            Repuesto('', 'Proveedor', 100)

    def test_nombre_solo_espacios_lanza_error(self):
        with pytest.raises(ValueError):
            Repuesto('   ', 'Proveedor', 100)

    def test_precio_negativo_lanza_error(self):
        with pytest.raises(ValueError):
            Repuesto('Pieza', 'Proveedor', -1)

    def test_precio_cero_es_valido(self):
        r = Repuesto('Pieza', 'Proveedor', 0)
        assert r.precio == 0.0

    def test_str(self, motor):
        resultado = str(motor)
        assert 'Motor Iónico' in resultado
        assert 'Sienar' in resultado
        assert '15000.5' in resultado


# ─── Almacen ──────────────────────────────────────────────────────────────────

class TestAlmacen:
    def test_creacion_correcta(self, almacen):
        assert almacen.nombre == 'Base Starkiller'
        assert almacen.ubicacion == 'Ilum'

    def test_catalogo_no_dict_lanza_error(self, motor):
        with pytest.raises(TypeError):
            Almacen('Base', [motor], 'Lugar')

    def test_catalogo_clave_invalida_lanza_error(self):
        with pytest.raises(TypeError):
            Almacen('Base', {'no_repuesto': 5}, 'Lugar')

    def test_catalogo_cantidad_negativa_lanza_error(self, motor):
        with pytest.raises(ValueError):
            Almacen('Base', {motor: -1}, 'Lugar')

    def test_consultar_stock(self, almacen, motor, laser):
        stock = almacen.consultar_stock()
        assert stock['Motor Iónico'] == 10
        assert stock['Cañón Láser'] == 50

    def test_adquirir_repuesto_existente(self, almacen, motor):
        almacen.adquirir_repuesto(motor, 5)
        assert almacen.consultar_stock()['Motor Iónico'] == 15

    def test_adquirir_repuesto_nuevo(self, almacen, escudo):
        almacen.adquirir_repuesto(escudo, 20)
        assert almacen.consultar_stock()['Deflector'] == 20

    def test_adquirir_cantidad_invalida_lanza_error(self, almacen, motor):
        with pytest.raises(ValueError):
            almacen.adquirir_repuesto(motor, 0)
        with pytest.raises(ValueError):
            almacen.adquirir_repuesto(motor, -3)

    def test_quitar_repuesto(self, almacen, motor):
        almacen.quitar_repuesto(motor, 3)
        assert almacen.consultar_stock()['Motor Iónico'] == 7

    def test_quitar_repuesto_no_existente_lanza_error(self, almacen, escudo):
        with pytest.raises(KeyError):
            almacen.quitar_repuesto(escudo, 1)

    def test_quitar_stock_insuficiente_lanza_error(self, almacen, motor):
        with pytest.raises(ValueError):
            almacen.quitar_repuesto(motor, 100)

    def test_quitar_cantidad_invalida_lanza_error(self, almacen, motor):
        with pytest.raises(ValueError):
            almacen.quitar_repuesto(motor, 0)
        with pytest.raises(ValueError):
            almacen.quitar_repuesto(motor, -1)


# ─── NaveEstelar ─────────────────────────────────────────────────────────────

class TestNaveEstelar:
    def test_creacion_correcta(self, nave_estelar):
        assert nave_estelar.nombre == 'Devastador'
        assert nave_estelar.clase == Clase.EJECUTOR
        assert nave_estelar.pasaje == 5000

    def test_id_combate_entero_se_convierte_a_str(self, motor):
        nave = NaveEstelar(42, 'clave', 'Nave', {motor: 1}, [], 0, Clase.ECLIPSE)
        assert nave.id_combate == '42'

    def test_nombre_vacio_lanza_error(self, motor):
        with pytest.raises(ValueError):
            NaveEstelar('ID', 'clave', '', {motor: 1}, [], 0, Clase.ECLIPSE)

    def test_tripulacion_no_lista_lanza_error(self, motor):
        with pytest.raises(TypeError):
            NaveEstelar('ID', 'clave', 'Nave', {motor: 1}, 'no_lista', 0, Clase.ECLIPSE)

    def test_pasaje_negativo_lanza_error(self, motor):
        with pytest.raises(ValueError):
            NaveEstelar('ID', 'clave', 'Nave', {motor: 1}, [], -1, Clase.ECLIPSE)

    def test_clase_invalida_lanza_error(self, motor):
        with pytest.raises(TypeError):
            NaveEstelar('ID', 'clave', 'Nave', {motor: 1}, [], 0, 'EJECUTOR')

    def test_get_info(self, nave_estelar):
        info = nave_estelar.get_info()
        assert 'Devastador' in info
        assert 'EJECUTOR' in info
        assert 'Darth Vader' in info

    def test_adquirir_repuesto_actualiza_piezas(self, nave_estelar, almacen, laser):
        nave_estelar.adquirir_repuesto(almacen, laser, 5)
        assert nave_estelar.piezas_repuesto[laser] == 5

    def test_adquirir_repuesto_descuenta_almacen(self, nave_estelar, almacen, laser):
        stock_antes = almacen.consultar_stock()['Cañón Láser']
        nave_estelar.adquirir_repuesto(almacen, laser, 10)
        assert almacen.consultar_stock()['Cañón Láser'] == stock_antes - 10

    def test_adquirir_repuesto_acumula_si_ya_existe(self, nave_estelar, almacen, motor):
        cantidad_antes = nave_estelar.piezas_repuesto[motor]
        nave_estelar.adquirir_repuesto(almacen, motor, 3)
        assert nave_estelar.piezas_repuesto[motor] == cantidad_antes + 3

    def test_adquirir_almacen_invalido_lanza_error(self, nave_estelar, laser):
        with pytest.raises(TypeError):
            nave_estelar.adquirir_repuesto('no_almacen', laser, 1)

    def test_adquirir_repuesto_invalido_lanza_error(self, nave_estelar, almacen):
        with pytest.raises(TypeError):
            nave_estelar.adquirir_repuesto(almacen, 'no_repuesto', 1)


# ─── EstacionEspacial ────────────────────────────────────────────────────────

class TestEstacionEspacial:
    def test_creacion_correcta(self, estacion):
        assert estacion.nombre == 'Estrella de la Muerte'
        assert estacion.ubicacion == 'Órbita de Endor'

    def test_get_info(self, estacion):
        info = estacion.get_info()
        assert 'Estrella de la Muerte' in info
        assert 'Gran Moff Tarkin' in info
        assert 'Órbita de Endor' in info


# ─── CazaEstelar ─────────────────────────────────────────────────────────────

class TestCazaEstelar:
    def test_creacion_correcta(self, caza):
        assert caza.nombre == 'TIE Avanzado'
        assert caza.dotacion == 1

    def test_dotacion_cero_lanza_error(self, laser):
        with pytest.raises(ValueError):
            CazaEstelar('ID', 'clave', 'Nave', {laser: 1}, 0)

    def test_dotacion_negativa_lanza_error(self, laser):
        with pytest.raises(ValueError):
            CazaEstelar('ID', 'clave', 'Nave', {laser: 1}, -5)

    def test_get_info(self, caza):
        info = caza.get_info()
        assert 'TIE Avanzado' in info
        assert '1' in info


# ─── Imperio ─────────────────────────────────────────────────────────────────

class TestImperio:
    def test_creacion_correcta(self, imperio):
        assert imperio.nombre == 'Imperio Galáctico'
        assert len(imperio.get_unidades()) == 2
        assert len(imperio.get_almacenes()) == 1

    def test_unidades_invalidas_lanza_error(self, almacen):
        with pytest.raises(TypeError):
            Imperio('Imperio', ['no_unidad'], [almacen])

    def test_almacenes_invalidos_lanza_error(self, nave_estelar):
        with pytest.raises(TypeError):
            Imperio('Imperio', [nave_estelar], ['no_almacen'])

    def test_set_unidad(self, imperio, caza):
        cantidad_antes = len(imperio.get_unidades())
        imperio.set_unidad(caza)
        assert len(imperio.get_unidades()) == cantidad_antes + 1
        assert caza in imperio.get_unidades()

    def test_set_unidad_invalida_lanza_error(self, imperio):
        with pytest.raises(TypeError):
            imperio.set_unidad('no_unidad')

    def test_get_unidades(self, imperio, nave_estelar, estacion):
        unidades = imperio.get_unidades()
        assert nave_estelar in unidades
        assert estacion in unidades

    def test_get_almacenes(self, imperio, almacen):
        assert almacen in imperio.get_almacenes()

    def test_str(self, imperio):
        resultado = str(imperio)
        assert 'Imperio Galáctico' in resultado
        assert 'Devastador' in resultado
        assert 'Base Starkiller' in resultado
