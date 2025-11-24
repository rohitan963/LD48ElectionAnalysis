import pandas as pd
df = pd.read_csv('Mid-Election-results-report.csv')

precinct = 'BEL 48-0125'
p_data = df[df['Precinct'] == precinct]
ss_data = p_data[p_data['Race'] == 'Legislative District No. 48 State Senator']

print(f'All State Senator records for {precinct}:')
print(ss_data[['CounterType', 'SumOfCount']])
print(f'\nTotal: {ss_data["SumOfCount"].sum()}')
print(f'\nCandidate only rows:')
candidates_only = ss_data[~ss_data['CounterType'].str.contains('Times|Registered|Approved|Rejected', na=False)]
print(candidates_only[['CounterType', 'SumOfCount']])
print(f'Candidates total: {candidates_only["SumOfCount"].sum()}')
