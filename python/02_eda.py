"""
02_eda.py
Exploratory Data Analysis script.
Generates distribution plots, funnel counts, revenue distribution (positive-revenue purchasers, N=4,066),
and correlation matrix.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def main():
    print("Running EDA...")
    os.makedirs('outputs', exist_ok=True)
    
    df = pd.read_csv('data/raw/ga4_user_level_funnel.csv')
    
    # 1. Device category distribution
    plt.figure(figsize=(10, 6))
    df['device_category'].value_counts().plot(kind='bar', color='#2b5c8f')
    plt.title('Device Category Distribution (N=270,154)', fontsize=14, pad=12)
    plt.xlabel('Device Category', fontsize=12)
    plt.ylabel('User Count', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('outputs/device_dist.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Top 15 countries distribution
    plt.figure(figsize=(12, 6))
    df['country'].value_counts().head(15).plot(kind='bar', color='#4575b4')
    plt.title('Top 15 Countries by User Volume', fontsize=14, pad=12)
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('User Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('outputs/country_dist.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Funnel stage counts (Marginal stage reach)
    stages = ['Viewed Item', 'Added to Cart', 'Began Checkout', 'Purchased']
    counts = [df['viewed_item'].sum(), df['added_to_cart'].sum(), df['began_checkout'].sum(), df['purchased'].sum()]
    plt.figure(figsize=(8, 6))
    bars = plt.bar(stages, counts, color=['#74add1', '#fdae61', '#f46d43', '#d73027'])
    plt.title('Funnel Stage Reach (User-Level Counts)', fontsize=14, pad=12)
    plt.ylabel('Unique Users', fontsize=12)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1000, f'{yval:,}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('outputs/funnel_counts.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. Revenue distribution (Positive-revenue purchasers only, N=4,066)
    pos_purchasers = df[(df['purchased'] == 1) & (df['total_revenue'] > 0)]
    plt.figure(figsize=(9, 6))
    plt.hist(pos_purchasers['total_revenue'], bins=40, color='#313695', edgecolor='white')
    plt.title('Revenue Distribution (Positive-Revenue Purchasers, N=4,066)\n[Note: 353 purchasers with $0 revenue excluded from histogram]', fontsize=13, pad=12)
    plt.xlabel('Total Revenue (USD)', fontsize=12)
    plt.ylabel('Purchaser Count', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('outputs/revenue_dist.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. Correlation matrix
    numeric_cols = ['viewed_item', 'added_to_cart', 'began_checkout', 'purchased', 'active_days', 'session_count', 'total_revenue']
    corr = df[numeric_cols].corr()
    plt.figure(figsize=(9, 7))
    plt.imshow(corr, cmap='Blues', interpolation='nearest')
    plt.colorbar()
    plt.xticks(range(len(numeric_cols)), numeric_cols, rotation=45, ha='right')
    plt.yticks(range(len(numeric_cols)), numeric_cols)
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha='center', va='center', color='white' if corr.iloc[i, j] > 0.5 else 'black')
    plt.title('Correlation Matrix (User-Level Metrics)', fontsize=14, pad=15)
    plt.savefig('outputs/correlation_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("EDA completed and plots saved.")

if __name__ == "__main__":
    main()
