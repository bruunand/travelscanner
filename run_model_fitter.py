import pickle
from logging import getLogger

import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor

from travelscanner.data.datasets import split_set, load_prices


def plot_predicted_actual(title, y_test, y_predict):
    # Predict and plot result
    fig, ax = plt.subplots()
    plt.suptitle(title)
    ax.scatter(y_test, y_predict)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    plt.show()


if __name__ == "__main__":
    # Load and split data
    getLogger().info("Retrieving data")
    x, y, features, price_objects = load_prices(include_objects=True)
    x_train, x_test, y_train, y_test = split_set(x, y, train_ratio=0.75)

    params = {
        "max_depth": 100
    }

    # Fit RF model to data
    getLogger().info(f'Fitting data using {len(y)} instances')
    regressor = RandomForestRegressor(**params)
    regressor.fit(x_train, y_train)

    # Save model to file
    pickle.dump(regressor, open("travelscanner/learning/xgboost.pickle.dat", "wb"))

    # Print significant values
    for i, feature in enumerate(features):
        print(f"{feature}: {regressor.feature_importances_[i] * 100:.2f}%")

    # Predict unseen data and plot result
    y_predict = regressor.predict(x_test)
    print(f"Variance score: {r2_score(y_test, y_predict)}")
    print(f"MAE: {mean_absolute_error(y_test, y_predict)}")
    plot_predicted_actual("XGBoost", y_test, y_predict)
