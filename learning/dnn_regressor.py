from keras import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.metrics import mean_absolute_error

from travelscanner.data.datasets import split_set, load_prices
from learning.plot import show_plot


def create_model():
    # Create a sequential model
    model = Sequential()
    model.add(Dense(256, input_dim=15, kernel_initializer='normal', activation='linear'))
    model.add(Dense(128, kernel_initializer='normal', activation='linear'))
    model.add(Dense(1, kernel_initializer='normal', activation='linear'))

    # Compile model
    model.compile(loss="mean_absolute_error", optimizer="rmsprop")
    return model


if __name__ == "__main__":
    x_train, x_test, y_train, y_test, n_samples = split_set(load_prices())

    # Train model
    estimator = KerasRegressor(build_fn=create_model, epochs=5, batch_size=25, verbose=1)
    estimator.fit(x_train, y_train)

    # Print MSE from predicted values
    y_pred = estimator.predict(x_test)

    print(f"MAE: {mean_absolute_error(y_pred, y_test)}")

    # Show plot
    show_plot(y_pred, y_test)
