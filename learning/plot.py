import matplotlib.pyplot as plt


def show_plot(predicted, actual):
    fig, ax = plt.subplots()
    ax.scatter(actual, predicted)
    ax.plot([actual.min(), actual.max()], [actual.min(), actual.max()], 'k--', lw=4)
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    plt.show()
