import pandas as pd
import logging


def dataframe_pre_analyze(
    df: pd.DataFrame, table_name: str, logger: logging.Logger
):
    """
    Analiza un DataFrame para detectar valores nulos, duplicados y tipos de
    datos y guarda el resultado en un diccionario y en el registro de logger.

    Args:
        df: pandas DataFrame a analizar
        table_name: nombre de la tabla para el reporte
    """

    # Diccionario para almacenar el análisis
    analysis_report = {}

    # Información general
    analysis_report["table_name"] = table_name
    analysis_report["general_info"] = {
        "num_rows": len(df),
        "num_columns": len(df.columns)
    }

    # Tipos de datos
    analysis_report["data_types"] = df.dtypes.to_dict()

    # Valores nulos
    null_counts = df.isnull().sum()
    null_percentages = (df.isnull().sum() / len(df)) * 100
    null_info = pd.DataFrame({
        "Valores Nulos": null_counts,
        "Porcentaje Nulos": null_percentages
    })
    analysis_report["null_values"] = null_info[null_info["Valores Nulos"] > 0].to_dict()

    # Duplicados
    analysis_report["duplicates"] = {
        "num_duplicates": df.duplicated().sum()
    }

    # Estadísticas básicas para columnas numéricas
    analysis_report["basic_stats"] = df.describe().to_dict()

    # Valores únicos para columnas categóricas
    categorical_columns = df.select_dtypes(include=["object"]).columns
    unique_values = {}
    for col in categorical_columns:
        unique_values[col] = df[col].nunique()
    analysis_report["unique_values"] = unique_values

    # Registro en logger
    logger.info("=" * 50)
    logger.info(f"Reporte completo de pre-análisis: {analysis_report}")
