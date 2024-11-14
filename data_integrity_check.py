import logging


def verify_relationships(dfs: dict, logger: logging.Logger):
    """
    Verifica la integridad referencial entre las tablas

    Args:
        dfs: diccionario con los DataFrames {nombre_tabla: DataFrame}
        logger: objeto logger para registro de eventos
    """
    logger.info("Verificando integridad referencial entre tablas")

    # Verificar film_id entre film e inventory
    if "film" in dfs and "inventory" in dfs:
        inv_films = set(dfs["inventory"]["film_id"])
        all_films = set(dfs["film"]["film_id"])
        invalid_films = inv_films - all_films
        if invalid_films:
            logger.error(f"Se encontraron {len(invalid_films)} film_ids en inventory que no existen en film")
            dfs["inventory"] = dfs["inventory"][~dfs["inventory"]["film_id"].isin(invalid_films)]

    # Verificar store_id entre inventory y store
    if "inventory" in dfs and "store" in dfs:
        inv_stores = set(dfs["inventory"]["store_id"])
        all_stores = set(dfs["store"]["store_id"])
        invalid_stores = inv_stores - all_stores
        if invalid_stores:
            logger.error(f"Se encontraron {len(invalid_stores)} store_ids en inventory que no existen en store")
            dfs["inventory"] = dfs["inventory"][~dfs["inventory"]["store_id"].isin(invalid_stores)]
