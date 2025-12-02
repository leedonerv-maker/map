import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("테스트 지도")

m = folium.Map(location=[37.5665, 126.9780], zoom_start=15)
st_folium(m, width=700, height=500)
