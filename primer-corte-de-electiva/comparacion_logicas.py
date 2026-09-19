
edad_1 = int(input("Ingrese la primera edad: "))
edad_2 = int(input("Ingrese la segunda edad: "))

son_iguales = edad_1 == edad_2 

primera_es_mayor = edad_1 > edad_2 

ambas_mayores_de_18 = edad_1 > 18 and edad_2 > 18 

print("¿Las edades son iguales?", son_iguales) 
print("¿La primera edad es mayor?", primera_es_mayor) 
print("¿Ambas personas son mayores de 18?", ambas_mayores_de_18)