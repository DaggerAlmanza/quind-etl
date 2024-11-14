import logging


# Configuración del logging
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
