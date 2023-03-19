import requests
from datetime import datetime
import pandas as pd

#EndYear = int(datetime.now().strftime("%Y"))
#InitialYear = EndYear - 2

def ExtractData(indicator, InitialYear, EndYear = None):
    """
    Con esta función se extraen los datos de los indicadores de Chile según API de https://mindicador.cl

    Args:
        indicator: str que debe indicar el indicador que se extraerá. Los posibles datos son [uf, ivp, dolar, dolar_intercambio, euro, ipc, utm, imacec, tpm, libra_cobre, tasa_desempleo, bitcoin]

        InitialYear: int con año que se desea extraer.

        EndYear: Argumento opcional en caso de requerir el análisis por más años.

    Returns:
        Dataframe: El retorno es un df con los datos del año o años seleccionados junto con el valor en CLP.
    """
    if EndYear is None:
        EndYear = InitialYear
    else:
        # Lo siguiente se realiza para no tener inconvenientes en el for por el índice de python
        EndYear = EndYear + 1
    if InitialYear > int(datetime.now().strftime("%Y")):
        return print('El año no puede sobrepasar al actual')

    indicadores_df = pd.DataFrame()
    if InitialYear == EndYear:
        url = f'https://mindicador.cl/api/{indicator}/{InitialYear}'
        response = requests.get(url)
        df = pd.DataFrame.from_dict(response.json())
        df = pd.DataFrame(df['serie'].values.tolist())
        indicadores_df = pd.concat([indicadores_df, df], ignore_index=True)
    elif InitialYear < EndYear:
        for year in range(InitialYear, EndYear):
            url = f'https://mindicador.cl/api/{indicator}/{year}'
            response = requests.get(url)
            df = pd.DataFrame.from_dict(response.json())
            df = pd.DataFrame(df['serie'].values.tolist())
            indicadores_df = pd.concat([indicadores_df, df], ignore_index=True)
    else:
        return print('El año final debe ser mayor al inicial')
    return indicadores_df