from Drone2D import Drone2D
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    drone2D = Drone2D(0, 0, 0., 0, 0, 0)
    drone2D.input = (9.81/4, 9.81/4)

    time = 0.
    dt = 10**(-2)
    max_step = 5 * 10**(2) + 1

    df = pd.DataFrame(columns=['time', 'X', 'Z', 'theta', 'x_dot', 'z_dot', 'theta_dot'])

    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + drone2D.state
        print(time)

        if 2.1 > time > 2:
            drone2D.input = (9.81/4 + 0.001, 9.81/4)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        drone2D.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x='X', y='Z')
    df.plot(x='time', y='x_dot')
    df.plot(x='time', y='theta')
    df.plot(x='time', y='X')
    df.plot(x='time', y='Z')
    plt.show()
