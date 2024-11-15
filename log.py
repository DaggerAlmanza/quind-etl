import datetime
import logging
import pandas as pd


class Logging:

    @staticmethod
    def setup_logging():
        """Configura el sistema de logging para que use un único archivo y agregue nuevos registros."""
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
    def report_data_issues(
        table_name: str,
        data_issues: dict
    ):
        """
        Crea un archivo CSV para registrar problemas de calidad de datos.

        :param table_name: Nombre de la tabla afectada.
        :param data_issues: DataFrame con los datos problemáticos.
        """
        logger = Logging.setup_logging()
        # Crear el nombre del archivo con fecha y hora completa
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{table_name}_{timestamp}.csv"
        df = pd.DataFrame(data_issues)

        try:
            # Guardar el DataFrame como un archivo CSV
            if not df.empty:  # Verificar si el DataFrame tiene datos
                df.to_csv(file_name, index=True)
                logger.info(f"Archivo CSV generado: {file_name}")
        except Exception as e:
            logger.error(f"Error al guardar el archivo CSV para {table_name}: {str(e)}")
