# Import packages
import folium
import pandas as pd

# Import data
data = pd.read_csv(
    "Volcanoes.txt",
    header=0
)

# Store required data as strings
lat = list(data["LAT"])
long = list(data["LON"])
elev = list(data["ELEV"])

# Create Map
map = folium.Map(
    location=[38.58, -99.09],
    zoom_start=6,
    tiles="CartoDB Positron"
)


# Create function to assign colour bassed on height
def height_color_mapping(elevation: float) -> str:
    """
    Takes in an elevation of a point and assigns a colour to it
    bassed on the elevation

    Args:
        elevation: the elevation of the map marker
    """
    if elevation < 1000:
        return "orange"
    elif elevation < 2000:
        return "lightred"
    elif elevation < 3000:
        return "red"
    else:
        return "darkred"


# Create feature group for the population chloropleth
fgp = folium.FeatureGroup(
    name="Population"
)


# Create shapes for areas and colour code based on population

fgp.add_child(
    # Get data from JSON file. needs to be geojson style
    folium.GeoJson(
        data=open("world.json", 'r', encoding='utf-8-sig').read(),
        # Add style to polygons
        style_function=lambda x: {
            # Make colours conditional on population size of area
            'fillColor': 'red' if x['properties']['POP2005'] < 10000000 else
            'orange' if 10000000 <= x['properties']['POP2005'] < 25000000
            else 'green',
            'color': 'white' if x['properties']['POP2005'] < 10000000 else
            'black' if 10000000 <= x['properties']['POP2005'] < 25000000
            else 'grey'
            }
    )
)
# Create a feature group for the volcanoes
fgv = folium.FeatureGroup(
    name="Volcanoes in the USA"
)

# Place markers for all the volcanos
for lt, ln, el in zip(lat, long, elev):
    fgv.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            radius=7,
            popup="Hi I am a Volcano, I am {}m tall".format(el),
            # icon=folium.Icon(
            #    color=height_color_mapping(el),
            #    icon='home',
            #    prefix='fa'
            # )
            fill_color=height_color_mapping(el),
            color="black",
            fill_opacity=0.5
        )
    )

# Add feature groups to map
for fg in [fgv, fgp]:
    map.add_child(fg)

# Add layer control pannel to enable turning the layers on and off
map.add_child(folium.LayerControl())

map.save("Map1.html")
