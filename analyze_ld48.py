import pandas as pd
import json
from collections import defaultdict

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

# Filter for Legislative District 48 State Senator race (Slatter v. Walen)
ld48_data = df[df['LegislativeDistrict'] == 48].copy()

# Get unique precincts in LD 48
precincts_ld48 = ld48_data['Precinct'].unique()

print("=" * 70)
print("LD 48 (Slatter v. Walen) - Precinct Analysis")
print("=" * 70)
print(f"\nTotal unique precincts in LD 48: {len(precincts_ld48)}")
print("\nPrecincts by City:\n")

# Create a mapping of precinct prefixes to cities
# Looking at the precinct names, they appear to start with city codes
city_mapping = {
    'BEL': 'Bellevue',
    'SEA': 'Seattle',
    'C-H': 'Cascade-Issaquah',
    'KIR': 'Kirkland',
    'MED': 'Medina',
    'RED': 'Redmond',
    'HPT': 'Highland Park',
    'YPT': 'Yarrow Point',
    'BEAR CREEK': 'Bear Creek',
    'BRIDLE TRAILS': 'Bridle Trails',
    'EVANS': 'Evans',
    'MARYMOOR': 'Marymoor Park',
}

# Organize precincts by city
precincts_by_city = defaultdict(list)

for precinct in sorted(precincts_ld48):
    # Extract city code from precinct name
    city_name = 'Unknown'
    
    # Check if it's a special named precinct (full name match)
    if precinct in city_mapping:
        city_name = city_mapping[precinct]
    else:
        # Extract city code from precinct name (first 3-4 characters)
        city_code = precinct.split()[0]  # Get the prefix before the space/number
        city_name = city_mapping.get(city_code, 'Unknown')
    
    precincts_by_city[city_name].append(precinct)

# Print results organized by city
for city in sorted(precincts_by_city.keys()):
    precincts = sorted(precincts_by_city[city])
    print(f"{city}:")
    for precinct in precincts:
        print(f"  • {precinct}")
    print(f"  (Total: {len(precincts)} precincts)\n")

# Create summary statistics
print("\n" + "=" * 70)
print("Summary Statistics by City")
print("=" * 70)

summary_data = []
for city in sorted(precincts_by_city.keys()):
    city_precincts = precincts_by_city[city]
    city_df = ld48_data[ld48_data['Precinct'].isin(city_precincts)]
    
    # Get vote totals for Slatter and Walen
    state_senator_data = city_df[city_df['Race'] == 'Legislative District No. 48 State Senator']
    
    # Candidates are in the CounterType column
    slatter_votes = state_senator_data[state_senator_data['CounterType'] == 'Vandana Slatter']['SumOfCount'].sum()
    walen_votes = state_senator_data[state_senator_data['CounterType'] == 'Amy Walen']['SumOfCount'].sum()
    
    summary_data.append({
        'City': city,
        'Precincts': len(city_precincts),
        'Slatter Votes': int(slatter_votes),
        'Walen Votes': int(walen_votes),
        'Total Votes': int(slatter_votes + walen_votes)
    })

summary_df = pd.DataFrame(summary_data)
print("\n" + summary_df.to_string(index=False))

# Calculate totals
print("\n" + "-" * 70)
totals = {
    'City': 'TOTAL',
    'Precincts': summary_df['Precincts'].sum(),
    'Slatter Votes': summary_df['Slatter Votes'].sum(),
    'Walen Votes': summary_df['Walen Votes'].sum(),
    'Total Votes': summary_df['Total Votes'].sum()
}
print(f"{totals['City']:15} {totals['Precincts']:10} {totals['Slatter Votes']:15} {totals['Walen Votes']:12} {totals['Total Votes']:12}")

# Save detailed results to JSON
output = {
    'district': 'LD 48',
    'race': 'State Senator (Slatter v. Walen)',
    'precincts_by_city': {city: sorted(precincts) for city, precincts in precincts_by_city.items()},
    'summary': summary_data
}

with open('ld48_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n✓ Analysis saved to 'ld48_analysis.json'")
