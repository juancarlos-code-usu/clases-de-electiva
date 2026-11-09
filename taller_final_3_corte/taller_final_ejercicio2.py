class Envio:
    """Clase base para modelar envíos de una empresa de logística."""

    def __init__(self, peso_kg, distancia_km, descripcion="Envío"):
        self.peso_kg = peso_kg
        self.distancia_km = distancia_km
        self.descripcion = descripcion

    def calcular_costo(self, monto_base):
        """Calcula el costo del envío a partir de un monto base.

        Este método se redefine en las subclases (polimorfismo).
        """
        raise NotImplementedError("Las subclases deben implementar calcular_costo().")

    def __str__(self):
        return (
            f"{self.__class__.__name__}(descripcion={self.descripcion!r}, "
            f"peso_kg={self.peso_kg}, distancia_km={self.distancia_km})"
        )


class EnvioEstandar(Envio):
    """Envío estándar con recargo del 5% sobre el monto base."""

    def __init__(self, peso_kg, distancia_km, descripcion="Envío estándar"):
        super().__init__(peso_kg, distancia_km, descripcion)

    def calcular_costo(self, monto_base):
        recargo = monto_base * 0.05
        return monto_base + recargo


class EnvioExpress(Envio):
    """Envío express con recargo del 15% por servicio prioritario."""

    def __init__(self, peso_kg, distancia_km, descripcion="Envío express"):
        super().__init__(peso_kg, distancia_km, descripcion)

    def calcular_costo(self, monto_base):
        recargo = monto_base * 0.15
        return monto_base + recargo


if __name__ == "__main__":
    # Lista mixta de envíos
    envios = [
        EnvioEstandar(2.5, 120, "Documentos"),
        EnvioExpress(1.0, 300, "Medicamentos"),
        EnvioEstandar(10.0, 50, "Ropa"),
        EnvioExpress(5.0, 800, "Electrónicos"),
        EnvioEstandar(0.8, 20, "Libros"),
        EnvioExpress(3.2, 450, "Repuestos urgentes"),
    ]

    monto_base = 20000  # monto base del paquete

    print("Sistema de Cotización de Envíos")
    print(f"Monto base: ${monto_base:,.2f}\n")
    print(f"{'Tipo':<15} {'Descripción':<22} {'Peso(kg)':>8} {'Dist(km)':>9} {'Costo total':>14}")
    print("-" * 72)

    # Recorrido polimórfico: se invoca el mismo método en objetos de distinto tipo
    for envio in envios:
        costo = envio.calcular_costo(monto_base)
        print(
            f"{envio.__class__.__name__:<15} {envio.descripcion:<22} "
            f"{envio.peso_kg:>8.1f} {envio.distancia_km:>9.1f} ${costo:>13,.2f}"
        )