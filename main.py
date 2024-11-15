from log import Logging
from data import DataProcessor, REQUIRED_SHEETS


logging = Logging()
logger = logging.setup_logging()
processor = DataProcessor(logger)


def main():

    try:
        numeric_columns = {
            "inventory": ["inventory_id", "film_id", "store_id"],
            "film": ["film_id", "release_year", "length", "num_voted_users", "language_id", "rental_rate", "replacement_cost", "rental_duration"],
            "rental": ["rental_id", "inventory_id", "customer_id", "staff_id"],
            "customer": ["customer_id"],
            "store": ["store_id", "address_id", "active"]
        }

        excel_file = "/home/dager/Documentos/Proyectos/Pruebas Técnica/Quind/Films_2 (3).xlsx"
        dataframes = {}

        df = processor.validate_if_file_exist(excel_file)
        if not df or processor.check_columns(excel_file):
            return None
        for table in REQUIRED_SHEETS:
            try:
                processor.load_file(excel_file, table)
                logger.info(f"{'=' * 50}\nCargando tabla: {table}")

                # Pre-analizar
                preanalice = processor.dataframe_pre_analyze(table)
                logging.report_data_issues(table, preanalice)

                if table in numeric_columns:
                    processor.clean_numeric_columns(table, numeric_columns[table])
                if table in ["film", "customer"]:
                    processor.clean_columns(table)
                processor.normalize_the_dates()
                df = processor.analyze_dataframe(table)
                dataframes[table] = df

            except Exception as e:
                logger.error(f"Error al procesar la tabla {table}: {str(e)}")

        processor.verify_relationships(dataframes)
        processor.merge_tables(dataframes)
        processor.save_data()

    except Exception as e:
        logger.error(f"Error general en el procesamiento: {str(e)}")


if __name__ == "__main__":
    main()
