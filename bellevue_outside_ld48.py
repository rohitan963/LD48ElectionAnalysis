import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

# Get all Bellevue precincts
all_bellevue_precincts = df[df['Precinct'].str.startswith('BEL')]['Precinct'].unique()

# Get the list of Bellevue precincts that ARE in LD 48
bellevue_ld48_precincts = [
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

# Get Bellevue precincts NOT in LD 48
bellevue_not_ld48 = [p for p in all_bellevue_precincts if p not in bellevue_ld48_precincts]

print("=" * 120)
print("BELLEVUE PRECINCTS NOT IN LD 48")
print("=" * 120)
print(f"\nTotal Bellevue precincts: {len(all_bellevue_precincts)}")
print(f"Bellevue precincts in LD 48: {len(bellevue_ld48_precincts)}")
print(f"Bellevue precincts NOT in LD 48: {len(bellevue_not_ld48)}\n")

if len(bellevue_not_ld48) == 0:
    print("No Bellevue precincts found outside of LD 48!")
else:
    # Filter data for Bellevue precincts NOT in LD 48
    bellevue_other_data = df[df['Precinct'].isin(bellevue_not_ld48)].copy()
    
    print("Precincts outside LD 48:")
    for precinct in sorted(bellevue_not_ld48):
        ld = bellevue_other_data[bellevue_other_data['Precinct'] == precinct]['LegislativeDistrict'].unique()
        if len(ld) > 0:
            print(f"  {precinct:<20} - Legislative District(s): {', '.join(map(str, sorted(ld)))}")
    
    # Define the three races we want to analyze
    races = {
        'State Senator': 'Legislative District No. 48 State Senator',
        'City Council Position No. 1': 'City of Bellevue Council Position No. 1',
        'City Council Position No. 2': 'City of Bellevue Council Position No. 2'
    }
    
    candidates = {
        'State Senator': {
            'progressive': 'Vandana Slatter',
            'conservative': 'Amy Walen'
        },
        'City Council Position No. 1': {
            'progressive': 'Vishal Bhargava',
            'conservative': 'Paul Clark'
        },
        'City Council Position No. 2': {
            'progressive': 'Naren Briar',
            'conservative': 'Conrad Lee'
        }
    }
    
    # Check if LD 48 State Senator race exists in these precincts
    state_senator_data = bellevue_other_data[bellevue_other_data['Race'] == 'Legislative District No. 48 State Senator']
    
    if len(state_senator_data) == 0:
        print("\nNOTE: These Bellevue precincts are not in LD 48, so the LD 48 State Senator race")
        print("(Slatter vs. Walen) is not available in these precincts.")
        print("\nShowing results for local Bellevue races only:\n")
        
        # Show local races only
        print("=" * 120)
        print("LOCAL BELLEVUE COUNCIL RACES")
        print("=" * 120 + "\n")
        
        for race_name in ['City Council Position No. 1', 'City Council Position No. 2']:
            print(f"\n{race_name.upper()}\n")
            print(f"{'Precinct':<20} {'Progressive':>30} {'Conservative':>30}")
            print("-" * 120)
            
            race_query = races[race_name]
            race_data = bellevue_other_data[bellevue_other_data['Race'] == race_query]
            
            if len(race_data) > 0:
                for precinct in sorted(bellevue_not_ld48):
                    precinct_data = race_data[race_data['Precinct'] == precinct]
                    
                    if len(precinct_data) > 0:
                        prog_votes = precinct_data[precinct_data['CounterType'] == candidates[race_name]['progressive']]['SumOfCount'].sum()
                        cons_votes = precinct_data[precinct_data['CounterType'] == candidates[race_name]['conservative']]['SumOfCount'].sum()
                        total_votes = prog_votes + cons_votes
                        
                        if total_votes > 0:
                            prog_pct = (prog_votes / total_votes * 100)
                            cons_pct = (cons_votes / total_votes * 100)
                            
                            prog_name = candidates[race_name]['progressive']
                            cons_name = candidates[race_name]['conservative']
                            
                            prog_str = f"{prog_name}: {int(prog_votes)} ({prog_pct:.1f}%)"
                            cons_str = f"{cons_name}: {int(cons_votes)} ({cons_pct:.1f}%)"
                            
                            print(f"{precinct:<20} {prog_str:>30} {cons_str:>30}")
            else:
                print(f"No data available for {race_name}")
    else:
        # Show all three races
        print("\n" + "=" * 120)
        print("CANDIDATE PERFORMANCE IN BELLEVUE PRECINCTS OUTSIDE LD 48")
        print("=" * 120 + "\n")
        
        for race_name in ['State Senator', 'City Council Position No. 1', 'City Council Position No. 2']:
            print(f"\n{race_name.upper()}\n")
            print(f"{'Precinct':<20} {'Progressive':>30} {'Conservative':>30}")
            print("-" * 120)
            
            race_query = races[race_name]
            race_data = bellevue_other_data[bellevue_other_data['Race'] == race_query]
            
            if len(race_data) > 0:
                for precinct in sorted(bellevue_not_ld48):
                    precinct_data = race_data[race_data['Precinct'] == precinct]
                    
                    if len(precinct_data) > 0:
                        prog_votes = precinct_data[precinct_data['CounterType'] == candidates[race_name]['progressive']]['SumOfCount'].sum()
                        cons_votes = precinct_data[precinct_data['CounterType'] == candidates[race_name]['conservative']]['SumOfCount'].sum()
                        total_votes = prog_votes + cons_votes
                        
                        if total_votes > 0:
                            prog_pct = (prog_votes / total_votes * 100)
                            cons_pct = (cons_votes / total_votes * 100)
                            
                            prog_name = candidates[race_name]['progressive']
                            cons_name = candidates[race_name]['conservative']
                            
                            prog_str = f"{prog_name}: {int(prog_votes)} ({prog_pct:.1f}%)"
                            cons_str = f"{cons_name}: {int(cons_votes)} ({cons_pct:.1f}%)"
                            
                            print(f"{precinct:<20} {prog_str:>30} {cons_str:>30}")
            else:
                print(f"No data available for {race_name}")
        
        # Summary statistics
        print("\n" + "=" * 120)
        print("SUMMARY STATISTICS")
        print("=" * 120 + "\n")
        
        walen_votes_total = 0
        slatter_votes_total = 0
        lee_votes_total = 0
        briar_votes_total = 0
        clark_votes_total = 0
        bhargava_votes_total = 0
        
        for race_name in ['State Senator', 'City Council Position No. 1', 'City Council Position No. 2']:
            race_query = races[race_name]
            race_data = bellevue_other_data[bellevue_other_data['Race'] == race_query]
            
            if len(race_data) > 0:
                prog_total = race_data[race_data['CounterType'] == candidates[race_name]['progressive']]['SumOfCount'].sum()
                cons_total = race_data[race_data['CounterType'] == candidates[race_name]['conservative']]['SumOfCount'].sum()
                total = prog_total + cons_total
                
                if total > 0:
                    prog_pct = (prog_total / total * 100)
                    cons_pct = (cons_total / total * 100)
                    
                    prog_name = candidates[race_name]['progressive']
                    cons_name = candidates[race_name]['conservative']
                    
                    print(f"{race_name}:")
                    print(f"  {prog_name}: {int(prog_total)} votes ({prog_pct:.1f}%)")
                    print(f"  {cons_name}: {int(cons_total)} votes ({cons_pct:.1f}%)")
                    print(f"  Total votes: {int(total)}\n")
                    
                    if race_name == 'State Senator':
                        slatter_votes_total = prog_total
                        walen_votes_total = cons_total
                    elif race_name == 'City Council Position No. 1':
                        bhargava_votes_total = prog_total
                        clark_votes_total = cons_total
                    elif race_name == 'City Council Position No. 2':
                        briar_votes_total = prog_total
                        lee_votes_total = cons_total

print("\n" + "=" * 120)
print("TOPLINE COMPARISON: LD 48 VS. OUTSIDE LD 48 (LOCAL COUNCIL RACES)")
print("=" * 120 + "\n")

# Read LD 48 data
bellevue_ld48_data = df[df['Precinct'].isin(bellevue_ld48_precincts)].copy()

# Define races for comparison
council_races = {
    'City Council Position No. 1': {
        'query': 'City of Bellevue Council Position No. 1',
        'progressive': 'Vishal Bhargava',
        'conservative': 'Paul Clark'
    },
    'City Council Position No. 2': {
        'query': 'City of Bellevue Council Position No. 2',
        'progressive': 'Naren Briar',
        'conservative': 'Conrad Lee'
    }
}

print(f"{'Race':<40} {'District':<15} {'Progressive':<25} {'Conservative':<25} {'Total Votes':<15}")
print("-" * 120)

for race_name, race_info in council_races.items():
    # LD 48 totals
    ld48_race_data = bellevue_ld48_data[bellevue_ld48_data['Race'] == race_info['query']]
    ld48_prog_votes = ld48_race_data[ld48_race_data['CounterType'] == race_info['progressive']]['SumOfCount'].sum()
    ld48_cons_votes = ld48_race_data[ld48_race_data['CounterType'] == race_info['conservative']]['SumOfCount'].sum()
    ld48_total = ld48_prog_votes + ld48_cons_votes
    
    if ld48_total > 0:
        ld48_prog_pct = (ld48_prog_votes / ld48_total * 100)
        ld48_cons_pct = (ld48_cons_votes / ld48_total * 100)
        ld48_prog_str = f"{race_info['progressive']}: {int(ld48_prog_votes)} ({ld48_prog_pct:.1f}%)"
        ld48_cons_str = f"{race_info['conservative']}: {int(ld48_cons_votes)} ({ld48_cons_pct:.1f}%)"
    else:
        ld48_prog_str = "N/A"
        ld48_cons_str = "N/A"
        ld48_total = 0
    
    # Outside LD 48 totals
    other_race_data = bellevue_other_data[bellevue_other_data['Race'] == race_info['query']]
    other_prog_votes = other_race_data[other_race_data['CounterType'] == race_info['progressive']]['SumOfCount'].sum()
    other_cons_votes = other_race_data[other_race_data['CounterType'] == race_info['conservative']]['SumOfCount'].sum()
    other_total = other_prog_votes + other_cons_votes
    
    if other_total > 0:
        other_prog_pct = (other_prog_votes / other_total * 100)
        other_cons_pct = (other_cons_votes / other_total * 100)
        other_prog_str = f"{race_info['progressive']}: {int(other_prog_votes)} ({other_prog_pct:.1f}%)"
        other_cons_str = f"{race_info['conservative']}: {int(other_cons_votes)} ({other_cons_pct:.1f}%)"
    else:
        other_prog_str = "N/A"
        other_cons_str = "N/A"
        other_total = 0
    
    # Print LD 48 row
    print(f"{race_name:<40} {'LD 48':<15} {ld48_prog_str:<25} {ld48_cons_str:<25} {int(ld48_total):<15}")
    
    # Print Outside LD 48 row
    print(f"{'(same race)':<40} {'LD 41':<15} {other_prog_str:<25} {other_cons_str:<25} {int(other_total):<15}")
    print()

print("=" * 120)

print("\n[DONE] Analysis complete!")
