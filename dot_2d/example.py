from dot_2d import Dot2D
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    X = 0.0
    Y = 0.0
    init_state = (X, Y)
    dot2D = Dot2D(init_state)

    time = 0.0
    dt = 10 ** (-2)
    max_step = 60 * 10 ** (2) + 1

    df = pd.DataFrame(columns=["time", "X", "Y"])

    dot2D.input = [1, 1]
    # def add_data(df):
    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + dot2D.state
        print(time)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        dot2D.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x="X", y="Y")
    df.plot(x="time", y="X")
    df.plot(x="time", y="Y")
    plt.show()
