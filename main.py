import logging
import sys
import filter

logger = logging.getLogger("main")


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


class KalmanFilter1D:
    def __init__(self):
        self.kg = None
        self.pn = None
        self.initial = True

    def _cov_update(self):
        self.pn = (1 - self.kg) * self.pn

    def _kalman_gain(self):
        self.kg = self.pn / (self.pn + self.rn)

    def _cov_extrapolation(self):
        self.pn = self.pn

    def _predict(self, dt):
        self.pred = [
            self.est[0] + self.est[1] * dt + self.est[2] * (pow(dt, 2) / 2), 
            self.est[1] + self.est[2] * dt,
            self.est[2]]
        logger.debug(f"Prediction: {self.pred}")
    
    def initialize(self, state, rn):
        logger.debug(f"Initialize: state: {state}")
        self.est = state
        self.rn = rn
        self.initial = True

    def estimate(self, m, dt):
        logger.debug(f"Measurement: {m}, interval: {dt}")

        if self.initial:
            self._predict(dt)
            self.initial = False
        


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    abg = filter.AlphaBetaGammaFilter(0.5, 0.4, 0.1)
    abg.initialize([30000, 50, 0])
    abg.estimate([30160], 5)
    abg.estimate([30365], 5)

    kalman = KalmanFilter1D()
    kalman


if __name__ == '__main__':
    main()
