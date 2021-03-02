import numpy as np

class DoublePendulum:

    def __init__(self, theta1, theta1_dot, theta2, theta2_dot, u1, u2, **kwargs):
        self.name = "DoublePendulum"
        self.GRAVITY = 9.81
        self.MASS = 0.3
        self.LENGTH = 0.2
        self.DRAG = 0.001
        self.set_param(**kwargs)

        self.state = (theta1, theta1_dot, theta2, theta2_dot)
        self.input = (u1, u2)

    def dynamics(self, theta1, theta1_dot, theta2, theta2_dot, u1, u2):
        A = np.array([[2 * self.MASS * self.LENGTH**2, self.MASS * self.LENGTH**2 * np.cos(theta1 - theta2)],
                      [self.MASS * self.LENGTH**2 * np.cos(theta1 - theta2), self.MASS * self.LENGTH**2]])
        B = np.array([[-self.MASS * self.LENGTH**2 * theta2_dot**2 * np.sin(theta1 - theta2) - 2 * self.MASS * self.LENGTH * self.GRAVITY * np.sin(theta1) + u1 - self.DRAG * theta1_dot],
                      [self.MASS * self.LENGTH**2 * theta1_dot**2 * np.sin(theta1 - theta2) - self.MASS * self.GRAVITY * self.LENGTH * np.sin(theta2) + u2 - self.DRAG * theta2_dot]])

        angle_accels = np.dot(np.linalg.inv(A), B)
        theta1_2dot, theta2_2dot = angle_accels[0][0], angle_accels[1][0]
        return np.array([theta1_dot, theta1_2dot, theta2_dot, theta2_2dot])

    def step(self, dt):
        current_state = np.array(self.state)
        k0 = dt * self.dynamics(*current_state, self.input[0], self.input[1])
        k1 = dt * self.dynamics(*current_state + k0/2, self.input[0], self.input[1])
        k2 = dt * self.dynamics(*current_state + k1/2, self.input[0], self.input[1])
        k3 = dt * self.dynamics(*current_state + k2, self.input[0], self.input[1])

        state_dot = (k0 + 2 * (k1 + k2) + k3)/6
        self.state = tuple(current_state + state_dot)

        return self.state

    def energy(self, theta1, theta1_dot, theta2, theta2_dot):
        y1 = -self.LENGTH * np.cos(theta1)
        y2 = -(self.LENGTH * np.cos(theta1) + self.LENGTH * np.cos(theta2))

        x1_dot = self.LENGTH * theta1_dot * np.cos(theta1)
        y1_dot = self.LENGTH * theta1_dot * np.sin(theta1)
        x2_dot = self.LENGTH * theta1_dot * np.cos(theta1) + self.LENGTH * theta2_dot * np.cos(theta2)
        y2_dot = self.LENGTH * theta1_dot * np.sin(theta1) + self.LENGTH * theta2_dot * np.sin(theta2)

        T = self.MASS / 2 * (x1_dot**2 + y1_dot**2) + self.MASS / 2 * (x2_dot**2 + y2_dot**2)
        U = self.MASS * self.GRAVITY * y1 + self.MASS * self.GRAVITY * y2

        return T + U

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
