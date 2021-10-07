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
        # Predict next state using system's dynamic model
        self.pred = [
            self.est[0] + dt * self.est[1], 
            self.est[1]] # Assuming constant

        # Estimate current state
        self.est = [
            self.pred[0] + self.a * (m[0] - self.pred[0]),
            self.pred[1] + self.b * ((m[0] - self.pred[0]) / dt)]

        return self.est


def main():
    filter = AlphaBetaFilter(0.2, 0.1)

    logger.info('Initialize: 30000 40')
    filter.initialize([30000, 40])

    logger.info("New measurement: 30110")
    val = filter.estimate([30110], 5)

    logger.info(f"Prediction: {val}")
    

if __name__ == '__main__':
    main()
