import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def train_model(input_file="input/weather.csv"):
    # Reading the CSV file.
    df = pd.read_csv(input_file)
    print("imported csv file")
    df = df.filter(items=["M_SESSION_UID", "M_SESSION_TIME", "M_PLAYER_CAR_INDEX", "TIMESTAMP", "M_TRACK_TEMPERATURE",
                          "M_FORECAST_ACCURACY", "M_AIR_TEMPERATURE", "M_NUM_WEATHER_FORECAST_SAMPLES", "M_TRACK_ID",
                          "M_SESSION_TYPE", "M_SESSION_DURATION", "M_WEATHER_FORECAST_SAMPLES_M_SESSION_TYPE",
                          "M_TIME_OFFSET", "M_WEATHER_FORECAST_SAMPLES_M_WEATHER",
                          "M_WEATHER_FORECAST_SAMPLES_M_TRACK_TEMPERATURE", "M_TRACK_TEMPERATURE_CHANGE",
                          "M_WEATHER_FORECAST_SAMPLES_M_AIR_TEMPERATURE", "M_AIR_TEMPERATURE_CHANGE",
                          "M_RAIN_PERCENTAGE",
                          "M_WEATHER"])
    print(df.shape)

    df.dropna(inplace=True)
    print(df.shape)

    df = df.loc[df['M_NUM_WEATHER_FORECAST_SAMPLES'] != 0]
    print(df.shape)

    df_full = df.copy()
    print(df_full.shape)

    X = df_full[
        ["M_WEATHER", "M_TRACK_TEMPERATURE", "M_FORECAST_ACCURACY", "M_AIR_TEMPERATURE", "M_TIME_OFFSET"]].values
    y = df_full.filter(items=["M_WEATHER_FORECAST_SAMPLES_M_WEATHER"])

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

    dt = DecisionTreeClassifier()
    dt.fit(x_train, y_train)
    print("score :", dt.score(x_test, y_test))

    print(f"\nValues that happened are :\n{df_full['M_WEATHER'].value_counts()}\n")
    print(f"\nValues that the fake system predicted are {df_full['M_WEATHER_FORECAST_SAMPLES_M_WEATHER'].unique()}\n")

    return dt


def preprocess(input_data: str) -> list:
    lines = input_data.split("\n")
    processed_entry = []
    for line in lines:
        processed_entry.append(line.split(","))

    print(processed_entry)
    return processed_entry


def predict(dt, input_data: list) -> list:
    predictions = dt.predict(input_data)
    return predictions
