import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Shiller S&P 500 data
# http://www.econ.yale.edu/~shiller/data.htm
df = pd.read_excel('ie_data.xls', sheet_name='Data', skiprows=7)
df = df.dropna(subset=['Price.1'])  # drop trailing empty row

monthly_returns = df['Price.1'].pct_change().dropna()
returns = monthly_returns.to_numpy()

# Work in log space to improve numerical stability
# and simplify arithmetic
log_returns = np.log(1 + returns)
cumsum_log = np.cumsum(log_returns)

def rolling_log_growth(cumsum_log, window):
    rp_log = np.empty(len(cumsum_log) - window + 1)
    rp_log[0] = cumsum_log[window - 1]
    rp_log[1:] = cumsum_log[window:] - cumsum_log[:-window]
    return rp_log

horizons = [1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 30]
cagr_results = {}
terminal_results = {}
loss_probs = {}

result_keys = ['p0','p25','p50','p75','p100']
for h in horizons:
    horizon_months = h * 12
    rlg = rolling_log_growth(cumsum_log, horizon_months)

    percentiles = np.percentile(rlg, [0, 25, 50, 75, 100])
    terminal_results[h] = dict(zip(result_keys, np.exp(percentiles)))
    cagr_results[h] = dict(zip(result_keys, np.exp(percentiles / h) - 1))
    loss_probs[h] = (rlg < 0).mean()

df_cagr = pd.DataFrame(cagr_results).T.mul(100).round(1) # Transpose for years as x-axis
df_terminal = pd.DataFrame(terminal_results).T
df_loss = pd.Series(loss_probs)


def plot_percentiles(plt, df):
    plt.figure(figsize=(10, 6))
    years = df.index  # [1,3,5,10,20,30]
    plt.plot(years, df[result_keys[3]], 'g--', label='75th percentile', linewidth=3, marker='o')
    plt.plot(years, df[result_keys[2]], 'b-', label='50th percentile', linewidth=3, marker='s')
    plt.plot(years, df[result_keys[1]], 'r--', label='25th percentile', linewidth=3, marker='o')
    plt.fill_between(years, df[result_keys[0]], df[result_keys[4]], alpha=0.2, color='gray')


# Create the funnel chart
plot_percentiles(plt, df_cagr)
plt.title('Time Horizon Funnel: 150+ Years S&P 500 Returns', fontsize=16, fontweight='bold')
plt.xlabel('Years Invested', fontsize=12)
plt.ylabel('Annualized Return (CAGR %)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('cagr_funnel.svg', format='svg', bbox_inches='tight')
plt.show()


# Terminal Fan
plot_percentiles(plt, df_terminal)

plt.title('Terminal Wealth Fan (Starting from $1)', fontsize=16, fontweight='bold')
plt.xlabel('Years Invested', fontsize=12)
plt.ylabel('Final Wealth Multiple', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('terminal_wealth_fan.svg', format='svg', bbox_inches='tight')
plt.show()


# Loss Probability
plt.figure(figsize=(10, 6))
plt.plot(df_loss.index, df_loss.values * 100, marker='o', linewidth=3)

plt.title('Probability of Ending with a Loss', fontsize=16, fontweight='bold')
plt.xlabel('Years Invested', fontsize=12)
plt.ylabel('Probability of Loss (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('loss_probability.svg', format='svg', bbox_inches='tight')
plt.show()
