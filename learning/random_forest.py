from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from travelscanner.data.datasets import load_prices, split_set

if __name__ == "__main__":
    x_train, x_test, y_train, y_test = split_set(load_prices())

    # Fit random forest model to data
    random_forest = RandomForestRegressor()
    random_forest.fit(x_train, y_train)

    # Print MSE from predicted values
    y_pred = random_forest.predict(x_test)

    print(mean_squared_error(y_pred, y_test))