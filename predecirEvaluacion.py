import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Cargar el dataset
df = pd.read_excel('riesgos_dataset.xlsx')

# Filtrar las columnas necesarias
df = df[['nSectorEmp', 'idEvaluacion', 'ixRiesgo', 'ixPuesto', 'ixFuenteRL']]

# Convertir las columnas relevantes a cadenas de texto
df['ixRiesgo'] = df['ixRiesgo'].astype(str)
df['ixPuesto'] = df['ixPuesto'].astype(str)
df['ixFuenteRL'] = df['ixFuenteRL'].astype(str)

# Agrupar los riesgos por evaluación y concatenarlos
grouped_df = df.groupby('idEvaluacion')['ixRiesgo'].apply(lambda x: ' '.join(x)).reset_index()

# Verificar si la columna 'nSectorEmp' está presente en 'grouped_df'
if 'nSectorEmp' not in df.columns:
    raise ValueError("La columna 'nSectorEmp' no está presente en el DataFrame 'grouped_df'.")

# Filtrar evaluaciones con información en 'nSectorEmp'
evaluaciones_con_sector = df.dropna(subset=['nSectorEmp'])

# Dividir el conjunto de datos en entrenamiento y prueba
train_data, test_data, train_labels, test_labels = train_test_split(evaluaciones_con_sector['ixRiesgo'], evaluaciones_con_sector['nSectorEmp'], test_size=0.2, random_state=42)

# Vectorizar los datos de texto
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_data)
X_test = vectorizer.transform(test_data)

# Entrenar un clasificador (usaremos Naive Bayes como ejemplo, puedes cambiarlo según sea necesario)
classifier = MultinomialNB()
classifier.fit(X_train, train_labels)

# Realizar predicciones en el conjunto de prueba
predictions = classifier.predict(X_test)

# Agregar la columna de predicciones al DataFrame
evaluaciones_con_sector['SectorPertenece'] = classifier.predict(vectorizer.transform(evaluaciones_con_sector['ixRiesgo']))

# Guardar el DataFrame con las predicciones en un nuevo archivo Excel
evaluaciones_con_sector.to_excel('resultados_prediccion_evaluaciones.xlsx', index=False)
