import pandas as pd

df = pd.read_csv('Mid-Election-results-report.csv')

# Get all Kirkland precincts
all_kirk = df[df['Precinct'].str.startswith('KIR')]['Precinct'].unique()

# Get Kirkland precincts in LD 48
kirk_ld48 = [
    'KIR 48-0614', 'KIR 48-0615', 'KIR 48-0616', 'KIR 48-0628', 'KIR 48-0629',
    'KIR 48-0636', 'KIR 48-0638', 'KIR 48-0639', 'KIR 48-0641', 'KIR 48-0642',
    'KIR 48-0643', 'KIR 48-0644', 'KIR 48-0645', 'KIR 48-0646', 'KIR 48-2598',
    'KIR 48-2657', 'KIR 48-2788', 'KIR 48-2863', 'KIR 48-2914', 'KIR 48-2915',
    'KIR 48-2919', 'KIR 48-2920', 'KIR 48-2921', 'KIR 48-2922', 'KIR 48-2925',
    'KIR 48-3196', 'KIR 48-3337', 'KIR 48-3401', 'KIR 48-3439', 'KIR 48-3760',
    'KIR 48-3985'
]

kirk_not_ld48 = [p for p in all_kirk if p not in kirk_ld48]

print("KIRKLAND PRECINCTS:")
print(f"  Total: {len(all_kirk)}")
print(f"  In LD 48: {len(kirk_ld48)}")
print(f"  Outside LD 48: {len(kirk_not_ld48)}")

if kirk_not_ld48:
    kirk_other_data = df[df['Precinct'].isin(kirk_not_ld48)]
    districts = kirk_other_data['LegislativeDistrict'].unique()
    print(f"  Districts outside LD 48: {sorted(districts)}")

print("\n" + "="*100 + "\n")

# Get all Redmond precincts
all_red = df[df['Precinct'].str.startswith('RED')]['Precinct'].unique()

# Get Redmond precincts in LD 48
red_ld48 = [
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

red_not_ld48 = [p for p in all_red if p not in red_ld48]

print("REDMOND PRECINCTS:")
print(f"  Total: {len(all_red)}")
print(f"  In LD 48: {len(red_ld48)}")
print(f"  Outside LD 48: {len(red_not_ld48)}")

if red_not_ld48:
    red_other_data = df[df['Precinct'].isin(red_not_ld48)]
    districts = red_other_data['LegislativeDistrict'].unique()
    print(f"  Districts outside LD 48: {sorted(districts)}")
