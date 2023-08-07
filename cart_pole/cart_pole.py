import numpy as np
import sys
import pathlib

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )
from common.physics_model import PhysicsModel

class CartPole(PhysicsModel):

    def __init__(self, init_state, **kwargs):
        self.name = "CartPole"
        self.GRAVITY = 9.81
        self.MASS_CART = 0.5
        self.MASS_POLE = 0.3
        self.LENGTH_POLE = 0.5 # actually half the pole's length
        self.INERTIA_POLE = (self.MASS_POLE * (2 * self.LENGTH_POLE)**2)/12
        self.DRAG_CART = 0.1
        self.DRAG_POLE = 0.01
        self.set_param(**kwargs)

        super().__init__(init_state, 0.0, **kwargs)

    def dynamics(self, states, u):
        x = states[0]
        x_dot = states[1]
        theta = states[2]
        theta_dot = states[3]

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
