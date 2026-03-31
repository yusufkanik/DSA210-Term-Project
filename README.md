# DSA210-Term-Project
DSA 210 Term Project

# 2.	Data Collection:

This project integrates three primary heterogeneous datasets covering 2014–2026, aligned geographically via ISO3 codes and temporally by year/month:

1.	Cyber Incident Data (General Activity)

•	Source: Cyber Events Tracker (Consolidated Incident Log)

•	Frequency: Event-based

•	Collection Method: Static CSV retrieval and parsing

•	Key Features for Analysis:

   o	event_date & year: For temporal alignment

   o	motive: Categorizes attacks as Financial, Protest, or Espionage.

   o	actor_type: Distinguishes between Criminal, Nation-State, and Hacktivist.

   o	country & actor_country: For mapping cross-border aggression.


2.	Geopolitical Cyber Incidents (EuRepoC)

•	Source: European Repository of Cyber Incidents (EuRepoC)

•	Frequency: Event-based (high-resolution coding)

•	Collection Method: Expert-curated repository (CSV export)

•	Key Features for Analysis:

   o	weighted_intensity: Quantifies the severity/damage of the attack.

   o	offline_conflict_intensity: Links the cyber event to physical military or political tension (e.g., HIIK intensity scores).

   o	political_response_type: Tracks if the incident led to sanctions or diplomatic protests.

   o	receiver_country_alpha_2_code: Facilitates the merge with other national datasets.


3. Socio-Economic Indicators (World Bank)
   
•	Source: World Bank Open Data (World Development Indicators)

•	Frequency: Annual

•	Collection Method: API retrieval (wbgapi) and CSV export

•	Key Features for Analysis:

   o	GDP per capita (current US$): Measures the economic "target value" of a country.

   o	GDP growth (annual %) & Inflation (CPI): Indicators of economic instability that may trigger criminal activity.

   o	Country Code: Primary key for relational joining (ISO3).
