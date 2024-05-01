import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Connect to Snowflake
conn = st.connection("snowflake")
    
def load_table(table:str):
    session = conn.session()
    return session.table(table).to_pandas()

def main():
    # Load data from Snowflake
    data = load_table("TOWERS_DATA_CLUSTRED")
    edges_df = load_table("EDGES_DATA")

    # Get locations between edges
    node_to_coordinates = dict(zip(data["TOWER_ID"].astype(int), zip(data["LAT"], data["LON"])))
    edges_df["SOURCE_LOCATION"] = edges_df["SOURCE_ID"].map(node_to_coordinates)
    edges_df["TARGET_LOCATION"] = edges_df["TARGET_ID"].map(node_to_coordinates)
    locations = edges_df[["SOURCE_LOCATION", "TARGET_LOCATION", "DISTANCE"]].values.tolist()


    # Set map center and zoom level
    map_center = [data.LAT.mean(), data.LON.mean()]
    map_zoom = 3

    # Create a folium map
    m = folium.Map(location=map_center, zoom_start=map_zoom, control_scale=True)

    # Add markers and offline markers to the map
    for _, row in data.iterrows():
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

    # Add polylines between coordinates
    for point1, point2, distance in locations:
        folium.PolyLine(
            locations=[point1, point2], 
            color="red",
            tooltip='{:.2f}'.format(distance),
            weight=4,
        ).add_to(m)

    # Display the folium map in Streamlit
    st_folium(m, width=700)