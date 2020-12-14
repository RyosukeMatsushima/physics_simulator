from TwoWheelRover import TwoWheelRover
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    twoWheelRover = TwoWheelRover(0, 0, 0, 0, 0)
    twoWheelRover.input = (0.1, -0.05)

    time = 0.
    dt = 10**(-2)
    max_step = 5 * 10**(2) + 1

    df = pd.DataFrame(columns=['time', 'X', 'Y', 'theta', 'v', 'theta_dot'])

    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + twoWheelRover.state
        print(time)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        twoWheelRover.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x='X', y='Y')
    df.plot(x='time', y='v')
    df.plot(x='time', y='theta')
    plt.show()

