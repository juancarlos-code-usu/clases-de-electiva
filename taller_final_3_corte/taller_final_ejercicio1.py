
class Producto:
    """Sistema de Control de Inventario y Precios.

    Modela el registro de inventarios de una tienda con encapsulamiento
    del nombre y del historial de prec
    ios.
    """

    def __init__(self, nombre, precio_inicial=None):
        # Atributos privados
        self.__nombre = nombre
        self.__precios_historicos = []

        if precio_inicial is not None:
            self.registrar_precio(precio_inicial)

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            print("Advertencia: el nombre debe ser un texto no vacío. No se alteró el registro.")
            return
        self.__nombre = valor.strip()

    @property
    def precios_historicos(self):
        # Se devuelve una copia para proteger el atributo privado
        return list(self.__precios_historicos)

    @property
    def precio(self):
        """Devuelve el último precio registrado, o None si no hay historial."""
        if not self.__precios_historicos:
            return None
        return self.__precios_historicos[-1]

    @precio.setter
    def precio(self, nuevo_precio):
        """Actualiza el precio registrándolo en el historial.

        Encapsulamiento con validación:
        - No permite valores negativos.
        - No permite valores superiores a $10,000.
        Si el valor es inválido, emite advertencia y no altera el registro.
        """
        self.registrar_precio(nuevo_precio)

    def registrar_precio(self, nuevo_precio):
        """Registra un nuevo precio en el historial si es válido."""
        try:
            valor = float(nuevo_precio)
        except (TypeError, ValueError):
            print(
                f"Advertencia: '{nuevo_precio}' no es un precio válido. "
                "No se alteró el registro."
            )
            return False

        if valor < 0 or valor > 10000:
            print(
                f"Advertencia: el precio ${valor:,.2f} está fuera del rango permitido "
                "(0 a $10,000). No se alteró el registro."
            )
            return False

        self.__precios_historicos.append(valor)
        return True

    @property
    def precio_promedio(self):
        """Calcula y retorna el precio promedio del producto."""
        if not self.__precios_historicos:
            return 0.0
        return sum(self.__precios_historicos) / len(self.__precios_historicos)

    def __str__(self):
        return (
            f"Producto(nombre={self.__nombre!r}, "
            f"precio_actual={self.precio}, "
            f"precio_promedio={self.precio_promedio:.2f}, "
            f"historial={self.precios_historicos})"
        )


if __name__ == "__main__":
    # Demostración del funcionamiento
    producto = Producto("Cuaderno", 2500)
    print(producto)

    # Registrar precios válidos
    producto.registrar_precio(3000)
    producto.precio = 2800  # también funciona mediante @property setter
    print("\nDespués de registrar precios válidos:")
    print(producto)

    # Intentos inválidos (no deben alterar el registro)
    print("\nIntentos con valores fuera de rango:")
    producto.precio = -500
    producto.precio = 15000

    print("\nRegistro final (sin cambios por valores inválidos):")
    print(producto)
    print(f"Nombre: {producto.nombre}")
    print(f"Precios históricos: {producto.precios_historicos}")
    print(f"Precio promedio: ${producto.precio_promedio:,.2f}") 