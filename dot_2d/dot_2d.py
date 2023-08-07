import numpy as np
import sys
import pathlib

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../")
from common.physics_model import PhysicsModel

# state: (X, Y)
# X and Y are defined in inertial coordinate system.

# input: (x_velocity, y_velocity)
# The direction of x_force and y_force are defined in body coordinate system.


class Dot2D(PhysicsModel):
    def __init__(self, init_state, **kwargs):
        # set default param values
        self.name = "Dot2D"

        init_input = (0.0, 0.0)

        super().__init__(init_state, init_input, **kwargs)

    def dynamics(self, states, u):
        X_dot = u[0]
        Y_dot = u[1]

        return np.array([X_dot, Y_dot])

    def get_param(self):
        return {}

    def set_param(self, **kwargs):
        for key in kwargs:
            raise TypeError(
                "The required key {key!r} " "are not in kwargs".format(key=key)
            )

    def get_sensor_data(self):
        X_dot = self.last_state_dot[0]
        Y_dot = self.last_state_dot[1]
        return {"velocity": [X_dot, Y_dot]}
