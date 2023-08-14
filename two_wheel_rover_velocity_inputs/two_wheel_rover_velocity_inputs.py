import numpy as np
import sys
import pathlib

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../")
from common.physics_model import PhysicsModel


class TwoWheelRover(PhysicsModel):
    def __init__(self, init_state, **kwargs):
        # set default param values
        self.name = "TwoWheelRover"

        init_inputs = (0.0, 0.0)  # (velocity, rotational velocity)

        super().__init__(init_state, init_inputs, **kwargs)

    def dynamics(self, states, u):
        yaw = states[2]

        velocity = u[0]
        rotational_velocity = u[1]

        x_dot = velocity * np.cos(yaw)
        y_dot = velocity * np.sin(yaw)
        yaw_dot = rotational_velocity

        return np.array([x_dot, y_dot, yaw_dot])

    def get_param(self):
        return {}

    def set_param(self, **kwargs):
        return
