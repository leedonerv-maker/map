import streamlit as st
import folium
from streamlit_folium import st_folium
import random

st.title("퇴근길 추천 지도 (시뮬레이션)")

# --- 1. 출발지 / 도착지 (가상 좌표) ---
company = (37.5665, 126.9780)  # 서울시청
home = (37.5512, 126.9882)     # 남산타워

# --- 2. 경로 좌표 생성 (출발지→도착지 직선 경로 20개 점) ---
route_points = []
lat_step = (home[0] - company[0]) / 20
lng_step = (home[1] - company[1]) / 20

for i in range(21):
    lat = company[0] + lat_step * i
    lng = company[1] + lng_step * i
    route_points.append((lat, lng))

# --- 3. 지도 생성 ---
m = folium.Map(location=company, zoom_start=15)

# --- 4. 경로 Polyline 표시 ---
folium.PolyLine(route_points, color="blue", weight=5, opacity=0.7).add_to(m)

# --- 5. 경로 주변 추천 장소 생성 ---
place_types = ['카페', '음식점', '편의점']
for point in route_points[::3]:  # 일정 간격마다 생성
    for _ in range(random.randint(1, 3)):  # 1~3개 랜덤 장소
        lat_offset = random.uniform(-0.001, 0.001)
        lng_offset = random.uniform(-0.001, 0.001)
        lat = point[0] + lat_offset
        lng = point[1] + lng_offset
        name = random.choice(place_types) + f" {random.randint(1,100)}"
        folium.Marker(
            [lat, lng],
            popup=name,
            icon=folium.Icon(color='green')
        ).add_to(m)

# --- 6. Streamlit에서 지도 표시 ---
st_folium(m, width=700, height=500)
