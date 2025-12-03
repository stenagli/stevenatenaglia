import numpy as np
import matplotlib.pyplot as plt
from config import Longevity

p = np.linspace(1/8, 4, 500)

longevity = Longevity(p)
longevity = np.clip(longevity, 1e-6, None)  # avoid zero

LTC = p / longevity 

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_ylim(0, 20)
ax.plot(p, LTC, color='navy', linewidth=2)
ax.set_xlabel('Price')
ax.set_ylabel('Long-term Cost')
ax.grid(True)

plt.savefig('long-term-cost-price-graph.svg', format='svg')
#plt.show()
