# Fecha: 09-04-2026
# Autores: Andrés Reyes, Allan González, Fernando Reyes, Mitchael Ruíz
# Descripción: Sistema de Gestión de Biblioteca: Consulta general y CRUD de Libros.

#========================= IMPORTS
import mariadb
import sys

#======================== FUNCIONES DE CONEXIÓN

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
        return cursor
    return None

#======================== FUNCIONES DE CONSULTA GENERAL

def consultar_tabla(cursor, tabla):
    try:
        print(f"\n--- CONTENIDO DE LA TABLA: {tabla.upper()} ---")
        cursor.execute(f"SELECT * FROM {tabla}")
        
        # Encabezados
        columnas = [desc[0] for desc in cursor.description]
        print(" | ".join(columnas))
        print("-" * 70)
        
        # Datos
        filas = cursor.fetchall()
        for fila in filas:
            print(" | ".join(str(valor) for valor in fila))
    except mariadb.Error as e:
        print(f"Error al consultar la tabla: {e}")

#======================== FUNCIONES CRUD (TABLA LIBROS)

def nuevo_libro(cursor, conn):
    print("\n--- REGISTRAR NUEVO LIBRO ---")
    isbn = input("ISBN: ")
    titulo = input("Título: ")
    editorial = input("Editorial: ")
    paginas = input("Número de páginas: ")
    id_autor = input("ID del Autor: ")
    
    sql = "INSERT INTO libros (isbn, titulo, editorial, num_paginas, id_autor) VALUES (?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql, (isbn, titulo, editorial, paginas, id_autor))
        conn.commit()
        print(f"Libro '{titulo}' guardado con éxito.")
    except mariadb.Error as e:
        print(f"Error al insertar: {e}")

def buscar_libro(cursor):
    print("\n--- BUSCAR LIBRO ---")
    isbn = input("Ingrese el ISBN a buscar: ")
    cursor.execute("SELECT * FROM libros WHERE isbn = ?", (isbn,))
    libro = cursor.fetchone()
    if libro:
        print(f"Resultado: {libro[1]} | Editorial: {libro[2]} | Autor ID: {libro[4]}")
    else:
        print("No se encontró el ISBN.")

def editar_libro(cursor, conn):
    print("\n--- EDITAR LIBRO ---")
    isbn = input("ISBN del libro a editar: ")
    nuevo_titulo = input("Nuevo Título: ")
    nueva_ed = input("Nueva Editorial: ")
    try:
        cursor.execute("UPDATE libros SET titulo = ?, editorial = ? WHERE isbn = ?", (nuevo_titulo, nueva_ed, isbn))
        conn.commit()
        print("Actualizado correctamente.")
    except mariadb.Error as e:
        print(f"Error al editar: {e}")

def eliminar_libro(cursor, conn):
    print("\n--- ELIMINAR LIBRO ---")
    isbn = input("ISBN del libro a eliminar: ")
    try:
        cursor.execute("DELETE FROM libros WHERE isbn = ?", (isbn,))
        conn.commit()
        print("Eliminado.")
    except mariadb.Error as e:
        print(f"Error al eliminar: {e}")

#======================== MENÚS

def mostrar_menu():
    print("\n========== SISTEMA BIBLIOTECA ==========")
    print("--- CONSULTA DE TABLAS ---")
    print("1. Ver Autores      2. Ver Libros")
    print("3. Ver Ejemplares   4. Ver Socios")
    print("5. Ver Préstamos")
    print("--- GESTIÓN DE LIBROS (CRUD) ---")
    print("6. Agregar Libro    7. Buscar Libro")
    print("8. Editar Libro     9. Eliminar Libro")
    print("10. Salir")
    return input("\nSeleccione una opción: ")

#============ MAIN

def main():
    conn = conectar_db("reyes", "1102", "127.0.0.1", "biblioteca")
    if not conn: return
    cursor = obtener_cursor(conn)
    
    tablas_map = {
        "1": "autores",
        "2": "libros",
        "3": "ejemplares",
        "4": "socios",
        "5": "prestamos"
    }

    while True:
        opcion = mostrar_menu()
        
        if opcion == "10":
            print("Saliendo...")
            break
        # Opciones de consulta simple (1 al 5)
        elif opcion in tablas_map:
            consultar_tabla(cursor, tablas_map[opcion])
        # Opciones de CRUD (6 al 9)
        elif opcion == "6": nuevo_libro(cursor, conn)
        elif opcion == "7": buscar_libro(cursor)
        elif opcion == "8": editar_libro(cursor, conn)
        elif opcion == "9": eliminar_libro(cursor, conn)
        else:
            print("Opción no válida.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
