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


## Methodological Note: Downsampling & The "Large N Problem"

Initial statistical tests (Hypothesis 2 and Hypothesis 3) on the complete dataset yielded a p-value of exactly `0.0`. This is a computational limitation (float underflow) caused by an "overpowered test," where massive sample sizes artificially inflate test statistics. To report mathematically valid p-values:

* **Statistical Testing:** We applied **random downsampling (n=600)** exclusively for the calculations. This resolved the overpowered test issue and yielded accurate, computable scientific p-values.
* **Visualization:** All charts and plots continue to use the **full dataset** to accurately represent the true, unmanipulated data distribution.


### Hypothesis 2: Observed vs. Expected Attack Motives (Chi-Square Statistic)

- **H₀:** The observed frequencies of attack motives (**Financial, Protest, Espionage**) during an economic crisis follow the expected historical distribution.  
- **Hₐ:** The observed frequencies significantly deviate from the expected distribution (e.g., Financial motives appear more than expected).  
- **Method:** Chi-Square Statistic to measure the discrepancy between actual crisis data and historical baseline data.
- **Result:** **Highly Statistically Significant (Reject H₀)**
* **Test Statistics:** Chi-Square Test | Chi-Square Statistic: `105.2180` | Degrees of Freedom: `4` | P-Value: `7.6109e-22`
* **Conclusion:** Severe economic crises (inflation > 10%) fundamentally shift hacker motivations. During normal conditions, threat actors prioritize **Financial** gain. However, during an economic crisis, financial attacks plummet to just **148** incidents, while **Protest** attacks heavily dominate the landscape. During financial panic, hackers abandon monetary theft to weaponize the internet for protest and disruption.



### Hypothesis 3: Target Country Wealth by Attack Motive
* **H₀:** The average wealth (GDP) of a target country is the same regardless of the cyber attack's motive.
* **Hₐ:** The average wealth (GDP) of a target country differs significantly based on the attack motive.
* **Method:** One-Way ANOVA (Analysis of Variance) to compare the mean GDP across the top three distinct attack motives, visualized using a log-scaled boxplot.
* **Result:** **Highly Statistically Significant (Reject H₀)**
* **Test Statistics:** One-Way ANOVA | F-Statistic: `99.3725` | P-Value: `5.5887e-38`
* **Conclusion:** There is a definitive link between the economic stature of a target nation and the motive of the cyber attack. Financial threat actors disproportionately target wealthier nations (higher GDP), likely seeking higher "return on investment." Conversely, Protest and Political-Espionage attacks are distributed more broadly across lower-GDP nations, indicating that these attacks are driven by geopolitical friction rather than purely economic gain.


## Machine Learning

### 1. Predicting Political Stability (Supervised Learning - Model Comparison & Tuning)
* **Method:** Both **Logistic Regression** and **Random Forest Classifier** were optimized via `GridSearchCV` to classify whether a nation's environment is **Stable** or **Unstable (High Risk)** based on cyber conflict features (Intensity, Motive, Actor Type).

* **Results & Performance Plateau (~58%):** The hyperparameter tuning revealed a strict informational ceiling. Tuned Logistic Regression achieved **57.97%** test accuracy, while Random Forest reached **58.06%**. This identical performance, combined with a low **Recall (~30%)** for the Unstable class, indicates severe **High Bias (Underfitting)**. It proves that cyber metadata alone provides a complementary signal but lacks the dense variance to independently predict macro-political risk.

* **Key Feature Insights:**
    * **Instability Drivers:** Cyber attacks directly intersecting with active physical conflicts (**`offline_conflict_intensity_Yes`**), alongside high-disruption motives like **Sabotage** and **Protest**, serve as the strongest predictors of a destabilizing political environment.
    * **The Espionage Paradox:** Operations such as **Industrial Espionage** and **Data Theft & Doxing** heavily correlate with stable environments. These "silent" threat actors require a functioning state apparatus to systematically harvest intelligence; structural chaos would only hinder data collection and expose their operations.

* **Conclusion:** Cyber warfare acts primarily as a diagnostic catalyst rather than an isolated cause. Stable nations are targets for silent espionage, whereas unstable nations face loud sabotage and hybrid warfare. To break past the 58% predictive barrier, future iterations must fuse cyber telemetry with external macroeconomic and institutional indicators.


