from CartPole import CartPole

def test():
    cartPole = CartPole(1., 2., 3., 4.)
    value = cartPole.dynamics(1., 2., 3., 4., 5.)
    print(value)

    state = cartPole.step()
    print(state)

if __name__ == '__main__':
    test()