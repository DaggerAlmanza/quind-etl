# quind-etl
ETL utilizando Python
Análisis y Limpieza de Datos de Alquiler de Películas

## Descripción
Este proyecto realiza la limpieza, análisis exploratorio y transformación de datos de un conjunto de tablas relacionadas con alquileres de películas. Incluye validación, manejo de valores no numéricos, y generación de reportes detallados en formatos CSV y Excel con los datos limpios.

### Estructura del Proyecto
1. Archivos principales:

    * main.py: Punto de entrada principal.
    * log.py: Configuración y gestión de registros.
    * data.py: Procesamiento y limpieza de datos.
    * data_analysis.log: Registro de análisis de datos.
2. Tablas procesadas:

    * film
    * inventory
    * rental
    * customer
    * store
## Requerimientos
* Python 3.12
* Librerías: pandas, openpyxl

## Instrucciones
1. Configuración Inicial:
    * Entorno de trabajo

        * Instalar virtualEnv e instalarlo Linux
            ```sh
            python3 -m venv venv
            ```
            ```sh
            source venv/bin/activate
            ```
        * Windows
            ```sh
            python -m venv venv
            ```
            ```sh
            venv/Scripts/activate
            ```
    * Instale las dependencias necesarias usando:
        ```sh
        pip install pandas
        ```

2. Ejecución:

    * Modifique la ruta del archivo Excel en main.py para apuntar al archivo fuente.
    * Ejecute el script principal:
        ```sh
        python main.py
        ```
3. Salidas Generadas:

    * Archivos CSV y Excel que contienen tablas procesadas.
    * Log detallado del análisis en data_analysis.log.
## Manejo de Datos

* Tablas separadas o combinadas según la variable is_separate_the_tables.
* Limpieza incluye:
    * Eliminación de columnas irrelevantes.
    * Conversión de valores no numéricos a numéricos o eliminación de filas.
    * Normalización de fechas.
## Preguntas de Negocio
1. ¿Cuáles son las películas más alquiladas por los clientes y en qué tiendas?
2. ¿Qué tienda tiene el mayor número de rentas?
3. ¿Cuáles son las películas con mayor y menor duración de renta, y cómo influye en su popularidad?
4. ¿Cuál es la frecuencia de rentas por cliente?
5. ¿Existen patrones en las rentas?
