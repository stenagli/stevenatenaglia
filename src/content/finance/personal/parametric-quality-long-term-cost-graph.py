import numpy as np
import matplotlib.pyplot as plt
from config import Quality, Longevity, LongTermCost, minimum_long_term_cost_per_price, maximum_quality_per_price


# relative price range (just above the x-intercept up to a few times median)
p = np.linspace(1.0/7.5, 4.0, 2000)
#p = np.linspace(.25, 1.5, 2000)

q = Quality(p)
l = Longevity(p)
ltc = LongTermCost(p)

# parametric plot: Quality vs Long-term Cost
fig, ax = plt.subplots(figsize=(8,6))
sc = ax.scatter(ltc, q, c=p, cmap='viridis', s=8)   # color by p
ax.set_xlabel('Long-term cost, relative units')
ax.set_ylabel('Quality (relative units)')
ax.set_title('Parametric: Quality vs Long-term Cost (p as parameter)')
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Relative price (1 = median price)')

# Plot reference price points
p_refs = np.array([0.5, 1.0, 2.0, 3.0])

for pr in p_refs:
    ax.scatter(
        LongTermCost(pr),
        Quality(pr),
        color='black',
        s=40,
        zorder=5
    )
    ax.annotate(
        f"p={pr:g}",
        (LongTermCost(pr), Quality(pr)),
        textcoords="offset points",
        xytext=(6, 6),
        fontsize=9
    )

# mark the cost-minimizing price
p_L_opt = minimum_long_term_cost_per_price
ax.scatter([LongTermCost(p_L_opt)], [Quality(p_L_opt)], color='red', s=60, label=f'Minimum Long-Term Cost={p_L_opt:.3f}')

ax.set_aspect('equal', adjustable='box')

ax.legend()
ax.grid(True, which='both', ls='--', lw=0.5)
#plt.show()
plt.savefig('parametric-quality-long-term-cost-price-graph.svg', format='svg')
