import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
logger = logging.getLogger("main")
logger.addHandler(sh)

class AlphaFilter:
    def __init__(self, a):
        self.a = a

    def initialize(self, state):
        self.est = state

    def estimate(self, m):
        # Dynamic model is constant, so predicition is previous state
        self.est = self.est + self.a * (m - self.est)
        return self.est
        

class AlphaBetaFilter:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def initialize(self, state):
        self.est = state

    def estimate(self, m, dt):
        # Predict next state
        self.pred = [
            self.est[0] + dt * self.est[1], 
            self.est[1],]

        # Estimate current state
        self.est = [
            self.pred[0] + self.a * (m[0] - self.pred[0]),
            self.pred[1] + self.b * ((m[0] - self.pred[0]) / dt),]

        return self.est


class AlphaBetaGammaFilter:
    def __init__(self, a, b, g):
        self.a = a
        self.b = b
        self.g = g

    def initialize(self, state):
        self.est = state

    def estimate(self, m, dt):
        # Predict next state
        self.pred = [
            self.est[0] + self.est[1] * dt + self.est[2] * (pow(dt, 2) / 2), 
            self.est[1] + self.est[2] * dt,]

        # Estimate current state
        self.est = [
            self.pred[0] + self.a * (m[0] - self.pred[0]),
            self.pred[1] + self.b * ((m[0] - self.pred[0]) / dt),
            self.pred[2] + self.g * ((m[0] - self.pred[0]) * (pow(dt, 2) / 2))]

        return self.est

def main():
    filter = AlphaBetaGammaFilter(0.5, 0.4, 0.1)

    logger.info('Initialize: 30000 50 0')
    filter.initialize([30000, 50, 0])

    logger.info("New measurement: 30160 at 5s interval")
    val = filter.estimate([30160], 5)
    logger.info(f"Prediction: {val}")

    logger.info("New measurement: 30365 at 5s interval")
    val = filter.estimate([30365], 5)
    logger.info(f"Prediction: {val}")
    

if __name__ == '__main__':
    main()
