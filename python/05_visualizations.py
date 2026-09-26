"""
05_visualizations.py
Production-quality visualizations for Product Analytics presentation.
Ensures all labels, caveats, and statistical findings match the locked Master Specification.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def main():
    print("Running Visualizations...")
    os.makedirs('outputs', exist_ok=True)
    
    df = pd.read_csv('data/processed/user_behavior_clean.csv')
    
    # ------------------------------------------------------------
    # 1. Funnel Chart (Horizontal Bar with Stage Reach & Users Lost)
    # ------------------------------------------------------------
    stages = ['All Users', 'Viewed Item', 'Added to Cart', 'Began Checkout', 'Purchased']
    counts = [len(df), df['viewed_item'].sum(), df['added_to_cart'].sum(), df['began_checkout'].sum(), df['purchased'].sum()]
    colors = ['#4a7bb0', '#5c9ebf', '#e69f00', '#d55e00', '#009e73']
    
    plt.figure(figsize=(10, 5.5))
    bars = plt.barh(stages[::-1], counts[::-1], color=colors[::-1])
    plt.title('Purchase Funnel Stage Reach (N=270,154 Unique Users)', fontsize=13, pad=12, fontweight='bold')
    plt.xlabel('Unique Users', fontsize=11)
    
    for bar in bars:
        w = bar.get_width()
        pct = (w / len(df)) * 100
        plt.text(w + 3000, bar.get_y() + bar.get_height()/2.0, f'{w:,} ({pct:.1f}%)', 
                 va='center', ha='left', fontsize=10, fontweight='bold')
        
    plt.xlim(0, 310000)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.savefig('outputs/funnel_chart.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------------------------------------------------------------
    # 2. Conversion Rate by Device (With Statistical Context)
    # ------------------------------------------------------------
    dev_stats = df.groupby('device_category').agg(
        total_users=('user_pseudo_id', 'count'),
        purchasers=('purchased', 'sum'),
        conv_rate=('purchased', lambda x: x.mean() * 100)
    ).reindex(['mobile', 'desktop', 'tablet'])
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(dev_stats.index, dev_stats['conv_rate'], color=['#3b82f6', '#10b981', '#f59e0b'], width=0.5)
    plt.title('Purchase Conversion Rate by Device Category\n[Chi-sq = 3.53, p = 0.171 — Difference is NOT statistically significant]', 
              fontsize=12, pad=12, fontweight='bold')
    plt.ylabel('Purchase Conversion Rate (%)', fontsize=11)
    plt.ylim(0, 2.5)
    
    for bar, dev in zip(bars, dev_stats.index):
        h = bar.get_height()
        u = dev_stats.loc[dev, 'total_users']
        plt.text(bar.get_x() + bar.get_width()/2.0, h + 0.08, f'{h:.2f}%\n(N={u:,})', 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig('outputs/conversion_device.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------------------------------------------------------------
    # 3. Conversion by Traffic Source (Distinguishing Data Quality Artifacts)
    # ------------------------------------------------------------
    src_stats = df.groupby('traffic_source').agg(
        users=('user_pseudo_id', 'count'),
        conv_rate=('purchased', lambda x: x.mean() * 100)
    ).sort_values('conv_rate', ascending=True)
    
    plt.figure(figsize=(10, 5))
    bars = plt.barh(src_stats.index, src_stats['conv_rate'], color='#2563eb', height=0.55)
    # Highlight data deleted as tracking artifact
    for i, (src, row) in enumerate(src_stats.iterrows()):
        if src == '(data deleted)':
            bars[i].set_color('#dc2626')
            
    plt.title('Purchase Conversion Rate by Traffic Source (%)\n[Red bar indicates (data deleted) redacted/tracking category, excluded from strategy]', 
              fontsize=11, pad=12, fontweight='bold')
    plt.xlabel('Purchase Conversion Rate (%)', fontsize=11)
    
    for bar, (src, row) in zip(bars, src_stats.iterrows()):
        w = bar.get_width()
        plt.text(w + 0.15, bar.get_y() + bar.get_height()/2.0, f'{w:.2f}% (N={row["users"]:,})', 
                 va='center', ha='left', fontsize=9.5)
        
    plt.xlim(0, 10.5)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.savefig('outputs/conversion_source.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------------------------------------------------------------
    # 4. Top 10 Countries by Purchase Conversion (>500 users)
    # ------------------------------------------------------------
    c_stats = df.groupby('country').agg(
        users=('user_pseudo_id', 'count'),
        conv_rate=('purchased', lambda x: x.mean() * 100)
    )
    top_c = c_stats[c_stats['users'] >= 500].sort_values('conv_rate', ascending=False).head(10)
    
    plt.figure(figsize=(11, 5))
    bars = plt.bar(top_c.index, top_c['conv_rate'], color='#7c3aed', width=0.55)
    plt.title('Top 10 Countries by Purchase Conversion Rate (Min Volume > 500 Users)', fontsize=12, pad=12, fontweight='bold')
    plt.ylabel('Conversion Rate (%)', fontsize=11)
    plt.xticks(rotation=35, ha='right')
    
    for bar, (c, row) in zip(bars, top_c.iterrows()):
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, h + 0.1, f'{h:.2f}%\n({row["users"]:,})', 
                 ha='center', va='bottom', fontsize=8.5)
        
    plt.ylim(0, max(top_c['conv_rate']) + 1.2)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig('outputs/top_countries_conv.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------------------------------------------------------------
    # 5. Revenue by Device (Positive-Revenue Purchasers Only, N=4,066)
    # ------------------------------------------------------------
    pos_purchasers = df[(df['purchased'] == 1) & (df['total_revenue'] > 0)]
    
    plt.figure(figsize=(9, 5.5))
    box_data = [pos_purchasers[pos_purchasers['device_category'] == d]['total_revenue'] for d in ['desktop', 'mobile', 'tablet']]
    plt.boxplot(box_data, tick_labels=['Desktop (N=2,316)', 'Mobile (N=1,684)', 'Tablet (N=66)'], 
                patch_artist=True, boxprops=dict(facecolor='#93c5fd', color='#1e40af'),
                medianprops=dict(color='#b91c1c', linewidth=2), showmeans=True,
                meanprops=dict(marker='o', markeredgecolor='black', markerfacecolor='yellow'))
    
    plt.title('Revenue Distribution by Device Category (Positive-Revenue Purchasers, N=4,066)\n[Kruskal-Wallis p = 0.126; 353 zero-revenue purchasers excluded from plot]', 
              fontsize=11, pad=12, fontweight='bold')
    plt.ylabel('Total Revenue (USD)', fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig('outputs/revenue_by_device.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------------------------------------------------------------
    # 6. Behavioral Segment Distribution (N=270,154)
    # ------------------------------------------------------------
    seg_counts = df['user_segment'].value_counts()
    colors_seg = ['#94a3b8', '#38bdf8', '#fb923c', '#f87171', '#4ade80']
    
    plt.figure(figsize=(7.5, 7.5))
    wedges, texts, autotexts = plt.pie(
        seg_counts, 
        labels=seg_counts.index, 
        autopct='%1.2f%%', 
        startangle=140, 
        colors=colors_seg,
        pctdistance=0.75,
        explode=(0.02, 0.05, 0.08, 0.08, 0.1)
    )
    plt.title('User Base Behavioral Segmentation (N=270,154)', fontsize=13, pad=15, fontweight='bold')
    for autotext in autotexts:
        autotext.set_fontsize(9.5)
        autotext.set_fontweight('bold')
    plt.savefig('outputs/segment_pie.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------------------------------------------------------------
    # 7. Engagement vs Conversion (With Non-Causal Association Disclaimer)
    # ------------------------------------------------------------
    eng_conv = df.groupby('engagement_level').agg(
        users=('user_pseudo_id', 'count'),
        conv_rate=('purchased', lambda x: x.mean() * 100)
    ).reindex(['Low', 'Medium', 'High'])
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(eng_conv.index, eng_conv['conv_rate'], color=['#93c5fd', '#3b82f6', '#1d4ed8'], width=0.5)
    plt.title('Purchase Conversion by Engagement Level\n[Chi-sq p < 0.001, Cramer\'s V = 0.271 — Strong Association; Non-Causal]', 
              fontsize=11, pad=12, fontweight='bold')
    plt.xlabel('Engagement Bucket (Active Days & Session Count)', fontsize=11)
    plt.ylabel('Purchase Conversion Rate (%)', fontsize=11)
    plt.ylim(0, 30)
    
    for bar, (lvl, row) in zip(bars, eng_conv.iterrows()):
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, h + 0.8, f'{h:.2f}%\n(N={row["users"]:,})', 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig('outputs/engagement_conversion.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # ------------------------------------------------------------
    # 8. Segment Revenue Contribution
    # ------------------------------------------------------------
    seg_rev = df.groupby('user_segment')['total_revenue'].sum().sort_values()
    
    plt.figure(figsize=(9, 5))
    bars = plt.barh(seg_rev.index, seg_rev.values, color='#059669', height=0.5)
    plt.title('Total Revenue Contribution by Behavioral Segment', fontsize=12, pad=12, fontweight='bold')
    plt.xlabel('Total Revenue (USD)', fontsize=11)
    
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 3000, bar.get_y() + bar.get_height()/2.0, f'${w:,.0f}', 
                 va='center', ha='left', fontsize=10, fontweight='bold')
        
    plt.xlim(0, 420000)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.savefig('outputs/segment_revenue.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("All production visualizations successfully generated.")

if __name__ == "__main__":
    main()
