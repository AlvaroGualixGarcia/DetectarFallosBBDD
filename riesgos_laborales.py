import pandas as pd
from tabulate import tabulate

# Paso 1: Cargar las columnas necesarias del Excel
excel_path = 'riesgos_dataset.xlsx' #cargar excel
columns_of_interest = ['sCodCliente', 'nSectorEmp', 'idEvaluacion', 'ixRiesgo', 'ixPuesto', 'ixFuenteRL'] #seleccionar columnas que necesitamos
data = pd.read_excel(excel_path, usecols=columns_of_interest) #recoger los datos que necesitamos

# Paso 2: Identificar riesgos por sector
sectores = data.groupby('nSectorEmp') #agrupamos por sectores
riesgos_por_sector = {} #creamos diccionario

for sector, sector_data in sectores:
    riesgos_por_sector[sector] = set(sector_data['ixRiesgo']) #introducimos dentro del diccionario por sectores el riesgo

# Paso 3: Verificar el cumplimiento por empresa y ordenar los resultados
resultados = [] #creamos array/lista vacia

for empresa, empresa_data in data.groupby('sCodCliente'): 
    sector_empresa = empresa_data['nSectorEmp'].values[0] #seleccionamos empresa y cogemos todos sus datos
    riesgos_sector = riesgos_por_sector.get(sector_empresa, set()) #seleccionamos el sector al que pertenece para ver que riesgos tiene ese sector

    riesgos_cumplidos = set(empresa_data['ixRiesgo']) #cogemos los riesgos de la empresa
    porcentaje_cumplimiento = (len(riesgos_cumplidos.intersection(riesgos_sector)) / len(riesgos_sector)) * 100 #dividimos entre los riesgos que se cuentan la empresa y los riesgos que tiene el sector y multiplicamos por 100 para sacar el%

    resultados.append({ #añadimos los resultados a la lista de resultados
        'empresa': empresa, #numero de la empresa
        'sector': sector_empresa, #numero de sector de la empresa
        'cumplimiento': porcentaje_cumplimiento #porcentaje de cumplimiento de revision de riesgos
    })

# Ordenar los resultados por sector (de menor a mayor) y por porcentaje de cumplimiento descendente
resultados_ordenados = sorted(resultados, key=lambda x: (x['sector'], -x['cumplimiento']))

# Mostrar los resultados en forma de tabla
headers = ["Empresa", "Sector", "Cumplimiento (%)"]
table = [[resultado['empresa'], resultado['sector'], f"{resultado['cumplimiento']:.2f}%"] for resultado in resultados_ordenados]

print(tabulate(table, headers=headers, tablefmt="pretty"))
