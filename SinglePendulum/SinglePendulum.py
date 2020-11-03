import numpy as np

class SinglePendulum:

    def __init__(self, theta, theta_dot, **kwargs):
        self.GRAVITY = 9.81
        self.MASS = 0.3
        self.LENGTH = 0.2 # actually half the pole's length
        self.DRAG = 0.001
        self.set_param(**kwargs)

        self.INERTIA = (self.MASS * (2 * self.LENGTH)**2)/12
        
        self.state = (theta, theta_dot)
        self.input = 0.

    def dynamics(self, theta, theta_dot, u):
        theta_2dot = (self.LENGTH * self.MASS * self.GRAVITY * np.sin(theta) - self.DRAG * theta_dot + u)/self.INERTIA

        return np.array([theta_dot, theta_2dot])

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
        return {"mass": self.MASS, "length": self.LENGTH, "drag": self.DRAG}

    def set_param(self, **kwargs):
        for key in kwargs:
            if key == "mass":
                self.MASS = kwargs[key]
                continue
            if key == "length":
                self.LENGTH = kwargs[key]
                continue
            if key == "drag":
                self.DRAG = kwargs[key]
                continue
            raise TypeError("The required key {key!r} ""are not in kwargs".format(key=key))
        self.INERTIA = (self.MASS * (2 * self.LENGTH)**2)/12
