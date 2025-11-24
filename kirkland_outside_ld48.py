import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

# Define Kirkland LD 48 precincts (to exclude them)
kirkland_ld48_precincts = [
    'KIR 48-0614', 'KIR 48-0615', 'KIR 48-0616', 'KIR 48-0628', 'KIR 48-0629',
    'KIR 48-0636', 'KIR 48-0638', 'KIR 48-0639', 'KIR 48-0641', 'KIR 48-0642',
    'KIR 48-0643', 'KIR 48-0644', 'KIR 48-0645', 'KIR 48-0646', 'KIR 48-2598',
    'KIR 48-2657', 'KIR 48-2788', 'KIR 48-2863', 'KIR 48-2914', 'KIR 48-2915',
    'KIR 48-2919', 'KIR 48-2920', 'KIR 48-2921', 'KIR 48-2922', 'KIR 48-2925',
    'KIR 48-3196', 'KIR 48-3337', 'KIR 48-3401', 'KIR 48-3439', 'KIR 48-3760',
    'KIR 48-3985'
]

# Get all Kirkland precincts
all_kirkland_precincts = df[df['Precinct'].str.startswith('KIR')]['Precinct'].unique()

# Get Kirkland precincts NOT in LD 48
kirkland_not_ld48 = [p for p in all_kirkland_precincts if p not in kirkland_ld48_precincts]

print("=" * 100)
print("KIRKLAND PRECINCTS OUTSIDE LD 48")
print("=" * 100)
print(f"\nTotal Kirkland precincts: {len(all_kirkland_precincts)}")
print(f"Kirkland precincts in LD 48: {len(kirkland_ld48_precincts)}")
print(f"Kirkland precincts NOT in LD 48: {len(kirkland_not_ld48)}\n")

# Filter data for Kirkland precincts NOT in LD 48
kirkland_other_data = df[df['Precinct'].isin(kirkland_not_ld48)].copy()

# Get legislative districts
districts = kirkland_other_data['LegislativeDistrict'].unique()
print(f"Legislative Districts: {sorted(districts)}")

# Define races for local comparison
kirkland_races = {
    'Council Pos. 1': 'City of Kirkland Council Position No. 1',
    'Council Pos. 3': 'City of Kirkland Council Position No. 3',
    'Council Pos. 5': 'City of Kirkland Council Position No. 5',
    'Council Pos. 7': 'City of Kirkland Council Position No. 7'
}

kirkland_candidates = {
    'Council Pos. 1': {'progressive': 'Jay Arnold', 'conservative': 'Ken Oberman'},
    'Council Pos. 3': {'progressive': 'Shilpa Prem', 'conservative': 'Catie Malik'},
    'Council Pos. 5': {'progressive': 'Neal Black', 'conservative': 'Ken MacKenzie'},
    'Council Pos. 7': {'progressive': 'Kurt Dresner', 'conservative': 'Jon Pascal'}
}

print("\n" + "=" * 100)
print("TOPLINE COMPARISON: KIRKLAND LD 48 vs. OUTSIDE LD 48 (LOCAL COUNCIL RACES)")
print("=" * 100)

# Get LD 48 data for Kirkland
kirkland_ld48_data = df[df['Precinct'].isin(kirkland_ld48_precincts)].copy()

print(f"\n{'Race':<35} {'District':<12} {'Progressive':<28} {'Conservative':<28} {'Total':<10}")
print("-" * 100)

for race_name, race_query in kirkland_races.items():
    # LD 48 totals
    ld48_race_data = kirkland_ld48_data[kirkland_ld48_data['Race'] == race_query]
    ld48_prog_votes = ld48_race_data[ld48_race_data['CounterType'] == kirkland_candidates[race_name]['progressive']]['SumOfCount'].sum()
    ld48_cons_votes = ld48_race_data[ld48_race_data['CounterType'] == kirkland_candidates[race_name]['conservative']]['SumOfCount'].sum()
    ld48_total = ld48_prog_votes + ld48_cons_votes
    
    if ld48_total > 0:
        ld48_prog_pct = (ld48_prog_votes / ld48_total * 100)
        ld48_cons_pct = (ld48_cons_votes / ld48_total * 100)
        ld48_prog_str = f"{kirkland_candidates[race_name]['progressive']}: {int(ld48_prog_votes)} ({ld48_prog_pct:.1f}%)"
        ld48_cons_str = f"{kirkland_candidates[race_name]['conservative']}: {int(ld48_cons_votes)} ({ld48_cons_pct:.1f}%)"
    else:
        ld48_prog_str = "N/A"
        ld48_cons_str = "N/A"
        ld48_total = 0
    
    # Outside LD 48 totals
    other_race_data = kirkland_other_data[kirkland_other_data['Race'] == race_query]
    other_prog_votes = other_race_data[other_race_data['CounterType'] == kirkland_candidates[race_name]['progressive']]['SumOfCount'].sum()
    other_cons_votes = other_race_data[other_race_data['CounterType'] == kirkland_candidates[race_name]['conservative']]['SumOfCount'].sum()
    other_total = other_prog_votes + other_cons_votes
    
    if other_total > 0:
        other_prog_pct = (other_prog_votes / other_total * 100)
        other_cons_pct = (other_cons_votes / other_total * 100)
        other_prog_str = f"{kirkland_candidates[race_name]['progressive']}: {int(other_prog_votes)} ({other_prog_pct:.1f}%)"
        other_cons_str = f"{kirkland_candidates[race_name]['conservative']}: {int(other_cons_votes)} ({other_cons_pct:.1f}%)"
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
print("\n[DONE] Kirkland analysis complete!")
