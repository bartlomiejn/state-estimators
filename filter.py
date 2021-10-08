import sys
import logging

logger = logging.getLogger("estimator")

class AlphaFilter:
    def __init__(self, a):
        self.a = a

    def initialize(self, state):
        self.est = state

    def estimate(self, m):
        self.est = self.est + self.a * (m - self.est)
        return self.est
        

class AlphaBetaFilter:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def initialize(self, state):
        self.est = state

    def estimate(self, m, dt):
        self.pred = [
            self.est[0] + dt * self.est[1], 
            self.est[1],]
        self.est = [
            self.pred[0] + self.a * (m[0] - self.pred[0]),
            self.pred[1] + self.b * ((m[0] - self.pred[0]) / dt),]

        return self.est


class AlphaBetaGammaFilter:
    def __init__(self, a, b, g):
        self.a = a
        self.b = b
        self.g = g
        self.initial = True

    def initialize(self, state):
        logger.debug(f"Initialization: {state}")
        self.est = state
        self.initial = True

    def estimate(self, m, dt):
        logger.debug(f"Measurement: {m}, interval: {dt}")

        if self.initial:
            self._predict(dt)
            self.initial = False

        self.est = [
            self.pred[0] + self.a * (m[0] - self.pred[0]),
            self.pred[1] + self.b * ((m[0] - self.pred[0]) / dt),
            self.pred[2] + self.g * ((m[0] - self.pred[0]) / (pow(dt, 2) / 2))]
        logger.debug(f"Estimate: {self.est}")

        self._predict(dt)
        
        return self.est

    def _predict(self, dt):
        self.pred = [
            self.est[0] + self.est[1] * dt + self.est[2] * (pow(dt, 2) / 2), 
            self.est[1] + self.est[2] * dt,
            self.est[2]]
        logger.debug(f"Prediction: {self.pred}")