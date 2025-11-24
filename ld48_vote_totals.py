import pandas as pd

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

print("=" * 100)
print("LD 48 STATE SENATOR RACE: TOTAL VOTES BY CITY")
print("=" * 100)

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

city_totals = {}

for city, precincts in [('Bellevue', bellevue_ld48), ('Kirkland', kirkland_ld48), ('Redmond', redmond_ld48)]:
    city_df = df[df['Precinct'].isin(precincts)]
    
    # Filter for State Senator race only
    ss_df = city_df[city_df['Race'] == 'Legislative District No. 48 State Senator']
    
    # Get votes for each candidate (excluding meta rows)
    slatter_votes = ss_df[ss_df['CounterType'] == 'Vandana Slatter']['SumOfCount'].sum()
    walen_votes = ss_df[ss_df['CounterType'] == 'Amy Walen']['SumOfCount'].sum()
    writein_votes = ss_df[ss_df['CounterType'] == 'Write-in']['SumOfCount'].sum()
    
    total_votes = slatter_votes + walen_votes + writein_votes
    
    slatter_pct = (slatter_votes / total_votes * 100) if total_votes > 0 else 0
    walen_pct = (walen_votes / total_votes * 100) if total_votes > 0 else 0
    writein_pct = (writein_votes / total_votes * 100) if total_votes > 0 else 0
    
    city_totals[city] = {
        'slatter': slatter_votes,
        'walen': walen_votes,
        'writein': writein_votes,
        'total': total_votes,
        'slatter_pct': slatter_pct,
        'walen_pct': walen_pct,
        'writein_pct': writein_pct,
        'precincts': len(precincts)
    }

# Print results
print("\n")
print(f"{'City':<15} {'Precincts':<12} {'Slatter':<15} {'Walen':<15} {'Write-in':<12} {'Total':<12}")
print(f"{'-' * 100}")

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    data = city_totals[city]
    print(f"{city:<15} {data['precincts']:<12} {data['slatter']:<15} {data['walen']:<15} {data['writein']:<12} {data['total']:<12}")

print(f"{'-' * 100}")

# Calculate LD 48 totals
total_slatter = sum(city_totals[city]['slatter'] for city in ['Bellevue', 'Kirkland', 'Redmond'])
total_walen = sum(city_totals[city]['walen'] for city in ['Bellevue', 'Kirkland', 'Redmond'])
total_writein = sum(city_totals[city]['writein'] for city in ['Bellevue', 'Kirkland', 'Redmond'])
total_all = total_slatter + total_walen + total_writein

print(f"{'TOTAL':<15} {71+31+49:<12} {total_slatter:<15} {total_walen:<15} {total_writein:<12} {total_all:<12}")

# Print percentages
print("\n" + "=" * 100)
print("VOTE SHARE BY CITY AND CANDIDATE")
print("=" * 100 + "\n")

print(f"{'City':<15} {'Slatter Votes':<15} {'Slatter %':<15} {'Walen Votes':<15} {'Walen %':<15}")
print(f"{'-' * 100}")

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    data = city_totals[city]
    print(f"{city:<15} {data['slatter']:<15} {data['slatter_pct']:<14.1f}% {data['walen']:<15} {data['walen_pct']:<14.1f}%")

print(f"{'-' * 100}")
total_slatter_pct = (total_slatter / total_all * 100)
total_walen_pct = (total_walen / total_all * 100)
print(f"{'TOTAL':<15} {total_slatter:<15} {total_slatter_pct:<14.1f}% {total_walen:<15} {total_walen_pct:<14.1f}%")

# Calculate what percentage of total LD 48 votes come from each city
print("\n" + "=" * 100)
print("SHARE OF TOTAL LD 48 VOTES BY CITY")
print("=" * 100 + "\n")

print(f"{'City':<15} {'Total Votes':<15} {'% of LD 48 Total':<20}")
print(f"{'-' * 100}")

for city in ['Bellevue', 'Kirkland', 'Redmond']:
    data = city_totals[city]
    city_pct = (data['total'] / total_all * 100)
    print(f"{city:<15} {data['total']:<15} {city_pct:<19.1f}%")

print(f"{'-' * 100}")
print(f"{'TOTAL':<15} {total_all:<15} {'100.0%':<19}")

print("\n" + "=" * 100 + "\n")
