import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('paywall_data.csv')

#SRM
observed = df['group'].value_counts()
expected = [len(df)/2, len(df)/2]
chi, p_srm = stats.chisquare(observed, f_exp=expected)
print(f"SRM Chi-Square: {chi:.2f}, p-value: {p_srm:.2f}")
if p_srm < 0.01:
    print("SRM failed: Significant difference in group sizes.")
else:
    print("SRM passed: No significant difference in group sizes. \n")

control = df[df['group'] == 'control(Soft Paywall)']
treatment = df[df['group'] == 'treatment(Hard Paywall)']
t_con, p_con = stats.ttest_ind(control['converted'], treatment['converted'])

#ci
def confidence_interval(data):
    mean = np.mean(data)
    se = stats.sem(data)
    return stats.t.interval(0.99, len(data)-1, loc=mean, scale = se)

#conversion rate result
print(f'Lift in Conversion Rate: {(treatment["converted"].mean() - control["converted"].mean())/control["converted"].mean() * 100:.2f}%')
print(f"Conversion Rate t-statistic: {t_con:.2f}, p-value: {p_con:.2f}")

if p_con < 0.01:
    print("Conversion rate difference is statistically significant.")
else:    print("No statistically significant difference in conversion rates.")

conversion_ci = confidence_interval(df['converted'])
print(f"Conversion Rate 99% CI: [{conversion_ci[0]:.2%}, {conversion_ci[1]:.2%}]\n")

#retention rate result
print(f'Lift in Retention Rate: {(treatment["retained"].mean() - control["retained"].mean())/control["retained"].mean() * 100:.2f}%')
t_ret, p_ret = stats.ttest_ind(control['retained'], treatment['retained'])
print(f"Retention Rate t-statistic: {t_ret:.2f}, p-value: {p_ret:.2f}")
if p_ret < 0.01:
    print("Retention rate difference is statistically significant.")
else:
    print("No statistically significant difference in retention rates.")

retention_ci = confidence_interval(df['retained'])
print(f"Retention Rate 99% CI: [{retention_ci[0]:.2%}, {retention_ci[1]:.2%}]")


# save results to a text file for AI Agent
with open("stats_summary.txt", "w") as f:
    f.write(f"SRM_Status: {'Pass' if p_srm > 0.01 else 'Fail'}\n")
    f.write(f"Conv_P: {p_con:.4f}, Ret_P: {p_ret:.4f}\n")
    f.write(f"Conversion Rate 99% CI: [{conversion_ci[0]:.2%}, {conversion_ci[1]:.2%}]\n")
    f.write(f"Retention Rate 99% CI: [{retention_ci[0]:.2%}, {retention_ci[1]:.2%}]\n")
    f.write(f"Conv_Lift: {(treatment['converted'].mean() - control['converted'].mean()) / control['converted'].mean():.2%}\n")
    f.write(f"Ret_Lift: {(treatment['retained'].mean() - control['retained'].mean()) / control['retained'].mean():.2%}")
