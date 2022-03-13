import numpy as np
import sys
import pathlib

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )
from common.physics_model import PhysicsModel

# state: (X, X_dot, Y, Y_dot, yaw, yaw_dot)
# X and Y are defined in inertial coordinate system.

# input: (x_force, y_force, yaw_torqe)
# The direction of x_force and y_force are defined in body coordinate system.

class RigidBody2D(PhysicsModel):

    def __init__(self, init_state, **kwargs):

        # set default param values
        self.name = "RigidBody2D"
        self.MASS = 0.3
        self.DRAG = 0.1
        self.DRAG_ROTATE = 0.0001
        self.INERTIA = 0.001

        init_input = (0.0, 0.0, 0.0)

        super().__init__(init_state, init_input, **kwargs)

    def dynamics(self, X, X_dot, Y, Y_dot, yaw, yaw_dot, u):
        x_2dot = u[0] / self.MASS
        y_2dot = u[1] / self.MASS
        X_2dot = x_2dot * np.cos(yaw) - y_2dot * np.sin(yaw) - self.DRAG * X_dot
        Y_2dot = x_2dot * np.sin(yaw) + y_2dot * np.cos(yaw) - self.DRAG * Y_dot
        yaw_2dot = ( u[2] - self.DRAG_ROTATE * yaw_dot ) / self.INERTIA

        return np.array([X_dot, X_2dot, Y_dot, Y_2dot, yaw_dot, yaw_2dot])

    def get_param(self):
        return {"mass": self.MASS, "drag": self.DRAG, "drag_rotate": self.DRAG_ROTATE, "inertia": self.INERTIA}

    def set_param(self, **kwargs):
        for key in kwargs:
            if key == "mass":
                self.MASS = kwargs[key]
                continue
            if key == "drag":
                self.DRAG = kwargs[key]
                continue
            if key == "drag_rotate":
                self.DRAG_ROTATE = kwargs[key]
                continue
            if key == "inertia":
                self.INERTIA = kwargs[key]
                continue
            raise TypeError("The required key {key!r} ""are not in kwargs".format(key=key))

    def get_sensor_data(self):
        X_2dot = self.last_state_dot[1]
        Y_2dot = self.last_state_dot[3]
        yaw = self.state[4]
        return {'accel': [X_2dot * np.cos(yaw) + Y_2dot * np.sin(yaw),
                          - X_2dot * np.sin(yaw) + Y_2dot * np.cos(yaw)],
                'angle_rate': self.state[4]}
