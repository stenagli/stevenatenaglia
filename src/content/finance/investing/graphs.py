import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Shiller S&P 500 data
# http://www.econ.yale.edu/~shiller/data.htm
df = pd.read_excel('ie_data.xls', sheet_name='Data', skiprows=7)
df['date'] = pd.to_datetime(df['Date'])
df['total_return'] = df['Price'] + df['Dividend']  # Price + div index

monthly_returns = df['total_return'].ffill().pct_change(fill_method=None).dropna()
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

for h in horizons:
    horizon_months = h * 12
    rlg = rolling_log_growth(cumsum_log, horizon_months)

    percentiles = np.percentile(rlg, [10, 50, 90])
    terminal_results[h] = dict(zip(['p10','p50','p90'], np.exp(percentiles)))
    cagr_results[h] = dict(zip(['p10','p50','p90'], np.exp(percentiles / h) - 1))
    loss_probs[h] = (rlg < 0).mean()

df = pd.DataFrame(cagr_results).T.mul(100).round(1) # Transpose for years as x-axis
df_terminal = pd.DataFrame(terminal_results).T
df_loss = pd.Series(loss_probs)


# Create the funnel chart
plt.figure(figsize=(10, 6))
years = df.index  # [1,3,5,10,20,30]
plt.plot(years, df['p90'], 'b--', label='90th percentile (gains)', linewidth=3, marker='^')
plt.plot(years, df['p50'], 'g-', label='50th percentile (median)', linewidth=3, marker='s') 
plt.plot(years, df['p10'], 'r--', label='10th percentile (losses)', linewidth=3, marker='o')
plt.fill_between(years, df['p90'], df['p10'], alpha=0.2, color='gray', label='80% range')

plt.title('Time Horizon Funnel: 150+ Years S&P 500 Returns', fontsize=16, fontweight='bold')
plt.xlabel('Years Invested', fontsize=12)
plt.ylabel('Annualized Return (CAGR %)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('cagr_funnel.svg', format='svg', bbox_inches='tight')
#plt.show()


# Terminal Fan
plt.figure(figsize=(10, 6))
years = df_terminal.index

plt.plot(years, df_terminal['p90'], '--', linewidth=3, label='90th percentile')
plt.plot(years, df_terminal['p50'], '-', linewidth=3, label='Median')
plt.plot(years, df_terminal['p10'], '--', linewidth=3, label='10th percentile')
plt.fill_between(years, df_terminal['p90'], df_terminal['p10'], alpha=0.2, label='80% range')

plt.title('Terminal Wealth Fan (Starting from $1)', fontsize=16, fontweight='bold')
plt.xlabel('Years Invested', fontsize=12)
plt.ylabel('Final Wealth Multiple', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('terminal_wealth_fan.svg', format='svg', bbox_inches='tight')
#plt.show()


# Loss Probability
plt.figure(figsize=(10, 6))
plt.plot(df_loss.index, df_loss.values * 100, marker='o', linewidth=3)

plt.title('Probability of Ending with a Loss', fontsize=16, fontweight='bold')
plt.xlabel('Years Invested', fontsize=12)
plt.ylabel('Probability of Loss (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('loss_probability.svg', format='svg', bbox_inches='tight')
#plt.show()
