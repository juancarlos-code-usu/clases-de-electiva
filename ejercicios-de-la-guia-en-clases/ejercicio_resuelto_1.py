class Vehiculo:
def init (self, marca: str, modelo: str):
self._marca = marca
self._modelo = modelo
def obtener_info(self) -> str:
return f"Vehículo: {self._marca} {self._modelo}"
class AutoElectrico(Vehiculo):
def init (self, marca: str, modelo: str, bateria_kwh: float):
super(). init (marca, modelo)
self. bateria = bateria_kwh
self. carga_actual = 20.0 # Porcentaje inicial
def cargar_bateria(self, porcentaje: float):
if 0 <= porcentaje <= (100 - self. carga_actual):
self. carga_actual += porcentaje
print(f"Carga exitosa. Batería al {self. carga_actual}%")
else:
print("Error: Excede el límite de carga (100%).")
# Prueba de Ejecución Paso a Paso
tesla = AutoElectrico("Tesla", "Model 3", 75.0)
print(tesla.obtener_info()) # Muestra información de la superclase
tesla.cargar_bateria(50.0) # Salida: Carga exitosa. Batería al 70.0%
