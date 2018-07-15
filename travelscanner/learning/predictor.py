import pickle
from logging import getLogger

from travelscanner.data.datasets import load_prices
from travelscanner.models.price import Price, Database


def predict_prices():
    x, _, _, price_objects = load_prices(include_objects=True, unpredicted_only=True)

    # Load saved model
    regressor = pickle.load(open("travelscanner/learning/randomforest.pickle.dat", "rb"))

    # Predict prices
    all_predict = regressor.predict(x)

    # Update prices
    with Database.get_driver().atomic():
        for i in range(len(price_objects)):
            query = Price.update(predicted_price=all_predict[i]).where(Price.id == price_objects[i].id)
            try:
                query.execute()
            except Exception:
                getLogger().error(f"Could not update price #{price_objects[i].id}")

            if i % 500 == 0:
                getLogger().info(f"Progress: {i}/{len(price_objects)}")

    getLogger().info("Prediction finished")
