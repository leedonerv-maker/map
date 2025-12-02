import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="퇴근길 추천 지도", layout="wide")
st.title("퇴근길 추천 지도 (시뮬레이션)")

company = (37.5665, 126.9780)
home = (37.5512, 126.9882)

# 경로 좌표 생성
route_points = []
lat_step = (home[0] - company[0]) / 20
lng_step = (home[1] - company[1]) / 20
for i in range(21):
    lat = company[0] + lat_step * i
    lng = company[1] + lng_step * i
    route_points.append((lat, lng))

# Folium 지도 생성
m = folium.Map(location=company, zoom_start=15)
folium.PolyLine(route_points, color="#FF6F61", weight=6, opacity=0.8).add_to(m)

# --- 버튼 클릭 시 추천 장소 생성 ---
if "markers" not in st.session_state:
    st.session_state.markers = []

if st.button("추천 장소 보기"):
    new_markers = []
    place_types = ['카페', '음식점', '편의점']
    for point in route_points[::3]:
        for _ in range(random.randint(1, 3)):
            lat_offset = random.uniform(-0.001, 0.001)
            lng_offset = random.uniform(-0.001, 0.001)
            lat = point[0] + lat_offset
            lng = point[1] + lng_offset
            name = random.choice(place_types) + f" {random.randint(1,100)}"
            new_markers.append((lat, lng, name))
    st.session_state.markers.extend(new_markers)

# --- 저장된 마커 지도에 표시 ---
for lat, lng, name in st.session_state.markers:
    folium.Marker(
        [lat, lng],
        popup=f"<b>{name}</b>",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)

# 지도 표시
st_folium(m, width=800, height=600)
