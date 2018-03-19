from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

from learning.plot import show_plot
from travelscanner.data.datasets import load_prices, split_set

if __name__ == "__main__":
    x_train, x_test, y_train, y_test = split_set(load_prices())

    # Fit random forest model to data
    random_forest = RandomForestRegressor(n_estimators=100, max_depth=80)
    random_forest.fit(x_train, y_train)

    # Print feature importances
    print(random_forest.feature_importances_.sort())

    # Print MSE from predicted values
    y_pred = random_forest.predict(x_test)

    print(f"MAE: {mean_absolute_error(y_pred, y_test)}")

    # Show plot
    show_plot(y_pred, y_test)