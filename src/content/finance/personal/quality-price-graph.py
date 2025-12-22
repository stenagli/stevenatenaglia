import numpy as np
import matplotlib.pyplot as plt
from config import Quality

x = np.linspace(1/8, 4, 500)
y = Quality(x)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color='navy', linewidth=2)
ax.set_xlabel('Price')
ax.set_ylabel('Quality')
ax.grid(True)

#plt.show()
plt.savefig('quality-price-graph.svg', format='svg')
