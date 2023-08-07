from SinglePendulum import SinglePendulum


def test():
    singlePendulum = SinglePendulum(1.0, 3.0)
    value = singlePendulum.singlependulum_dynamics(1.0, 3.0, 1.0)
    print(value)

    state = singlePendulum.step()
    print(state)


if __name__ == "__main__":
    test()
