import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Read the CSV file
df = pd.read_csv('Mid-Election-results-report.csv')

# Get the list of Bellevue precincts from our previous analysis
bellevue_precincts = [
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

# Filter data for Bellevue precincts in LD 48
bellevue_data = df[df['Precinct'].isin(bellevue_precincts)].copy()

print("=" * 100)
print("BELLEVUE LD 48 ELECTION ANALYSIS - BY PRECINCT")
print("=" * 100)

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

# Collect results by precinct
precinct_results = {}

for precinct in bellevue_precincts:
    precinct_data = bellevue_data[bellevue_data['Precinct'] == precinct]
    precinct_results[precinct] = {}
    
    for race_name, race_query in races.items():
        race_data = precinct_data[precinct_data['Race'] == race_query]
        
        # Get vote counts for candidates
        prog_votes = race_data[race_data['CounterType'] == candidates[race_name]['progressive']]['SumOfCount'].sum()
        cons_votes = race_data[race_data['CounterType'] == candidates[race_name]['conservative']]['SumOfCount'].sum()
        total_votes = prog_votes + cons_votes
        
        # Calculate percentages
        prog_pct = (prog_votes / total_votes * 100) if total_votes > 0 else 0
        cons_pct = (cons_votes / total_votes * 100) if total_votes > 0 else 0
        
        precinct_results[precinct][race_name] = {
            'progressive': {
                'name': candidates[race_name]['progressive'],
                'votes': int(prog_votes),
                'pct': prog_pct
            },
            'conservative': {
                'name': candidates[race_name]['conservative'],
                'votes': int(cons_votes),
                'pct': cons_pct
            },
            'total': int(total_votes)
        }

# Print detailed precinct results
print("\nPRECINCT-BY-PRECINCT RESULTS\n")
print(f"{'Precinct':<15} {'Walen %':>8} {'Lee %':>8} {'Clark %':>8} {'Walen-Lee':>10} {'Walen-Clark':>12}")
print("-" * 100)

walen_pcts = []
lee_pcts = []
clark_pcts = []

for precinct in sorted(bellevue_precincts):
    if precinct in precinct_results:
        walen_pct = precinct_results[precinct]['State Senator']['conservative']['pct']
        lee_pct = precinct_results[precinct]['City Council Position No. 2']['conservative']['pct']
        clark_pct = precinct_results[precinct]['City Council Position No. 1']['conservative']['pct']
        
        walen_lee_diff = walen_pct - lee_pct
        walen_clark_diff = walen_pct - clark_pct
        
        print(f"{precinct:<15} {walen_pct:>7.1f}% {lee_pct:>7.1f}% {clark_pct:>7.1f}% {walen_lee_diff:>9.1f}pp {walen_clark_diff:>11.1f}pp")
        
        walen_pcts.append(walen_pct)
        lee_pcts.append(lee_pct)
        clark_pcts.append(clark_pct)

print("-" * 100)
print(f"{'MEAN':<15} {np.mean(walen_pcts):>7.1f}% {np.mean(lee_pcts):>7.1f}% {np.mean(clark_pcts):>7.1f}%")
print(f"{'STDEV':<15} {np.std(walen_pcts):>7.1f}  {np.std(lee_pcts):>7.1f}  {np.std(clark_pcts):>7.1f}")

# Create comparison visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Bellevue LD 48 Precincts: Conservative Performance by Precinct\n' + 
             'Walen (State Senator) vs. Lee (Council Pos. 2) and Clark (Council Pos. 1)',
             fontsize=14, fontweight='bold')

# Plot 1: Walen % vs Lee %
ax1 = axes[0]
ax1.scatter(walen_pcts, lee_pcts, s=100, alpha=0.6, color='#1f77b4', edgecolor='black', linewidth=1.5, label='Walen vs. Lee')

# Add reference line (perfect correlation)
min_val = min(min(walen_pcts), min(lee_pcts))
max_val = max(max(walen_pcts), max(lee_pcts))
ax1.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.3, linewidth=1.5, label='Perfect Correlation')

ax1.set_xlabel('Walen % (State Senator - Conservative)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Lee % (Council Pos. 2 - Conservative)', fontsize=11, fontweight='bold')
ax1.set_title('Walen vs. Lee Correlation by Precinct', fontsize=12, fontweight='bold')
ax1.grid(alpha=0.3, linestyle='--')
ax1.legend(loc='upper left', fontsize=10)

# Add correlation coefficient
from scipy.stats import pearsonr
corr_walen_lee, _ = pearsonr(walen_pcts, lee_pcts)
ax1.text(0.98, 0.02, f'Correlation: {corr_walen_lee:.3f}', 
         transform=ax1.transAxes, ha='right', va='bottom',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=10)

# Plot 2: Walen % vs Clark %
ax2 = axes[1]
ax2.scatter(walen_pcts, clark_pcts, s=100, alpha=0.6, color='#ff7f0e', edgecolor='black', linewidth=1.5, label='Walen vs. Clark')

# Add reference line (perfect correlation)
min_val = min(min(walen_pcts), min(clark_pcts))
max_val = max(max(walen_pcts), max(clark_pcts))
ax2.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.3, linewidth=1.5, label='Perfect Correlation')

ax2.set_xlabel('Walen % (State Senator - Conservative)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Clark % (Council Pos. 1 - Conservative)', fontsize=11, fontweight='bold')
ax2.set_title('Walen vs. Clark Correlation by Precinct', fontsize=12, fontweight='bold')
ax2.grid(alpha=0.3, linestyle='--')
ax2.legend(loc='upper left', fontsize=10)

# Add correlation coefficient
corr_walen_clark, _ = pearsonr(walen_pcts, clark_pcts)
ax2.text(0.98, 0.02, f'Correlation: {corr_walen_clark:.3f}', 
         transform=ax2.transAxes, ha='right', va='bottom',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), fontsize=10)

plt.tight_layout()
plt.savefig('bellevue_ld48_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved to 'bellevue_ld48_analysis.png'")

# Analysis summary
print("\n" + "=" * 100)
print("STATISTICAL SUMMARY")
print("=" * 100 + "\n")

print(f"Walen vs. Lee Correlation: {corr_walen_lee:.3f}")
print(f"Walen vs. Clark Correlation: {corr_walen_clark:.3f}")
print(f"\nMean Conservative Vote %:")
print(f"  Walen (State Senator): {np.mean(walen_pcts):.1f}%")
print(f"  Lee (Council Pos. 2):  {np.mean(lee_pcts):.1f}%")
print(f"  Clark (Council Pos. 1): {np.mean(clark_pcts):.1f}%")

print(f"\nStandard Deviation:")
print(f"  Walen: {np.std(walen_pcts):.1f}%")
print(f"  Lee:   {np.std(lee_pcts):.1f}%")
print(f"  Clark: {np.std(clark_pcts):.1f}%")

print("\n✓ Analysis complete!")
