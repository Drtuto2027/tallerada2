def merge(left, right):
    result = []
    i = j = 0
    
    # Comparar los elementos de ambos subarreglos y agregar el menor a 'result'
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Agregar los elementos restantes de 'left' o 'right'
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

# Función principal de Merge Sort con impresión de cada paso de la división
def merge_sort(arr, level=0):
    print(f"{'  ' * level}División Nivel {level}: {arr}")
    
    # Caso base: Si el arreglo tiene 1 o 0 elementos, ya está ordenado
    if len(arr) <= 1:
        return arr
    
    # Dividir el arreglo en dos mitades
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # Llamada recursiva para ordenar ambas mitades
    left = merge_sort(left, level + 1)
    right = merge_sort(right, level + 1)
    
    # Combinar las dos mitades ordenadas
    merged = merge(left, right)
    
    print(f"{'  ' * level}Combinación Nivel {level}: {merged}")
    
    return merged

# Ejemplo de uso con solo 2 divisiones (4 elementos)
arr = [38, 27, 43, 12]
print("Arreglo original:", arr)
sorted_arr = merge_sort(arr)
print("Arreglo final ordenado:", sorted_arr)