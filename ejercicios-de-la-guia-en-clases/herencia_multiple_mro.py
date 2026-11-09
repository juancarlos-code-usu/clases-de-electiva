class DispositivoConectado:
def conectar(self):
print("Estableciendo conexión a la red...")
class CamaraSeguridad:
def grabar(self):
print("Grabando video HD...")
class CamaraIP(DispositivoConectado, CamaraSeguridad): # Herencia Múltiple
pass
cam = CamaraIP()
cam.conectar()
cam.grabar()
# Inspección del MRO
print(CamaraIP.mro()
