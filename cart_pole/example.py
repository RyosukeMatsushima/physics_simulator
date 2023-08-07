from cart_pole import CartPole
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    init_x = 0
    init_x_dot = 0
    init_theta = 0.1
    init_theta_dot = 0
    cartPole = CartPole((init_x, init_x_dot, init_theta, init_theta_dot))

    time = 0.
    dt = 10**(-2)
    max_step = 5 * 10**(2) + 1

    df = pd.DataFrame(columns=['time', 'x', 'x_dot', 'theta', 'theta_dot'])

    # def add_data(df):
        

    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + cartPole.state
        print(time)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        cartPole.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x='time', y='x')
    df.plot(x='time', y='x_dot')
    df.plot(x='time', y='theta')
    df.plot(x='time', y='theta_dot')
    plt.show()

