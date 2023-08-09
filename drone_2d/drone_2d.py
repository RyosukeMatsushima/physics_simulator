import numpy as np
import sys
import pathlib

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../")
from common.physics_model import PhysicsModel


class Drone2D(PhysicsModel):
    def __init__(self, init_state, **kwargs):
        self.name = "Drone2D"
        self.MASS = 0.5
        self.LENGTH = 0.2  # motor to center of gravity
        self.INERTIA = 0.007
        self.DRAG = 0.0
        self.DRAG_ROTATE = 0.0
        self.GRAVITY = 9.81
        self.disturbance = (0, 0)  # disturbance for each axis (X, Z)
        self.set_param(**kwargs)

        init_input = (0.0, 0.0)  # (right motor, left motor)
        super().__init__(init_state, init_input, **kwargs)

    def dynamics(self, states, u):
        X = states[0]
        Z = states[1]
        theta = states[2]
        x_dot = states[3]
        z_dot = states[4]
        theta_dot = states[5]

        X_dot = x_dot * np.cos(theta) + z_dot * np.sin(theta)
        Z_dot = -x_dot * np.sin(theta) + z_dot * np.cos(theta)

        disturbance_x = self.disturbance[0] * np.cos(theta) - self.disturbance[
            1
        ] * np.sin(theta)
        disturbance_z = self.disturbance[0] * np.sin(theta) + self.disturbance[
            1
        ] * np.cos(theta)

        x_2dot = (
            -self.MASS * self.GRAVITY * np.sin(theta)
            - x_dot * self.DRAG
            + disturbance_x
        ) / self.MASS
        z_2dot = (
            -u[0]
            - u[1]
            + self.MASS * self.GRAVITY * np.cos(theta)
            - z_dot * self.DRAG
            + disturbance_z
        ) / self.MASS
        theta_2dot = (
            u[0] * self.LENGTH
            - u[1] * self.LENGTH
            - theta_dot * self.DRAG_ROTATE
        ) / self.INERTIA
        return np.array([X_dot, Z_dot, theta_dot, x_2dot, z_2dot, theta_2dot])

    def get_param(self):
        return {
            "mass": self.MASS,
            "length": self.LENGTH,
            "inertia": self.INERTIA,
            "drag": self.DRAG,
            "drag_rotate": self.DRAG_ROTATE,
        }

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
            raise TypeError(
                "The required key {key!r} " "are not in kwargs".format(key=key)
            )
