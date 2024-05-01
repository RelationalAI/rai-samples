import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Connect to Snowflake
conn = st.connection("snowflake")
    
def load_table():
    session = conn.session()
    return session.table("TOWERS_DATA_CLUSTRED").to_pandas()

def main():
    # Load data from Snowflake
    df = load_table()

    # Set map center and zoom level
    map_center = [df.LAT.mean(), df.LON.mean()]
    map_zoom = 3

    # Create a folium map
    m = folium.Map(location=map_center, zoom_start=map_zoom, control_scale=True)

    # Add markers and offline markers to the map
    for _, row in df.iterrows():
        status = 'Status: ' + row['STATUS']
        popup_content = 'Tower: ' + str(row["TOWER_ID"]) + '<br>' + status
        iframe = folium.IFrame(popup_content)
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=popup,
            tooltip=popup_content,
            icon=folium.Icon(color=row['COLOR'], icon="tower-cell", prefix='fa'),
            c=row['TOWER_ID']
        ).add_to(m)

        # Add black circle markers for offline towers
        if row['STATUS'] != "Online":
            offline_marker = folium.CircleMarker(
                location=[row['LAT'], row['LON']],
                color="black",
                weight=1,
                fill_opacity=0.6,
                opacity=1,
                fill_color="black",
                fill=False,
            )
            offline_marker.add_to(m)

    # Display the folium map in Streamlit
    st_folium(m, width=700)
