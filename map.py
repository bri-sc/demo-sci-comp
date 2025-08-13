import folium
import json

def create_map():
    """
    Creates the map of Bristol and shades the area that is the Clean Air Zone, using the publicly available GeoJSON file from https://opendata.westofengland-ca.gov.uk/explore/dataset/weca_caz/export/
    
    Parameters:
        None
    """
    
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

    m._legend_items = []

    # Icon for the Clean Air Zone to be placed in the legend
    caz_legend_html = (
        '<i style="background:crimson; '
        'width:18px; height:12px; display:inline-block; margin-right:5px; border:1px solid darkred;"></i> '
        'Clean Air Zone<br>'
    )
    m._legend_items.append(caz_legend_html)

    # Call the function to add legend so that it doesn't need to be called in the main code
    add_legend(m)
    return m

def add_marker(m, lat, lon, location, colour):
    """
    Adds a marker to the map based on specified coordinates and labels
    
    Parameters:
        m (Folium map object): map
        lat (float): latitude of location
        lon (float): longitude of location
        location (string): name of location
        colour (string): desired colour of marker

    Returns:
        m: the updated map
    """
    
        # Add this to the legend entries
    m._legend_items.append(
        f'<i style="background:{colour}; width:12px; height:12px; border-radius:50%;'
        f'display:inline-block; margin-right:5px;"></i> {location}<br>'
        )

    # Use CircleMarker with color
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color=colour,
        fill=True,
        fill_color=colour,
        fill_opacity=0.7,
        tooltip=str(location)
    ).add_to(m)
    add_legend(m)
    return m

def add_legend(m):
    """
    Adds a legend to the map

    Parameters:
        m (Folium map object): map
    """
    legend_html = f'''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 180px; height: auto; 
                    background-color: white;
                    border:2px solid grey; z-index:9999; font-size:14px;
                    padding: 10px;">
        <b>Legend</b><br>
        {''.join(m._legend_items)}
        </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
