import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

print("=" * 140)
print("WALEN vs. KEY CONSERVATIVE CANDIDATES: COMPREHENSIVE ANALYSIS")
print("=" * 140)

# Define precincts by city and district
bellevue_ld48 = [
    'BEL 48-0125', 'BEL 48-0126', 'BEL 48-0127', 'BEL 48-0128', 'BEL 48-0132',
    'BEL 48-0133', 'BEL 48-0134', 'BEL 48-0153', 'BEL 48-0154', 'BEL 48-0156',
    'BEL 48-0159', 'BEL 48-0160', 'BEL 48-0162', 'BEL 48-0165', 'BEL 48-0166',
    'BEL 48-0178', 'BEL 48-0179', 'BEL 48-0186', 'BEL 48-0188', 'BEL 48-0189',
    'BEL 48-0190', 'BEL 48-0191', 'BEL 48-0192', 'BEL 48-0193', 'BEL 48-0194',
    'BEL 48-0196', 'BEL 48-0198', 'BEL 48-0201', 'BEL 48-0203', 'BEL 48-0205',
    'BEL 48-0206', 'BEL 48-0211', 'BEL 48-0212', 'BEL 48-0213', 'BEL 48-0216',
    'BEL 48-0217', 'BEL 48-0218', 'BEL 48-0219', 'BEL 48-0220', 'BEL 48-0221',
    'BEL 48-0223', 'BEL 48-0224', 'BEL 48-0225', 'BEL 48-0226', 'BEL 48-0227',
    'BEL 48-2430', 'BEL 48-2432', 'BEL 48-2434', 'BEL 48-2715', 'BEL 48-2716',
    'BEL 48-2772', 'BEL 48-2773', 'BEL 48-2774', 'BEL 48-2775', 'BEL 48-2776',
    'BEL 48-2782', 'BEL 48-3140', 'BEL 48-3143', 'BEL 48-3166', 'BEL 48-3593',
    'BEL 48-3608', 'BEL 48-3658', 'BEL 48-3674', 'BEL 48-3675', 'BEL 48-3695',
    'BEL 48-3759', 'BEL 48-3761', 'BEL 48-3827', 'BEL 48-3878', 'BEL 48-4003',
    'BEL 48-4005'
]

kirkland_ld48 = [
    'KIR 48-0614', 'KIR 48-0615', 'KIR 48-0616', 'KIR 48-0628', 'KIR 48-0629',
    'KIR 48-0636', 'KIR 48-0638', 'KIR 48-0639', 'KIR 48-0641', 'KIR 48-0642',
    'KIR 48-0643', 'KIR 48-0644', 'KIR 48-0645', 'KIR 48-0646', 'KIR 48-2598',
    'KIR 48-2657', 'KIR 48-2788', 'KIR 48-2863', 'KIR 48-2914', 'KIR 48-2915',
    'KIR 48-2919', 'KIR 48-2920', 'KIR 48-2921', 'KIR 48-2922', 'KIR 48-2925',
    'KIR 48-3196', 'KIR 48-3337', 'KIR 48-3401', 'KIR 48-3439', 'KIR 48-3760',
    'KIR 48-3985'
]

redmond_ld48 = [
    'RED 48-0935', 'RED 48-0937', 'RED 48-0938', 'RED 48-0939', 'RED 48-0940',
    'RED 48-0941', 'RED 48-0942', 'RED 48-0944', 'RED 48-0945', 'RED 48-0947',
    'RED 48-0948', 'RED 48-0949', 'RED 48-0950', 'RED 48-0952', 'RED 48-0953',
    'RED 48-2449', 'RED 48-2466', 'RED 48-2467', 'RED 48-2628', 'RED 48-2629',
    'RED 48-2630', 'RED 48-2632', 'RED 48-2633', 'RED 48-2634', 'RED 48-2635',
    'RED 48-2636', 'RED 48-2640', 'RED 48-2789', 'RED 48-2790', 'RED 48-2967',
    'RED 48-2968', 'RED 48-2969', 'RED 48-3134', 'RED 48-3147', 'RED 48-3208',
    'RED 48-3316', 'RED 48-3415', 'RED 48-3475', 'RED 48-3548', 'RED 48-3664',
    'RED 48-3738', 'RED 48-3739', 'RED 48-3809', 'RED 48-3874', 'RED 48-3930',
    'RED 48-3970', 'RED 48-3979', 'RED 48-3982', 'RED 48-4007'
]

all_data = []

