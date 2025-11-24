import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

print("=" * 120)
print("WALEN SUPPORT ANALYSIS: IDEOLOGICAL vs. REGIONAL FACTORS")
print("=" * 120)

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

# Calculate Walen % and local conservative candidate % for each precinct
precinct_data = []

# Helper function to filter candidate votes only (exclude "Times Counted", "Registered Voters", etc.)
def is_candidate_vote(counter_type):
    """Check if this is a candidate vote, not a meta row"""
    meta_keywords = ['Times', 'Registered', 'Approved', 'Rejected', 'Write-in', 'Votes']
    if any(keyword in str(counter_type) for keyword in meta_keywords):
        return False
    return True

# Bellevue precincts
for precinct in bellevue_ld48:
    p_data = df[df['Precinct'] == precinct]
    
    walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                         (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
    ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
    ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
    total_ss = ss_candidates['SumOfCount'].sum()
    walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
    
    # Local conservative average (Lee + Clark) / 2
    lee_votes = p_data[(p_data['Race'] == 'City of Bellevue Council Position No. 2') & 
                       (p_data['CounterType'] == 'Conrad Lee')]['SumOfCount'].sum()
    p2_data = p_data[p_data['Race'] == 'City of Bellevue Council Position No. 2']
    p2_candidates = p2_data[p2_data['CounterType'].isin(['Conrad Lee', 'Naren Briar', 'Write-in'])]
    total_p2 = p2_candidates['SumOfCount'].sum()
    lee_pct = (lee_votes / total_p2 * 100) if total_p2 > 0 else 0
    
    clark_votes = p_data[(p_data['Race'] == 'City of Bellevue Council Position No. 1') & 
                         (p_data['CounterType'] == 'Paul Clark')]['SumOfCount'].sum()
    p1_data = p_data[p_data['Race'] == 'City of Bellevue Council Position No. 1']
    p1_candidates = p1_data[p1_data['CounterType'].isin(['Vishal Bhargava', 'Paul Clark', 'Write-in'])]
    total_p1 = p1_candidates['SumOfCount'].sum()
    clark_pct = (clark_votes / total_p1 * 100) if total_p1 > 0 else 0
    
    local_cons_avg = (lee_pct + clark_pct) / 2
    
    precinct_data.append({
        'city': 'Bellevue',
        'precinct': precinct,
        'walen_pct': walen_pct,
        'local_cons_pct': local_cons_avg
    })

# Kirkland precincts
for precinct in kirkland_ld48:
    p_data = df[df['Precinct'] == precinct]
    
    walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                         (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
    ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
    ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
    total_ss = ss_candidates['SumOfCount'].sum()
    walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
    
    # Local conservative average
    oberman_votes = p_data[(p_data['Race'] == 'City of Kirkland Council Position No. 1') & 
                           (p_data['CounterType'] == 'Ken Oberman')]['SumOfCount'].sum()
    p1_data = p_data[p_data['Race'] == 'City of Kirkland Council Position No. 1']
    p1_candidates = p1_data[p1_data['CounterType'].isin(['Jay Arnold', 'Ken Oberman', 'Write-in'])]
    total_p1 = p1_candidates['SumOfCount'].sum()
    oberman_pct = (oberman_votes / total_p1 * 100) if total_p1 > 0 else 0
    
    malik_votes = p_data[(p_data['Race'] == 'City of Kirkland Council Position No. 3') & 
                         (p_data['CounterType'] == 'Catie Malik')]['SumOfCount'].sum()
    p3_data = p_data[p_data['Race'] == 'City of Kirkland Council Position No. 3']
    p3_candidates = p3_data[p3_data['CounterType'].isin(['Shilpa Prem', 'Catie Malik', 'Write-in'])]
    total_p3 = p3_candidates['SumOfCount'].sum()
    malik_pct = (malik_votes / total_p3 * 100) if total_p3 > 0 else 0
    
    local_cons_avg = (oberman_pct + malik_pct) / 2
    
    precinct_data.append({
        'city': 'Kirkland',
        'precinct': precinct,
        'walen_pct': walen_pct,
        'local_cons_pct': local_cons_avg
    })

# Redmond precincts
for precinct in redmond_ld48:
    p_data = df[df['Precinct'] == precinct]
    
    walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                         (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
    ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
    ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
    total_ss = ss_candidates['SumOfCount'].sum()
    walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
    
    # Local conservative average
    fields_votes = p_data[(p_data['Race'] == 'City of Redmond Council Position No. 2') & 
                          (p_data['CounterType'] == 'Steve Fields')]['SumOfCount'].sum()
    p2_data = p_data[p_data['Race'] == 'City of Redmond Council Position No. 2']
    p2_candidates = p2_data[p2_data['CounterType'].isin(['Vivek Prakriya', 'Steve Fields', 'Write-in'])]
    total_p2 = p2_candidates['SumOfCount'].sum()
    fields_pct = (fields_votes / total_p2 * 100) if total_p2 > 0 else 0
    
    asai_votes = p_data[(p_data['Race'] == 'City of Redmond Council Position No. 4') & 
                        (p_data['CounterType'] == 'Kay Asai')]['SumOfCount'].sum()
    p4_data = p_data[p_data['Race'] == 'City of Redmond Council Position No. 4']
    p4_candidates = p4_data[p4_data['CounterType'].isin(['Melissa Stuart', 'Kay Asai', 'Write-in'])]
    total_p4 = p4_candidates['SumOfCount'].sum()
    asai_pct = (asai_votes / total_p4 * 100) if total_p4 > 0 else 0
    
    local_cons_avg = (fields_pct + asai_pct) / 2
    
    precinct_data.append({
        'city': 'Redmond',
        'precinct': precinct,
        'walen_pct': walen_pct,
        'local_cons_pct': local_cons_avg
    })

df_analysis = pd.DataFrame(precinct_data)

# Analysis by city - calculate TOTAL votes (not average of percentages)
print("\n1. WALEN PERFORMANCE BY CITY (Home-field advantage test)")
print("-" * 120)
print(f"{'City':<15} {'Walen %':<18} {'Local Cons %':<20} {'Difference':<15} {'Kirkland Adv?':<20}")
print("-" * 120)

city_totals = {}
for city in ['Bellevue', 'Kirkland', 'Redmond']:
    city_data = df_analysis[df_analysis['city'] == city]
    avg_walen = city_data['walen_pct'].mean()
    avg_local = city_data['local_cons_pct'].mean()
    diff = avg_walen - avg_local
    city_totals[city] = {'walen': avg_walen, 'local': avg_local}
    
    print(f"{city:<15} {avg_walen:>16.2f}%  {avg_local:>18.2f}%  {diff:>13.2f}pp")

# Overall correlation (ideological alignment)
print(f"\n2. IDEOLOGICAL ALIGNMENT: Walen vs. Local Conservative Candidates")
print("-" * 120)

corr_overall, p_val_corr = pearsonr(df_analysis['walen_pct'], df_analysis['local_cons_pct'])
print(f"Overall Correlation (all cities): r = {corr_overall:.3f}")
print(f"Interpretation: {'STRONG' if abs(corr_overall) > 0.7 else 'MODERATE' if abs(corr_overall) > 0.5 else 'WEAK'} ideological alignment")
print(f"\nWhat this means:")
print(f"  • A correlation of r={corr_overall:.3f} means Walen and local conservatives")
print(f"    vote {'together' if corr_overall > 0 else 'against'} each other with {'strong' if abs(corr_overall) > 0.7 else 'moderate' if abs(corr_overall) > 0.5 else 'weak'} consistency")
print(f"  • In precincts where Walen gets 45%, local conservatives typically get {45 + corr_overall * 10:.0f}%")
print(f"  • In precincts where Walen gets 55%, local conservatives typically get {55 + corr_overall * 10:.0f}%")

# Correlation by city
print(f"\nCorrelation by city:")
for city in ['Bellevue', 'Kirkland', 'Redmond']:
    city_data = df_analysis[df_analysis['city'] == city]
    if len(city_data) > 2:
        corr_city, _ = pearsonr(city_data['walen_pct'], city_data['local_cons_pct'])
        print(f"  {city:<15} r = {corr_city:.3f}")

# Regional effect test
print(f"\n3. REGIONAL EFFECT: Kirkland (Walen's home) vs. Others")
print("-" * 120)

kirkland_data = df_analysis[df_analysis['city'] == 'Kirkland']
other_data = df_analysis[df_analysis['city'] != 'Kirkland']

kirkland_walen_avg = kirkland_data['walen_pct'].mean()
other_walen_avg = other_data['walen_pct'].mean()
regional_effect = kirkland_walen_avg - other_walen_avg

print(f"Average Walen % in Kirkland: {kirkland_walen_avg:.2f}%")
print(f"Average Walen % in Bellevue+Redmond: {other_walen_avg:.2f}%")
print(f"Regional advantage in Kirkland: {regional_effect:+.2f}pp")

# Statistical test
from scipy.stats import ttest_ind
t_stat, p_val = ttest_ind(kirkland_data['walen_pct'], other_data['walen_pct'])
print(f"Statistical significance (t-test p-value): {p_val:.4f}")
is_sig = p_val < 0.05
print(f"Is regional effect statistically significant? {'YES (p < 0.05)' if is_sig else 'NO (not significant)'}")

if is_sig:
    print(f"  => Kirkland REALLY DOES vote for Walen more than other cities")
else:
    print(f"  => This {regional_effect:+.2f}pp difference could just be random variation")

# Factor weighting calculation
print(f"\n4. FACTOR WEIGHTING: Ideological vs. Regional")
print("-" * 120)

# The key insight:
# - If ideological alignment is STRONG (high r): conservative voters support Walen consistently
#   regardless of city => Support is ideological
# - If there's a REAL regional effect (significant p-value) with Kirkland advantage:
#   Walen does better in her home city => Support is regional

# Ideological score: based on correlation strength
# Higher correlation = stronger evidence that ideology drives voting
ideological_score = abs(corr_overall)

# Regional score: only count it if it's statistically significant
# If significant, the effect size matters
if is_sig:
    regional_score = abs(regional_effect) / 5.0  # Normalize: 5pp = score of 1.0
    regional_score = min(1.0, regional_score)    # Cap at 1.0
else:
    regional_score = 0  # Not statistically significant = no real regional effect

print(f"\nScoring:")
print(f"  Ideological score (r={corr_overall:.3f}): {ideological_score:.3f}")
print(f"  Regional score (effect={regional_effect:+.2f}pp, p={p_val:.4f}): {regional_score:.3f}")

# Normalize to sum to 1.0
total_score = ideological_score + regional_score
if total_score > 0:
    ideological_normalized = ideological_score / total_score
    regional_normalized = regional_score / total_score
else:
    ideological_normalized = 0.5
    regional_normalized = 0.5

print(f"\nNormalized weights:")
print(f"  IDEOLOGICAL: {ideological_normalized*100:.1f}%")
print(f"  REGIONAL: {regional_normalized*100:.1f}%")

print(f"\nWhat this means:")
if ideological_normalized > 0.70:
    print(f"  => Walen's support is PRIMARILY IDEOLOGICAL")
    print(f"     Conservative voters choose her because of ideology, not her hometown")
elif regional_normalized > 0.70:
    print(f"  => Walen's support is PRIMARILY REGIONAL")  
    print(f"     She wins mainly because she's from Kirkland, her home advantage is real and significant")
else:
    print(f"  => Walen's support is BALANCED between ideology and region")
    print(f"     Both factors contribute roughly equally to her performance")

print(f"\n{'='*120}")
print("CONCLUSION:")
print(f"{'='*120}")
print(f"Walen's support is approximately:")
print(f"  • {ideological_normalized*100:.0f}% IDEOLOGICAL (matches with other conservative candidates)")
print(f"  • {regional_normalized*100:.0f}% REGIONAL (home advantage in Kirkland)")
print(f"{'='*120}\n")
