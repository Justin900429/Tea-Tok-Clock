import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # Set figure size
    plt.figure(figsize=(10, 16))

    # Read in data
    data = pd.read_csv("record.csv")
    ax1 = plt.subplot(3, 1, 1)
    plt.plot(data.loc[:, "temperature"], label="temperature")
    plt.title("Original plot")
    plt.legend()
    ax1.set_xticks([])
    ax1.set_xticklabels([])

    # Add log scale
    data["log_scale"] = np.log(data.iloc[:, 0] - 23.0)

    # Fit the linear regression line
    model = LinearRegression().fit(
        data.loc[:, "time"].array.reshape(-1, 1), data["log_scale"].array.reshape(-1, 1)
    )
    y_pred = model.predict(np.arange(len(data)).reshape(-1, 1) + 1)

    # Plot the log data
    ax2 = plt.subplot(3, 1, 2)
    plt.plot(data["log_scale"], label="Log-scale")
    plt.plot(y_pred, c="red", label=f"y = {model.coef_[0][0]:.5f}t+{model.intercept_[0]:.3f}")
    plt.title("Log-scale plot")
    plt.legend()
    ax2.set_xticks([])
    ax2.set_xticklabels([])

    # Compute k value
    data["k"] = -np.log((data.loc[:, "temperature"] - 23.0) / 100) / data.loc[:, "time"]
    average_k = data["k"].mean()

    plt.subplot(3, 1, 3)
    plt.scatter(range(len(data["k"])), data["k"], s=1, label="k")
    plt.hlines(average_k, xmin=0, xmax=len(data), colors=["orange"], label=f"average, k={average_k:.3f}")
    plt.title("K value")
    plt.legend()
    plt.tight_layout()

    plt.savefig("../images/exp.svg")

    plt.show()
