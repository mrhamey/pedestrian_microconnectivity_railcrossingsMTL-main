import json
import csv

# ----------------------------
# Load walkshed lengths (CSV)
# ----------------------------
walkshed_lookup = {}  # { crossing_name: {400: value, 800: value} }

with open("./data/walkshed_network_lengths.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["crossing_name"]
        length = float(row["total_length_m"])
        distance = int(row["distance_m"])

        if name not in walkshed_lookup:
            walkshed_lookup[name] = {}

        walkshed_lookup[name][distance] = length

# ----------------------------
# Load places.geojson
# ----------------------------
with open("./data/places.geojson", encoding="utf-8") as f:
    places = json.load(f)

# ----------------------------
# Join data into GeoJSON
# ----------------------------
for feature in places["features"]:
    name = feature["properties"].get("name")

    # initialize empty values
    feature["properties"]["walkshed_400m"] = None
    feature["properties"]["walkshed_800m"] = None

    # insert only if a match exists
    if name in walkshed_lookup:
        dist_dict = walkshed_lookup[name]
        if 400 in dist_dict:
            feature["properties"]["walkshed_400m"] = f"{round(dist_dict[400]):,}"
        if 800 in dist_dict:
            feature["properties"]["walkshed_800m"] = f"{round(dist_dict[800]):,}"

# ----------------------------
# Save joined file
# ----------------------------
with open("places_with_walksheds.geojson", "w", encoding="utf-8") as f:
    json.dump(places, f, ensure_ascii=False, indent=2)

print("Join complete → places_with_walksheds.geojson")