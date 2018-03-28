import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Dense, Dropout

from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, BaggingRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Lasso, BayesianRidge
from sklearn.model_selection import cross_val_score, KFold
from sklearn.neighbors import KNeighborsRegressor

from travelscanner.data.datasets import load_prices


def get_dnn_regressor(num_features):
    def create_model():
        # Create a sequential model
        dnn_model = Sequential()
        dnn_model.add(Dense(32, input_dim=num_features, kernel_initializer='normal', activation='relu'))
        dnn_model.add(Dense(200, kernel_initializer='normal', activation='relu'))
        dnn_model.add(Dense(256, kernel_initializer='normal', activation='relu'))
        dnn_model.add(Dense(1, kernel_initializer='normal', activation='relu'))

        # Compile model
        dnn_model.compile(loss="mean_absolute_error", optimizer="adam")
        return dnn_model

    return KerasRegressor(build_fn=create_model, epochs=200, batch_size=2000)


def get_random_forest():
    return RandomForestRegressor(max_depth=64)


if __name__ == "__main__":
    x, y, feature_list = load_prices()

    # Add models to dictionary
    models = {'GradientBoosting': GradientBoostingRegressor(),
              'Linear': LinearRegression(),
              'RandomForest': get_random_forest(),
              'Lasso': Lasso(alpha=0.1),
              'AdaBoost': AdaBoostRegressor(),
              'Bagging': BaggingRegressor(),
              'KNeighbors': KNeighborsRegressor(n_neighbors=5, weights='uniform'),
              'BayesianRidge': BayesianRidge()}
              #'DNN': get_dnn_regressor(len(feature_list))}

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
