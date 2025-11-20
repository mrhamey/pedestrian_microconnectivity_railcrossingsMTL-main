import geopandas as gpd
import pandas as pd
import os

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
data_dir = "data"
output_csv = os.path.join(data_dir, "walkshed_network_lengths.csv")
geojson_files = [
    os.path.join(data_dir, "reachable_lines_400m.geojson"),
    os.path.join(data_dir, "reachable_lines_800m.geojson"),
]

# ---------------------------------------------------
# Compute total network length per crossing & distance
# ---------------------------------------------------
summary = []

for file in geojson_files:
    if not os.path.exists(file):
        print(f"⚠️ File not found: {file}")
        continue

    gdf = gpd.read_file(file)
    print(f"Loaded {file} with {len(gdf)} features")

    # Reproject to meters for accurate length calculation
    gdf_m = gdf.to_crs(epsg=3857)

    # Compute total length per crossing
    totals = (
        gdf_m.groupby("crossing_name")
        .apply(lambda x: x.length.sum())
        .reset_index(name="total_length_m")
    )

    # Add distance info
    dist = int(os.path.basename(file).split("_")[-1].replace("m.geojson", ""))
    totals["distance_m"] = dist

    summary.append(totals)

# ---------------------------------------------------
# Combine and export summary
# ---------------------------------------------------
if summary:
    summary_df = pd.concat(summary, ignore_index=True)
    summary_df = summary_df.sort_values(["distance_m", "crossing_name"])

    summary_df.to_csv(output_csv, index=False)
    print(f"\n✅ Saved summary to {output_csv}")
    print(summary_df)
else:
    print("⚠️ No GeoJSON files found — nothing to summarize.")