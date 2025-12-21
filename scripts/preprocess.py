import pandas as pd
import numpy as np

def preprocess():

    co2 = pd.read_csv("data/raw/co2.csv")
    energy = pd.read_csv("data/raw/energy.csv")


    co2_cols = [
        "country", "year",
        "co2", "co2_per_capita", "co2_growth_prct",
        "share_global_co2", "gdp",
        "population", "coal_co2", "oil_co2", "gas_co2",
        "cement_co2", "flaring_co2"
    ]
    co2 = co2[co2_cols]


    energy_cols = [
        "country", "year",
        "primary_energy_consumption",
        "renewables_share_energy",
        "fossil_share_energy",
        "low_carbon_share_energy",
        "wind_share_energy",
        "solar_share_energy",
        "biofuel_consumption",
        "biofuel_share_energy",
        "coal_consumption",
        "coal_share_energy",
        "electricity_demand",
        "electricity_generation",
        "electricity_share_energy",
        "gas_consumption",
        "gas_share_energy",
        "greenhouse_gas_emissions",
        "hydro_consumption",
        "hydro_share_energy",
        "low_carbon_consumption",
        "nuclear_consumption",
        "nuclear_share_energy",
        "oil_consumption",
        "oil_share_energy",
        "other_renewable_consumption",
        "other_renewables_share_energy",
        "renewables_consumption",
        "solar_consumption",
        "wind_consumption",
        "iso_code"
    ]
    energy = energy[energy_cols]


    df = pd.merge(co2, energy, on=["country", "year"], how="inner")


    df = df[~df["country"].isin([
        "World", "Asia", "Europe", "North America", "South America",
        "Africa", "European Union (27)", "Oceania", "International transport"
    ])]


    df = df.dropna(subset=["co2", "year"])


    df.to_csv("data/processed/global_panel.csv", index=False)
    print("Saved processed dataset to data/processed/global_panel.csv")

if __name__ == "__main__":
    preprocess()
