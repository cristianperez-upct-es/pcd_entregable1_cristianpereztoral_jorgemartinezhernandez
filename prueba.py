from codigo import *

bolt = Repuesto('bolt', 'paco', 10)
wing = Repuesto('wing', 'francisco', 50432)

milenialfalcon = NaveEstelar('1', 1, 'milenial_falcon',{bolt:3, wing:1}, ['Lonely Han', 'Chewbacca'], 1, Clase.EJECUTOR)
deathstar = EstacionEspacial('2', 2, 'death_star', {bolt: 100}, ['Darth Vader', 'Death Moul', 'Palpatin'], 2, 'espacio')
xwing = CazaEstelar('3', 3, 'x-wing', {wing:2}, 3)

droiddepot = Almacen('Droid Depot', {bolt: 100, wing:200}, 'Tatooine')

imperio = Imperio('imperio estelar', [deathstar, xwing], [droiddepot])
print(imperio)
print(imperio.get_unidades())
print(imperio.get_almacenes())
imperio.set_unidad(xwing)
print(imperio.get_unidades())