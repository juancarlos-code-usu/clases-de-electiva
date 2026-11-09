class UsuarioSistema: # Superclase
def init (self, username: str, email: str):
self.username = username
self.email = email
def autenticar(self):
print(f"Usuario {self.username} autenticado en el sistema.")
class Administrador(UsuarioSistema): # Subclase
def init (self, username: str, email: str, nivel_acceso: int):
super(). init (username, email) # Hereda inicialización
self.nivel_acceso = nivel_acceso
admin = Administrador("root_neider", "nhernandez@unicaribe.edu", 1)
admin.autenticar() # Salida: Usuario root_neider autenticado en el sistema.
