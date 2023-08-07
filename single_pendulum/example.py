from single_pendulum import SinglePendulum
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    init_theta = 3
    init_theta_dot = 0
    singlePendulum = SinglePendulum((init_theta, init_theta_dot))

    time = 0.0
    dt = 10 ** (-2)
    max_step = 5 * 10 ** (2) + 1
    singlePendulum.input = 0.1

    df = pd.DataFrame(columns=["time", "theta", "theta_dot"])

    # def add_data(df):

    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + singlePendulum.state
        print(time)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        singlePendulum.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x="time", y="theta")
    df.plot(x="time", y="theta_dot")
    plt.show()
