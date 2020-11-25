import numpy as np

class TwoWheelRover:

    def __init__(self, X, Y, theta, v, theta_dot, **kwargs):
        self.MASS = 0.5
        self.LENGTH = 0.2 # wheel to center of gravity
        self.INERTIA = 0.007
        self.DRAG = 0.1
        self.DRAG_ROTATE = 0.01
        self.set_param(**kwargs)

        self.state = (X, Y, theta, v, theta_dot)
        self.input = (0., 0.) # (right wheel, left wheel)

    def dynamics(self, X, Y, theta, v, theta_dot, input):
        X_dot = v * np.cos(theta)
        Y_dot = v * np.sin(theta)
        v_dot = (input[0] + input[1] - v * self.DRAG) / self.MASS
        theta_2dot = (input[0] - input[1] - theta_dot * self.DRAG_ROTATE) * self.LENGTH / self.INERTIA
        return np.array([X_dot, Y_dot, theta_dot, v_dot, theta_2dot])

    def step(self, dt):
        current_state = np.array(self.state)
        k0 = dt * self.dynamics(*current_state, self.input)
        k1 = dt * self.dynamics(*current_state + k0/2, self.input)
        k2 = dt * self.dynamics(*current_state + k1/2, self.input)
        k3 = dt * self.dynamics(*current_state + k2, self.input)

        state_dot = (k0 + 2 * (k1 + k2) + k3)/6
        self.state = tuple(current_state + state_dot)

    def get_param(self):
        return {"mass": self.MASS,
                "length": self.LENGTH,
                "inertia": self.INERTIA,
                "drag": self.DRAG,
                "drag_rotate": self.DRAG_ROTATE}

    def set_param(self, **kwargs):
        for key in kwargs:
            if key == "mass":
                self.MASS = kwargs[key]
                continue
            if key == "length":
                 self.LENGTH = kwargs[key]
                 continue
            if key == "inertia":
                self.INERTIA = kwargs[key]
                continue
            if key == "drag":
                self.DRAG = kwargs[key]
                continue
            if key == "drag_rotate":
                self.DRAG_ROTATE = kwargs[key]
                continue
            raise TypeError("The required key {key!r} ""are not in kwargs".format(key=key))
