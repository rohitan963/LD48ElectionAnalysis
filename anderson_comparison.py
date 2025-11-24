import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

print("=" * 140)
print("WALEN vs. JERALEE ANDERSON: PRECINCT-BY-PRECINCT COMPARISON")
print("=" * 140)

# Define Redmond precincts
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

print(f"\nREDMOND - {len(redmond_ld48)} PRECINCTS")
print(f"{'=' * 140}\n")

print(f"{'Precinct':<15} {'Walen %':<12} {'Anderson %':<15} {'Difference':<15}")
print(f"{'-' * 140}\n")

all_diffs = []

for precinct in redmond_ld48:
    p_data = df[df['Precinct'] == precinct]
    
    # Get Walen %
    walen_votes = p_data[(p_data['Race'] == 'Legislative District No. 48 State Senator') & 
                         (p_data['CounterType'] == 'Amy Walen')]['SumOfCount'].sum()
    ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']
    ss_candidates = ss_data[ss_data['CounterType'].isin(['Vandana Slatter', 'Amy Walen', 'Write-in'])]
    total_ss = ss_candidates['SumOfCount'].sum()
    walen_pct = (walen_votes / total_ss * 100) if total_ss > 0 else 0
    
    # Get Jeralee Anderson %
    anderson_votes = p_data[(p_data['Race'] == 'City of Redmond Council Position No. 6') & 
                            (p_data['CounterType'] == 'Jeralee Anderson')]['SumOfCount'].sum()
    p6_data = p_data[p_data['Race'] == 'City of Redmond Council Position No. 6']
    p6_candidates = p6_data[p6_data['CounterType'].isin(['Menka Soni', 'Jeralee Anderson', 'Write-in'])]
    total_p6 = p6_candidates['SumOfCount'].sum()
    anderson_pct = (anderson_votes / total_p6 * 100) if total_p6 > 0 else 0
    
    diff = walen_pct - anderson_pct
    all_diffs.append(diff)
    
    print(f"{precinct:<15} {walen_pct:>10.1f}% {anderson_pct:>13.1f}% {diff:>13.1f}pp")

print(f"\n{'-' * 140}\n")
print(f"STATISTICS:")
print(f"  Average difference: {np.mean(all_diffs):+.2f}pp")
print(f"  Median difference: {np.median(all_diffs):+.2f}pp")
print(f"  Min (best for Walen): {np.min(all_diffs):+.2f}pp")
print(f"  Max (worst for Walen): {np.max(all_diffs):+.2f}pp")
print(f"  Std Dev: {np.std(all_diffs):.2f}pp")

outperforms = sum(1 for d in all_diffs if d > 0)
underperforms = sum(1 for d in all_diffs if d < 0)
print(f"\n  Walen OUTPERFORMS Anderson: {outperforms} times ({outperforms/len(all_diffs)*100:.1f}%)")
print(f"  Walen UNDERPERFORMS Anderson: {underperforms} times ({underperforms/len(all_diffs)*100:.1f}%)")

print(f"\n{'=' * 140}\n")
