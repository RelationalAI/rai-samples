import streamlit as st
import streamlit_graph
import streamlit_map

page_options = ["Show Map", "Show Graph"]
selected_page = st.sidebar.radio("Select Page", page_options)

# Display the selected page
if selected_page == "Show Map":
    streamlit_map.main()
elif selected_page == "Show Graph":
    streamlit_graph.main()
