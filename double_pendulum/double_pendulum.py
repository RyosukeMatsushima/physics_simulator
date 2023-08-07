import numpy as np
import sys
import pathlib

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../")
from common.physics_model import PhysicsModel


class DoublePendulum(PhysicsModel):
    def __init__(self, init_state, **kwargs):
        self.name = "DoublePendulum"
        self.GRAVITY = 9.81
        self.MASS = 0.3
        self.LENGTH = 0.2
        self.DRAG = 0.01
        self.set_param(**kwargs)

        super().__init__(init_state, (0.0, 0.0), **kwargs)

    def dynamics(self, states, u):
        u1 = u[0]
        u2 = u[1]

        theta1 = states[0]
        theta1_dot = states[1]
        theta2 = states[2]
        theta2_dot = states[3]

        theta1 += np.pi
        theta2 += np.pi
        A = np.array(
            [
                [
                    2 * self.MASS * self.LENGTH**2,
                    self.MASS * self.LENGTH**2 * np.cos(theta1 - theta2),
                ],
                [
                    self.MASS * self.LENGTH**2 * np.cos(theta1 - theta2),
                    self.MASS * self.LENGTH**2,
                ],
            ]
        )
        B = np.array(
            [
                [
                    -self.MASS
                    * self.LENGTH**2
                    * theta2_dot**2
                    * np.sin(theta1 - theta2)
                    - 2 * self.MASS * self.LENGTH * self.GRAVITY * np.sin(theta1)
                    + u1
                    - self.DRAG * theta1_dot
                ],
                [
                    self.MASS
                    * self.LENGTH**2
                    * theta1_dot**2
                    * np.sin(theta1 - theta2)
                    - self.MASS * self.GRAVITY * self.LENGTH * np.sin(theta2)
                    + u2
                    - self.DRAG * theta2_dot
                ],
            ]
        )

        angle_accels = np.dot(np.linalg.inv(A), B)
        theta1_2dot, theta2_2dot = angle_accels[0][0], angle_accels[1][0]
        return np.array([theta1_dot, theta1_2dot, theta2_dot, theta2_2dot])

    def energy(self, theta1, theta1_dot, theta2, theta2_dot):
        theta1 += np.pi
        theta2 += np.pi

        y1 = -self.LENGTH * np.cos(theta1)
        y2 = -(self.LENGTH * np.cos(theta1) + self.LENGTH * np.cos(theta2))

        x1_dot = self.LENGTH * theta1_dot * np.cos(theta1)
        y1_dot = self.LENGTH * theta1_dot * np.sin(theta1)
        x2_dot = self.LENGTH * theta1_dot * np.cos(
            theta1
        ) + self.LENGTH * theta2_dot * np.cos(theta2)
        y2_dot = self.LENGTH * theta1_dot * np.sin(
            theta1
        ) + self.LENGTH * theta2_dot * np.sin(theta2)

        T = self.MASS / 2 * (x1_dot**2 + y1_dot**2) + self.MASS / 2 * (
            x2_dot**2 + y2_dot**2
        )
        U = self.MASS * self.GRAVITY * y1 + self.MASS * self.GRAVITY * y2

        return T + U

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
            raise TypeError(
                "The required key {key!r} " "are not in kwargs".format(key=key)
            )
        self.INERTIA = (self.MASS * (2 * self.LENGTH) ** 2) / 12
