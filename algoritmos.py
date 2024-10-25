import pandas as pd  
from sklearn.model_selection import train_test_split  
from sklearn.ensemble import RandomForestClassifier  
from sklearn.svm import SVC  
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.ensemble import GradientBoostingClassifier  
from sklearn.metrics import accuracy_score  

# Paso 1: Cargar el dataset desde el archivo 'riesgos_dataset.xlsx' y lo guarda en un DataFrame llamado 'df'
df = pd.read_excel("riesgos_dataset.xlsx")

# Paso 2: Preprocesar los datos (si es necesario)

# Filtra el DataFrame para conservar solo las columnas 'sCodCliente', 'nSectorEmp', 'idEvaluacion' y 'ixRiesgo'
df = df[['sCodCliente', 'nSectorEmp', 'idEvaluacion', 'ixRiesgo']]  

# Agrupa los datos por 'sCodCliente' e 'ixRiesgo', luego cuenta la frecuencia de cada combinación y resetea el índice
frecuencia_por_sector = df.groupby(['sCodCliente', 'ixRiesgo']).size().reset_index(name='Frecuencia')  

# Encuentra el sector más asociado a cada riesgo buscando el índice del máximo valor de frecuencia para cada 'ixRiesgo'
sector_max_asociado = frecuencia_por_sector.loc[frecuencia_por_sector.groupby('ixRiesgo')['Frecuencia'].idxmax()]  

# Fusiona el DataFrame original 'df' con el DataFrame de sectores máximos asociados usando 'ixRiesgo' como clave
df = df.merge(sector_max_asociado[['ixRiesgo', 'sCodCliente']], on='ixRiesgo') 

# Calcula el total de riesgos por evaluación de cada empresa contando el número de riesgos de cada combinación de 'sCodCliente' y 'idEvaluacion'
total_riesgos_por_evaluacion = df.groupby(['sCodCliente_y', 'idEvaluacion']).size().reset_index(name='TotalRiesgos')  

# Paso 3: Entrenar los modelos de clasificación

# Selección de características y variable objetivo
X = df[['idEvaluacion', 'ixRiesgo']]  
y = df['sCodCliente_y']  

# División de datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  

# Inicialización de los clasificadores
classifiers = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(),
    "KNN": KNeighborsClassifier(),
    "Gradient Boosting": GradientBoostingClassifier()
}

# Entrenamiento y evaluación de los modelos
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{name}: Accuracy = {accuracy}")

# Paso 4: Predecir el sector para cada evaluación en el conjunto de prueba
predictions = {}
for name, clf in classifiers.items():
    predictions[name] = clf.predict(X_test)

# Paso 5: Calcular el porcentaje de acierto en cada evaluación para cada empresa
results = {}
for name, pred in predictions.items():
    results[name] = pd.DataFrame({'idEvaluacion': X_test['idEvaluacion'], 'Predicciones': pred})
    results[name]['sCodCliente'] = y_test
    results[name]['Acierto'] = results[name]['Predicciones'] == results[name]['sCodCliente']
    results[name] = results[name].groupby(['sCodCliente', 'idEvaluacion']).agg({'Acierto': 'mean'}).reset_index()
    results[name]['PorcentajeAcierto'] = results[name]['Acierto'] * 100

# Paso 6: Guardar los resultados en un archivo Excel
for name, result_df in results.items():
    result_df.to_excel(f"{name}_acierto_por_evaluacion.xlsx", index=False)
