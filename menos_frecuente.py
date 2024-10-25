import pandas as pd
from tabulate import tabulate

# Paso 1: Cargar las columnas necesarias del Excel
excel_path = 'riesgos_dataset.xlsx' #seleccionar excel
columns_of_interest = ['sCodCliente', 'nSectorEmp', 'ixRiesgo'] #seleccionar columnas que necesitamos
data = pd.read_excel(excel_path, usecols=columns_of_interest) #filtrar el excel y guardar los datos

# Paso 2: Identificar el riesgo menos frecuente por empresa
resultados = [] #crear array vacio

for (empresa, sector), empresa_data in data.groupby(['sCodCliente', 'nSectorEmp']):
    riesgo_menos_frecuente = empresa_data['ixRiesgo'].value_counts().idxmin() #calcular riesgo menos frecuente
    cantidad_ocurrencias = empresa_data['ixRiesgo'].value_counts().min() #contar veces que ha pasado el riesgo menos frecuente

    resultados.append({ #añadir datos al diccionario
        'empresa': empresa,
        'sector': sector,
        'riesgo_menos_frecuente': riesgo_menos_frecuente,
        'cantidad_ocurrencias': cantidad_ocurrencias
    })

# Ordenar los resultados por sector y por cantidad de ocurrencias
resultados_ordenados = sorted(resultados, key=lambda x: (x['sector'], x['cantidad_ocurrencias']))

# Mostrar los resultados en forma de tabla
headers = ["Empresa", "Sector", "Riesgo Menos Frecuente", "Cantidad de Ocurrencias"]
table = [
    [resultado['empresa'], resultado['sector'], resultado['riesgo_menos_frecuente'], resultado['cantidad_ocurrencias']]
    for resultado in resultados_ordenados
]

print(tabulate(table, headers=headers, tablefmt="pretty"))
