# Fecha: 09-04-2026
# Autores: Andŕes Reyes, Allan González, Fernando Reyes, Mitchael Ruíz
# Descripción: Sistema de gestión de base de datos para biblioteca.

#========================= IMPORTS
import mariadb
import sys

#======================== FUNCIONES

# Conectar a la Base de Datos
def conectar_db(usuario, contraseña, equipo, base_datos):
    try:
        conn = mariadb.connect(
            user=usuario,
            password=contraseña,
            host=equipo,
            port=3306,
            database=base_datos
        )
        print(f"Conexión exitosa a MariaDB: {base_datos}")        
        return conn
    except mariadb.Error as e:
        print(f"Error al conectar: {e}")
        return None
        
def obtener_cursor(conn):
    if conn:
        cursor = conn.cursor()
        print("Cursor listo para operar")
        return cursor
    return None

def consultar_tabla(cursor, tabla):
    try:
        print(f"\n--- CONTENIDO DE LA TABLA: {tabla.upper()} ---")
        cursor.execute(f"SELECT * FROM {tabla}")
        
        # Obtener y mostrar encabezados
        columnas = [desc[0] for desc in cursor.description]
        print(" | ".join(columnas))
        print("-" * 60)
        
        # Mostrar filas
        filas = cursor.fetchall()
        for fila in filas:
            print(" | ".join(str(valor) for valor in fila))
    except mariadb.Error as e:
        print(f"Error al consultar la tabla: {e}")

#============ MAIN

def main():
    # 1. Conectar a la base de datos (Tus datos de acceso)
    conn = conectar_db("reyes", "1102", "127.0.0.1", "biblioteca")
    
    if not conn:
        print("No se pudo establecer la conexión. Saliendo...")
        return

    # 2. Obtener Cursor
    cursor = obtener_cursor(conn)
    
    # 3. Uso de la Base de Datos (Menú interactivo)
    tablas_map = {
        "1": "autores",
        "2": "libros",
        "3": "ejemplares",
        "4": "socios",
        "5": "prestamos"
    }

    while True:
        print("\n=== MENÚ BIBLIOTECA ===")
        print("1. Ver Autores\n2. Ver Libros\n3. Ver Ejemplares\n4. Ver Socios\n5. Ver Préstamos\n6. Salir")
        opcion = input("Elija una opción: ")

        if opcion == "6":
            print("Cerrando sistema...")
            break
        elif opcion in tablas_map:
            consultar_tabla(cursor, tablas_map[opcion])
        else:
            print("Opción inválida.")

    # 4. Cerrar conexiones
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
