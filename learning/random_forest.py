from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from travelscanner.data.datasets import load_prices

if __name__ == "__main__":
    X, y = load_prices()

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=int(len(X) * 0.75), random_state=4)

    random_forest = RandomForestRegressor()
    random_forest.fit(X_train, y_train)

    y_pred = random_forest.predict(X_test)

    print(r2_score(y_pred, y_test))
