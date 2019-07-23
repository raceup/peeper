import numpy as np


class KalmanFilter:
    def __init__(self, F=None, B=None, H=None, Q=None, R=None, P=None, x0=None):
        self.n = F.shape[1]
        self.m = H.shape[1]

        self.F = F
        self.H = H
        self.B = 0 if B is None else B
        self.Q = np.eye(self.n) if Q is None else Q
        self.R = np.eye(self.n) if R is None else R
        self.P = np.eye(self.n) if P is None else P
        self.x = np.zeros((self.n, 1)) if x0 is None else x0

    def predict(self, u=0):
        self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        return self.x

    def update(self, z):
        y = z - np.dot(self.H, self.x)
        S = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        I = np.eye(self.n)
        self.P = np.dot(np.dot(I - np.dot(K, self.H), self.P),
                        (I - np.dot(K, self.H)).T) + np.dot(np.dot(K, self.R), K.T)


def kalman(measurements):
    dt = 0.001
    F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]])
    H = np.array([1, 0, 0]).reshape(1, 3)
    Q = np.array([[0.0001, 0.0001, 0.0], [0.0001, 0.0001, 0.0], [0.0001, 0.0001, 0.0]])
    R = np.array([1]).reshape(1, 1)

    kf = KalmanFilter(F=F, H=H, Q=Q, R=R)
    predictions = []

    for z in measurements:
        prediction = np.dot(H, kf.predict())[0]
        predictions.append(prediction)
        kf.update(z)

    return predictions