# BELLEVUE - Conrad Lee
print("\nBELLEVUE (Conrad Lee)")
print("-" * 140)
for precinct in bellevue_ld48:
    p_data = df[df['Precinct'] == precinct]
    
    walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                         (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
    ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
    ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
    total_ss = ss_candidates['SumOfCount'].sum()
    walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
    
    lee_votes = p_data[(p_data['Race'] == 'City of Bellevue Council Position No. 2') & 
                       (p_data['CounterType'] == 'Conrad Lee')]['SumOfCount'].sum()
    p2_data = p_data[p_data['Race'] == 'City of Bellevue Council Position No. 2']
    p2_candidates = p2_data[p2_data['CounterType'].isin(['Conrad Lee', 'Naren Briar', 'Write-in'])]
    total_p2 = p2_candidates['SumOfCount'].sum()
    lee_pct = (lee_votes / total_p2 * 100) if total_p2 > 0 else 0
    
    all_data.append({'city': 'Bellevue', 'precinct': precinct, 'walen_pct': walen_pct, 'cons_pct': lee_pct})

# KIRKLAND - Catie Malik
print("KIRKLAND (Catie Malik)")
print("-" * 140)
for precinct in kirkland_ld48:
    p_data = df[df['Precinct'] == precinct]
    
    walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                         (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
    ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
    ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
    total_ss = ss_candidates['SumOfCount'].sum()
    walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
    
    malik_votes = p_data[(p_data['Race'] == 'City of Kirkland Council Position No. 3') & 
                         (p_data['CounterType'] == 'Catie Malik')]['SumOfCount'].sum()
    p3_data = p_data[p_data['Race'] == 'City of Kirkland Council Position No. 3']
    p3_candidates = p3_data[p3_data['CounterType'].isin(['Shilpa Prem', 'Catie Malik', 'Write-in'])]
    total_p3 = p3_candidates['SumOfCount'].sum()
    malik_pct = (malik_votes / total_p3 * 100) if total_p3 > 0 else 0
    
    all_data.append({'city': 'Kirkland', 'precinct': precinct, 'walen_pct': walen_pct, 'cons_pct': malik_pct})

# REDMOND - Steve Fields
print("REDMOND (Steve Fields)")
print("-" * 140)
for precinct in redmond_ld48:
    p_data = df[df['Precinct'] == precinct]
    
    walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                         (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
    ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
    ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
    total_ss = ss_candidates['SumOfCount'].sum()
    walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
    
    fields_votes = p_data[(p_data['Race'] == 'City of Redmond Council Position No. 2') & 
                          (p_data['CounterType'] == 'Steve Fields')]['SumOfCount'].sum()
    p2_data = p_data[p_data['Race'] == 'City of Redmond Council Position No. 2']
    p2_candidates = p2_data[p2_data['CounterType'].isin(['Vivek Prakriya', 'Steve Fields', 'Write-in'])]
    total_p2 = p2_candidates['SumOfCount'].sum()
    fields_pct = (fields_votes / total_p2 * 100) if total_p2 > 0 else 0
    
    all_data.append({'city': 'Redmond', 'precinct': precinct, 'walen_pct': walen_pct, 'cons_pct': fields_pct})

df_data = pd.DataFrame(all_data)

# Print summary statistics
print("\n" + "=" * 140)
print("SUMMARY STATISTICS BY CITY")
print("=" * 140 + "\n")

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    city_data = df_data[df_data['city'] == city]
    corr, p_val = pearsonr(city_data['walen_pct'], city_data['cons_pct'])
    avg_diff = (city_data['walen_pct'] - city_data['cons_pct']).mean()
    
    print(f"{city}:")
    print(f"  Precincts: {len(city_data)}")
    print(f"  Walen avg: {city_data['walen_pct'].mean():.1f}%")
    print(f"  Conservative avg: {city_data['cons_pct'].mean():.1f}%")
    print(f"  Average difference: {avg_diff:+.1f}pp (Walen vs. conservative)")
    print(f"  Correlation: r = {corr:.3f}")
    print()

# Create scatter plot
fig, ax = plt.subplots(figsize=(12, 8))

colors = {'Bellevue': '#1f77b4', 'Kirkland': '#ff7f0e', 'Redmond': '#2ca02c'}
labels = {'Bellevue': 'Bellevue (Conrad Lee)', 'Kirkland': 'Kirkland (Catie Malik)', 'Redmond': 'Redmond (Steve Fields)'}

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    city_data = df_data[df_data['city'] == city]
    ax.scatter(city_data['cons_pct'], city_data['walen_pct'], 
              color=colors[city], s=100, alpha=0.6, label=labels[city], edgecolors='black', linewidth=0.5)

# Add 45-degree reference line (where they tie)
min_val = min(df_data['walen_pct'].min(), df_data['cons_pct'].min())
max_val = max(df_data['walen_pct'].max(), df_data['cons_pct'].max())
ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.3, linewidth=1.5, label='Equal performance')

# Add labels and formatting
ax.set_xlabel('Conservative Candidate %', fontsize=12, fontweight='bold')
ax.set_ylabel('Amy Walen %', fontsize=12, fontweight='bold')
ax.set_title('Amy Walen vs. Key Conservative Candidates by Precinct\nBellevue (Conrad Lee), Kirkland (Catie Malik), Redmond (Steve Fields)', 
            fontsize=14, fontweight='bold', pad=20)

ax.grid(True, alpha=0.3)
ax.legend(loc='best', fontsize=11, framealpha=0.9)
ax.set_xlim([10, 75])
ax.set_ylim([10, 75])

# Add reference zones
ax.axhspan(10, 45, alpha=0.05, color='red', label='_nolegend_')
ax.axvspan(45, 75, alpha=0.05, color='blue', label='_nolegend_')

plt.tight_layout()
plt.savefig('walen_vs_conservatives_scatter.png', dpi=300, bbox_inches='tight')
print("=" * 140)
print("Scatter plot saved as: walen_vs_conservatives_scatter.png")
print("=" * 140)
plt.show()
