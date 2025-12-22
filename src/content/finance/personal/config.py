import math
import numpy as np

a = 1 / math.log(2)
b = 3
k = -math.log(0.85)

def Quality(p):
    return a * np.log(p) + b

def Longevity(p):
    return 1 - np.exp(-k * b) * p ** (-k * a)

def LongTermCost(p):
    return p / Longevity(p)

minimum_long_term_cost_per_price = math.exp(-b / a) * (1 + a * k)**(1 / (a * k))

maximum_quality_per_price = math.exp(1 - (b / a))

def dQ_dp(p):
    return a / p
