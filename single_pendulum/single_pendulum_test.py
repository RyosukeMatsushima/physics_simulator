from SinglePendulum import SinglePendulum

def test():
    singlePendulum = SinglePendulum(1., 3.)
    value = singlePendulum.singlependulum_dynamics(1., 3., 1.)
    print(value)

    state = singlePendulum.step()
    print(state)

if __name__ == '__main__':
    test()