import os
import random
from numpy.random import geometric

N = 100000

def create_file(numbers, filename):
    with open(filename, 'w+') as f:
        f.writelines([str(x)+'\n' for x in numbers])


def small_in():
    # 1000 copies of 10 numbers
    numbers = [x for x in range(10) for i in range(1000)]
    create_file(numbers, "small.in")

def random_small_in():
    numbers = [random.randint(0, 100) for i in range(N)]
    create_file(numbers, "random.100.in")

def random_medium_in():
    numbers = [random.randint(0, 1000) for i in range(N)]
    create_file(numbers, "random.1000.in")

def random_large_in():
    numbers = [random.randint(0, 10000) for i in range(N)]
    create_file(numbers, "random.10000.in")

def exp_small_in():
    numbers = geometric(0.5, N)
    create_file(numbers, "exp.5.in")

def exp_medium_in():
    numbers = geometric(0.25, N)
    create_file(numbers, "exp.25.in")
    
def exp_large_in():
    numbers = geometric(0.125, N)
    create_file(numbers, "exp.125.in")

def remove_files():
    for f in os.listdir():
        if f.endswith('.in'):
            os.remove(f)

if __name__ == "__main__":
    remove_files()
    small_in()
    random_small_in()
    random_medium_in()
    random_large_in()
    exp_small_in()
    exp_medium_in()
    exp_large_in()