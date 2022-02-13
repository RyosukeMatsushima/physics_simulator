import numpy as np

class PhysicsModel:

    def __init__(self, init_state, init_input, **kwargs):

        self.set_param(**kwargs)
        self.GRAVITY = 9.81

        self.state = init_state
        self.input = init_input

    def dynamics(self, state, u):

        # return time derivative of each state variables
        # ex: return np.array([theta_dot, theta_2dot])
        return 


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
        # return parameters of the model
        # ex: return {"mass": self.MASS, "length": self.LENGTH, "drag": self.DRAG}
        return

    def set_param(self, **kwargs):
        # set parameters from kwargs
        return
