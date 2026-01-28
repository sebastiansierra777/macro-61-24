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

# Load Excel
data_file = DATA_DIR / 'P_Data_Extract_From_World_Development_Indicators_GDP_Per_Capita_PPP.xlsx'
df = pd.read_excel(data_file)

# Extract Asian countries
asian_countries = [
    'Japan', 'Korea, Rep.', 'China', 'Hong Kong SAR, China', 'India', 'Singapore',
    'Malaysia', 'Thailand', 'Indonesia', 'Philippines', 'Iran, Islamic Rep.', 'Pakistan',
    'Bangladesh', 'Saudi Arabia', 'Oman', 'Iraq', 'Syrian Arab Republic', 'United Arab Emirates'
]

# Filter countries
df_asia = df[df['Country Name'].isin(asian_countries)].copy()

# Filter year columns
year_cols = [f'{year} [YR{year}]' for year in range(1990, 2025)]

# DATA MATRIX
data_matrix = df_asia.set_index("Country Name")[year_cols]

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
    vmin=1500,
    vmax=70000,
    cmap='YlGn',
    # center
    annot=True,
    fmt=',.0f',
    annot_kws={'size': 8},
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

# TITLE & LABELS
plt.title("ASIA: GDP PER CAPITA 1990 - 2024 (PPP Constant 2021 Int$)",
          fontsize=21, fontweight='bold', pad=10)
plt.xlabel('')
plt.ylabel('')
plt.xticks(rotation=90, fontweight='bold')
plt.yticks(rotation=0, fontweight='bold')
plt.tight_layout()

# SOURCE & ATTRIBUTION
fig.text(0.98, -0.01, "Source: World Bank, HeatMap by Sebastián S.G.",
         ha='right', va='bottom', fontsize=12, style='italic', color='gray')

# Save figure
output_file = FIGURES_DIR / 'asia_gdp_pc_ppp_heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"figure saved to: {output_file}")

plt.show()




