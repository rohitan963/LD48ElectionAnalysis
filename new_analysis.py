# New LD48 Election Analysis
# Created: December 27, 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import json
import base64
from openai import OpenAI
import os

# Read both mid-election and final results
df_mid = pd.read_csv('Mid-Election-results-report.csv')
df_final = pd.read_csv('final-precinct-results.csv')

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

def get_candidate_pct(df, precinct, race, candidate, all_candidates):
    """Helper function to get candidate percentage"""
    p_data = df[df['Precinct'] == precinct]
    cand_votes = p_data[(p_data['Race'] == race) & 
                        (p_data['CounterType'] == candidate)]['SumOfCount'].sum()
    race_data = p_data[p_data['Race'] == race]
    race_candidates = race_data[race_data['CounterType'].isin(all_candidates)]
    total = race_candidates['SumOfCount'].sum()
    return (cand_votes / total * 100) if total > 0 else 0

# BELLEVUE - Conrad Lee
print("\nBELLEVUE (Conrad Lee)")
print("-" * 140)
for precinct in bellevue_ld48:
    # Mid-election results
    walen_mid = get_candidate_pct(df_mid, precinct, 'Legislative District No. 48 State Senator', 
                                   'Amy Walen', ['Vandana Slatter', 'Amy Walen', 'Write-in'])
    lee_mid = get_candidate_pct(df_mid, precinct, 'City of Bellevue Council Position No. 2',
                                 'Conrad Lee', ['Conrad Lee', 'Naren Briar', 'Write-in'])
    
    # Final results
    walen_final = get_candidate_pct(df_final, precinct, 'Legislative District No. 48 State Senator',
                                     'Amy Walen', ['Vandana Slatter', 'Amy Walen', 'Write-in'])
    lee_final = get_candidate_pct(df_final, precinct, 'City of Bellevue Council Position No. 2',
                                   'Conrad Lee', ['Conrad Lee', 'Naren Briar', 'Write-in'])
    
    all_data.append({
        'city': 'Bellevue',
        'precinct': precinct,
        'conservative_candidate': 'Conrad Lee',
        'walen_mid': walen_mid,
        'walen_final': walen_final,
        'walen_change': walen_final - walen_mid,
        'cons_mid': lee_mid,
        'cons_final': lee_final,
        'cons_change': lee_final - lee_mid
    })

# KIRKLAND - Catie Malik
print("KIRKLAND (Catie Malik)")
print("-" * 140)
for precinct in kirkland_ld48:
    # Mid-election results
    walen_mid = get_candidate_pct(df_mid, precinct, 'Legislative District No. 48 State Senator',
                                   'Amy Walen', ['Vandana Slatter', 'Amy Walen', 'Write-in'])
    malik_mid = get_candidate_pct(df_mid, precinct, 'City of Kirkland Council Position No. 3',
                                   'Catie Malik', ['Shilpa Prem', 'Catie Malik', 'Write-in'])
    
    # Final results
    walen_final = get_candidate_pct(df_final, precinct, 'Legislative District No. 48 State Senator',
                                     'Amy Walen', ['Vandana Slatter', 'Amy Walen', 'Write-in'])
    malik_final = get_candidate_pct(df_final, precinct, 'City of Kirkland Council Position No. 3',
                                     'Catie Malik', ['Shilpa Prem', 'Catie Malik', 'Write-in'])
    
    all_data.append({
        'city': 'Kirkland',
        'precinct': precinct,
        'conservative_candidate': 'Catie Malik',
        'walen_mid': walen_mid,
        'walen_final': walen_final,
        'walen_change': walen_final - walen_mid,
        'cons_mid': malik_mid,
        'cons_final': malik_final,
        'cons_change': malik_final - malik_mid
    })

# REDMOND - Steve Fields
print("REDMOND (Steve Fields)")
print("-" * 140)
for precinct in redmond_ld48:
    # Mid-election results
    walen_mid = get_candidate_pct(df_mid, precinct, 'Legislative District No. 48 State Senator',
                                   'Amy Walen', ['Vandana Slatter', 'Amy Walen', 'Write-in'])
    fields_mid = get_candidate_pct(df_mid, precinct, 'City of Redmond Council Position No. 2',
                                    'Steve Fields', ['Vivek Prakriya', 'Steve Fields', 'Write-in'])
    
    # Final results
    walen_final = get_candidate_pct(df_final, precinct, 'Legislative District No. 48 State Senator',
                                     'Amy Walen', ['Vandana Slatter', 'Amy Walen', 'Write-in'])
    fields_final = get_candidate_pct(df_final, precinct, 'City of Redmond Council Position No. 2',
                                      'Steve Fields', ['Vivek Prakriya', 'Steve Fields', 'Write-in'])
    
    all_data.append({
        'city': 'Redmond',
        'precinct': precinct,
        'conservative_candidate': 'Steve Fields',
        'walen_mid': walen_mid,
        'walen_final': walen_final,
        'walen_change': walen_final - walen_mid,
        'cons_mid': fields_mid,
        'cons_final': fields_final,
        'cons_change': fields_final - fields_mid
    })

df_data = pd.DataFrame(all_data)

# Save to JSON
output_data = {
    'metadata': {
        'description': 'Mid-election vs Final election results comparison for LD48 precincts',
        'date_generated': '2025-12-27',
        'data_sources': ['Mid-Election-results-report.csv', 'final-precinct-results.csv']
    },
    'precincts': all_data
}

