import random
from bisect import bisect_left, bisect_right

from src.constants import primes

toHex = lambda x: "".join([hex(ord(c))[2:] for c in x])

class Hasher:
    def __init__(self, M):
        """
        Arguments:
            M {int} -- output range of hash function
        """
        self.M = M

        # pick some prime number that is greater than 
        lower = bisect_left(primes, 3 * M) + 5
        upper = bisect_left(primes, 7 * M) + 5
        self.p = primes[random.randint(lower, upper)]
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(1, self.p - 1)
    
    def hash(self, x):
        return ((self.a * x + self.b) % self.p ) % self.M


class Counter:

    def scan(self, x): pass
    def query(self, x): pass


class StreamCounter(Counter):

    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.counter = [[0 for j in range(B)] for i in range(A)]

        # create hashers
        self.hashers = [Hasher(self.B) for i in range(self.A)]


    def quickselect_median(self, l, pivot_fn=random.choice):
        if len(l) % 2 == 1:
            return self.quickselect(l, len(l) // 2, pivot_fn)
        else:
            return 0.5 * (self.quickselect(l, len(l) // 2 - 1, pivot_fn) +
                        self.quickselect(l, len(l) // 2, pivot_fn))


    def quickselect(self, l, k, pivot_fn):
        """
        Select the kth element in l (0 based)
        :param l: List of numerics
        :param k: Index
        :param pivot_fn: Function to choose a pivot, defaults to random.choice
        :return: The kth element of l
        """
        if len(l) == 1:
            assert k == 0
            return l[0]

        pivot = pivot_fn(l)

        lows = [el for el in l if el < pivot]
        highs = [el for el in l if el > pivot]
        pivots = [el for el in l if el == pivot]

        if k < len(lows):
            return self.quickselect(lows, k, pivot_fn)
        elif k < len(lows) + len(pivots):
            # We got lucky and guessed the median
            return pivots[0]
        else:
            return self.quickselect(highs, k - len(lows) - len(pivots), pivot_fn)


    def scan(self, x):
        if isinstance(x, str):
            x = int(toHex(x), 16)
        for i in range(self.A):
            h_i_x = self.hashers[i].hash(x)
            self.counter[i][h_i_x] += 1
    

    def query(self, x):
        pass

class StreamCounterMedian(StreamCounter):

    def query(self, x):
        if isinstance(x, str):
            x = int(toHex(x), 16)

        C = [self.counter[i][self.hashers[i].hash(x) ]for i in range(self.A)]
        return self.quickselect_median(C)


class StreamCounterNeighourMedian(StreamCounter):

    def estimate(self, x, i):
        h_i_x = self.hashers[i].hash(x)
        return self.counter[i][h_i_x] - self.neighbour(i, h_i_x)


    def neighbour(self, i, j):
        j = j+1 if j % 2 == 0 else j-1
        return self.counter[i][j]

    def query(self, x):
        if isinstance(x, str):
            x = int(toHex(x), 16)
        C = [self.estimate(x, i) for i in range(self.A)]
        ret = self.quickselect_median(C)
        return ret if ret > 0 else 0
        