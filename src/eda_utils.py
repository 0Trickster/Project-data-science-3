# Funciones de detección de outliers y duplicados 

def detectar_outliers_iqr(df):
    #Detecta valores atípicos (outliers) en un DataFrame utilizando el método del rango intercuartílico (IQR)
    """
    Retorna:
    dict: Diccionario con estadísticas por cada columna numérica, incluyendo:
          - skew: asimetría de la distribución
          - cantidad_outliers: número de valores fuera de los límites
          - limite_inferior: límite inferior calculado
          - limite_superior: límite superior calculado
    """
    resultados = {}
    columnas_numericas = df.select_dtypes(include='number').columns

    for col in columnas_numericas:

        serie = df[col].dropna()    # Se eliminan valores nulos para evitar sesgos en el cálculo
        # Cálculo de los cuartiles
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1   # Rango intercuartílico

        # Definición de límites para detección de outliers
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        # Identificación de valores fuera de los límites
        mascara = (serie < limite_inferior) | (serie > limite_superior)

        # Almacenamiento de resultados
        resultados[col] = {
            "skew": serie.skew(),
            "cantidad_outliers": mascara.sum(),
            "limite_inferior": limite_inferior,
            "limite_superior": limite_superior
        }

    return resultados


def detectar_outliers_3sigmas(df):
    #Detecta valores atípicos (outliers) utilizando la regla de las 3 desviaciones estándar

    """
    Retorna:
    dict: Diccionario con estadísticas por columna numérica, incluyendo:
          - skew: asimetría de la distribución
          - cantidad_outliers: número de valores fuera de los límites
          - limite_inferior: media - 3 * desviación estándar
          - limite_superior: media + 3 * desviación estándar
    """
    resultados = {}
    columnas_numericas = df.select_dtypes(include='number').columns

    for col in columnas_numericas:
        serie = df[col].dropna()

        # Cálculo de media y desviación estándar
        media = serie.mean()
        std = serie.std()

        # Definición de límites según regla de 3 sigmas
        limite_inferior = media - 3 * std
        limite_superior = media + 3 * std

        # Identificación de outliers
        mascara = (serie < limite_inferior) | (serie > limite_superior)

        resultados[col] = {
            "skew": serie.skew(),
            "cantidad_outliers": mascara.sum(),
            "limite_inferior": limite_inferior,
            "limite_superior": limite_superior
        }

    return resultados


def eliminar_outliers_3sigmas(serie):
    #Genera una máscara booleana para identificar outliers en una serie
    #utilizando la regla de las 3 desviaciones estándar
    
    """
    Retorna:
    tuple:
        - mascara (pandas.Series): True en posiciones con outliers
        - limite_inferior (float): límite inferior calculado
        - limite_superior (float): límite superior calculado
    """
    media = serie.mean()
    std = serie.std()

    limite_inferior = media - 3 * std
    limite_superior = media + 3 * std

    # Máscara de detección de valores atípicos
    mascara = (serie < limite_inferior) | (serie > limite_superior)

    return mascara, limite_inferior, limite_superior


# DEPRECADO: no se hallaron duplicados que deban borrarse
def detectar_duplicados(df):
    #Calcula la cantidad de valores duplicados por columna en un DataFrame

    #Nota:
    #Esta función ha sido marcada como deprecada debido a que no se encontraron
    #duplicados relevantes que justifiquen su uso en el análisis actual.

    """
    Retorna:
    dict: Diccionario con la cantidad de duplicados por columna.
    """
    resultados = {}

    for col in df.columns:

        duplicados = df[col].duplicated().sum()

        resultados[col] = {
            "cantidad_duplicados": duplicados
        }

    return resultados