with open('mid_vs_final_comparison.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("\n" + "=" * 140)
print("JSON FILE SAVED: mid_vs_final_comparison.json")
print("=" * 140)

# Print summary statistics
print("\n" + "=" * 140)
print("SUMMARY STATISTICS BY CITY - CHANGES FROM MID-ELECTION TO FINAL")
print("=" * 140 + "\n")

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    city_data = df_data[df_data['city'] == city]
    
    print(f"{city} ({city_data.iloc[0]['conservative_candidate']}):")
    print(f"  Precincts: {len(city_data)}")
    print(f"  Walen avg change: {city_data['walen_change'].mean():+.2f}pp")
    print(f"  Conservative avg change: {city_data['cons_change'].mean():+.2f}pp")
    print(f"  Walen final avg: {city_data['walen_final'].mean():.1f}%")
    print(f"  Conservative final avg: {city_data['cons_final'].mean():.1f}%")
    
    # Correlation between changes
    if len(city_data) > 2:
        corr, _ = pearsonr(city_data['walen_change'], city_data['cons_change'])
        print(f"  Correlation of changes: r = {corr:.3f}")
    print()

# Create scatter plot comparing final results
fig, ax = plt.subplots(figsize=(12, 8))

colors = {'Bellevue': '#1f77b4', 'Kirkland': '#ff7f0e', 'Redmond': '#2ca02c'}
labels = {'Bellevue': 'Bellevue (Conrad Lee)', 'Kirkland': 'Kirkland (Catie Malik)', 'Redmond': 'Redmond (Steve Fields)'}

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    city_data = df_data[df_data['city'] == city]
    ax.scatter(city_data['cons_final'], city_data['walen_final'], 
              color=colors[city], s=100, alpha=0.6, label=labels[city], edgecolors='black', linewidth=0.5)

# Add 45-degree reference line (where they tie)
min_val = min(df_data['walen_final'].min(), df_data['cons_final'].min())
max_val = max(df_data['walen_final'].max(), df_data['cons_final'].max())
ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.3, linewidth=1.5, label='Equal performance')

# Add labels and formatting
ax.set_xlabel('Conservative Candidate % (Final)', fontsize=12, fontweight='bold')
ax.set_ylabel('Amy Walen % (Final)', fontsize=12, fontweight='bold')
ax.set_title('Amy Walen vs. Key Conservative Candidates by Precinct - FINAL RESULTS\nBellevue (Conrad Lee), Kirkland (Catie Malik), Redmond (Steve Fields)', 
            fontsize=14, fontweight='bold', pad=20)

ax.grid(True, alpha=0.3)
ax.legend(loc='best', fontsize=11, framealpha=0.9)
ax.set_xlim([10, 75])
ax.set_ylim([10, 75])

# Add reference zones
ax.axhspan(10, 45, alpha=0.05, color='red', label='_nolegend_')
ax.axvspan(45, 75, alpha=0.05, color='blue', label='_nolegend_')

plt.tight_layout()
plt.savefig('walen_vs_conservatives_scatter_final.png', dpi=300, bbox_inches='tight')
print("=" * 140)
print("Scatter plot saved as: walen_vs_conservatives_scatter_final.png")
print("=" * 140)

# OpenAI Vision Analysis for Campaign Memo
print("\n" + "=" * 140)
print("GENERATING AI ANALYSIS FOR CAMPAIGN MEMO...")
print("=" * 140)

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

try:
    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Encode the chart image
    base64_image = encode_image('walen_vs_conservatives_scatter_final.png')
    
    # Create the prompt for a campaign memo
    prompt = """You are a political analyst reviewing election data for a campaign memo. 
    
Analyze this scatter plot comparing Amy Walen's performance against key conservative candidates 
(Conrad Lee in Bellevue, Catie Malik in Kirkland, Steve Fields in Redmond) across LD48 precincts.

Write a strategic memo for Amy Walen's PRIMARY OPPONENT (a Democratic challenger). Focus on:

1. VULNERABILITY ANALYSIS: Where does Walen underperform? What patterns suggest weakness?
2. CONSERVATIVE CROSSOVER: How does her alignment with conservative candidates reveal positioning issues?
3. GEOGRAPHIC WEAKNESSES: Which cities/areas show the most vulnerability?
4. STRATEGIC RECOMMENDATIONS: How should a primary challenger exploit these patterns?

Be direct, data-driven, and strategic. This is internal campaign strategy, not public messaging."""

    # Call OpenAI Vision API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=2000
    )
    
    # Get the analysis
    analysis = response.choices[0].message.content
    
    # Print the analysis
    print("\n" + "=" * 140)
    print("CAMPAIGN MEMO: STRATEGIC ANALYSIS FOR PRIMARY CHALLENGE")
    print("=" * 140 + "\n")
    print(analysis)
    print("\n" + "=" * 140)
    
    # Save to file
    with open('walen_vulnerability_memo.txt', 'w') as f:
        f.write("CAMPAIGN MEMO: STRATEGIC ANALYSIS FOR PRIMARY CHALLENGE AGAINST AMY WALEN\n")
        f.write("=" * 100 + "\n\n")
        f.write(analysis)
    
    print("\nMemo saved to: walen_vulnerability_memo.txt")
    print("=" * 140)
    
except Exception as e:
    print(f"\nError generating OpenAI analysis: {e}")
    print("Make sure OPENAI_API_KEY environment variable is set.")
    print("=" * 140)

plt.show()
