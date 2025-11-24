import pandas as pd

df = pd.read_csv('Mid-Election-results-report.csv')

kirkland_data = df[(df['Precinct'].str.startswith('KIR')) & (df['LegislativeDistrict'] == 48)]
redmond_data = df[(df['Precinct'].str.startswith('RED')) & (df['LegislativeDistrict'] == 48)]

print('KIRKLAND CANDIDATES:')
for race in ['City of Kirkland Council Position No. 1', 'City of Kirkland Council Position No. 3', 
             'City of Kirkland Council Position No. 5', 'City of Kirkland Council Position No. 7']:
    print(f'\n{race}:')
    race_data = kirkland_data[kirkland_data['Race'] == race]
    candidates = race_data['CounterType'].unique()
    for c in sorted(candidates):
        votes = race_data[race_data['CounterType'] == c]['SumOfCount'].sum()
        print(f'  {c}: {int(votes)} votes')

print('\n' + '='*100 + '\n')

print('REDMOND CANDIDATES:')
for race in ['City of Redmond Council Position No. 2', 'City of Redmond Council Position No. 4', 
             'City of Redmond Council Position No. 6']:
    print(f'\n{race}:')
    race_data = redmond_data[redmond_data['Race'] == race]
    candidates = race_data['CounterType'].unique()
    for c in sorted(candidates):
        votes = race_data[race_data['CounterType'] == c]['SumOfCount'].sum()
        print(f'  {c}: {int(votes)} votes')
