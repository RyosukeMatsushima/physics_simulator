from DoublePendulum import DoublePendulum
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    theta1, theta1_dot, theta2, theta2_dot = -2.7, 2.7, 0., 0.
    model = DoublePendulum(theta1, theta1_dot, theta2, theta2_dot, 0., 0., mass=0.3, length=0.2, drag=0.0)

    time = 0.
    dt = 10**(-2)
    max_step = 30 * 10**(2) + 1

    df = pd.DataFrame(columns=['time', 'theta1', 'theta1_dot', 'theta2', 'theta2_dot', 'energy'])

    # def add_data(df):

    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + model.state + tuple([model.energy(*model.state)])
        print(time)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        model.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x='time', y='theta1')
    df.plot(x='time', y='theta1_dot')
    df.plot(x='time', y='theta2')
    df.plot(x='time', y='theta2_dot')
    df.plot(x='time', y='energy')
    plt.show()
