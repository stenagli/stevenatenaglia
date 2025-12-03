import numpy as np
import matplotlib.pyplot as plt
from config import a, k, Quality, Longevity, LongTermCost, minimum_long_term_cost_per_price

# Price range (avoid the singular very close to p_opt = 0.3069513985874212)
p = np.linspace(0.30696, 4, 2000)

Q = Quality(p)

L = Longevity(p)

LTC = LongTermCost(p)

# Derivatives
dQ_dp = a / p
dL_dp = (k * np.exp(-k * Q)) * dQ_dp
dLTC_dp = (L - p * dL_dp) / (L**2)

# Slope of Quality vs LTC
slope = dQ_dp / dLTC_dp

# Plot
plt.figure(figsize=(8,5))
plt.plot(p, slope)
plt.xlabel('Relative Price')
plt.ylabel('Slope of Quality vs Long-Term Cost')
plt.title('Marginal Quality Gain per Unit Long-Term Cost')
plt.grid(True)

# Mark the asymptote at p_opt
plt.axvline(x=minimum_long_term_cost_per_price, color='k', linestyle='--')

low = np.percentile(slope, 1)
high = np.percentile(slope, 99.5)
plt.ylim(low, high)

#plt.show()
plt.savefig('slope-quality-long-term-cost-graph.svg', format='svg')
