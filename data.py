import datetime
import logging
import os
import pandas as pd
import re

from log import Logging


REQUIRED_SHEETS = ["film", "inventory", "rental", "customer", "store"]
logger = Logging()


class DataProcessor:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.df = None

    def validate_if_file_exist(self, file_path: str) -> bool:
        """
        Carga y valida un archivo Excel.

        :param file_path: Ruta del archivo Excel a cargar.
        """
        # Verificar si el archivo existeexcel_file
        return os.path.isfile(file_path)

    def check_columns(self, file_path: str) -> list:
        # Leer las hojas del archivo Excel
        all_sheets = pd.ExcelFile(file_path).sheet_names
        cleaned_sheets = [sheet.strip() for sheet in all_sheets]

        # Validar que las hojas requeridas estén presentes
        missing_sheets = [
            sheet for sheet in REQUIRED_SHEETS if sheet not in cleaned_sheets
        ]
        if missing_sheets:
            self.logger.error(
                f"El archivo '{file_path}' no contiene las hojas requeridas: {missing_sheets}."
            )
        return missing_sheets

    def load_file(self, file_path: str, table: str):
        # Cargar cada hoja requerida en un DataFrame
        self.df = pd.read_excel(file_path, sheet_name=table)
        self.logger.info(f"Archivo '{file_path}' cargado correctamente.")

    def dataframe_pre_analyze(self, table_name: str):
        """
        Analiza un DataFrame para detectar valores nulos, duplicados y tipos de
        datos y guarda el resultado en un diccionario y en el registro de logger.

        Args:
            df: pandas DataFrame a analizar
            table_name: nombre de la tabla para el reporte
        """
        self.logger.info(f"Iniciando pre-análisis de la tabla {table_name}")

        # Diccionario para almacenar el análisis
        analysis_report = {
            "table_name": table_name,
            "general_info": {
                "num_rows": len(self.df),
                "num_columns": len(self.df.columns)
            },
            "data_types": self.df.dtypes.to_dict(),
            "null_values": self.df.isnull().sum().to_dict(),
            "duplicates": {"num_duplicates": self.df.duplicated().sum()},
            "basic_stats": self.df.describe().to_dict()
        }

        # Valores únicos para columnas categóricas
        categorical_columns = self.df.select_dtypes(include=["object"]).columns
        unique_values = {col: self.df[col].nunique() for col in categorical_columns}
        analysis_report["unique_values"] = unique_values

        # Registro en logger
        self.logger.info("Reporte de pre-análisis realizado")
        return analysis_report

    @staticmethod
    def extract_numeric_values(value):
        """Extrae el valor numérico de una cadena, si es posible."""
        match = re.search(r'\d+', str(value))
        return int(match.group()) if match else value

    def handle_non_numeric_values(
        self, column: str, table_name: str, action: str = "recover"
    ):
        """
        Maneja valores no numéricos en una columna: intenta recuperarlos o elimina las filas según la acción.

        Args:
            column (str): Nombre de la columna a procesar.
            table_name (str): Nombre de la tabla.
            action (str): Acción a realizar, "recover" para intentar recuperar valores o "drop" para eliminar filas.
                          Valores predeterminados: "recover".

        Returns:
            dict: Diccionario con los valores no numéricos procesados o eliminados.
        """
        non_numeric_values_dict = {}
        non_numeric_mask = pd.to_numeric(self.df[column], errors="coerce").isna()
        if non_numeric_mask.any():
            non_numeric_values = self.df[non_numeric_mask][column]
            non_numeric_indices = self.df[non_numeric_mask].index
            self.logger.info(f"Procesando valores no numéricos en '{column}' de la tabla '{table_name}'.")
            if action == "recover":
                # Intentar recuperar valores numéricos
                new_data = [DataProcessor.extract_numeric_values(data) for data in non_numeric_values.tolist()]
                if len(new_data) == len(non_numeric_indices):
                    self.df.loc[non_numeric_indices, column] = new_data
                    self.logger.info(f"Se reemplazaron {len(non_numeric_indices)} valores no numéricos en '{column}'.")
                else:
                    self.logger.error(
                        f"No se pudieron recuperar todos los valores: {len(new_data)} recuperados, "
                        f"{len(non_numeric_indices)} encontrados en '{column}'."
                    )
                non_numeric_values_dict[f"{table_name}_{column}"] = new_data
                non_numeric_values_dict["error"] = non_numeric_values
            elif action == "drop":
                # Eliminar filas con valores no numéricos
                self.df.drop(non_numeric_indices, inplace=True)
                non_numeric_values_dict[f"{table_name}_{column}"] = non_numeric_values.tolist()
                self.logger.info(f"Se eliminaron {len(non_numeric_indices)} filas con valores no numéricos en '{column}'.")
            else:
                self.logger.error(f"Acción '{action}' no válida. Use 'recover' o 'drop'.")
        return non_numeric_values_dict

    def clean_columns(self, table_name: str):
        """
        Elimina columnas específicas de un DataFrame según la tabla dada.

        Args:
            table_name (str): Nombre de la tabla (e.g., "film", "customer").
        """
        # Definición de las columnas a eliminar por tabla
        columns_to_remove = {
            "film": ["language_id", "original_language_id"],
            "customer": ["email", "address_id", "customer_id_old"]
        }
        # Normalizar columnas del DataFrame (remover espacios en los nombres)
        self.df.columns = self.df.columns.str.strip()

        # Verificar si la tabla tiene columnas para eliminar
        if table_name in columns_to_remove:
            columns = columns_to_remove[table_name]
            columns_found = [col for col in columns if col in self.df.columns]
            columns_not_found = [col for col in columns if col not in self.df.columns]

            # Eliminar las columnas encontradas
            if columns_found:
                self.df.drop(columns=columns_found, inplace=True)
                self.logger.info(f"Columnas eliminadas de {table_name}: {columns_found}")
            else:
                self.logger.info(f"No se encontraron columnas para eliminar en {table_name}.")

            # Informar sobre las columnas que no se encontraron
            if columns_not_found:
                self.logger.warning(
                    f"Las siguientes columnas no existen en {table_name} y no se pudieron eliminar: {columns_not_found}"
                )
        else:
            self.logger.error(f"No hay columnas definidas para eliminar en la tabla '{table_name}'.")

    def normalize_the_dates(self):
        # Normalizar columnas del DataFrame (remover espacios en los nombres)
        self.df.columns = self.df.columns.str.strip()

        # Limpiar y convertir columnas de fecha
        date_columns = [col for col in self.df.columns if "date" in col.lower()]
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col].str.strip().str.lstrip("'\"").str.rstrip("'\""), errors='coerce')

    def clean_numeric_columns(self, table_name: str, numeric_columns: list):
        """
        Limpia las columnas numéricas, eliminando filas con valores no numéricos

        Args:
            table_name: nombre de la tabla
            numeric_columns: lista de columnas que deben ser numéricas
        """
        rows_before = len(self.df)
        non_numeric_values_dict = {}
        self.df.columns = self.df.columns.str.strip()

        for column in numeric_columns:
            if column in self.df.columns:
                logger.report_data_issues(
                    f"{table_name}_data_change",
                    self.handle_non_numeric_values(column, table_name, "recover")
                )
                non_numeric_values_dict = self.handle_non_numeric_values(
                    column, table_name, "drop")
                # Convertir al tipo numérico adecuado
                if any(keyword in column for keyword in ["id", "year", "length", "num_voted"]):
                    self.df[column] = pd.to_numeric(self.df[column], errors="coerce").astype("Int64")
                else:
                    self.df[column] = pd.to_numeric(self.df[column], errors="coerce").astype("float64")

        if non_numeric_values_dict:
            logger.report_data_issues(f"{table_name}_non_numeric", non_numeric_values_dict)
            # self.logger.warning(f"Valores no numéricos encontrados en {table_name}: {non_numeric_values_dict}")
            rows_after = len(self.df)
            self.logger.info(f"Se eliminaron {rows_before - rows_after} filas con valores no numéricos en {table_name}")

    def analyze_dataframe(self, table_name: str):
        """
        Analiza un DataFrame para detectar valores nulos, duplicados y tipos de datos

        Args:
            table_name: nombre de la tabla para el reporte
        """
        self.logger.info(f"Dimensiones después de limpieza de {table_name}: {self.df.shape}")
        data_types = {column: dtype for column, dtype in self.df.dtypes.items()}
        self.logger.info(f"Tipos de datos en {table_name}: {data_types}")

        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.logger.warning(f"Se encontraron {duplicates} filas duplicadas")
        return self.df

    def verify_relationships(self, dfs: dict):
        """
        Verifica la integridad referencial entre las tablas

        Args:
            dfs: diccionario con los DataFrames {nombre_tabla: DataFrame}
        """
        self.logger.info("Verificando integridad referencial entre tablas")

        # Verificar integridad referencial entre film y inventory
        if "film" in dfs and "inventory" in dfs:
            invalid_films = set(dfs["inventory"]["film_id"]) - set(dfs["film"]["film_id"])
            if invalid_films:
                self.logger.error(f"Film_ids en inventory que no existen en film: {len(invalid_films)}")
                dfs["inventory"] = dfs["inventory"][~dfs["inventory"]["film_id"].isin(invalid_films)]

        # Verificar integridad referencial entre inventory y store
        if "inventory" in dfs and "store" in dfs:
            invalid_stores = set(dfs["inventory"]["store_id"]) - set(dfs["store"]["store_id"])
            if invalid_stores:
                self.logger.error(f"Store_ids en inventory que no existen en store: {len(invalid_stores)}")
                dfs["inventory"] = dfs["inventory"][~dfs["inventory"]["store_id"].isin(invalid_stores)]

    def merge_tables(self, dataframes: pd.DataFrame):
        film_df = dataframes["film"]
        inventory_df = dataframes["inventory"]
        rental_df = dataframes["rental"]
        customer_df = dataframes["customer"]

        merged_df = rental_df.merge(inventory_df, on="inventory_id")
        merged_df = merged_df.merge(film_df, on="film_id")
        customer_df = customer_df.rename(columns={"last_update": "customer_last_update"})
        merged_df = merged_df.merge(customer_df, on="customer_id")
        self.df = merged_df

    def save_data(self):
        output_file = f"cleaned_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with pd.ExcelWriter(output_file) as writer:
            self.df.to_excel(writer, sheet_name="clean_data", index=False)
            self.logger.info(f"Datos limpios guardados en: {output_file}")
