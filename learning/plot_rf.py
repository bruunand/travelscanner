from learning.compare_models import get_random_forest
from travelscanner.data.datasets import split_set, load_prices
import matplotlib.pyplot as plt

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
    fig, ax = plt.subplots()
    ax.scatter(rf.predict(x_test), y_test)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    plt.show()
