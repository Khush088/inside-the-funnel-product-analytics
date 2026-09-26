import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal
import os

def cramers_v(confusion_matrix):
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

def main():
    print("Running Statistical Analysis...")
    os.makedirs('outputs', exist_ok=True)
    
    df = pd.read_csv('data/processed/user_behavior_clean.csv')
    results = []
    
    # Chi-squared: device vs purchased
    cont_dev = pd.crosstab(df['device_category'], df['purchased'])
    chi2_dev, p_dev, _, _ = chi2_contingency(cont_dev)
    v_dev = cramers_v(cont_dev)
    results.append({'Test': 'Chi-squared (device vs purchased)', 'Statistic': chi2_dev, 'p-value': p_dev, 'Effect_Size_CramersV': v_dev})
    
    # Chi-squared: engagement_level vs purchased
    cont_eng = pd.crosstab(df['engagement_level'], df['purchased'])
    chi2_eng, p_eng, _, _ = chi2_contingency(cont_eng)
    v_eng = cramers_v(cont_eng)
    results.append({'Test': 'Chi-squared (engagement vs purchased)', 'Statistic': chi2_eng, 'p-value': p_eng, 'Effect_Size_CramersV': v_eng})
    
    # Mann-Whitney: session_count
    purchasers = df[df['purchased'] == 1]
    non_purchasers = df[df['purchased'] == 0]
    stat_sess, p_sess = mannwhitneyu(purchasers['session_count'], non_purchasers['session_count'])
    results.append({'Test': 'Mann-Whitney (session_count: purch vs non-purch)', 'Statistic': stat_sess, 'p-value': p_sess, 'Effect_Size_CramersV': None})
    
    # Mann-Whitney: active_days
    stat_days, p_days = mannwhitneyu(purchasers['active_days'], non_purchasers['active_days'])
    results.append({'Test': 'Mann-Whitney (active_days: purch vs non-purch)', 'Statistic': stat_days, 'p-value': p_days, 'Effect_Size_CramersV': None})
    
    # Kruskal-Wallis: revenue across devices (purchasers only)
    devs = [group['total_revenue'].values for name, group in purchasers.groupby('device_category')]
    stat_kw, p_kw = kruskal(*devs)
    results.append({'Test': 'Kruskal-Wallis (revenue across devices)', 'Statistic': stat_kw, 'p-value': p_kw, 'Effect_Size_CramersV': None})
    
    print("\nStatistical Tests Results (NOTE: Associations found do NOT imply causation):")
    res_df = pd.DataFrame(results)
    print(res_df)
    res_df.to_csv('outputs/statistical_tests.csv', index=False)

if __name__ == "__main__":
    main()
