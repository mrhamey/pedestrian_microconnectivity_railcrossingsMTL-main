# The purpose of this algorithm was to identify the networks that are unique to one walkshed,
# i.e. the increase in connectivity provided by the specific crossing
# This could then be used to analyse the connectivity opportunities of future potential crossings 
# (here represented by the informal crossings that are already being used by citizens)



import json





TARGET = "Outdoor Gym Crossing" #insert crossing name here 


input_file = "data/reachable_lines_800m.geojson"
safe_target = TARGET.replace(" ", "_")
output_file = f"data/{safe_target}_uniquewalkshed.geojson"


# Load input geojson
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]

# --- STEP 1: Build a mapping geometry → set of crossing_names

def geom_key(feat):
    """Returns a canonical JSON string of geometry for exact comparison."""
    return json.dumps(feat["geometry"], sort_keys=True)

geometry_crossing_map = {}

for feat in features:
    key = geom_key(feat)
    crossing = feat["properties"]["crossing_name"]

    if key not in geometry_crossing_map:
        geometry_crossing_map[key] = set()

    geometry_crossing_map[key].add(crossing)

# --- STEP 2: Identify geometries used exclusively by Rue Cartier Crossing

exclusive_geometry_keys = {
    key for key, crossings in geometry_crossing_map.items()
    if crossings == {TARGET}
}

# --- STEP 3: Extract the original features whose geometry is exclusive

unique_features = [
    feat for feat in features
    if geom_key(feat) in exclusive_geometry_keys
]

# --- STEP 4: Save result as new GeoJSON

output_geojson = {
    "type": "FeatureCollection",
    "features": unique_features
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output_geojson, f, indent=2)

print(f"Saved {len(unique_features)} exclusive features to {output_file}")
