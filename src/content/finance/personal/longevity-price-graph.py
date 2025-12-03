import numpy as np
import matplotlib.pyplot as plt
from config import Longevity

p = np.linspace(1/8, 4, 500)

longevity = Longevity(p)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(p, longevity, color='navy', linewidth=2)
ax.set_xlabel('Price')
ax.set_ylabel('Longevity')
ax.grid(True)

plt.savefig('longevity-price-graph.svg', format='svg')
#plt.show()
