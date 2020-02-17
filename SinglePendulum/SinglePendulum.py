import numpy as np

class SinglePendulum:

    def __init__(self, theta, theta_dot):
        self.GRAVITY = 9.81
        self.MASS = 0.3
        self.LENGTH = 0.2 # actually half the pole's length
        self.INERTIA = (self.MASS * (2 * self.LENGTH)**2)/12
        self.DRAG = 0.001
        
        self.state = (theta, theta_dot)
        self.input = 0.

    def singlependulum_dynamics(self, theta, theta_dot, u):
        theta_2dot = (self.LENGTH * self.MASS * self.GRAVITY * np.sin(theta) - self.DRAG * theta_dot)/self.INERTIA

        return np.array([theta_dot, theta_2dot])

    def step(self, dt):
        current_state = np.array(self.state)
        k0 = dt * self.singlependulum_dynamics(*current_state, self.input)
        k1 = dt * self.singlependulum_dynamics(*current_state + k0/2, self.input)
        k2 = dt * self.singlependulum_dynamics(*current_state + k1/2, self.input)
        k3 = dt * self.singlependulum_dynamics(*current_state + k2, self.input)

        state_dot = (k0 + 2 * (k1 + k2) + k3)/6
        self.state = tuple(current_state + state_dot)

        return self.state