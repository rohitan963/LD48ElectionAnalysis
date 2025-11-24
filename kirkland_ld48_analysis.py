import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

# Define Kirkland LD 48 precincts
kirkland_ld48_precincts = [
    'KIR 48-0614', 'KIR 48-0615', 'KIR 48-0616', 'KIR 48-0628', 'KIR 48-0629',
    'KIR 48-0636', 'KIR 48-0638', 'KIR 48-0639', 'KIR 48-0641', 'KIR 48-0642',
    'KIR 48-0643', 'KIR 48-0644', 'KIR 48-0645', 'KIR 48-0646', 'KIR 48-2598',
    'KIR 48-2657', 'KIR 48-2788', 'KIR 48-2863', 'KIR 48-2914', 'KIR 48-2915',
    'KIR 48-2919', 'KIR 48-2920', 'KIR 48-2921', 'KIR 48-2922', 'KIR 48-2925',
    'KIR 48-3196', 'KIR 48-3337', 'KIR 48-3401', 'KIR 48-3439', 'KIR 48-3760',
    'KIR 48-3985'
]

print("=" * 100)
print("KIRKLAND - LD 48 PRECINCT ANALYSIS")
print("=" * 100)
print(f"\nTotal Kirkland precincts in LD 48: {len(kirkland_ld48_precincts)}")

# Filter data for Kirkland LD 48
kirkland_data = df[df['Precinct'].isin(kirkland_ld48_precincts)].copy()

# Define races and candidates
races = {
    'State Senator': 'Legislative District No. 48 State Senator',
    'Council Pos. 1': 'City of Kirkland Council Position No. 1',
    'Council Pos. 3': 'City of Kirkland Council Position No. 3',
    'Council Pos. 5': 'City of Kirkland Council Position No. 5',
    'Council Pos. 7': 'City of Kirkland Council Position No. 7'
}

# Progressive vs Conservative
candidates = {
    'State Senator': {'progressive': 'Vandana Slatter', 'conservative': 'Amy Walen'},
    'Council Pos. 1': {'progressive': 'Jay Arnold', 'conservative': 'Ken Oberman'},
    'Council Pos. 3': {'progressive': 'Shilpa Prem', 'conservative': 'Catie Malik'},
    'Council Pos. 5': {'progressive': 'Neal Black', 'conservative': 'Ken MacKenzie'},
    'Council Pos. 7': {'progressive': 'Kurt Dresner', 'conservative': 'Jon Pascal'}
}

# Build precinct results
precinct_results = {}
for precinct in sorted(kirkland_ld48_precincts):
    precinct_results[precinct] = {}
    precinct_data = kirkland_data[kirkland_data['Precinct'] == precinct]
    
    for race_name, race_query in races.items():
        race_data = precinct_data[precinct_data['Race'] == race_query]
        prog_votes = race_data[race_data['CounterType'] == candidates[race_name]['progressive']]['SumOfCount'].sum()
        cons_votes = race_data[race_data['CounterType'] == candidates[race_name]['conservative']]['SumOfCount'].sum()
        total = prog_votes + cons_votes
        
        if total > 0:
            precinct_results[precinct][race_name] = {
                'prog': prog_votes,
                'cons': cons_votes,
                'total': total,
                'cons_pct': cons_votes / total * 100
            }

# Display precinct-by-precinct results
print(f"\n{'Precinct':<18} {'Walen %':<12} {'Oberman %':<14} {'Malik %':<12} {'MacKenzie %':<15} {'Pascal %':<12}")
print("-" * 100)

walen_pcts = []
oberman_pcts = []
malik_pcts = []
mackenzie_pcts = []
pascal_pcts = []

for precinct in sorted(precinct_results.keys()):
    result = precinct_results[precinct]
    if all(r in result for r in ['State Senator', 'Council Pos. 1', 'Council Pos. 3', 'Council Pos. 5', 'Council Pos. 7']):
        walen = result['State Senator']['cons_pct']
        oberman = result['Council Pos. 1']['cons_pct']
        malik = result['Council Pos. 3']['cons_pct']
        mackenzie = result['Council Pos. 5']['cons_pct']
        pascal = result['Council Pos. 7']['cons_pct']
        
        walen_pcts.append(walen)
        oberman_pcts.append(oberman)
        malik_pcts.append(malik)
        mackenzie_pcts.append(mackenzie)
        pascal_pcts.append(pascal)
        
        print(f"{precinct:<18} {walen:>10.1f}%  {oberman:>12.1f}%  {malik:>10.1f}%  {mackenzie:>13.1f}%  {pascal:>10.1f}%")

# Statistics
print("-" * 100)
print(f"{'MEAN':<18} {np.mean(walen_pcts):>10.1f}%  {np.mean(oberman_pcts):>12.1f}%  {np.mean(malik_pcts):>10.1f}%  {np.mean(mackenzie_pcts):>13.1f}%  {np.mean(pascal_pcts):>10.1f}%")
print(f"{'STDEV':<18} {np.std(walen_pcts):>10.1f}  {np.std(oberman_pcts):>12.1f}  {np.std(malik_pcts):>10.1f}  {np.std(mackenzie_pcts):>13.1f}  {np.std(pascal_pcts):>10.1f}")

# Correlation analysis
print("\n" + "=" * 100)
print("CORRELATION ANALYSIS: Conservative Candidate Performance")
print("=" * 100)

corr_walen_oberman, p_wo = pearsonr(walen_pcts, oberman_pcts)
corr_walen_malik, p_wm = pearsonr(walen_pcts, malik_pcts)
corr_walen_mackenzie, p_wma = pearsonr(walen_pcts, mackenzie_pcts)
corr_walen_pascal, p_wp = pearsonr(walen_pcts, pascal_pcts)

print(f"\nWalen (State Senator) vs. Oberman (Council Pos. 1): r = {corr_walen_oberman:.3f}")
print(f"Walen (State Senator) vs. Malik (Council Pos. 3): r = {corr_walen_malik:.3f}")
print(f"Walen (State Senator) vs. MacKenzie (Council Pos. 5): r = {corr_walen_mackenzie:.3f}")
print(f"Walen (State Senator) vs. Pascal (Council Pos. 7): r = {corr_walen_pascal:.3f}")

# Aggregate totals
print("\n" + "=" * 100)
print("AGGREGATE TOTALS - KIRKLAND LD 48")
print("=" * 100)

for race_name in ['State Senator', 'Council Pos. 1', 'Council Pos. 3', 'Council Pos. 5', 'Council Pos. 7']:
    race_query = races[race_name]
    race_data = kirkland_data[kirkland_data['Race'] == race_query]
    
    prog_total = race_data[race_data['CounterType'] == candidates[race_name]['progressive']]['SumOfCount'].sum()
    cons_total = race_data[race_data['CounterType'] == candidates[race_name]['conservative']]['SumOfCount'].sum()
    total = prog_total + cons_total
    
    if total > 0:
        prog_pct = (prog_total / total * 100)
        cons_pct = (cons_total / total * 100)
        
        prog_name = candidates[race_name]['progressive']
        cons_name = candidates[race_name]['conservative']
        
        print(f"\n{race_name}:")
        print(f"  {prog_name}: {int(prog_total)} votes ({prog_pct:.1f}%)")
        print(f"  {cons_name}: {int(cons_total)} votes ({cons_pct:.1f}%)")

print("\n[DONE] Analysis complete!")
