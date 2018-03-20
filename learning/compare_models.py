import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, BaggingRegressor
from sklearn.linear_model import LinearRegression, Lasso, BayesianRidge
from sklearn.model_selection import cross_val_score, KFold
from sklearn.neighbors import KNeighborsRegressor

from travelscanner.data.datasets import load_prices


def get_dnn_regressor(features):
    def create_model():
        # Create a sequential model
        dnn_model = Sequential()
        dnn_model.add(Dense(256, input_dim=features, kernel_initializer='normal', activation='linear'))
        dnn_model.add(Dense(128, kernel_initializer='normal', activation='linear'))
        dnn_model.add(Dense(1, kernel_initializer='normal', activation='linear'))

        # Compile model
        dnn_model.compile(loss="mean_absolute_error", optimizer="rmsprop")
        return dnn_model

    return KerasRegressor(build_fn=create_model, epochs=5, batch_size=25)


if __name__ == "__main__":
    x, y, n_features = load_prices()

    # Add models to dictionary
    models = {'Linear': LinearRegression(),
              'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=64),
              'Lasso': Lasso(alpha=0.1),
              'AdaBoost': AdaBoostRegressor(),
              'Bagging': BaggingRegressor(),
              'KNeighbors': KNeighborsRegressor(n_neighbors=5, weights='uniform'),
              'DNN': get_dnn_regressor(n_features),
              'BayesianRidge': BayesianRidge()}

    # Compare models using 5-fold CV
    results = {}
    for name, model in models.items():
        print(f"Testing model {name}")

        kfold = KFold(n_splits=5, random_state=42)
        result = cross_val_score(model, x, y, cv=kfold)
        results[name] = result

        print(f"{name}: {result.mean()}, {result.std()}")

    # Plot results
    plot = plt.figure()
    plt.ylabel("Mean score")
    plt.xlabel("Model")
    plt.bar(range(len(results)), [r.mean() for r in results.values()], align='center')
    plt.xticks(range(len(results)), list(results.keys()))
    plt.show()
