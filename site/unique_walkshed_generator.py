# The purpose of this algorithm was to identify the networks that are unique to one walkshed,
# i.e. the increase in connectivity provided by the specific crossing
# This could then be used to analyse the connectivity opportunities of future potential crossings 
# (here represented by the informal crossings that are already being used by citizens)


import json
import geopandas as gpd
import pandas as pd
import os
from shapely.geometry import shape

# -------------------------------------------------------------
# INPUT + OUTPUT
# -------------------------------------------------------------
INPUT_FILE = "data/reachable_lines_800m.geojson"
OUTPUT_FOLDER = "data"

# -------------------------------------------------------------
# LOAD ALL 800m WALKSHEETS
# -------------------------------------------------------------
print("Loading reachable lines (800m)...")
gdf = gpd.read_file(INPUT_FILE)

# Ensure CRS is available
if gdf.crs is None:
    raise ValueError("❌ ERROR: The GeoJSON file has no CRS. It must have EPSG:3857 or EPSG:4326.")

# Sort crossings into groups
crossing_groups = {
    name: gdf[gdf["crossing_name"] == name].copy()
    for name in gdf["crossing_name"].unique()
}

print(f"Found {len(crossing_groups)} crossings in the walkshed file.")
print("Crossings:", list(crossing_groups.keys()))


# -------------------------------------------------------------
# FUNCTION: GENERATE UNIQUE WALKSHEETS FOR ONE CROSSING
# -------------------------------------------------------------
def generate_unique_for_crossing(target_name: str):
    print(f"\n==============================")
    print(f"🔍 Processing UNIQUE walkshed for: {target_name}")
    print("==============================")

    if target_name not in crossing_groups:
        print(f"⚠️ ERROR: Crossing '{target_name}' not found in dataset.")
        return

    target_gdf = crossing_groups[target_name]

    # Combine all OTHER crossings
    others = [
        g for name, g in crossing_groups.items()
        if name != target_name
    ]

    if len(others) == 0:
        print("⚠️ Only one crossing in dataset — everything would be unique.")
        return

    others_gdf = gpd.GeoDataFrame(pd.concat(others, ignore_index=True), crs=gdf.crs)

    # Build spatial index for faster overlap checks
    sindex = others_gdf.sindex

    unique_features = []

    for idx, row in target_gdf.iterrows():
        geom = row.geometry

        # quickly grab candidates via bbox
        possible = list(sindex.intersection(geom.bounds))
        candidates = others_gdf.iloc[possible]

        # direct spatial intersection check
        if not candidates.intersects(geom).any():
            unique_features.append(row)

    # Convert back to GeoDataFrame
    out_gdf = gpd.GeoDataFrame(unique_features, crs=gdf.crs)

    # Save file
    safe_name = target_name.replace(" ", "_")
    output_file = os.path.join(OUTPUT_FOLDER, f"{safe_name}_uniquewalkshed.geojson")

    out_gdf.to_file(output_file, driver="GeoJSON")

    print(f"✅ Saved {len(out_gdf)} unique features → {output_file}")


# -------------------------------------------------------------
# RUN FOR ALL FOUR CROSSINGS
# -------------------------------------------------------------
targets = [
    "Avenue de l’Épée Crossing",
    "Skatepark Crossing",
    "Rue Cartier Crossing",
    "Outdoor Gym Crossing"
]

for crossing in targets:
    generate_unique_for_crossing(crossing)

print("\n🎉 All unique walkshed files generated.")