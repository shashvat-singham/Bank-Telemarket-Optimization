import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report

# Load the dataset
data = pd.read_csv('bank_raw.csv', delimiter=';')

# Encode the target column ('y')
label_encoder = LabelEncoder()
data['y'] = label_encoder.fit_transform(data['y'])

# Encode categorical features
categorical_cols = data.select_dtypes(include=['object']).columns
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

# Splitting the dataset into features and target
X = data_encoded.drop(columns=['y'])
y = data_encoded['y']

# Splitting into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize and train the XGBoost model
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = xgb_model.predict(X_test)

# Add predictions to the test set
X_test['Predicted'] = y_pred

# Filter potential clients (subscribed: 1)
potential_clients = X_test[X_test['Predicted'] == 1]

# Save the potential clients to a CSV file
potential_clients.to_csv('potential_clients.csv', index=False)

print("Predictions saved to 'potential_clients.csv'")
