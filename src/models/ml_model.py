# src/models/ml_model.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Initialize a global model variable
model = None


def train_model(X_train, y_train):
    """
    Train a RandomForestClassifier model.

    Args:
        X_train (pd.DataFrame): Features for training.
        y_train (pd.Series): Target for training.
    """
    global model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, 'model.joblib')


def predict(input_data):
    """
    Make a prediction using the trained model.

    Args:
        input_data (list or array): Data to predict.

    Returns:
        The model's prediction.
    """
    if model is None:
        model = joblib.load('model.joblib')

    prediction = model.predict([input_data])
    return prediction[0]


def evaluate_model(X_test, y_test):
    """
    Evaluate the model's performance.

    Args:
        X_test (pd.DataFrame): Features for testing.
        y_test (pd.Series): Target for testing.

    Returns:
        float: The accuracy of the model.
    """
    global model
    if model is None:
        model = joblib.load('model.joblib')

    y_pred = model.predict(X_test)
    return accuracy_score(y_test, y_pred)
