from abc import ABC, abstractmethod
class ProcesadorPago(ABC):
@abstractmethod
def procesar(self, monto: float) -> bool:
pass
class PagoTarjetas(ProcesadorPago):
def procesar(self, monto: float) -> bool:
print(f"Cobrando ${monto} vía Pasarela de Tarjeta.")
return True
# p = ProcesadorPago() -> Lanzará TypeError por ser abstracta
pago = PagoTarjetas() 
