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

# Load the Excel Data
data_file = DATA_DIR / 'P_Data_Extract_From_World_Development_Indicators_GDP_Per_Capita_PPP.xlsx'
df = pd.read_excel(data_file)

# Extract Latin American countries
latam_countries = [
    'Argentina', 'Brazil', 'Bolivia', 'Chile', 'Colombia', 'Dominican Republic',
    'Ecuador', 'Mexico', 'Peru', 'Panama', 'Paraguay', 'Uruguay'
]

# Filter countries
df_latam = df[df['Country Name'].isin(latam_countries)].copy()

# Filter year columns
year_cols = [f'{year} [YR{year}]' for year in range(1990, 2025)]

# DataMatrix with countries as rows and years as columns
data_matrix = df_latam.set_index('Country Name')[year_cols]

# Clean up year columns (remove World Bank format)
data_matrix.columns = [col.split()[0] for col in data_matrix.columns]

# Convert to numeric (automatically handles '..' as NaN)
data_matrix = data_matrix.apply(pd.to_numeric, errors='coerce')

# Sort countries alphabetically
data_matrix = data_matrix.sort_index()

# HEATMAP
fig, ax = plt.subplots(figsize=(21, 7))
sns.heatmap(
    data_matrix,
    # vmin
    # vmax
    cmap='YlGn',
    # center
    annot=True,
    fmt=',.0f',
    annot_kws={'size': 9},
    cbar=False,
    linewidths=.5,
    linecolor='lightgray',
    mask=data_matrix.isna(),
    ax=ax
)

# Show years both on top and bottom
ax.tick_params(top=True, bottom=True, labeltop=True, labelbottom=True)

# Show country names both left and right
ax.yaxis.tick_right()
ax.tick_params(left=True, right=True, labelleft=True, labelright=True)

plt.title('LATIN AMERICA: GDP PER CAPITA 1990 - 2024 (PPP Constant 2021 Int$)',
          fontsize=21, fontweight='bold', pad=10)
plt.xlabel('')
plt.ylabel('')
plt.xticks(rotation=90, fontweight='bold')
plt.yticks(rotation=0, fontweight='bold')
plt.tight_layout()

# Source & Attribution
fig.text(0.98, -0.01, 'Source: World Bank, HeatMap by Sebastián S.G.',
         ha='right', va='bottom', fontsize=12, style='italic', color='gray')

# Save the figure
output_file = FIGURES_DIR / 'latam_gdp_pc_ppp_heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"figure saved to: {output_file}")
plt.show()



