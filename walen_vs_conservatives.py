import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

print("=" * 140)
print("WALEN vs. CONSERVATIVE CANDIDATES: PRECINCT-BY-PRECINCT COMPARISON")
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

all_precincts = {
    'Bellevue': bellevue_ld48,
    'Kirkland': kirkland_ld48,
    'Redmond': redmond_ld48
}

# Define conservative candidates by city
conservative_by_city = {
    'Bellevue': {
        'Paul Clark': 'City of Bellevue Council Position No. 1',
        'Conrad Lee': 'City of Bellevue Council Position No. 2',
    },
    'Kirkland': {
        'Ken Oberman': 'City of Kirkland Council Position No. 1',
        'Catie Malik': 'City of Kirkland Council Position No. 3',
    },
    'Redmond': {
        'Steve Fields': 'City of Redmond Council Position No. 2',
        'Kay Asai': 'City of Redmond Council Position No. 4',
    }
}

# Collect all comparisons
all_comparisons = []

for city, precincts in all_precincts.items():
    print(f"\n{'=' * 140}")
    print(f"{city.upper()} - {len(precincts)} PRECINCTS")
    print(f"{'=' * 140}")
    
    for precinct in precincts:
        p_data = df[df['Precinct'] == precinct]
        
        # Get Walen %
        walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                             (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
        ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
        ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
        total_ss = ss_candidates['SumOfCount'].sum()
        walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
        
        # Get each conservative candidate's %
        for candidate_name, race_name in conservative_by_city[city].items():
            cand_votes = p_data[(p_data['Race'] == race_name) & 
                               (p_data['CounterType'] == candidate_name)]['SumOfCount'].sum()
            race_data = p_data[p_data['Race'] == race_name]
            
            # Filter for candidates only
            if 'Position No. 1' in race_name and city == 'Bellevue':
                race_candidates = race_data[race_data['CounterType'].isin(['Vishal Bhargava', 'Paul Clark', 'Write-in'])]
            elif 'Position No. 2' in race_name and city == 'Bellevue':
                race_candidates = race_data[race_data['CounterType'].isin(['Conrad Lee', 'Naren Briar', 'Write-in'])]
            elif 'Position No. 1' in race_name and city == 'Kirkland':
                race_candidates = race_data[race_data['CounterType'].isin(['Jay Arnold', 'Ken Oberman', 'Write-in'])]
            elif 'Position No. 3' in race_name and city == 'Kirkland':
                race_candidates = race_data[race_data['CounterType'].isin(['Shilpa Prem', 'Catie Malik', 'Write-in'])]
            elif 'Position No. 2' in race_name and city == 'Redmond':
                race_candidates = race_data[race_data['CounterType'].isin(['Vivek Prakriya', 'Steve Fields', 'Write-in'])]
            elif 'Position No. 4' in race_name and city == 'Redmond':
                race_candidates = race_data[race_data['CounterType'].isin(['Melissa Stuart', 'Kay Asai', 'Write-in'])]
            
            total_race = race_candidates['SumOfCount'].sum()
            cand_pct = (cand_votes / total_race * 100) if total_race > 0 else 0
            
            diff = walen_pct - cand_pct
            
            all_comparisons.append({
                'city': city,
                'precinct': precinct,
                'candidate': candidate_name,
                'walen_pct': walen_pct,
                'cand_pct': cand_pct,
                'diff': diff
            })

# Print detailed comparison table
print(f"\n\n{'=' * 140}")
print("DETAILED PRECINCT-BY-PRECINCT COMPARISON")
print(f"{'=' * 140}\n")

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    city_data = [c for c in all_comparisons if c['city'] == city]
    
    print(f"\n{city.upper()}")
    print(f"{'-' * 140}")
    print(f"{'Precinct':<15} {'Conservative':<20} {'Walen %':<12} {'Cons %':<12} {'Difference':<12}")
    print(f"{'-' * 140}")
    
    for row in city_data:
        print(f"{row['precinct']:<15} {row['candidate']:<20} {row['walen_pct']:>10.1f}% {row['cand_pct']:>10.1f}% {row['diff']:>10.1f}pp")

# Calculate aggregate statistics
print(f"\n\n{'=' * 140}")
print("AGGREGATE STATISTICS BY CANDIDATE")
print(f"{'=' * 140}\n")

candidates = {}
for comparison in all_comparisons:
    key = (comparison['city'], comparison['candidate'])
    if key not in candidates:
        candidates[key] = []
    candidates[key].append(comparison['diff'])

print(f"{'City':<15} {'Conservative Candidate':<25} {'# Precincts':<15} {'Avg Diff':<15} {'Min':<12} {'Max':<12} {'StDev':<12}")
print(f"{'-' * 140}")

for (city, candidate), diffs in sorted(candidates.items()):
    avg_diff = np.mean(diffs)
    min_diff = np.min(diffs)
    max_diff = np.max(diffs)
    std_diff = np.std(diffs)
    
    print(f"{city:<15} {candidate:<25} {len(diffs):<15} {avg_diff:>13.2f}pp {min_diff:>10.2f}pp {max_diff:>10.2f}pp {std_diff:>10.2f}pp")

# Overall summary
print(f"\n\n{'=' * 140}")
print("OVERALL SUMMARY")
print(f"{'=' * 140}\n")

all_diffs = [c['diff'] for c in all_comparisons]
print(f"Across all {len(all_comparisons)} candidate comparisons:")
print(f"  Walen averages {np.mean(all_diffs):+.2f}pp vs. conservative candidates")
print(f"  Range: {np.min(all_diffs):+.2f}pp to {np.max(all_diffs):+.2f}pp")
print(f"  Standard deviation: {np.std(all_diffs):.2f}pp")

# How often does Walen underperform?
underperforms = sum(1 for d in all_diffs if d < 0)
outperforms = sum(1 for d in all_diffs if d > 0)
print(f"\n  Walen UNDERPERFORMS conservative candidates: {underperforms} times ({underperforms/len(all_diffs)*100:.1f}%)")
print(f"  Walen OUTPERFORMS conservative candidates: {outperforms} times ({outperforms/len(all_diffs)*100:.1f}%)")

print(f"\n{'=' * 140}\n")
