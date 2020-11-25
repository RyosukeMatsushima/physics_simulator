import numpy as np

class CartPole:

    def __init__(self, x, x_dot, theta, theta_dot, **kwargs):
        self.GRAVITY = 9.81
        self.MASS_CART = 0.5
        self.MASS_POLE = 0.3
        self.LENGTH_POLE = 0.2 # actually half the pole's length
        self.INERTIA_POLE = (self.MASS_POLE * (2 * self.LENGTH_POLE)**2)/12
        self.DRAG_CART = 0.1
        self.DRAG_POLE = 0.01
        self.set_param(**kwargs)

        self.state = (x, x_dot, theta, theta_dot)
        self.input = 0.

    def dynamics(self, x, x_dot, theta, theta_dot, u):
        alpha = self.MASS_POLE * self.LENGTH_POLE * np.cos(theta)
        A = [[self.MASS_CART + self.MASS_POLE, alpha],
             [alpha, self.INERTIA_POLE + self.MASS_POLE * self.LENGTH_POLE**2]]

        B = [[-self.MASS_POLE * self.LENGTH_POLE * theta_dot**2 * np.sin(theta)],
             [-self.MASS_POLE * self.GRAVITY * self.LENGTH_POLE * np.sin(theta)]]

        C = [[self.DRAG_CART * x_dot],
             [self.DRAG_POLE * theta_dot]]

        D = [[u],
             [0]]

        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        D = np.array(D)

        inv_A = np.linalg.inv(A)
        x_2dot, theta_2dot =  np.dot(inv_A, -B - C + D)
        x_2dot, theta_2dot = x_2dot[0], theta_2dot[0]

        return np.array([x_dot, x_2dot, theta_dot, theta_2dot])

    def step(self, dt):
        current_state = np.array(self.state)
        k0 = dt * self.dynamics(*current_state, self.input)
        k1 = dt * self.dynamics(*current_state + k0/2, self.input)
        k2 = dt * self.dynamics(*current_state + k1/2, self.input)
        k3 = dt * self.dynamics(*current_state + k2, self.input)

        state_dot = (k0 + 2 * (k1 + k2) + k3)/6
        self.state = tuple(current_state + state_dot)

    def get_param(self):
        return {"mass_cart": self.MASS_CART,
                "mass_pole": self.MASS_POLE,
                "length_pole": self.LENGTH_POLE,
                "drag_cart": self.DRAG_CART,
                "drag_pole": self.DRAG_POLE}

    def set_param(self, **kwargs):
        for key in kwargs:
            if key == "mass_cart":
                self.MASS_CART = kwargs[key]
                continue
            if key == "mass_pole":
                 self.MASS_POLE = kwargs[key]
                 continue
            if key == "length_pole":
                self.LENGTH_POLE = kwargs[key]
                continue
            if key == "drag_cart":
                self.DRAG_CART = kwargs[key]
                continue
            if key == "drag_pole":
                self.DRAG_POLE = kwargs[key]
                continue
            raise TypeError("The required key {key!r} ""are not in kwargs".format(key=key))
        self.INERTIA_POLE = (self.MASS_POLE * (2 * self.LENGTH_POLE)**2)/12
