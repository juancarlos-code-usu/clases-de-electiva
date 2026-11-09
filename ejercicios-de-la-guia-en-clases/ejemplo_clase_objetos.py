 class ServidorCloud:
# Atributo de clase (compartido por todas las instancias)
proveedor = "Unicaribe Cloud"
def init (self, hostname: str, ram_gb: int):
# Atributos de instancia
self.hostname = hostname
self.ram_gb = ram_gb
self.encendido = False
def encender(self):
self.encendido = True
print(f"Servidor {self.hostname} operando correctamente.")
# Instanciación de Objetos concretos
srv01 = ServidorCloud("srv-db-01", 64)
srv01.encender() # Salida: Servidor srv-db-01 operando correctamente.
