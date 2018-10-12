# only store the first 10 000 primes
lines = open('primes.txt').readlines()[:10000]
primes = [int(x) for l in lines for x in l.split()]
print(primes)