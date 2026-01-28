import pandas as pd
from pathlib import Path

# PATHS
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'processed'

# LOAD EXCEL
data_file = DATA_DIR / 'P_Data_Extract_From_World_Development_Indicators_GDP_Per_Capita_PPP.xlsx'
df = pd.read_excel(data_file)

# TARGET YEARS
years = [1990, 2000, 2010, 2024]

rankings = {}

for year in years:
    year_col = f'{year} [YR{year}]'

    rankings[year] = (
        df[['Country Name', year_col]]
        .rename(columns={year_col: str(year)})
        .replace('..', pd.NA)
        .dropna()
        .assign(**{str(year): lambda x: pd.to_numeric(x[str(year)])})
        .sort_values(str(year), ascending=False)
        .reset_index(drop=True)
        .assign(Rank=lambda x: range(1, len(x) + 1))
        .assign(**{str(year): lambda x: x[str(year)].round(0).astype(int)})
        [['Rank', 'Country Name', str(year)]]
    )

# WRITE RANKINGS TO EXCEL
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_file = OUTPUT_DIR / 'gdp_pc_ppp_ranks.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for year, ranked_df in rankings.items():
        ranked_df.to_excel(writer, sheet_name=f'Year_{year}', index=False)

print(f"Rankings exported to: {output_file}")













