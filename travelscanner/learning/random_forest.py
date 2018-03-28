from travelscanner.learning.plot import plot_predicted_actual
from sklearn.metrics import r2_score, mean_absolute_error

from travelscanner.data.database import Database
from travelscanner.data.datasets import split_set, load_prices
from travelscanner.learning.compare_models import get_random_forest

if __name__ == "__main__":
    # Load and split data
    x, y, features, price_objects = load_prices(include_objects=True)
    x_train, x_test, y_train, y_test = split_set(x, y)

    # Fit RF model to data
    rf = get_random_forest()
    rf.fit(x_train, y_train)

    # Print significant values
    for i, feature in enumerate(features):
        print(f"{feature}: {rf.feature_importances_[i] * 100:.2f}%")

    # Predict prices
    all_predict = rf.predict(x)
    with Database.get_driver().atomic():
        for i in range(len(price_objects)):
            price_objects[i].predicted_price = all_predict[i]
            price_objects[i].save()

    # Predict and plot result
    y_predict = rf.predict(x_test)
    print(f"Variance score: {r2_score(y_test, y_predict)}")
    print(f"MAE: {mean_absolute_error(y_test, y_predict)}")
    plot_predicted_actual("RandomForest", y_test, y_predict)
