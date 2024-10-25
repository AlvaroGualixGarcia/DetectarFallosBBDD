import pandas as pd

# Cargar el dataset
df = pd.read_excel("riesgos_dataset.xlsx")

# Filtrar el dataset para quedarnos solo con las columnas necesarias
df = df[['sCodCliente', 'nSectorEmp', 'idEvaluacion', 'ixRiesgo']]

# Identificar a qué sector está más asociado cada riesgo
frecuencia_por_sector = df.groupby(['nSectorEmp', 'ixRiesgo']).size().reset_index(name='Frecuencia')
sector_max_asociado = frecuencia_por_sector.loc[frecuencia_por_sector.groupby('ixRiesgo')['Frecuencia'].idxmax()]

# Fusionar el DataFrame original con el DataFrame de los sectores máximos asociados
df = df.merge(sector_max_asociado[['ixRiesgo', 'nSectorEmp']], on='ixRiesgo')

# Calcular el total de riesgos por evaluación de cada empresa
total_riesgos_por_evaluacion = df.groupby(['sCodCliente', 'idEvaluacion']).size().reset_index(name='TotalRiesgos')

# Fusionar el DataFrame original con el DataFrame de los totales de riesgos por evaluación
df = df.merge(total_riesgos_por_evaluacion, on=['sCodCliente', 'idEvaluacion'])

# Calcular el porcentaje de acierto de cada evaluación de riesgos para cada empresa
def calcular_porcentaje_acierto(group):
    total_riesgos = group['TotalRiesgos'].iloc[0]
    riesgos_correctos = sum(group['nSectorEmp_x'] == group['nSectorEmp_y'])
    return (riesgos_correctos / total_riesgos) * 100

# Calcular el porcentaje de acierto de cada evaluación de riesgos para cada empresa
acierto_por_evaluacion = df.groupby(['sCodCliente', 'idEvaluacion']).apply(calcular_porcentaje_acierto).reset_index(name='PorcentajeAcierto')

# Mostrar el sector más asociado a cada riesgo
print("Sector más asociado a cada riesgo:")
print(sector_max_asociado)

# Mostrar el porcentaje de acierto de cada evaluación de riesgos para cada empresa
print("\nPorcentaje de acierto de cada evaluación de riesgos para cada empresa:")
print(acierto_por_evaluacion)
