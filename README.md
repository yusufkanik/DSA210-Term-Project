# Analysis of the Economic and Political Impacts on Cybercrime

## Motivation
 I am interested in cyber security. Cybercrimes are a huge part of cyber security, and it is an important research topic. I have always wondered what the factors that push people or organizations to commit cybercrimes are. While most cybersecurity research focuses on technical vulnerabilities, in this project I will be focusing on how economic and geopolitical factors are associated with cybercrime.

## Data Collection

This project integrates **three primary heterogeneous datasets** covering the years **2014–2026**, aligned geographically via **ISO3 codes** and temporally by **year/month**.  

### 1. Cyber Incident Data (General Activity)

- **Source:** Cyber Events Tracker (Consolidated Incident Log)  
- **Frequency:** Event-based  
- **Collection Method:** Static CSV retrieval and parsing  
- **Key Features for Analysis:**
    
  - `event_date` & `year`: For temporal alignment  
  - `motive`: Categorizes attacks as **Financial**, **Protest**, or **Espionage**  
  - `actor_type`: Distinguishes between **Criminal**, **Nation-State**, and **Hacktivist**  
  - `country` & `actor_country`: For mapping cross-border aggression  

### 2. Geopolitical Cyber Incidents (EuRepoC)

- **Source:** European Repository of Cyber Incidents (EuRepoC)  
- **Frequency:** Event-based (high-resolution coding)  
- **Collection Method:** Expert-curated repository (CSV export)  
- **Key Features for Analysis:**
  
  - `weighted_intensity`: Quantifies the severity/damage of the attack  
  - `offline_conflict_intensity`: Links the cyber event to physical military or political tension (e.g., HIIK intensity scores)  
  - `political_response_type`: Tracks if the incident led to sanctions or diplomatic protests  
  - `receiver_country_alpha_2_code`: Facilitates merging with other national datasets  

### 3. Socio-Economic Indicators (World Bank)

- **Source:** World Bank Open Data (World Development Indicators)  
- **Frequency:** Annual  
- **Collection Method:** API retrieval (`wbgapi`) and CSV export  
- **Key Features for Analysis:**
   
  - `GDP per capita (current US$)`: Measures the economic "target value" of a country  
  - `GDP growth (annual %)` & `Inflation (CPI)`: Indicators of economic instability that may trigger criminal activity
  - `Political Stability`: Measures the likelihood of political instability or politically-motivated violence (merged via CSV)
  - `Country Code`: Primary key for relational joining (ISO3)
 
 ## Methodology

This project employs a **quantitative, correlation-based approach** to analyze the impact of socio-economic and political volatility on global cyber activity. The research will be executed in the following phases:

### 1. Data Integration & Preprocessing

The primary technical challenge involves merging **event-based cyber data** with **annual economic indicators**. Python (`pandas`) will be used to:

The dataset generation (`scripts/final_data.py`) involves the following steps:

* **Ingestion & Scope:** Loading Maryland and EuRepoC cyber datasets, filtered to match 2014-2026 timeline.
* **Standardization:** Cleaning and converting country names into standard ISO-3 codes using `pycountry`and fuzzy search, and extracting event years.
* **Economic Integration:** Fetching GDP and Inflation using the World Bank API (`wbgapi`), while integrating Political Stability via a manually downloaded CSV export (as the API for this specific indicator could not be used). This step also required significant data cleaning, such as handling static dataset merges and parsing text-based stability metrics into functional `float64` numeric types.
* **Merging & Imputation:** Joining the cyber and economic data based on country code and year, **forward-filling** is used to handle missing economic data, which automatically carries over a country's last known value (like the previous year's GDP) to fill in blank years so the statistical tests don't fail.

### 2. Exploratory Data Analysis (EDA)

- Visualization is performed using Matplotlib and Seaborn to explore the macroeconomic drivers of cyber warfare:
* **Time-Series Trends:** A temporal line chart tracking the volume of top attack motives (e.g., Financial, Protest) from 2014 to 2026, revealing macro-shifts in the global threat landscape.
* **Macro Bubble Plots:** Mapping GDP per Capita against total attack volume to visualize the "Wealthy Target" effect, with bubble sizes representing the real-world intensity of the attacks.
* **Correlation Heatmaps:** Analyzing the statistical relationships between baseline economic indicators (GDP, Political Stability) and cyber metrics (Attack Volume, Attack Intensity).
* **Motive & Actor Distributions:** Tracking the dominant cyber threat actors and their primary attack motives globally.

## Hypothesis Tests

### Hypothesis 1: Political Stability Shock (Paired T-Test)

* **H₀:** The average number of "Protest" motivated attacks is the same the year before vs. the year of a sudden drop in a country’s "Political Stability" score.
* **Hₐ:** The average number of "Protest" motivated attacks is greater in the year of a stability drop than in the year prior.
* **Method:** Paired T-Test to compare the "before" (Year - 1) and "after" (Year 0) states of the exact same country.
- **Result:** **Not Statistically Significant (Fail to Reject H₀)**
* **Test Statistics:** Paired T-Test (n=387 shocks) | T-Statistic: `0.5429` | P-Value: `0.2938`
* **Conclusion:** Sudden drops in political stability do not universally trigger an immediate surge in cyber protests. The high variance indicates that hacktivist responses are highly localized. A stability drop might cause a massive cyber reaction in one country, but zero response in another. 



