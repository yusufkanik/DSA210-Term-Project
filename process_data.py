import pandas as pd
import wbgapi as wb
import pycountry
import warnings

warnings.filterwarnings('ignore')

CYBER_MARYLAND_FILE = 'datasets/raw/cyber_events_2026-03-31.csv'
CYBER_EUREPOC_FILE = 'datasets/raw/eurepoc_global_dataset_1_3.csv'
POLITICAL_STABILITY_FILE = 'datasets/raw/political_stability.csv'

country_cache = {}

def get_iso3_robust(name): #standardize the country names
    if pd.isna(name) or str(name).strip() == '' or str(name).lower() == 'nan': 
        return None
    
    # Remove alternate names for example:"Iran (Islamic Republic of)" -> "Iran"
    clean_name = str(name).split('(')[0].strip() 
    if clean_name in country_cache: 
        return country_cache[clean_name]
    
    # If the country is already a 2-letter code, convert it to 3-letter
    if len(clean_name) == 2:
        try:
            # Fuzzy search guesses the country if the spelling is slightly off. 
            # grabs the most likely match from the search results.
            res = pycountry.countries.get(alpha_2=clean_name.upper()).alpha_3
            country_cache[clean_name] = res
            return res
        except: pass
    try:
        res = pycountry.countries.search_fuzzy(clean_name)[0].alpha_3
        country_cache[clean_name] = res
        return res
    except:
        country_cache[clean_name] = None
        return None
    


print("1. Processing Cyber Incident Files...")
df_md = pd.read_csv(CYBER_MARYLAND_FILE, low_memory=False)
df_md['iso3'] = df_md['country'].apply(get_iso3_robust)
df_md['event_date'] = pd.to_datetime(df_md['event_date'], errors='coerce')
df_md['year'] = df_md['event_date'].dt.year

df_eu = pd.read_csv(CYBER_EUREPOC_FILE, low_memory=False)
df_eu['iso3'] = df_eu['receiver_country_alpha_2_code'].apply(get_iso3_robust)
df_eu['start_date'] = pd.to_datetime(df_eu['start_date'], dayfirst=True, errors='coerce')
df_eu['year'] = df_eu['start_date'].dt.year

# Combine both datasets into one combined DataFrame
cyber_combined = pd.concat([
    df_md[['iso3', 'year', 'motive', 'actor_type', 'event_type']].assign(source='Maryland'),
    df_eu[['iso3', 'year', 'incident_type', 'weighted_intensity', 'offline_conflict_intensity']].rename(columns={'incident_type':'motive'}).assign(source='EuRepoC')
], ignore_index=True)

print("2. Fetching World Bank indicators...")

# Fetch GDP and Inflation (Main API Database)
ind_wdi = {'NY.GDP.PCAP.CD': 'gdp_per_capita', 'FP.CPI.TOTL.ZG': 'inflation_cpi'}
wb_wdi = wb.data.DataFrame(list(ind_wdi.keys()), time=range(2014, 2025)).reset_index()

# Fetch Political Stability (LOCAL CSV)
ind_wgi = {'PV.EST': 'political_stability'}
try:
    # Read the downloaded CSV
    wgi_raw = pd.read_csv(POLITICAL_STABILITY_FILE)
    
    # Rename 'Country Code' column to 'economy'
    wgi_raw = wgi_raw.rename(columns={'Country Code': 'economy'})
    
    # Set the indicator code to 'PV.EST' for the system to recognize it
    wgi_raw['series'] = 'PV.EST'
    
    # Rename columns from "2014 [YR2014]" to just "YR2014"
    rename_dict = {f"{y} [YR{y}]": f"YR{y}" for y in range(2014, 2025)}
    wgi_raw = wgi_raw.rename(columns=rename_dict)
    
    # Keep only the columns needed
    cols_to_keep = ['economy', 'series'] + [f"YR{y}" for y in range(2014, 2025) if f"YR{y}" in wgi_raw.columns]
    wb_wgi = wgi_raw[cols_to_keep]

    # Combine both datasets
    wb_reset = pd.concat([wb_wdi, wb_wgi], ignore_index=True)
    print("Successfully loaded Political Stability from local CSV bypass!")
    
except Exception as e:
    print(f"Warning: Could not load Political Stability. Error: {e}")
    wb_reset = wb_wdi

# Combine dictionary to rename columns later
indicators = {**ind_wdi, **ind_wgi}

# Reshape World Bank Data
# Find all column names that represent years
year_cols = [c for c in wb_reset.columns if c.startswith('YR')]

# Reshape the data from wide to long so 'year' is a single column instead of multiple
wb_long = pd.melt(wb_reset, id_vars=['economy', 'series'], value_vars=year_cols, var_name='year', value_name='value')

wb_long['year'] = wb_long['year'].str.replace('YR', '').astype(int)

# Force the value column to be numeric before pivoting
wb_long['value'] = pd.to_numeric(wb_long['value'], errors='coerce')

# Pivot the data so each indicator gets its own column
wb_final = wb_long.pivot_table(index=['economy', 'year'], columns='series', values='value').reset_index()
wb_final.rename(columns=indicators, inplace=True)

wb_final = wb_final.sort_values(['economy', 'year'])

# Impute missing World Bank data using forward-fill (carrying previous year's data forward)
for col in indicators.values():
    if col in wb_final.columns:
        # Convert values to numeric, turning missing dots ("..") into NaNs before forward filling
        wb_final[col] = pd.to_numeric(wb_final[col], errors='coerce')
        
        wb_final[col] = wb_final.groupby('economy')[col].ffill()

print("3. Joining datasets...")

# Merge the cyber data with the economic data based on country code (iso3/economy) and year
final_df = pd.merge(cyber_combined, wb_final, left_on=['iso3', 'year'], right_on=['economy', 'year'], how='left')

final_df = final_df.sort_values(['iso3', 'year'])

# Apply one final forward-fill to ensure all rows in the merged dataset have economic context
for col in indicators.values():
    if col in final_df.columns:
        final_df[col] = final_df.groupby('iso3')[col].ffill()

final_df = final_df.dropna(subset=['iso3'])

# Filter the final dataset to perfectly match the project scope (2014-2026)
final_df = final_df[final_df['year'] >= 2014]

final_df.to_csv('datasets/processed/processed_cyber_data.csv', index=False)
print(f"Success! Final dataset saved with {len(final_df)} rows.")