# DSA210-Term-Project
DSA 210 Term Project

# Data Collection

This project integrates **three primary heterogeneous datasets** covering the years **2014–2026**, aligned geographically via **ISO3 codes** and temporally by **year/month**.  

## 1. Cyber Incident Data (General Activity)

- **Source:** Cyber Events Tracker (Consolidated Incident Log)  
- **Frequency:** Event-based  
- **Collection Method:** Static CSV retrieval and parsing  
- **Key Features for Analysis:**
    
  - `event_date` & `year`: For temporal alignment  
  - `motive`: Categorizes attacks as **Financial**, **Protest**, or **Espionage**  
  - `actor_type`: Distinguishes between **Criminal**, **Nation-State**, and **Hacktivist**  
  - `country` & `actor_country`: For mapping cross-border aggression  

## 2. Geopolitical Cyber Incidents (EuRepoC)

- **Source:** European Repository of Cyber Incidents (EuRepoC)  
- **Frequency:** Event-based (high-resolution coding)  
- **Collection Method:** Expert-curated repository (CSV export)  
- **Key Features for Analysis:**
  
  - `weighted_intensity`: Quantifies the severity/damage of the attack  
  - `offline_conflict_intensity`: Links the cyber event to physical military or political tension (e.g., HIIK intensity scores)  
  - `political_response_type`: Tracks if the incident led to sanctions or diplomatic protests  
  - `receiver_country_alpha_2_code`: Facilitates merging with other national datasets  

## 3. Socio-Economic Indicators (World Bank)

- **Source:** World Bank Open Data (World Development Indicators)  
- **Frequency:** Annual  
- **Collection Method:** API retrieval (`wbgapi`) and CSV export  
- **Key Features for Analysis:**
   
  - `GDP per capita (current US$)`: Measures the economic "target value" of a country  
  - `GDP growth (annual %)` & `Inflation (CPI)`: Indicators of economic instability that may trigger criminal activity  
  - `Country Code`: Primary key for relational joining (ISO3)  
