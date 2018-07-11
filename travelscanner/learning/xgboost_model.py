from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBClassifier

from travelscanner.data.database import Database
from travelscanner.data.datasets import split_set, load_prices
from travelscanner.learning.plot import plot_predicted_actual

if __name__ == "__main__":
    # Load and split data
    x, y, features, price_objects = load_prices(include_objects=True)
    x_train, x_test, y_train, y_test = split_set(x, y)

    # Fit RF model to data
    classifier = XGBClassifier()
    classifier.fit(x_train, y_train, verbose=True)

    # Print significant values
    for i, feature in enumerate(features):
        print(f"{feature}: {classifier.feature_importances_[i] * 100:.2f}%")

    # Predict prices
    all_predict = classifier.predict(x)
    with Database.get_driver().atomic():
        print("Saving prices")

        for i in range(len(price_objects)):
            price_objects[i].predicted_price = all_predict[i]
            price_objects[i].save()

    # Predict and plot result
    y_predict = classifier.predict(x_test)
    print(f"Variance score: {r2_score(y_test, y_predict)}")
    print(f"MAE: {mean_absolute_error(y_test, y_predict)}")
    plot_predicted_actual("XGBoost", y_test, y_predict)


