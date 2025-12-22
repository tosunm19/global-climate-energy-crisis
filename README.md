# Global Climate and Energy Analysis

A data-driven and visual analysis of global CO₂ emissions, energy use, and economic growth using Python and Power BI.  
This project explores long-run emission and energy trends, the relationship between CO₂ emissions and GDP, time-series forecasting, and interactive visualizations designed for dashboards.  
The primary goal was to strengthen my Python and Power BI skills while analyzing climate and energy data of personal interest.

## Data
The analysis is based on the **Our World in Data (OWID)** energy and CO₂ datasets, covering the period **1990–2022**.  
All variables used in the analysis are documented in `codebook.csv`, which provides detailed definitions and sources.

## Forecast Model
The forecasts were produced using an additive time-series forecasting framework (Prophet), fitted using historical CO2 emissions. The forecast is 15 years ahead and the frequency is year-end.

## Conclusion
The results provide empirical support for the **Environmental Kuznets Curve (EKC)** hypothesis, indicating a non-linear relationship between economic growth and CO₂ emissions.  
In addition, the analysis suggests that developed economies such as the United States and Germany have begun transitioning toward cleaner and more renewable energy sources over time.
