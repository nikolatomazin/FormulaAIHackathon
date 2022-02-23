import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor


def read_csv(input_file="input/weather.csv"):
    print("importing csv file")
    df = pd.read_csv(input_file)
    print("imported csv file successfully")
    return df


def train_model_classifier(df):
    df = df.filter(items=["M_SESSION_UID", "M_SESSION_TIME", "M_PLAYER_CAR_INDEX", "TIMESTAMP", "M_TRACK_TEMPERATURE",
                          "M_FORECAST_ACCURACY", "M_AIR_TEMPERATURE", "M_NUM_WEATHER_FORECAST_SAMPLES", "M_TRACK_ID",
                          "M_SESSION_TYPE", "M_SESSION_DURATION", "M_WEATHER_FORECAST_SAMPLES_M_SESSION_TYPE",
                          "M_WEATHER_FORECAST_SAMPLES_M_WEATHER",
                          "M_WEATHER_FORECAST_SAMPLES_M_TRACK_TEMPERATURE", "M_TRACK_TEMPERATURE_CHANGE",
                          "M_WEATHER_FORECAST_SAMPLES_M_AIR_TEMPERATURE", "M_AIR_TEMPERATURE_CHANGE",
                          "M_RAIN_PERCENTAGE",
                          "M_WEATHER", "M_TIME_OFFSET"])
    print(df.shape)

    df.dropna(inplace=True)
    print(df.shape)

    df = df.loc[df['M_NUM_WEATHER_FORECAST_SAMPLES'] != 0]
    print(df.shape)
    df = df[df['M_WEATHER_FORECAST_SAMPLES_M_WEATHER'] != 6]

    df = df.drop_duplicates(subset=["M_SESSION_UID", "TIMESTAMP", "M_PLAYER_CAR_INDEX", "M_TIME_OFFSET"],
                            keep="first", inplace=False)
    df = df.drop(columns=["M_SESSION_UID", "TIMESTAMP", "M_PLAYER_CAR_INDEX"], inplace=False)

    df_full = df.copy()
    print(df_full.shape)

    X = df_full.drop(columns=["M_WEATHER_FORECAST_SAMPLES_M_WEATHER", "M_RAIN_PERCENTAGE"], inplace=False)
    y = df_full.filter(items=["M_WEATHER_FORECAST_SAMPLES_M_WEATHER"])

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=100)

    dt = DecisionTreeClassifier()
    dt.fit(x_train, y_train)
    print("score :", dt.score(x_test, y_test))

    return dt


def train_model_regressor(df):
    df = df.filter(items=["M_SESSION_UID", "M_SESSION_TIME", "M_PLAYER_CAR_INDEX", "TIMESTAMP", "M_TRACK_TEMPERATURE",
                          "M_FORECAST_ACCURACY", "M_AIR_TEMPERATURE", "M_NUM_WEATHER_FORECAST_SAMPLES", "M_TRACK_ID",
                          "M_SESSION_TYPE", "M_SESSION_DURATION", "M_WEATHER_FORECAST_SAMPLES_M_SESSION_TYPE",
                          "M_WEATHER_FORECAST_SAMPLES_M_WEATHER",
                          "M_WEATHER_FORECAST_SAMPLES_M_TRACK_TEMPERATURE", "M_TRACK_TEMPERATURE_CHANGE",
                          "M_WEATHER_FORECAST_SAMPLES_M_AIR_TEMPERATURE", "M_AIR_TEMPERATURE_CHANGE",
                          "M_RAIN_PERCENTAGE",
                          "M_WEATHER", "M_TIME_OFFSET"])
    print(df.shape)

    df.dropna(inplace=True)
    print(df.shape)

    df = df.loc[df['M_NUM_WEATHER_FORECAST_SAMPLES'] != 0]
    print(df.shape)
    df = df[df['M_WEATHER_FORECAST_SAMPLES_M_WEATHER'] != 6]

    df = df.drop_duplicates(subset=["M_SESSION_UID", "TIMESTAMP", "M_PLAYER_CAR_INDEX", "M_TIME_OFFSET"],
                            keep="first", inplace=False)
    df = df.drop(columns=["M_SESSION_UID", "TIMESTAMP", "M_PLAYER_CAR_INDEX"], inplace=False)

    df_full = df.copy()
    print(df_full.shape)

    X = df_full.drop(columns=["M_WEATHER_FORECAST_SAMPLES_M_WEATHER", "M_RAIN_PERCENTAGE"], inplace=False)
    y = df_full.filter(items=["M_RAIN_PERCENTAGE"])

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=100)
    dt = DecisionTreeRegressor(random_state=2202)
    dt.fit(x_train, y_train)
    print("score :", dt.score(x_test, y_test))
    return dt


def preprocess(input_data: str) -> list:
    lines = input_data.split("\n")
    processed_entry = []
    for line in lines:
        processed_entry.append(line.split(","))

    return processed_entry


def multiple_prediction(row, model_reg, model_cls):
    predictions = {}
    for offset in [5, 10, 15, 30, 60]:
        row["M_TIME_OFFSET"] = offset
        temp_row = row.copy()
        temp_row = temp_row.ravel().reshape(1, -1)
        pred_reg = model_reg.predict(temp_row)
        pred_cls = model_cls.predict(temp_row)
        predictions[str(offset)] = {'type': pred_cls[0], 'rain_percentage': pred_reg[0]}
    return predictions


def predict(dt, input_data: list) -> list:
    predictions = []
    for row in input_data:
        predict_data = []
        for offset in [5, 10, 15, 30, 60]:
            if len(row) == 15:
                row[len(row)-1] = offset
            else:
                row.append(offset)
            predict_data.append(row)

        prediction = dt.predict(predict_data)
        predictions.append(prediction)
    return predictions


def format_output(result_dt, result_dtr):
    structures = []
    for res_dt, res_dtr in zip(result_dt, result_dtr):
        structure = {
            '5': {
                'type': res_dt[0],
                'rain_percentage': res_dtr[0]
            },
            '10': {
                'type': res_dt[1],
                'rain_percentage': res_dtr[1]
            },
            '15': {
                'type': res_dt[2],
                'rain_percentage': res_dtr[2]
            },
            '30': {
                'type': res_dt[3],
                'rain_percentage': res_dtr[3]
            },
            '60': {
                'type': res_dt[4],
                'rain_percentage': res_dtr[4]
            }
        }
        structures.append(structure)
    return structures