### 2. Forecasting Attack Motives (Supervised Learning - Model Comparison & Tuning)
* **Method:** Both **Logistic Regression** and a **Random Forest Classifier** were optimized via `GridSearchCV` to predict the primary **Motive** of a cyber attack (Financial, Protest, Political-Espionage) based on a country's macroeconomic signature (**GDP per Capita** and **Inflation**).

* **Results (Best Accuracy: 79.52%):** The non-linear Random Forest significantly outperformed the linear Logistic Regression baseline (67.48%), proving that macroeconomic thresholds have a non-linear relationship with cyber target selection:

    * **Financial (86% Recall):** The model excels at identifying profit-driven attacks, confirming that national wealth and inflation fluctuations are the primary baselines for commercial cybercrime.

    * **Protest (67% Recall):** Macro-level economic distress triggers a mathematically predictable and traceable level of ideological hacktivism and protest-motivated cyber activity.

    * **Political-Espionage (40% Recall):** The model faced structural limitations here, proving that state-sponsored espionage is driven by long-term geopolitical and military strategies rather than immediate domestic economic indicators.

* **Conclusion:** Macroeconomics serves as a highly reliable framework for predicting profit-motivated cybercrime and localized hacktivism, but remains structurally insufficient for forecasting high-level, state-sponsored cyber espionage.


### 3. Global Cyber Threat Zoning (Unsupervised Learning - K-Means)
* **Method:** A **K-Means Clustering** algorithm was trained using standard scaled features: **Log GDP per Capita**, **Inflation (CPI)**, and **Log Total Attacks** to automatically segment nations into distinct strategic risk profiles. The optimal cluster count ($k=3$) was mathematically justified using the **Elbow Method**.

* **Results & Cluster Segments:**
    * **Zone A (High-Value Targets):** Wealthy, stable economies (Median GDP: ~$27.6k, Inflation: ~3.25%) that act as financial magnets, absorbing the highest volume of cyber operations (Median: 48 attacks).

    * **Zone B (Low-Profile Passives):** Developing nations with lower digital asset density, resulting in minimal cyber target visibility (Median: 6 attacks).

    * **Zone C (Hyperinflation Crisis Zones):** Effectively isolated volatile outlier nations suffering from severe hyperinflation (Median CPI: ~138.8%). Despite lower GDP, they exhibit a high vulnerability vector (Median: 30 attacks), linking macro-collapse to cyber exposure.

* **Conclusion:** Unsupervised clustering proves that a nation's cyber-risk landscape is explicitly bounded by its macroeconomic health; capital-dense nations face steady commercial threats, while hyperinflationary environments trigger structural security vulnerabilities.


## Limitations and Future Work

### Limitations
* **Temporal Resolution Mismatch:** Merging event-based cyber incidents (recorded daily/monthly) with macroeconomic data (available only as annual global updates) forces the models to assume a static economic environment throughout a given year. This limits the ability to capture immediate, real-time cyber reactions to sudden financial shifts.
* **The Informational Ceiling (Feature Sparsity):** As demonstrated by the 58% performance plateau in political stability predictions, utilizing purely cyber metadata (intensity, attacker type, motive) creates an underfitted model. Cyber telemetry is an excellent diagnostic signal, but it lacks the internal variance required to independently forecast complex nation-state stability.
* **Extreme Class Imbalance:** The target variable for motives is heavily skewed toward profit-driven cybercrime (1,796 Financial cases vs. 154 Political-Espionage cases). This imbalance restricts the machine learning architectures from thoroughly learning the nuances of state-sponsored espionage, leading to lower recall rates in that sector.

### Future Work
* **Cross-Domain Feature Fusion:** To break the 58% predictive barrier, future iterations should ingest non-cyber external indicators directly into the pipeline, such as the World Bank’s Institutional Governance Indicators, military spending metrics, and regional alliance networks (e.g., NATO membership).
* **Advanced Imbalance Mitigation:** Implementing synthetic oversampling techniques (such as SMOTE tailored for categorical/continuous mixes) or implementing cost-sensitive loss functions could improve the model’s sensitivity toward covert Political-Espionage patterns.
* **Transition to Sequential Models:** Instead of processing data through static classification algorithms, transforming the preprocessed data into a sequence-ready format would allow the utilization of Recurrent Neural Networks (LSTMs) or Transformer-based time-series models. This setup could better capture the long-term lag between economic degradation and subsequent cyber mobilization.