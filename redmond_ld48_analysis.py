import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

# Define Redmond LD 48 precincts
redmond_ld48_precincts = [
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

print("=" * 100)
print("REDMOND - LD 48 PRECINCT ANALYSIS")
print("=" * 100)
print(f"\nTotal Redmond precincts in LD 48: {len(redmond_ld48_precincts)}")

# Filter data for Redmond LD 48
redmond_data = df[df['Precinct'].isin(redmond_ld48_precincts)].copy()

# Define races and candidates
races = {
    'State Senator': 'Legislative District No. 48 State Senator',
    'Council Pos. 2': 'City of Redmond Council Position No. 2',
    'Council Pos. 4': 'City of Redmond Council Position No. 4',
    'Council Pos. 6': 'City of Redmond Council Position No. 6'
}

# Progressive vs Conservative
candidates = {
    'State Senator': {'progressive': 'Vandana Slatter', 'conservative': 'Amy Walen'},
    'Council Pos. 2': {'progressive': 'Vivek Prakriya', 'conservative': 'Steve Fields'},
    'Council Pos. 4': {'progressive': 'Melissa Stuart', 'conservative': 'Kay Asai'},
    'Council Pos. 6': {'progressive': 'Menka Soni', 'conservative': 'Jeralee Anderson'}
}

# Build precinct results
precinct_results = {}
for precinct in sorted(redmond_ld48_precincts):
    precinct_results[precinct] = {}
    precinct_data = redmond_data[redmond_data['Precinct'] == precinct]
    
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
print(f"\n{'Precinct':<18} {'Walen %':<12} {'Fields %':<12} {'Asai %':<12} {'Anderson %':<15}")
print("-" * 100)

walen_pcts = []
fields_pcts = []
asai_pcts = []
anderson_pcts = []

for precinct in sorted(precinct_results.keys()):
    result = precinct_results[precinct]
    if all(r in result for r in ['State Senator', 'Council Pos. 2', 'Council Pos. 4', 'Council Pos. 6']):
        walen = result['State Senator']['cons_pct']
        fields = result['Council Pos. 2']['cons_pct']
        asai = result['Council Pos. 4']['cons_pct']
        anderson = result['Council Pos. 6']['cons_pct']
        
        walen_pcts.append(walen)
        fields_pcts.append(fields)
        asai_pcts.append(asai)
        anderson_pcts.append(anderson)
        
        print(f"{precinct:<18} {walen:>10.1f}%  {fields:>10.1f}%  {asai:>10.1f}%  {anderson:>13.1f}%")

# Statistics
print("-" * 100)
print(f"{'MEAN':<18} {np.mean(walen_pcts):>10.1f}%  {np.mean(fields_pcts):>10.1f}%  {np.mean(asai_pcts):>10.1f}%  {np.mean(anderson_pcts):>13.1f}%")
print(f"{'STDEV':<18} {np.std(walen_pcts):>10.1f}  {np.std(fields_pcts):>10.1f}  {np.std(asai_pcts):>10.1f}  {np.std(anderson_pcts):>13.1f}")

# Correlation analysis
print("\n" + "=" * 100)
print("CORRELATION ANALYSIS: Conservative Candidate Performance")
print("=" * 100)

corr_walen_fields, p_wf = pearsonr(walen_pcts, fields_pcts)
corr_walen_asai, p_wa = pearsonr(walen_pcts, asai_pcts)
corr_walen_anderson, p_wand = pearsonr(walen_pcts, anderson_pcts)

print(f"\nWalen (State Senator) vs. Fields (Council Pos. 2): r = {corr_walen_fields:.3f}")
print(f"Walen (State Senator) vs. Asai (Council Pos. 4): r = {corr_walen_asai:.3f}")
print(f"Walen (State Senator) vs. Anderson (Council Pos. 6): r = {corr_walen_anderson:.3f}")

# Aggregate totals
print("\n" + "=" * 100)
print("AGGREGATE TOTALS - REDMOND LD 48")
print("=" * 100)

for race_name in ['State Senator', 'Council Pos. 2', 'Council Pos. 4', 'Council Pos. 6']:
    race_query = races[race_name]
    race_data = redmond_data[redmond_data['Race'] == race_query]
    
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
