import numpy as np

from scipy.optimize import curve_fit


def interpol_function(x, a, b, c):
    # return a * (1 - np.power(x, b)) + c
    return a * np.log(np.multiply(x, b)) + c
    # return a - np.divide(b, np.multiply(x, c))


def log_interpol_events(x, y):
    coeffs, covariance = curve_fit(interpol_function, x, y)

    def interpol(x_data):
        return interpol_function(x_data, *coeffs)

    return interpol, coeffs
