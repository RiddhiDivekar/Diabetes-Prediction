import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load your dataset
data = pd.read_csv("C:/Users/Riddhi Divekar/OneDrive/Desktop/Diabetes Project/diabetes.csv")

# Prepare data
X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "C:/Users/Riddhi Divekar/OneDrive/Desktop/Diabetes Project/diabetes_model.pkl")

print("✅ Model trained and saved as 'diabetes_model.pkl'")
