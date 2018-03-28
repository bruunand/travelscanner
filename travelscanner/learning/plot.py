import matplotlib.pyplot as plt


def plot_predicted_actual(title, y_test, y_predict):
    # Predict and plot result
    fig, ax = plt.subplots()
    plt.suptitle(title)
    ax.scatter(y_test, y_predict)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    plt.show()
