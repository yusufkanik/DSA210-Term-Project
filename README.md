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
  - `Country Code`: Primary key for relational joining (ISO3)
 
 ## Methodology

This project employs a **quantitative, correlation-based approach** to analyze the impact of socio-economic and political volatility on global cyber activity. The research will be executed in the following phases:

### 1. Data Integration & Preprocessing

The primary technical challenge involves merging **event-based cyber data** with **annual economic indicators**. Python (`pandas`) will be used to:

- **Reshape Indicators:** Transform World Bank data from "Wide" to "Long" format using `pd.melt()` to align with the temporal timeline.  
- **Relational Joining:** Execute a left-join using a composite key of `[ISO3_Country]` and `[Year]`.  
- **Normalization:** Convert nominal GDP values to real terms and normalize cyber-attack counts per capita to ensure cross-country comparability.  

### 2. Exploratory Data Analysis (EDA)

Visualization will be performed using **Matplotlib/Seaborn** to explore:

- **Temporal Trends:** Identify if spikes in Inflation (CPI) or drops in GDP Growth precede a rise in Financial motive cyber incidents.  
- **Geospatial Heatmaps:** Map `actor_country` against `offline_conflict_intensity` to identify global "hotspots" of digital aggression.

## Hypothesis Tests

### Hypothesis 1: Political Stability Shock (Paired T-Test)

- **H₀:** The average number of "Protest" motivated attacks is the same **6 months before** and **6 months after** a sudden drop in a country’s "Political Stability" score.  
- **Hₐ:** The average number of "Protest" motivated attacks is greater in the 6 months following a decline in stability than in the 6 months before.  
- **Method:** Paired T-Test to compare the "before" and "after" states of the same country.  

### Hypothesis 2: Observed vs. Expected Attack Motives (Chi-Square Statistic)

- **H₀:** The observed frequencies of attack motives (**Financial, Protest, Espionage**) during an economic crisis follow the expected historical distribution.  
- **Hₐ:** The observed frequencies significantly deviate from the expected distribution (e.g., Financial motives appear more than expected).  
- **Method:** Chi-Square Statistic to measure the discrepancy between actual crisis data and historical baseline data.      
