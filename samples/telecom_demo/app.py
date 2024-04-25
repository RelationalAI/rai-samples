import streamlit as st

def read_html_file(file_path):
    with open(file_path, 'r') as f:
        html_content = f.read()
    return html_content

# Read HTML content
html_content = read_html_file('graph.html')

show_html = st.button("Show Graph")

if show_html:
    # Embed HTML content in Streamlit app
    st.write("### Network Connectivity")
    st.write("##### Weakly Connected Components")
    st.components.v1.html(html_content, height=1000)