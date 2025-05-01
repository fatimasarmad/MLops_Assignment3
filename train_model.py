import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

def train_model(data_path='processed_data.csv', model_path='model.pkl'):
    df = pd.read_csv(data_path)

   
    X = df[['Humidity (%)', 'Wind Speed (m/s)']]
    y = df['Temperature (°C)']

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()
