class NotificadorEmail:
def enviar(self, mensaje: str):
print(f"Enviando Email: {mensaje}")
class NotificadorSMS:
def enviar(self, mensaje: str):
print(f"Enviando SMS: {mensaje}")
# Función Polimórfica que opera sin importar el tipo concreto
def notificar_alerta(notificador, texto):
notificador.enviar(texto) # Invocación Polimórfica
canal_1 = NotificadorEmail()
canal_2 = NotificadorSMS()
notificar_alerta(canal_1, "Fallo en servidor DB")
notificar_alerta(canal_2, "Fallo en servidor DB")
