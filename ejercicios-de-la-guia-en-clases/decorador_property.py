class Empleado:
def init (self, nombre: str, salario: float):
self.nombre = nombre
self. salario = salario
@property
def salario(self) -> float: # Getter de propiedad
return self. salario
@salario.setter
def salario(self, nuevo_salario: float): # Setter con validación
if nuevo_salario >= 1300.0:
self. salario = nuevo_salario
else:
raise ValueError("El salario no puede ser inferior al mínimo legal.")
emp = Empleado("Carlos Gómez", 2000.0)
emp.salario = 2500.0 # Asignación limpia usando el Setter
print(emp.salario) # Lectura usando Getter: 2500.0
