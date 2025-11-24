import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

# Define Redmond LD 48 precincts (to exclude them)
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

# Get all Redmond precincts
all_redmond_precincts = df[df['Precinct'].str.startswith('RED')]['Precinct'].unique()

# Get Redmond precincts NOT in LD 48
redmond_not_ld48 = [p for p in all_redmond_precincts if p not in redmond_ld48_precincts]

print("=" * 100)
print("REDMOND PRECINCTS OUTSIDE LD 48")
print("=" * 100)
print(f"\nTotal Redmond precincts: {len(all_redmond_precincts)}")
print(f"Redmond precincts in LD 48: {len(redmond_ld48_precincts)}")
print(f"Redmond precincts NOT in LD 48: {len(redmond_not_ld48)}\n")

# Filter data for Redmond precincts NOT in LD 48
redmond_other_data = df[df['Precinct'].isin(redmond_not_ld48)].copy()

# Get legislative districts
districts = redmond_other_data['LegislativeDistrict'].unique()
print(f"Legislative Districts: {sorted(districts)}")

# Define races for local comparison
redmond_races = {
    'Council Pos. 2': 'City of Redmond Council Position No. 2',
    'Council Pos. 4': 'City of Redmond Council Position No. 4',
    'Council Pos. 6': 'City of Redmond Council Position No. 6'
}

redmond_candidates = {
    'Council Pos. 2': {'progressive': 'Vivek Prakriya', 'conservative': 'Steve Fields'},
    'Council Pos. 4': {'progressive': 'Melissa Stuart', 'conservative': 'Kay Asai'},
    'Council Pos. 6': {'progressive': 'Menka Soni', 'conservative': 'Jeralee Anderson'}
}

print("\n" + "=" * 100)
print("TOPLINE COMPARISON: REDMOND LD 48 vs. OUTSIDE LD 48 (LOCAL COUNCIL RACES)")
print("=" * 100)

# Get LD 48 data for Redmond
redmond_ld48_data = df[df['Precinct'].isin(redmond_ld48_precincts)].copy()

print(f"\n{'Race':<35} {'District':<12} {'Progressive':<28} {'Conservative':<28} {'Total':<10}")
print("-" * 100)

for race_name, race_query in redmond_races.items():
    # LD 48 totals
    ld48_race_data = redmond_ld48_data[redmond_ld48_data['Race'] == race_query]
    ld48_prog_votes = ld48_race_data[ld48_race_data['CounterType'] == redmond_candidates[race_name]['progressive']]['SumOfCount'].sum()
    ld48_cons_votes = ld48_race_data[ld48_race_data['CounterType'] == redmond_candidates[race_name]['conservative']]['SumOfCount'].sum()
    ld48_total = ld48_prog_votes + ld48_cons_votes
    
    if ld48_total > 0:
        ld48_prog_pct = (ld48_prog_votes / ld48_total * 100)
        ld48_cons_pct = (ld48_cons_votes / ld48_total * 100)
        ld48_prog_str = f"{redmond_candidates[race_name]['progressive']}: {int(ld48_prog_votes)} ({ld48_prog_pct:.1f}%)"
        ld48_cons_str = f"{redmond_candidates[race_name]['conservative']}: {int(ld48_cons_votes)} ({ld48_cons_pct:.1f}%)"
    else:
        ld48_prog_str = "N/A"
        ld48_cons_str = "N/A"
        ld48_total = 0
    
    # Outside LD 48 totals
    other_race_data = redmond_other_data[redmond_other_data['Race'] == race_query]
    other_prog_votes = other_race_data[other_race_data['CounterType'] == redmond_candidates[race_name]['progressive']]['SumOfCount'].sum()
    other_cons_votes = other_race_data[other_race_data['CounterType'] == redmond_candidates[race_name]['conservative']]['SumOfCount'].sum()
    other_total = other_prog_votes + other_cons_votes
    
    if other_total > 0:
        other_prog_pct = (other_prog_votes / other_total * 100)
        other_cons_pct = (other_cons_votes / other_total * 100)
        other_prog_str = f"{redmond_candidates[race_name]['progressive']}: {int(other_prog_votes)} ({other_prog_pct:.1f}%)"
        other_cons_str = f"{redmond_candidates[race_name]['conservative']}: {int(other_cons_votes)} ({other_cons_pct:.1f}%)"
    else:
        other_prog_str = "N/A"
        other_cons_str = "N/A"
        other_total = 0
    
    # Print LD 48 row
    print(f"{race_name:<35} {'LD 48':<12} {ld48_prog_str:<28} {ld48_cons_str:<28} {int(ld48_total):<10}")
    
    # Print Outside LD 48 row
    print(f"{'(same race)':<35} {'Other':<12} {other_prog_str:<28} {other_cons_str:<28} {int(other_total):<10}")
    print()

print("=" * 100)
print("\n[DONE] Redmond analysis complete!")
