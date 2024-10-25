import pandas as pd
from sklearn.model_selection import train_test_split #Función para dividir el conjunto de datos en conjuntos de entrenamiento y prueba.
from sklearn.feature_extraction.text import CountVectorizer #Transforma una colección de documentos de texto en una matriz de recuentos de tokens.
from sklearn.naive_bayes import MultinomialNB #Clasificador Naive Bayes multinomial.
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report # Métricas de evaluación del modelo.

# Cargar el dataset
df = pd.read_excel('riesgos_dataset.xlsx')

# Filtrar las columnas necesarias
df = df[['nSectorEmp', 'idEvaluacion', 'ixRiesgo', 'ixPuesto', 'ixFuenteRL']]

# Convertir las columnas relevantes a cadenas de texto
df['ixRiesgo'] = df['ixRiesgo'].astype(str)
df['ixPuesto'] = df['ixPuesto'].astype(str)
df['ixFuenteRL'] = df['ixFuenteRL'].astype(str)

# Dividir el conjunto de datos en entrenamiento y prueba
train_data, test_data, train_labels, test_labels = train_test_split(df[['ixRiesgo', 'ixPuesto', 'ixFuenteRL']], df['nSectorEmp'], test_size=0.2, random_state=42)

# Vectorizar los datos de texto (Convierte el texto en una representación numérica utilizando la frecuencia de palabras.)
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_data.apply(lambda x: ' '.join(x), axis=1))
X_test = vectorizer.transform(test_data.apply(lambda x: ' '.join(x), axis=1))

# Entrenar un clasificador (Naive Bayes multinomial.)
classifier = MultinomialNB()
classifier.fit(X_train, train_labels)

# Realizar predicciones en el conjunto de prueba
predictions = classifier.predict(X_test)

# Agregar la columna de predicciones al DataFrame y guardar los resultados en una nueva columna que sera "SectorPertenece"
df['SectorPertenece'] = classifier.predict(vectorizer.transform(df[['ixRiesgo', 'ixPuesto', 'ixFuenteRL']].apply(lambda x: ' '.join(x), axis=1)))

# Guardar el DataFrame con las predicciones en un nuevo archivo Excel
df.to_excel('resultados_prediccion.xlsx', index=False)
