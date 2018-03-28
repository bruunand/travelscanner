from learning.plot import plot_predicted_actual

from travelscanner.data.datasets import load_prices, split_set
from travelscanner.learning.compare_models import get_dnn_regressor

if __name__ == "__main__":
    # Load and split data
    x, y, features = load_prices()
    x_train, x_test, y_train, y_test = split_set(x, y)

    # Fit DNN model to data
    dnn = get_dnn_regressor(len(features))
    dnn.fit(x_train, y_train)

    # Predict and plot result
    y_predict = dnn.predict(x_test)
    plot_predicted_actual("DNN", y_test, y_predict)
