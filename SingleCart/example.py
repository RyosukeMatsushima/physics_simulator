from SingleCart import SingleCart
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    init_x = 0.1
    init_x_dot = 0.
    singleCart = SingleCart(init_x, init_x_dot, mass=1, drag=0)

    time = 0.
    dt = 10**(-2)
    max_step = 5 * 10**(2) + 1

    df = pd.DataFrame(columns=['time', 'x', 'x_dot'])

    # def add_data(df):
        

    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + singleCart.state
        print(time)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        singleCart.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x='time', y='x')
    df.plot(x='time', y='x_dot')
    plt.show()
