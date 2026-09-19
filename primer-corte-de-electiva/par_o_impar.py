try:
    numero = int(input("Ingresa un número: "))

    if numero % 2 == 0:
        print("El número es par")
    else:
        print("El número es impar")

except ValueError:
    print("Por favor, ingresa un número válido")