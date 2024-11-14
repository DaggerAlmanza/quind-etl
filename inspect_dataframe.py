import pandas as pd


def analyze_dataframe(df: pd.DataFrame, table_name: str, logger):
    """
    Analiza un DataFrame para detectar valores nulos, duplicados y tipos de datos

    Args:
        df: pandas DataFrame a analizar
        table_name: nombre de la tabla para el reporte
        logger: objeto logger para registro de eventos
    """

    # Información general
    logger.info(f"Dimensiones luego de limpienza de {table_name}: {df.shape}")

    # Tipos de datos
    data_types = {column: dtype for column, dtype in df.dtypes.items()}
    logger.info(f"Tipos de datos en {table_name}: {data_types}")

    # Duplicados
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        logger.warning(f"Se encontraron {duplicates} filas duplicadas")

    return df
