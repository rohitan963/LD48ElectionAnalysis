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

print("=" * 80)
print("BELLEVUE LD 48 ELECTION ANALYSIS")
print("=" * 80)

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

# Collect results by race
race_results = {}

for race_name, race_query in races.items():
    race_data = bellevue_data[bellevue_data['Race'] == race_query]
    
    # Get vote counts for candidates
    prog_votes = race_data[race_data['CounterType'] == candidates[race_name]['progressive']]['SumOfCount'].sum()
    cons_votes = race_data[race_data['CounterType'] == candidates[race_name]['conservative']]['SumOfCount'].sum()
    total_votes = prog_votes + cons_votes
    
    # Calculate percentages
    prog_pct = (prog_votes / total_votes * 100) if total_votes > 0 else 0
    cons_pct = (cons_votes / total_votes * 100) if total_votes > 0 else 0
    
    race_results[race_name] = {
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

# Print topline numbers
print("\nTOPLINE RESULTS (Bellevue LD 48 Precincts Only)\n")

for race_name in ['State Senator', 'City Council Position No. 1', 'City Council Position No. 2']:
    results = race_results[race_name]
    prog = results['progressive']
    cons = results['conservative']
    
    print(f"{race_name}:")
    print(f"  {prog['name']:20} (Progressive): {prog['votes']:5} votes ({prog['pct']:5.1f}%)")
    print(f"  {cons['name']:20} (Conservative):  {cons['votes']:5} votes ({cons['pct']:5.1f}%)")
    print(f"  Total Votes: {results['total']}\n")

# Create comparison visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Bellevue LD 48 Precincts: Conservative Performance Comparison\n' + 
             'Walen (State Senator) vs. Lee (Council Pos. 2) and Clark (Council Pos. 1)',
             fontsize=14, fontweight='bold')

# Plot 1: Walen % vs Lee %
ax1 = axes[0]
walen_pct = race_results['State Senator']['conservative']['pct']
lee_pct = race_results['City Council Position No. 2']['conservative']['pct']
clark_pct = race_results['City Council Position No. 1']['conservative']['pct']

candidates_list = ['Walen\n(State Senator)', 'Lee\n(Council Pos. 2)', 'Clark\n(Council Pos. 1)']
percentages = [walen_pct, lee_pct, clark_pct]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

bars1 = ax1.bar(candidates_list, percentages, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Conservative Vote Percentage (%)', fontsize=11, fontweight='bold')
ax1.set_ylim(0, 100)
ax1.set_title('Conservative Candidates Performance', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add percentage labels on bars
for bar, pct in zip(bars1, percentages):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Plot 2: Scatter plot showing correlation
ax2 = axes[1]
ax2.scatter([walen_pct], [lee_pct], s=200, alpha=0.6, color='#1f77b4', edgecolor='black', linewidth=2, label='Walen vs. Lee')
ax2.scatter([walen_pct], [clark_pct], s=200, alpha=0.6, color='#ff7f0e', edgecolor='black', linewidth=2, label='Walen vs. Clark')

# Add reference line (45 degree - perfect correlation)
ax2.plot([30, 70], [30, 70], 'k--', alpha=0.3, linewidth=1, label='Perfect Correlation')

ax2.set_xlabel('Walen % (State Senator - Conservative)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Other Conservative Candidates %', fontsize=11, fontweight='bold')
ax2.set_xlim(30, 70)
ax2.set_ylim(30, 70)
ax2.set_title('Conservative Vote Alignment', fontsize=12, fontweight='bold')
ax2.grid(alpha=0.3, linestyle='--')
ax2.legend(loc='upper left', fontsize=10)

# Add annotations
ax2.annotate('Lee', xy=(walen_pct, lee_pct), xytext=(walen_pct + 1, lee_pct - 2),
            fontsize=10, fontweight='bold')
ax2.annotate('Clark', xy=(walen_pct, clark_pct), xytext=(walen_pct + 1, clark_pct + 2),
            fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('bellevue_ld48_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved to 'bellevue_ld48_analysis.png'")

# Create a detailed comparison table
print("\n" + "=" * 80)
print("DETAILED VOTE COMPARISON")
print("=" * 80 + "\n")

comparison_data = {
    'Race': [
        'State Senator',
        'Council Position No. 1',
        'Council Position No. 2'
    ],
    'Progressive': [
        f"{race_results['State Senator']['progressive']['name']}: {race_results['State Senator']['progressive']['votes']} ({race_results['State Senator']['progressive']['pct']:.1f}%)",
        f"{race_results['City Council Position No. 1']['progressive']['name']}: {race_results['City Council Position No. 1']['progressive']['votes']} ({race_results['City Council Position No. 1']['progressive']['pct']:.1f}%)",
        f"{race_results['City Council Position No. 2']['progressive']['name']}: {race_results['City Council Position No. 2']['progressive']['votes']} ({race_results['City Council Position No. 2']['progressive']['pct']:.1f}%)"
    ],
    'Conservative': [
        f"{race_results['State Senator']['conservative']['name']}: {race_results['State Senator']['conservative']['votes']} ({race_results['State Senator']['conservative']['pct']:.1f}%)",
        f"{race_results['City Council Position No. 1']['conservative']['name']}: {race_results['City Council Position No. 1']['conservative']['votes']} ({race_results['City Council Position No. 1']['conservative']['pct']:.1f}%)",
        f"{race_results['City Council Position No. 2']['conservative']['name']}: {race_results['City Council Position No. 2']['conservative']['votes']} ({race_results['City Council Position No. 2']['conservative']['pct']:.1f}%)"
    ]
}

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# Analysis summary
print("\n" + "=" * 80)
print("KEY INSIGHTS")
print("=" * 80 + "\n")

# Calculate vote spreads
slatter_spread = race_results['State Senator']['progressive']['pct'] - race_results['State Senator']['conservative']['pct']
briar_spread = race_results['City Council Position No. 2']['progressive']['pct'] - race_results['City Council Position No. 2']['conservative']['pct']
bhargava_spread = race_results['City Council Position No. 1']['progressive']['pct'] - race_results['City Council Position No. 1']['conservative']['pct']

print(f"Progressive margin in State Senator race (Slatter vs. Walen): {slatter_spread:+.1f}%")
print(f"Progressive margin in Council Pos. 2 race (Briar vs. Lee):    {briar_spread:+.1f}%")
print(f"Progressive margin in Council Pos. 1 race (Bhargava vs. Clark): {bhargava_spread:+.1f}%")

# Compare conservative performance
walen_vs_lee = race_results['State Senator']['conservative']['pct'] - race_results['City Council Position No. 2']['conservative']['pct']
walen_vs_clark = race_results['State Senator']['conservative']['pct'] - race_results['City Council Position No. 1']['conservative']['pct']

print(f"\nConservative performance differential:")
print(f"  Walen performed {walen_vs_lee:+.1f} percentage points vs. Lee")
print(f"  Walen performed {walen_vs_clark:+.1f} percentage points vs. Clark")

print("\n✓ Analysis complete!")
