class CuentaBancaria:
def init (self, titular: str, saldo_inicial: float):
self.titular = titular
self. saldo = saldo_inicial # Atributo Privado
def depositar(self, monto: float):
if monto > 0:
self. saldo += monto
else:
print("Error: Monto inválido.")
def obtener_saldo(self) -> float: # Getter controlado
return self. saldo
cuenta = CuentaBancaria("Ing. Hernández", 5000.0)
cuenta.depositar(1500.0)
print(cuenta.obtener_saldo()) # Imprime: 6500.0
# print(cuenta. saldo) -> Eleva AttributeError
