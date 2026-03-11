/*
 ESTRUCTURA DE BASE DE DATOS - EVAL N° 4

González Allan V-28.660.376
Reyes Andrés V-30.520.333
Reyes Fernando V-30.159.566
Ruiz Mitchael V-31.416.127
Sección: DCM0501V1
*/

CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE libros (
    isbn VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    editorial VARCHAR(100),
    num_paginas INT,
    id_autor INT,
    CONSTRAINT fk_libro_autor FOREIGN KEY (id_autor) 
        REFERENCES autores(id_autor) ON DELETE CASCADE
);

CREATE TABLE ejemplares (
    id_ejemplar INT AUTO_INCREMENT PRIMARY KEY,
    localizacion VARCHAR(100),
    isbn VARCHAR(20),
    CONSTRAINT fk_ejemplar_libro FOREIGN KEY (isbn) 
        REFERENCES libros(isbn) ON DELETE CASCADE
);

CREATE TABLE socios (
    dni VARCHAR(15) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    telefono VARCHAR(20)
);

CREATE TABLE prestamos (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15),
    id_ejemplar INT,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE,
    CONSTRAINT fk_prestamo_socio FOREIGN KEY (dni) 
        REFERENCES socios(dni) ON DELETE CASCADE,
    CONSTRAINT fk_prestamo_ejemplar FOREIGN KEY (id_ejemplar) 
        REFERENCES ejemplares(id_ejemplar) ON DELETE CASCADE
);