def cargar_csv(ruta):
    #Carga un archivo CSV desde una ruta especificada y lo retorna como un DataFrame.
    """
    Parámetros:
    ruta (str): Ruta del archivo CSV a cargar.

    Retorna:
    pandas.DataFrame: DataFrame con los datos del archivo si la carga es exitosa.

    Manejo de errores:
    - Si el archivo no se encuentra en la ruta especificada, se captura la excepción
      FileNotFoundError y se muestra un mensaje informativo por consola.
    """
    import pandas as pd
    try:
        # Intento de lectura del archivo CSV
        return pd.read_csv(ruta)
    except FileNotFoundError:
        # Manejo del error en caso de que el archivo no exista
        print("Archivo no encontrado")