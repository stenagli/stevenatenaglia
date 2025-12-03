import numpy as np
import matplotlib.pyplot as plt
from config import k

q = np.linspace(0, 5, 500)

longevity = 1 - np.exp(-k * q)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(q, longevity, color='navy', linewidth=2)
ax.set_xlabel('Quality')
ax.set_ylabel('Longevity')
ax.grid(True)

plt.savefig('longevity-quality-graph.svg', format='svg')
#plt.show()

