class TarjetaCredito:
    def __init__(self, titular: str, numero: str):
        self.titular = titular
        self.__numero = numero

    def obtener_numero_oculto(self) -> str:
        return f"**** **** **** {self.__numero[-4:]}"

    def calcular_cashback(self, monto: float) -> float:
        return 0.0


class TarjetaGold(TarjetaCredito):
    def calcular_cashback(self, monto: float) -> float:
        return monto * 0.02


class TarjetaBlack(TarjetaCredito):
    def calcular_cashback(self, monto: float) -> float:
        return monto * 0.05


def mostrar_cashback(tarjetas: list[TarjetaCredito], monto: float):
    for t in tarjetas:
        cashback = t.calcular_cashback(monto)
        print(f"{type(t).__name__} de {t.titular} ({t.obtener_numero_oculto()}): "
                f"cashback ${cashback:.2f}")


tarjetas = [
    TarjetaCredito("Ana Torres", "1111222233334444"),
    TarjetaGold("Carlos Gómez", "5555666677778888"),
    TarjetaBlack("Ing. Hernández", "9999000011112222"),
]

mostrar_cashback(tarjetas, 1000.0)