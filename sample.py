import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
train_df = pd.read_csv('insta_train.csv')
test_df = pd.read_csv('insta_test.csv')

# Feature selection and target definition
features = ['profile pic', 'nums/length username', 'fullname words',
            'nums/length fullname', 'name==username', 'description length',
            'external URL', 'private', '#posts', '#followers', '#follows']
target = 'fake'

X_train = train_df[features]
y_train = train_df[target]
X_test = test_df[features]
y_test = test_df[target]

# Handle class imbalance with SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Create preprocessing and modeling pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
])

# Train the model
pipeline.fit(X_train_res, y_train_res)

# Save the model pipeline and metadata
joblib.dump({
    'pipeline': pipeline,
    'features': features,
    'class_names': ['Real', 'Fake'],
    'smote': smote
}, 'fake_profile_model.pkl')

# Evaluation
y_pred = pipeline.predict(X_test)
print("\nModel Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
rf_model = pipeline.named_steps['model']
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)

# Plot feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance)
plt.title('Feature Importance')
plt.tight_layout()
plt.savefig('feature_importance.png')  # Save plot instead of showing
plt.close()

# Save predictions
results = test_df.copy()
results['predicted_fake'] = y_pred
results['prediction_correct'] = results['fake'] == results['predicted_fake']
results.to_csv('fake_profile_predictions.csv', index=False)