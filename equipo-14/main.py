import mysql.connector

def mostrar_menu():
    print("\n--- SISTEMA DE GESTIÓN DE BIBLIOTECA ---")
    print("1. Ver Autores")
    print("2. Ver Libros")
    print("3. Ver Ejemplares")
    print("4. Ver Socios")
    print("5. Ver Préstamos")
    print("6. Salir")
    return input("Seleccione una opción (1-6): ")

def consultar_tabla(cursor, tabla):
    print(f"\n>>> MOSTRANDO TABLA: {tabla.upper()} <<<")
    cursor.execute(f"SELECT * FROM {tabla}")
    
    # 3. Almacenar resultados en variables
    columnas = [desc[0] for desc in cursor.description]
    print(" | ".join(columnas))
    print("-" * 50)
    
    filas = cursor.fetchall()
    for fila in filas:
        # 4. Imprimir el resultado
        print(" | ".join(str(valor) for valor in fila))

try:
    conexion = mysql.connector.connect(
        user='reyes',
        password='1102',
        host='localhost',
        database='biblioteca'
    )
    
    cursor = conexion.cursor()
    
    tablas_map = {
        "1": "autores",
        "2": "libros",
        "3": "ejemplares",
        "4": "socios",
        "5": "prestamos"
    }

    while True:
        opcion = mostrar_menu()
        
        if opcion == "6":
            print("Saliendo del sistema...")
            break
        elif opcion in tablas_map:
            consultar_tabla(cursor, tablas_map[opcion])
        else:
            print("Opción no válida, intente de nuevo.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
