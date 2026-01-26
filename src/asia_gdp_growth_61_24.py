import pandas as pd
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

# List of selected Asian countries
asian_countries = [
    'Japan', 'Korea, Rep.', 'China', 'Hong Kong SAR, China', 'India', 'Singapore',
    'Malaysia', 'Thailand', 'Indonesia', 'Philippines', 'Iran, Islamic Rep.', 'Pakistan',
    'Bangladesh', 'Saudi Arabia', 'Oman', 'Iraq', 'Syrian Arab Republic', 'United Arab Emirates'
]

# Filter countries
df_asia = df[df['Country Name'].isin(asian_countries)].copy()

# Filter columns
year_cols = [f'{year} [YR{year}]' for  year in range(1961, 2025)]

# Create a clean dataframe with countries as rows and years as columns
data_matrix = df_asia.set_index('Country Name')[year_cols]

# Clean up year column names (remove World Bank format)
data_matrix.columns = [col.split()[0] for col in data_matrix.columns]

# Convert to numeric (this converts '..' to NaNs)
data_matrix = data_matrix.apply(pd.to_numeric, errors='coerce')

# CALCULATE CUMULATIVE GROWTH
rates_only = data_matrix.copy()
data_matrix['CUM.'] = ((rates_only / 100 + 1).prod(axis=1, skipna=True) - 1) * 100

# Sort countries alphabetically
data_matrix = data_matrix.sort_index()

# --- Friendly display names for heatmap ---
name_map = {
    "Hong Kong SAR, China": "Hong Kong",
    "Iran, Islamic Rep.": "Iran",
    "Korea, Rep.": "South Korea",
    "Syrian Arab Republic": "Syria",
    "United Arab Emirates": "UAE"
}

# Rename index for display only
data_matrix.rename(index=name_map, inplace=True)

# HEATMAP
fig, ax = plt.subplots(figsize=(30, 7))
sns.heatmap(
    data_matrix,
    vmin=-12,
    vmax=12,
    cmap='RdYlGn',
    center=0,
    annot=True,
    fmt='.1f',
    annot_kws={'size': 7},
    cbar=False,
    linewidths=0.5,
    linecolor='lightgray',
    mask=data_matrix.isna(),
    ax=ax,
)

# Show years both top and bottom
ax.tick_params(top=True, bottom=True, labeltop=True, labelbottom=True)

# Show country names both left and right
ax.yaxis.tick_right()
ax.tick_params(left=True, right=True, labelleft=True, labelright=True)

# TITLES AND LABELS
plt.title('GDP GROWTH RATES: ASIA (1961 - 2024)', fontsize=28, fontweight='bold', pad=10)
plt.xlabel('')
plt.ylabel('')
plt.xticks(rotation=90, fontweight='bold')
plt.yticks(rotation=0, fontweight='bold')
plt.tight_layout()

# SOURCE AND ATTRIBUTION
fig.text(0.98, -0.01, 'Source: World Bank, HeatMap by Sebastián S.G.',
         ha='right', va='bottom', fontsize=11, style='italic', color='gray')

# Save the figure
output_file = FIGURES_DIR / 'asia_gdp_growth_heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.show()

