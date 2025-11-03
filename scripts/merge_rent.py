import pandas as pd

airbnb_path = "Airbnb_Dataset/processeddata/nyc_airbnb_clean.csv"
rent_path   = "Airbnb_Dataset/rawdata/nyc_rent_by_neighborhood.csv"
out_path    = "Airbnb_Dataset/processeddata/nyc_airbnb_clean_with_rent.csv"

airbnb = pd.read_csv(airbnb_path, low_memory=False)
rent   = pd.read_csv(rent_path)

airbnb.columns = [c.strip().lower().replace(" ", "_") for c in airbnb.columns]
rent.columns   = [c.strip().lower().replace(" ", "_") for c in rent.columns]

borough_fix = {"brookln": "Brooklyn", "manhatan": "Manhattan"}
airbnb["neighbourhood_group"] = (
    airbnb["neighbourhood_group"].astype(str).str.strip().replace(borough_fix).str.title()
)

neigh_fix = {
    "Bedford Stuyvesant": "Bedford-Stuyvesant",
    "St George": "St. George",
    "Hells Kitchen": "Hell's Kitchen",
}
airbnb["neighbourhood"] = airbnb["neighbourhood"].astype(str).str.strip().replace(neigh_fix)

merged = airbnb.merge(rent, on=["neighbourhood_group", "neighbourhood"], how="left")
print("Merged rows:", len(merged))
print("Missing median_rent before fill:", merged["median_rent"].isna().sum())

borough_med = rent.groupby("neighbourhood_group")["median_rent"].median()
merged["median_rent"] = merged["median_rent"].fillna(
    merged["neighbourhood_group"].map(borough_med)
)
print("Missing median_rent after fill:", merged["median_rent"].isna().sum())

merged.to_csv(out_path, index=False)
print("✅ Saved:", out_path)

