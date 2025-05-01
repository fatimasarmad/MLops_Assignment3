import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def train_model(data_path='processed_data.csv', model_path='model.pkl'):
    print(f"\nLoading data from {data_path}...")
    df = pd.read_csv(data_path)

    # Select features and target
    X = df[['Humidity (%)', 'Wind Speed (m/s)']]
    y = df['Temperature (°C)']

    print("\nSample features (X):")
    print(X.head())

    print("\nSample target (y):")
    print(y.head())

    print("\nTraining Linear Regression model...")
    model = LinearRegression()
    model.fit(X, y)

    # Print model coefficients
    print(f"\nModel Coefficients: {model.coef_}")
    print(f"Model Intercept: {model.intercept_:.4f}")

    # Evaluate on training data
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    print(f"Training Mean Squared Error (MSE): {mse:.4f}")

    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"\nModel trained and saved to {model_path}\n")

if __name__ == "__main__":
    train_model()
