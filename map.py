def create_map():
    # """""
    # Function to create the map of Bristol, and shade the area that is the Clean Air Zone, using the publicly available GeoJSON file from https://opendata.westofengland-ca.gov.uk/explore/dataset/weca_caz/export/
    # """""
    import folium
    import json
    
    bristol_coords = [51.4545, -2.5879]
    m = folium.Map(location=bristol_coords, zoom_start=13)
    
    # Load the GeoJSON file, which has been downloaded from https://opendata.westofengland-ca.gov.uk/explore/dataset/weca_caz/export/
    with open('data/weca_caz.geojson', 'r') as f:
        caz = json.load(f)
    
    folium.GeoJson(
        caz,
        name='Clean Air Zone (Bristol)',
        style_function=lambda feat: {
            'fillColor': 'crimson',
            'color': 'darkred',
            'weight': 2,
            'fillOpacity': 0.2,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['geo_point_2d', 'ladnm', 'ladcd', 'caz_class'],
            aliases=['geo_point_2d', 'ladnm', 'ladcd', 'caz_class'],
            localize=True
        )
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    return m

def add_marker(m, lat, lon, location):
    # """"
    # Function to add markers to the map
    # """"
    import folium
    import json
    folium.Marker(
    location = [lat, lon],
    tooltip = str(location),
    # popup = str(location),
    # icon = folium.Icon(),
    ).add_to(m)
    return m