import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# --- 1. 페이지 제목 & 스타일 ---
st.set_page_config(page_title="퇴근길 추천 지도", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>퇴근길 추천 지도</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🚗 경로와 주변 추천 장소 시뮬레이션</p>", unsafe_allow_html=True)

# --- 2. 출발지 / 도착지 (가상 좌표) ---
company = (37.5665, 126.9780)  # 서울시청
home = (37.5512, 126.9882)     # 남산타워

# --- 3. 경로 좌표 생성 ---
route_points = []
lat_step = (home[0] - company[0]) / 20
lng_step = (home[1] - company[1]) / 20

for i in range(21):
    lat = company[0] + lat_step * i
    lng = company[1] + lng_step * i
    route_points.append((lat, lng))

# --- 4. 지도 생성 ---
m = folium.Map(location=company, zoom_start=15)

# --- 5. 경로 Polyline 표시 ---
folium.PolyLine(route_points, color="#FF6F61", weight=6, opacity=0.8).add_to(m)

# --- 6. 사용자 버튼으로 추천 표시 ---
if st.button("추천 장소 보기"):
    place_types = ['카페', '음식점', '편의점']
    for point in route_points[::3]:
        for _ in range(random.randint(1, 3)):
            lat_offset = random.uniform(-0.001, 0.001)
            lng_offset = random.uniform(-0.001, 0.001)
            lat = point[0] + lat_offset
            lng = point[1] + lng_offset
            name = random.choice(place_types) + f" {random.randint(1,100)}"
            folium.Marker(
                [lat, lng],
                popup=f"<b>{name}</b>",
                icon=folium.Icon(color='green', icon='info-sign')
            ).add_to(m)

# --- 7. Streamlit에서 지도 표시 ---
st_folium(m, width=800, height=600)

# --- 8. 부가 안내 문구 ---
st.markdown("<p style='text-align: center; color: gray;'>※ 추천 장소는 시뮬레이션입니다.</p>", unsafe_allow_html=True)
