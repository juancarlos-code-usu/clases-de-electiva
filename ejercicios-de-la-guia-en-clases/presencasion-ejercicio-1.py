class Estudiante:
    def __init__(self, nombre: str, notas: list = None):
        self.__nombre = nombre   
        self.__notas = []       
        if notas is not None:
            self.notas = notas   

    #Validación interna (método privado)
    def __validar_nota(self, nota: float):
        if not isinstance(nota, (int, float)) or isinstance(nota, bool):
            raise ValueError("La nota debe ser un valor numérico.")
        if nota < 0 or nota > 5.0:
            raise ValueError("La nota debe estar entre 0.0 y 5.0.")

    #Getter de propiedad: nombre (solo lectura)
    @property
    def nombre(self) -> str:
        return self.__nombre

    #Getter de propiedad: notas (retorna una copia)
    @property
    def notas(self) -> list:
        return self.__notas.copy()  

    #Setter con validación
    @notas.setter
    def notas(self, nuevas_notas: list):
        for nota in nuevas_notas:
            self.__validar_nota(nota) 
        self.__notas = list(nuevas_notas)


    def agregar_nota(self, nota: float):
        self.__validar_nota(nota)
        self.__notas.append(nota)
        print(f"Nota {nota} registrada para {self.__nombre}.")

    def calcular_promedio(self) -> float:
        if not self.__notas:
            return 0.0
        return sum(self.__notas) / len(self.__notas)


# Prueba de Ejecución
est = Estudiante("Laura Pérez")
est.agregar_nota(4.5)   
est.agregar_nota(3.8)   
est.agregar_nota(5.0)   
print(f"Promedio: {est.calcular_promedio():.2f}") 

# Intentos de registrar valores inválidos
try:
    est.agregar_nota(-1.0)
except ValueError as e:
    print(f"Error: {e}")

try:
    est.agregar_nota(5.5)
except ValueError as e:
    print(f"Error: {e}")

try:
    est.notas = [3.0, 6.0]
except ValueError as e:
    print(f"Error: {e}")

# La copia protege la lista interna
copia = est.notas
copia.append(1.0)
print(est.notas)

# print(est.__notas) -> Eleva AttributeError