### Hypothesis 2: Observed vs. Expected Attack Motives (Chi-Square Statistic)

- **H₀:** The observed frequencies of attack motives (**Financial, Protest, Espionage**) during an economic crisis follow the expected historical distribution.  
- **Hₐ:** The observed frequencies significantly deviate from the expected distribution (e.g., Financial motives appear more than expected).  
- **Method:** Chi-Square Statistic to measure the discrepancy between actual crisis data and historical baseline data.
- **Result:** **Highly Statistically Significant (Reject H₀)**
* **Test Statistics:** Chi-Square Test | Chi-Square Statistic: `3081.9728` | Degrees of Freedom: `4` | P-Value: `0.0000e+00`
* **Conclusion:** Severe economic crises (inflation > 10%) fundamentally shift hacker motivations. During normal conditions, threat actors prioritize **Financial** gain (**9,109** baseline attacks vs. **1,170** protest attacks). However, during an economic crisis, financial attacks plummet to just **148** incidents, while **Protest** attacks heavily dominate the landscape. During financial panic, hackers abandon monetary theft to weaponize the internet for protest and disruption.



### Hypothesis 3: Target Country Wealth by Attack Motive
* **H₀:** The average wealth (GDP) of a target country is the same regardless of the cyber attack's motive.
* **Hₐ:** The average wealth (GDP) of a target country differs significantly based on the attack motive.
* **Method:** One-Way ANOVA (Analysis of Variance) to compare the mean GDP across the top three distinct attack motives, visualized using a log-scaled boxplot.
* **Result:** **Highly Statistically Significant (Reject H₀)**
* **Test Statistics:** One-Way ANOVA | F-Statistic: `1574.6477` | P-Value: `0.0000e+00`
* **Conclusion:** There is a definitive link between the economic stature of a target nation and the motive of the cyber attack. Financial threat actors disproportionately target wealthier nations (higher GDP), likely seeking higher "return on investment." Conversely, Protest and Political-Espionage attacks are distributed more broadly across lower-GDP nations, indicating that these attacks are driven by geopolitical friction rather than purely economic gain.


## Machine Learning

### 1. Predicting Political Stability (Supervised Learning - Logistic Regression)
* **Method:** **Logistic Regression** was used to classify whether a nation's environment is **Stable** or **Unstable (High Risk)** based on cyber conflict features (Intensity, Motive, Actor Type).
* **Results (Accuracy: 58.17%):** While political stability is influenced by many non-digital factors, the model revealed critical "Impact Coefficients":
    * **Instability Drivers:** Cyber attacks linked to **Physical Warfare (Offline Conflict)**, **Sabotage**, and **Protests** are the strongest predictors of a destabilizing environment.
    * **The Espionage Paradox:** Surprisingly, **Espionage** (Political and Industrial) is negatively correlated with instability. These "silent" operations require a stable target to remain undetected; chaos would hinder intelligence collection.
* **Conclusion:** Cyber warfare acts as a catalyst. Stable nations are targets for "silent" espionage, whereas unstable nations face "loud" sabotage and hybrid warfare.


### 2. Forecasting Attack Motives (Supervised Learning - Random Forest)
* **Method:** A **Random Forest Classifier** was trained to predict the primary **Motive** of a cyber attack (Financial, Protest, Espionage) based on a country's macroeconomic signature (**GDP per Capita** and **Inflation**).
* **Results (Accuracy: 86.25%):**
    * **Financial (97% Recall):** The model excels at identifying profit-driven attacks, confirming that national wealth and inflation are the primary magnets for global cybercrime.
    * **Protest (61% Recall):** Economic distress triggers a mathematically predictable level of hacktivism and protest-motivated cyber activity.
    * **Espionage (22% Recall):** The model struggled here, proving that state-sponsored espionage is driven by long-term military strategy rather than immediate macroeconomic indicators.
* **Conclusion:** Macroeconomics is a near-perfect predictor for profit-motivated cybercrime, but insufficient for forecasting high-level state-sponsored espionage.


### 3. Geopolitical Risk Profiling (Unsupervised Learning - K-Means Clustering)
* **Method:** **K-Means Clustering** was applied to group countries based on their economic stature (GDP), inflation rates, and cyber target frequency to identify hidden patterns without predefined labels.
* **Results:** The model successfully identified three distinct "Geopolitical Risk Clusters":
    1.  **Stable Wealthy Targets:** High-GDP nations with high attack frequency but low inflation.
    2.  **Volatile Emerging Markets:** Countries with moderate GDP and high inflation, attracting different motive profiles (predominantly protests).
    3.  **Low-Intensity Zones:** Nations with minimal cyber-economic correlation.
* **Conclusion:** Cybercrime patterns are not uniform across the globe; a country's economic "cluster" is a strong indicator of the specific threat landscape it will inhabit.