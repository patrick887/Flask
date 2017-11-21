from random import randint
import math


def get_factors(x):
    factors = []
    for i in range(2, x + 1):
        if x % i == 0:
            factors.append(i)
    return factors


def isPrime(primeList, candidate):
    upperLimit = math.sqrt(candidate)
    for p in primeList:
        if candidate % p == 0:
            return False
        if p >= upperLimit:
            break

    return True


def primeList(listLength):
    if listLength < 1:
        return []
    primes = [2]

    candidate = 3
    while listLength > len(primes):
        if isPrime(primes, candidate):
            primes.append(candidate)
        candidate += 2

    return primes


def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x


p = primeList(1000)
p = p[randint(500, 999)]
q = primeList(1000)
q = q[randint(500, 999)]

n = p * q
phin = (p - 1) * (q - 1)
# 1<e<phin
factor_phin = get_factors(phin)
encrypt = []
for e in range(2, phin):
    if gcd(phin, e) == 1:
        encrypt.append(e)
e = encrypt[randint(0, len(encrypt))]

