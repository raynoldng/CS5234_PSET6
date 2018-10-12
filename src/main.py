from collections import Counter
import time

from src.counter import StreamCounterMedian, StreamCounterNeighourMedian

class Experiment:
    def __init__(self, numbers, counter):
        self.numbers = numbers
        self.exact_counter = Counter(numbers)
        self.counter = counter

    def run(self):
        start = time.time()
        for x in self.numbers:
            self.counter.scan(x)
        elapsed = time.time() - start
        error = 0
        for k, v in self.exact_counter.items():
            error += abs(v - self.counter.query(k))
        avg_error = error / len(self.exact_counter.keys())
        return (avg_error, elapsed)

if __name__ == '__main__':
    c = StreamCounterMedian(50, 50)
    numbers = [int(x.strip()) for x in open('datasets/random.40.in').readlines()]
    exp = Experiment(numbers, c)
    mean_error = exp.run()
    print(mean_error)