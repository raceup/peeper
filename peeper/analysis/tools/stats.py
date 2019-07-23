import numpy as np


def rms(x):
    return np.sqrt(np.vdot(x, x) / x.size)
