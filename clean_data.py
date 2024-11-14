import logging
import pandas as pd


def clean_numeric_columns(
    df: pd.DataFrame,
    table_name: str,
    numeric_columns: list,
    logger: logging.Logger
):
    """
    Limpia las columnas numéricas, eliminando filas con valores no numéricos

    Args:
        df: DataFrame a limpiar
        table_name: nombre de la tabla
        numeric_columns: lista de columnas que deben ser numéricas
        logger: objeto logger para registro de eventos
    """
    rows_before = len(df)
    df.columns = df.columns.str.strip()
    non_numeric_values_dict = {}

    for column in numeric_columns:
        if column in df.columns:
            # Verificar si la columna contiene valores no numéricos
            non_numeric_mask = pd.to_numeric(df[column], errors="coerce").isna()
            if non_numeric_mask.any():
                non_numeric_values = df[non_numeric_mask][column].unique()
                non_numeric_values_dict[f"{table_name}.{column}"] = non_numeric_values.tolist()

                # Eliminar filas con valores no numéricos
                df.drop(df[non_numeric_mask].index, inplace=True)

                # Convertir la columna al tipo numérico apropiado
                if "id" in column or "year" in column or "length" in column or "num_voted" in column:
                    df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
                else:
                    df[column] = pd.to_numeric(df[column], errors="coerce").astype("float64")
    if non_numeric_values_dict:
        logger.warning(f"Valores no numéricos encontrados en {table_name}: {non_numeric_values_dict}")

    rows_after = len(df)
    if rows_before != rows_after:
        logger.info(f"Se eliminaron {rows_before - rows_after} filas con valores no numéricos en {table_name}")

    return df
