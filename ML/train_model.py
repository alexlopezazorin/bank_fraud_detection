"""
created by: Alejandro Lopez Azorin
LinkedIn: www.linkedin.com/in/alejandro-lopez-azorin/
"""

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import numpy as np
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


# -------------------- RUTAS --------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "final_data.csv"
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"

# -------------------- CARGA DE df  --------------------
df = pd.read_csv(DATA_PATH, index_col=0)
print("This is my initial data set:\n", df)

# -------------------- VECTORIZACION DE CONCEPTS Y ESCALAR VARIABLES NUMERICAS --------------------

text_features = 'Concept'
numeric_features = ['Amount', 'time_sin', 'time_cos', 'Is_Night']

preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(ngram_range=(1,2)), text_features),
        ("num", StandardScaler(), numeric_features)
    ]
)

# -------------------- CARGA DE DATOS --------------------
X = df[['Amount','Concept','time_sin','time_cos','Is_Night']]
y = df['Is_Fraud']


# -------------------- TRAIN / TEST SPLIT --------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1) #20%test, 80%training ---> de 200.000 rows: 160.000 for training and 40.000 for testing

# -------------------- MODELO --------------------
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=1))
])

pipeline.fit(X_train, y_train)

preprocessor = pipeline.named_steps['preprocessor']
X_train_transformed = preprocessor.transform(X_train)
print("\nHemos vectorizado la columna 'Concept', obteniendo features de esta forma:",X_train_transformed.shape)

tfidf = preprocessor.named_transformers_["text"]
feature_names = tfidf.get_feature_names_out()
print("\nLas features obtenidas al vectorizar son: \n",feature_names)

# -------------------- EVALUACION --------------------
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

print("\nMETRICAS DE EVALUACION:")
print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))


# -------------------- GUARDAR MODELO --------------------
joblib.dump(pipeline, MODEL_PATH)
print(f"\nModel saved successfully at: {MODEL_PATH}")
