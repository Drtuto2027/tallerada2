import csv
import time
from typing import List, Tuple

class Producto:
    def __init__(self, id: int, nombre: str, precio: float, calificacion: int, stock: int):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.calificacion = calificacion
        self.stock = stock
    
    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Precio: ${self.precio:.2f}, Calificación: {self.calificacion}★, Stock: {self.stock}"

def leer_csv(nombre_archivo: str = "productos.csv") -> List[Producto]:
    """Lee productos desde un archivo CSV"""
    productos = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                producto = Producto(
                    int(fila['id']),
                    fila['nombre'],
                    float(fila['precio']),
                    int(fila['calificacion']),
                    int(fila['stock'])
                )
                productos.append(producto)
        print(f"✓ Se leyeron {len(productos)} productos desde '{nombre_archivo}'")
    except FileNotFoundError:
        print(f"✗ Error: El archivo '{nombre_archivo}' no existe.")
    
    return productos

def comparar_productos(a: Producto, b: Producto) -> int:
    """
    Compara dos productos según los criterios:
    1. Calificación (mayor a menor)
    2. Precio (menor a mayor en caso de empate en calificación)
    
    Retorna:
    - Número negativo si a debe ir antes que b
    - Número positivo si b debe ir antes que a
    - 0 si son iguales según los criterios
    """
    # Primero comparar por calificación (mayor a menor)
    if a.calificacion != b.calificacion:
        return b.calificacion - a.calificacion
    
    # Si tienen la misma calificación, comparar por precio (menor a mayor)
    if a.precio != b.precio:
        return a.precio - b.precio
    
    return 0

def merge_sort(productos: List[Producto]) -> List[Producto]:
    """
    Implementación de Merge Sort usando Divide y Vencerás
    
    DIVIDE: Divide la lista en dos mitades
    VENCE: Ordena recursivamente cada mitad  
    COMBINA: Mezcla las dos mitades ordenadas
    """
    # Caso base: lista vacía o con un solo elemento
    if len(productos) <= 1:
        return productos
    
    # DIVISIÓN: Dividir la lista en dos mitades
    medio = len(productos) // 2
    izquierda = productos[:medio]
    derecha = productos[medio:]
    
    # CONQUISTA: Ordenar recursivamente cada mitad
    izquierda_ordenada = merge_sort(izquierda)
    derecha_ordenada = merge_sort(derecha)
    
    # COMBINACIÓN: Mezclar las dos mitades ordenadas
    return mezclar(izquierda_ordenada, derecha_ordenada)

def mezclar(izquierda: List[Producto], derecha: List[Producto]) -> List[Producto]:
    """Mezcla dos listas ordenadas en una sola lista ordenada"""
    resultado = []
    i = j = 0
    
    # Comparar elementos de ambas listas y agregar el menor/mayor según criterio
    while i < len(izquierda) and j < len(derecha):
        if comparar_productos(izquierda[i], derecha[j]) <= 0:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    
    # Agregar los elementos restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    
    return resultado

def mostrar_mejores_productos(productos: List[Producto], n: int = 20):
    """Muestra los n mejores productos"""
    print(f"\n🏆 TOP {n} MEJORES PRODUCTOS 🏆")
    print("=" * 90)
    print("(Ordenados por calificación de mayor a menor, y por precio de menor a mayor)")
    print("=" * 90)
    
    for i, producto in enumerate(productos[:n], 1):
        print(f"{i:2d}. {producto}")

def analizar_datos(productos: List[Producto]):
    """Analiza y muestra estadísticas de los productos"""
    print("\n📊 ANÁLISIS DE DATOS")
    print("-" * 50)
    
    # Conteo por calificación
    calificaciones = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for producto in productos:
        calificaciones[producto.calificacion] += 1
    
    for calif, cantidad in sorted(calificaciones.items(), reverse=True):
        print(f"Calificación {calif}★: {cantidad:4d} productos ({cantidad/len(productos)*100:.1f}%)")
    
    # Productos con calificación 5
    productos_5_estrellas = [p for p in productos if p.calificacion == 5]
    print(f"\n✨ Productos con 5 estrellas: {len(productos_5_estrellas)}")
    
    if productos_5_estrellas:
        mas_barato_5 = min(productos_5_estrellas, key=lambda x: x.precio)
        print(f"💰 Más barato con 5★: {mas_barato_5.nombre} - ${mas_barato_5.precio:.2f}")

def guardar_resultados(productos: List[Producto], nombre_archivo: str = "productos_ordenados.csv"):
    """Guarda los productos ordenados en un archivo CSV"""
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(['id', 'nombre', 'precio', 'calificacion', 'stock'])
        
        for producto in productos:
            writer.writerow([
                producto.id, 
                producto.nombre, 
                producto.precio, 
                producto.calificacion, 
                producto.stock
            ])
    
    print(f"✓ Resultados guardados en '{nombre_archivo}'")

def main():
    """Función principal que ejecuta todo el proceso"""
    print("🎯 SISTEMA DE ORDENACIÓN DE PRODUCTOS CON DIVIDE Y VENCERÁS")
    print("=" * 60)
    
    # Paso 1: Leer productos desde el archivo CSV
    print("\n1. 📖 Leyendo productos desde el archivo...")
    productos = leer_csv("productos.csv")
    
    if not productos:
        print("No se pudieron leer los productos. Saliendo...")
        return
    
    # Mostrar algunos productos sin ordenar
    print("\n2. 🔍 Algunos productos sin ordenar:")
    print("-" * 80)
    for i in range(5):
        print(f"   {productos[i]}")
    
    # Analizar datos antes de ordenar
    analizar_datos(productos)
    
    # Paso 2: Aplicar Merge Sort
    print(f"\n3. 🚀 Aplicando Merge Sort (Divide y Vencerás) a {len(productos)} productos...")
    
    inicio = time.time()
    productos_ordenados = merge_sort(productos)
    fin = time.time()
    
    print(f"✓ ¡Ordenación completada en {fin - inicio:.4f} segundos!")
    
    # Paso 3: Mostrar los mejores productos
    mostrar_mejores_productos(productos_ordenados, 25)
    
    # Paso 4: Guardar resultados
    print("\n4. 💾 Guardando productos ordenados...")
    guardar_resultados(productos_ordenados)
    
    print("\n🎉 ¡Proceso completado exitosamente!")

# Ejecutar el programa
if __name__ == "__main__":
    main()