import numpy as np
import sys
import pathlib

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )
from common.physics_model import PhysicsModel

class SinglePendulum(PhysicsModel):

    def __init__(self, init_state, **kwargs):

        # set default param values
        self.name = "SinglePendulum"
        self.MASS = 0.3
        self.LENGTH = 0.2 # actually half the pole's length
        self.DRAG = 0.001
        self.INERTIA = (self.MASS * (2 * self.LENGTH)**2)/12

        super().__init__(init_state, 0.0, **kwargs)

    def dynamics(self, states, u):
        theta = states[0]
        theta_dot = states[1]

        theta_2dot = ( self.LENGTH * self.MASS * self.GRAVITY * np.sin(theta)
                     - self.DRAG * theta_dot
                     + u ) / self.INERTIA

        return np.array([theta_dot, theta_2dot])

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
