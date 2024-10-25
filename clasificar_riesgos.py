import pandas as pd

# Cargar el dataset
df = pd.read_excel("riesgos_dataset.xlsx")

# Seleccionar columnas relevantes
df = df[['sCodCliente', 'nSectorEmp', 'idEvaluacion', 'ixRiesgo', 'ixPuesto', 'ixFuenteRL']]

# Inicializar una lista para almacenar los resultados
resultados = []

# Comprobar coincidencias en riesgos dentro de cada sector
for sector, data_sector in df.groupby('nSectorEmp'):
    # Iterar sobre cada riesgo único en el sector
    for riesgo, data_riesgo_actual in data_sector.groupby('ixRiesgo'):
        # Verificar si el riesgo procede de un puesto o una fuente
        riesgo_procede_de_puesto = (data_riesgo_actual['ixPuesto'] != 0).all()
        riesgo_procede_de_fuente = (data_riesgo_actual['ixFuenteRL'] != 0).all()

        # Comprobar si el riesgo, puesto y fuente son iguales dentro del sector
        es_igual = (data_riesgo_actual['ixPuesto'].nunique() == 1 and riesgo_procede_de_puesto) or \
                   (data_riesgo_actual['ixFuenteRL'].nunique() == 1 and riesgo_procede_de_fuente)

        # Almacenar los resultados en la lista
        for _, row in data_riesgo_actual.iterrows():
            resultados.append((row['sCodCliente'], sector, row['idEvaluacion'], riesgo,
                               row['ixPuesto'], row['ixFuenteRL'], int(es_igual)))

# Crear un nuevo DataFrame con los resultados
resultados_df = pd.DataFrame(resultados, columns=['sCodCliente', 'nSectorEmp', 'idEvaluacion', 'ixRiesgo',
                                                   'ixPuesto', 'ixFuenteRL', 'es_igual'])

# Exportar a Excel
resultados_df.to_excel("resultados_evaluaciones.xlsx", index=False)
print("Se han clasificado los riesgos")