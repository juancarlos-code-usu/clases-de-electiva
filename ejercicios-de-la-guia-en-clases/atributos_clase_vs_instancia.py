class ConexionBaseDatos:
total_conexiones = 0 # Atributo de Clase
def init (self, db_name: str):
self.db_name = db_name # Atributo de Instancia
ConexionBaseDatos.total_conexiones += 1
c1 = ConexionBaseDatos("Ventas")
c2 = ConexionBaseDatos("Inventario")
print(ConexionBaseDatos.total_conexiones) # Imprime: 2
