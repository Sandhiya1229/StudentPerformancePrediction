import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

FEATURES = [
    "attendance",
    "previous_marks",
    "assignment_marks",
    "study_hours",
    "internal_marks"
]


def build_model():

    data = []

    # Generate sample training data
    for attendance in range(40, 101, 5):
        for previous in range(30, 101, 10):
            for assignment in range(30, 101, 10):
                for hours in range(1, 7):
                    for internal in range(30, 101, 10):

                        final_marks = (
                            attendance * 0.15
                            + previous * 0.30
                            + assignment * 0.15
                            + hours * 3
                            + internal * 0.35
                            - 5
                        )

                        final_marks = max(
                            0, min(100, final_marks)
                        )

                        data.append([
                            attendance,
                            previous,
                            assignment,
                            hours,
                            internal,
                            final_marks
                        ])

    df = pd.DataFrame(
        data,
        columns=FEATURES + ["final_marks"]
    )

    X = df[FEATURES]
    y = df["final_marks"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=50,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    print("Model training completed!")
    print("Mean Absolute Error:", round(mae, 2))

    return model


model = build_model()


def predict_performance(values):

    input_data = pd.DataFrame(
        [values],
        columns=FEATURES
    )

    marks = float(model.predict(input_data)[0])
    marks = round(max(0, min(100, marks)), 2)

    if marks >= 85:
        category = "Excellent"
    elif marks >= 70:
        category = "Good"
    elif marks >= 50:
        category = "Average"
    else:
        category = "Needs Improvement"

    return marks, category