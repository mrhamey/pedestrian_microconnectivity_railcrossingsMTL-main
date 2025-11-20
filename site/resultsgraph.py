import json
import pandas as pd
import plotly.express as px

# Load GeoJSON
with open("data/places_with_walksheds.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Flatten into DataFrame
rows = []
for feature in geojson["features"]:
    props = feature["properties"]
    lon, lat = feature["geometry"]["coordinates"]
    rows.append({
        "name": props["name"],
        "lon": lon,
        "walkshed_800m": int(props["walkshed_800m"].replace(",", "")),
        "walkshed_400m": int(props["walkshed_400m"].replace(",", ""))
    })

df = pd.DataFrame(rows)

df = df.sort_values(by="lon", ascending=True)

# Melt for plotting
df_melted = df.melt(
    id_vars=["name", "lon"],
    value_vars=["walkshed_800m", "walkshed_400m"],  # 800m first, 400m second
    var_name="walkshed",
    value_name="meters"
)

# Create Plotly figure
fig = px.bar(
            df_melted,
             x="name",
             y="meters",
             color="walkshed",
             hover_data={"meters": True, "name": False, "walkshed": False},
             labels={"meters": "Network length (m)", "name": "Crossing"},
             title="Walkshed Network Length per Crossing",
             color_discrete_map={
                "walkshed_400m": "#62b955",  # green for 400m
                "walkshed_800m": "#C4DEA0"   # light green for 800m
            }
)
            
fig.update_layout(
    xaxis_tickangle=-45,
    barmode="overlay"   # <-- makes bars draw from x-axis instead of stacking
)

# Export to a standalone HTML snippet
div_snippet_path = "site/graph_walksheds_ordered.html"
fig.write_html(div_snippet_path, include_plotlyjs=False, full_html=False)
print(f"Graph saved to {div_snippet_path}")
