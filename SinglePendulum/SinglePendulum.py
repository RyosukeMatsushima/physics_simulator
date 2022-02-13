import numpy as np
from common.physics_model import PhysicsModel

class SinglePendulum(PhysicsModel):

    def __init__(self, theta, theta_dot, **kwargs):

        # set default param values
        self.name = "SinglePendulum"
        self.MASS = 0.3
        self.LENGTH = 0.2 # actually half the pole's length
        self.DRAG = 0.001
        self.INERTIA = (self.MASS * (2 * self.LENGTH)**2)/12

        super().__init__((theta, theta_dot), 0.0, **kwargs)

    def dynamics(self, theta, theta_dot, u):
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
