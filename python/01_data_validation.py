import pandas as pd
import numpy as np
import os

def main():
    print("Running Data Validation...")
    os.makedirs('outputs', exist_ok=True)
    
    df = pd.read_csv('data/raw/ga4_user_level_funnel.csv')
    
    results = {}
    results['shape'] = df.shape
    results['duplicates'] = df.duplicated().sum()
    results['missing_values'] = df.isna().sum().sum()
    
    # Boolean flag consistency
    bool_cols = ['viewed_item', 'added_to_cart', 'began_checkout', 'purchased']
    results['bool_flags_valid'] = all(df[c].isin([0, 1]).all() for c in bool_cols)
    
    # Funnel inconsistencies
    began_without_cart = df[(df['began_checkout'] == 1) & (df['added_to_cart'] == 0)].shape[0]
    cart_without_view = df[(df['added_to_cart'] == 1) & (df['viewed_item'] == 0)].shape[0]
    purchased_without_checkout = df[(df['purchased'] == 1) & (df['began_checkout'] == 0)].shape[0]
    
    results['began_without_cart'] = began_without_cart
    results['cart_without_view'] = cart_without_view
    results['purchased_without_checkout'] = purchased_without_checkout
    
    # Zero revenue purchasers
    zero_rev_purchasers = df[(df['purchased'] == 1) & (df['total_revenue'] == 0)].shape[0]
    results['zero_revenue_purchasers'] = zero_rev_purchasers
    
    # Negative revenue
    neg_revenue = df[df['total_revenue'] < 0].shape[0]
    results['negative_revenue'] = neg_revenue
    
    # Session count edge case
    session_count_zero = df[df['session_count'] == 0].shape[0]
    results['session_count_zero'] = session_count_zero
    
    print("--- Data Quality Report ---")
    for k, v in results.items():
        print(f"{k}: {v}")
        
    report_df = pd.DataFrame(list(results.items()), columns=['Metric', 'Value'])
    report_df.to_csv('outputs/data_quality_report.csv', index=False)
    print("Report saved to outputs/data_quality_report.csv")

if __name__ == "__main__":
    main()
