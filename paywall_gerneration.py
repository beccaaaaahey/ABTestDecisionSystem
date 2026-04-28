import pandas as pd
import numpy as np

#building data for AB test
np.random.seed(42)
num_users = 5000
user_ids = np.arange(5001, 5001+num_users)
group = np.random.choice(['control(Soft Paywall)', 'treatment(Hard Paywall)'], num_users)

df = pd.DataFrame({'user_id': user_ids, 'group': group})

#Setting Conversion Rate (Control: 5%, Treatment: 8%)
def conversion_rate(group):
    if group == 'control(Soft Paywall)':
        return int(np.random.rand() <0.05)
    else:
        return int(np.random.rand() < 0.08)

#Setting Retention Rate (Control: 35%, Treatment: 30%)
def retention_rate(group):
    if group == 'control(Soft Paywall)':
        return int(np.random.rand() <0.35)
    else:
        return int(np.random.rand() < 0.30)

df['converted'] = df['group'].apply(conversion_rate)
df['retained'] = df['group'].apply(retention_rate)

#adding other features
df['past_sessions'] = np.random.gamma(shape=2, scale=5, size=num_users).astype(int)
df['hesitation_time'] = np.where(
    df['group'] == 'treatment(Hard Paywall)', 
    np.random.normal(loc=12, scale=4, size=num_users),
    np.random.normal(loc=3, scale=1, size=num_users))

df['hesitation_time'] = df['hesitation_time'].clip(lower=0)

df.to_csv('paywall_data.csv', index=False)
