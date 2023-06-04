from rigid_body_2d import RigidBody2D
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    X = 0.0
    X_dot = 1.0
    Y = 0.0
    Y_dot = 1.0
    yaw = 0.0
    yaw_dot = 1.0
    init_state = (X, X_dot, Y, Y_dot, yaw, yaw_dot)
    rigidBody2D = RigidBody2D(init_state)

    time = 0.
    dt = 10**(-2)
    max_step = 60 * 10**(2) + 1

    df = pd.DataFrame(columns=['time',
                               'X',
                               'X_dot',
                               'Y',
                               'Y_dot',
                               'yaw',
                               'yaw_dot'])
 
    # def add_data(df):
    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + rigidBody2D.state
        print(time)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        rigidBody2D.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x='X', y='Y')
    df.plot(x='time', y='X')
    df.plot(x='time', y='Y')
    df.plot(x='time', y='yaw')
    plt.show()
