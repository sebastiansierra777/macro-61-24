import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Define paths relative to project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
FIGURES_DIR = PROJECT_ROOT / 'figures'

# Ensure figures directory exists
FIGURES_DIR.mkdir(exist_ok=True)

# Load the Excel data
data_file = DATA_DIR / 'P_Data_Extract_From_World_Development_Indicators.xlsx'
df = pd.read_excel(data_file)

# Define the Latin American countries you want
latam_countries = [
    'Argentina', 'Brazil', 'Bolivia', 'Chile', 'Colombia',
    'Cuba', 'Dominican Republic', 'Ecuador', 'Mexico',
    'Peru', 'Panama', 'Paraguay', 'Uruguay', 'Venezuela, RB'
]

# Filter for your countries
df_latam = df[df['Country Name'].isin(latam_countries)].copy()

# Get year columns (1961-2024 only)
year_cols = [col for col in df.columns if (col.startswith('19') or col.startswith('20')) and not col.startswith('1960')]

# Create a clean dataframe with countries as rows and years as columns
data_matrix = df_latam.set_index('Country Name')[year_cols]

# Clean up year column names (remove World Bank format)
data_matrix.columns = [col.split()[0] for col in data_matrix.columns]

# Convert to numeric (this automatically handles '..' as NaN)
data_matrix = data_matrix.apply(pd.to_numeric, errors='coerce')

# Calculate cumulative growth using compound formula
# (1 + r1/100) * (1 + r2/100) * ... - 1, then convert back to percentage
data_matrix['Total'] = ((data_matrix / 100 + 1).prod(axis=1, skipna=True) - 1) * 100

# Sort countries alphabetically
data_matrix = data_matrix.sort_index()

# Create the heatmap
fig, ax = plt.subplots(figsize=(30, 7))
sns.heatmap(
    data_matrix,
    vmin=-12,
    vmax=12,
    cmap='RdYlGn',
    center=0,
    annot=True,
    fmt='.1f',
    annot_kws={'size': 8},
    cbar=False,
    linewidths=0.5,
    linecolor='lightgray',
    mask=data_matrix.isna(),
    ax=ax
)

# Show country names on both left and right
ax.yaxis.tick_right()
ax.tick_params(left=True, right=True, labelleft=True, labelright=True)

plt.title('GDP Growth Rates: Latin America (1961-2024)', fontsize=21, fontweight='bold', pad=20)
plt.xlabel('')
plt.ylabel('')
plt.xticks(rotation=90, fontweight='bold')
plt.yticks(rotation=0, fontweight='bold')
plt.tight_layout()

# Add source attribution at bottom right
fig.text(0.98, -0.01, 'Source: World Bank, HeatMap by Sebastián S.G.',
         ha='right', va='bottom', fontsize=11, style='italic', color='gray')

# Save the figure
output_file = FIGURES_DIR / 'latam_gdp_growth_heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.show()





