import datetime
import pandas as pd

from inspect_dataframe import analyze_dataframe
from clean_data import clean_numeric_columns
from log_configuration import setup_logging
from exploratory_data_analysis import dataframe_pre_analyze
from data_integrity_check import verify_relationships


def main():
    # Configurar logging
    logger = setup_logging()
    # logger.info("Iniciando análisis de calidad de datos")

    try:

        # Definir columnas numéricas para cada tabla
        numeric_columns = {
            "inventory": ["inventory_id", "film_id", "store_id"],
            "film": [
                "film_id", "release_year", "length",
                "num_voted_users", " language_id",
                "rental_rate", "replacement_cost",
                " rental_duration"
            ],
            "rental": ["rental_id", "inventory_id", "customer_id", "staff_id"],
            "customer": ["customer_id"],
            "store": ["store_id", "address_id", "active"]
        }

        # Leer cada hoja del archivo Excel
        excel_file = "/home/dager/Documentos/Proyectos/Pruebas Técnica/Quind/Films_2 (3).xlsx"
        tables = ["film", "inventory", "rental", "customer", "store"]
        dataframes = {}

        for table in tables:
            try:
                logger.info(f"{'=' * 50}\nCargando tabla: : {table}")
                df = pd.read_excel(excel_file, sheet_name=table)

                # Pre-analizar cada DataFrame
                dataframe_pre_analyze(df, table, logger)

                # Limpiar columnas numéricas si la tabla está en numeric_columns
                if table in numeric_columns:
                    df = clean_numeric_columns(
                        df, table, numeric_columns[table], logger
                    )

                # Analizar DataFrame
                df = analyze_dataframe(df, table, logger)

                dataframes[table] = df

            except Exception as e:
                logger.error(f"Error al procesar la tabla {table}: {str(e)}")

        # Verificar relaciones entre tablas
        verify_relationships(dataframes, logger)

        # Guardar los DataFrames limpios en un nuevo archivo Excel
        output_file = f"cleaned_data_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"
        with pd.ExcelWriter(output_file) as writer:
            for table_name, df in dataframes.items():
                df.to_excel(writer, sheet_name=table_name, index=False)
        logger.info(f"Datos limpios guardados en: {output_file}")

    except Exception as e:
        logger.error(f"Error general en el procesamiento: {str(e)}")


if __name__ == "__main__":
    main()
