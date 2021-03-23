from functools import wraps
from threading import Thread
import time

import matplotlib.pyplot as plt
import seaborn as sns
import random
from controller.cursor import Cursor


class Variable(object):
    def __init__(self, value=0, name="undefine"):
        self.inter = value
        self.data = [value]
        self.name = name
        self.startTime = time.time()
        self.time = [time.time()-self.startTime]
        self.grad = 0

    def setName(self, name):
        self.name = name

    def update(self, val):
        actualTime = time.time() - self.startTime
        dt = (actualTime - self.time[-1]) + 1
        self.inter += val*dt
        self.grad = (val-self.data[-1])/dt
        self.time.append(actualTime)
        self.data.append(val)

    @property
    def value(self):
        return self.data[-1]


class PIDController(object):
    def __init__(self, p: float, i: float, d: float, V_input: Variable, V_output: Variable, V_observable: Variable):
        self.input = V_input
        self.observable = V_observable
        self.output = V_output
        self.error = Variable(value=0, name="error")
        self.signal = 0

        self.p = p
        self.i = i
        self.d = d

    def observable_observe(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            self.observable.update(val)
            self.update()
        return wrapper

    def input_observe(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            self.input.update(val)
        return wrapper

    def update(self):
        self.error.update(self.input.value - self.observable.value)
        p = self.error.value * self.p
        d = self.error.grad * self.d
        i = self.error.inter * self.i
        self.output.update(p+i+d)

    def visualize(self):
        self.input.time.append(self.observable.time[-1])
        self.input.data.append(self.input.data[-1])

        fig, ax = plt.subplots()
        ax.set_title('Visualization')

        ax.plot(self.input.time, self.input.data, label=self.input.name)
        ax.plot(self.observable.time, self.observable.data, label=self.observable.name)
        cursor = Cursor(ax)
        fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)
        plt.grid()
        plt.legend()
        plt.show()
