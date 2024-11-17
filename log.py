import datetime
import logging
import pandas as pd


class Logging:
    """Clase para manejar configuraciones y reportes de logging."""

    @staticmethod
    def setup_logging():
        """Configura el sistema de logging."""
        log_filename = "data_analysis.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_filename, mode="a"),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    @staticmethod
    def report_data_issues(table_name: str, data_issues: dict):
        """
        Genera un archivo CSV con problemas de calidad de datos.

        Args:
            table_name (str): Nombre de la tabla afectada.
            data_issues (dict): Diccionario con datos problemáticos.
        """
        logger = Logging.setup_logging()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{table_name}_{timestamp}.csv"

        df = pd.DataFrame(data_issues)
        if not df.empty:
            try:
                df.to_csv(file_name, index=True)
                logger.info(f"Archivo CSV generado: {file_name}")
            except Exception as e:
                logger.error(f"Error al guardar el archivo CSV para {table_name}: {str(e)}")
