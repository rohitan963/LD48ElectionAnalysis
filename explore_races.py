import pandas as pd

df = pd.read_csv('Mid-Election-results-report.csv')

print('KIRKLAND RACES IN LD 48:')
kirkland_data = df[(df['Precinct'].str.startswith('KIR')) & (df['LegislativeDistrict'] == 48)]
races = sorted(kirkland_data['Race'].unique())
for race in races:
    print(f'  {race}')

print('\n' + '='*100 + '\n')

print('REDMOND RACES IN LD 48:')
redmond_data = df[(df['Precinct'].str.startswith('RED')) & (df['LegislativeDistrict'] == 48)]
races = sorted(redmond_data['Race'].unique())
for race in races:
    print(f'  {race}')

print('\n' + '='*100 + '\n')

print('KIRKLAND PRECINCTS IN LD 48:')
kirk_precincts = kirkland_data['Precinct'].unique()
print(f'Total: {len(kirk_precincts)}')
for p in sorted(kirk_precincts):
    print(f'  {p}')

print('\n' + '='*100 + '\n')

print('REDMOND PRECINCTS IN LD 48:')
red_precincts = redmond_data['Precinct'].unique()
print(f'Total: {len(red_precincts)}')
for p in sorted(red_precincts):
    print(f'  {p}')
