import numpy as np

class SingleCart:

    def __init__(self, x, x_dot, **kwargs):
        self.MASS = 0.3
        self.DRAG = 0.0
        self.set_param(**kwargs)

        self.state = (x, x_dot)
        self.input = 0.

    def dynamics(self, x, x_dot, u):
        x_2dot = (u)/self.MASS
        return np.array([x_dot, x_2dot])

    def step(self, dt):
        current_state = np.array(self.state)
        k0 = dt * self.dynamics(*current_state, self.input)
        k1 = dt * self.dynamics(*current_state + k0/2, self.input)
        k2 = dt * self.dynamics(*current_state + k1/2, self.input)
        k3 = dt * self.dynamics(*current_state + k2, self.input)

        state_dot = (k0 + 2 * (k1 + k2) + k3)/6
        self.state = tuple(current_state + state_dot)

        return self.state

    def get_param(self):
        return {"mass": self.MASS, "drag": self.DRAG}

    def set_param(self, **kwargs):
        for key in kwargs:
            if key == "mass":
                self.MASS = kwargs[key]
                continue
            if key == "drag":
                self.DRAG = kwargs[key]
                continue
            raise TypeError("The required key {key!r} ""are not in kwargs".format(key=key))
