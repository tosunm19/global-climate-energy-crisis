import pandas as pd

CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
ENERGY_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

def download():
    print("Downloading CO₂ data...")
    co2 = pd.read_csv(CO2_URL)
    co2.to_csv("data/raw/co2.csv", index=False)
    print("Saved CO₂ data to data/raw/co2.csv")

    print("Downloading Energy data...")
    energy = pd.read_csv(ENERGY_URL)
    energy.to_csv("data/raw/energy.csv", index=False)
    print("Saved Energy data to data/raw/energy.csv")

    print("Download completed.")

if __name__ == "__main__":
    download()
