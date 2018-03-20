from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from learning.plot import show_plot
from travelscanner.data.datasets import load_prices, split_set
from travelscanner.models.price import Price
from travelscanner.models.travel import Travel

if __name__ == "__main__":
    x_train, x_test, y_train, y_test = split_set(load_prices())

    # Fit random forest model to data
    random_forest = RandomForestRegressor(n_estimators=100)
    random_forest.fit(x_train, y_train)

    # Print feature importances
    print(random_forest.feature_importances_)

    # Print MSE from predicted values
    y_pred = random_forest.predict(x_test)

    print(f"MAE: {mean_absolute_error(y_pred, y_test)}")

    # Show plot
    show_plot(y_pred, y_test)

    # Find biggest differences
    joined_prices = Travel.select(Travel, Price).join(Price)
