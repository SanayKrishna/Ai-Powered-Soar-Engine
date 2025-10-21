import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Loading training data...")
df = pd.read_csv('data/training_alerts.csv')

X = df.drop('is_critical', axis=1)
y = df['is_critical']

categorical_features = ['source', 'asset_type', 'user_role']
textual_feature = 'description'

preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(stop_words='english'), textual_feature),
        ('categorical', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', model)])

print("Splitting data and training the model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipeline.fit(X_train, y_train)

print("Model training complete.")

y_pred = pipeline.predict(X_test)
print(f"\nModel Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Saving trained model pipeline to 'risk_model.joblib'...")
joblib.dump(pipeline, 'risk_model.joblib')
print("Save complete. The model is ready for integration.")