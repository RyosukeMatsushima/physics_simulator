import numpy as np

class Drone2D:

    def __init__(self, X, Z, theta, x_dot, z_dot, theta_dot, **kwargs):
        self.name = "Drone2D"
        self.MASS = 0.5
        self.LENGTH = 0.2 # motor to center of gravity
        self.INERTIA = 0.007
        self.DRAG = 0.0
        self.DRAG_ROTATE = 0.0
        self.GRAVITY = 9.81
        self.set_param(**kwargs)

        self.state = (X, Z, theta, x_dot, z_dot, theta_dot)
        self.input = (0., 0.) # (right motor, left motor)

    def dynamics(self, X, Z, theta, x_dot, z_dot, theta_dot, input):
        X_dot = x_dot * np.cos(theta) + z_dot * np.sin(theta)
        Z_dot = -x_dot * np.sin(theta) + z_dot * np.cos(theta)
        
        x_2dot = ( -self.MASS * self.GRAVITY * np.sin(theta) - x_dot * self.DRAG ) / self.MASS
        z_2dot = ( -input[0] - input[1] + self.MASS * self.GRAVITY * np.cos(theta) - z_dot * self.DRAG ) / self.MASS
        theta_2dot = (input[0] * self.LENGTH - input[1] * self.LENGTH - theta_dot * self.DRAG_ROTATE) / self.INERTIA
        return np.array([X_dot, Z_dot, theta_dot, x_2dot, z_2dot, theta_2dot])

    def step(self, dt):
        current_state = np.array(self.state)
        k0 = dt * self.dynamics(*current_state, self.input)
        k1 = dt * self.dynamics(*current_state + k0/2, self.input)
        k2 = dt * self.dynamics(*current_state + k1/2, self.input)
        k3 = dt * self.dynamics(*current_state + k2, self.input)

        state_dot = (k0 + 2 * (k1 + k2) + k3)/6
        self.state = tuple(current_state + state_dot)

        return state_dot

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
