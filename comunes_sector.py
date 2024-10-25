import pandas as pd

# Paso 1: Cargar las columnas necesarias del Excel
excel_path = 'riesgos_dataset.xlsx' #excel que vamos a leer
columns_of_interest = ['nSectorEmp', 'ixRiesgo'] #columnas que nos interesan
data = pd.read_excel(excel_path, usecols=columns_of_interest) #leemos excel y cogemos solo las columnas y lo guardamos en la variabla data

# Paso 2: Identificar riesgos únicos por sector y mostrar en forma de lista
sectores = data['nSectorEmp'].unique() #filtramos los sectores

#bucle para cada sector
for sector in sorted(sectores): #y ordenamos por numero de sector
    sector_data = data[data['nSectorEmp'] == sector]
    riesgos_sector = sorted(sector_data['ixRiesgo'].unique()) #filtramos riesgos para no mostrarlos repetidos y los ordenamos

    print(f"Riesgos del sector {sector}: {riesgos_sector}\n")
