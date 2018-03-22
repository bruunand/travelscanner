from learning.compare_models import get_random_forest
from learning.plot import plot_predicted_actual
from travelscanner.data.datasets import split_set, load_prices

if __name__ == "__main__":
    # Load and split data
    x, y, features = load_prices()
    x_train, x_test, y_train, y_test = split_set(x, y)

    # Fit RF model to data
    rf = get_random_forest()
    rf.fit(x_train, y_train)

    # Print significant values
    for i, feature in enumerate(features):
        print(f"{feature}: {rf.feature_importances_[i] * 100:.2f}%")

    # Predict and plot result
    y_predict = rf.predict(x_test)
    plot_predicted_actual("RandomForest", y_test, y_predict)
