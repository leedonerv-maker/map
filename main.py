import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# ----------------------------
# 1. 페이지 설정
# ----------------------------
st.set_page_config(
    page_title="퇴근길 추천 지도",
    layout="wide",
    page_icon="🚗"
)

st.markdown(
    "<h1 style='text-align: center; color: #FF6F61;'>퇴근길 추천 지도</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray;'>버튼을 눌러 경로 주변 추천 장소를 확인하세요!</p>",
    unsafe_allow_html=True
)

# ----------------------------
# 2. 출발지 / 도착지 설정 (가상 좌표)
# ----------------------------
company = (37.5665, 126.9780)  # 서울시청
home = (37.5512, 126.9882)     # 남산타워

# ----------------------------
# 3. 경로 좌표 생성
# ----------------------------
route_points = []
lat_step = (home[0] - company[0]) / 20
lng_step = (home[1] - company[1]) / 20
for i in range(21):
    lat = company[0] + lat_step * i
    lng = company[1] + lng_step * i
    route_points.append((lat, lng))

# ----------------------------
# 4. Folium 지도 생성
# ----------------------------
m = folium.Map(location=company, zoom_start=15)

# 경로 표시
folium.PolyLine(
    route_points,
    color="#FF6F61",
    weight=6,
    opacity=0.8,
    tooltip="퇴근길 경로"
).add_to(m)

# ----------------------------
# 5. 추천 장소 상태 관리
# ----------------------------
if "markers" not in st.session_state:
    st.session_state.markers = []  # 항상 빈 리스트로 초기화

# 버튼 클릭 시 추천 장소 생성
if st.button("추천 장소 보기"):
    place_types = {
        '카페': 'blue',
        '음식점': 'red',
        '편의점': 'green'
    }
    new_markers = []
    for point in route_points[::3]:  # 일정 간격마다 생성
        for _ in range(random.randint(1, 3)):
            lat_offset = random.uniform(-0.001, 0.001)
            lng_offset = random.uniform(-0.001, 0.001)
            lat = point[0] + lat_offset
            lng = point[1] + lng_offset
            category = random.choice(list(place_types.keys()))
            name = f"{category} {random.randint(1,100)}"
            color = place_types[category]
            new_markers.append((lat, lng, name, color))
    st.session_state.markers.extend(new_markers)

# ----------------------------
# 6. 지도에 마커 표시
# ----------------------------
for marker in st.session_state.markers:
    lat, lng, name, color = marker  # 항상 4개로 unpack
    folium.Marker(
        [lat, lng],
        popup=f"<b>{name}</b>",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# ----------------------------
# 7. Streamlit에 지도 표시
# ----------------------------
st_folium(m, width=900, height=600)

# ----------------------------
# 8. 안내 문구
# ----------------------------
st.markdown(
    "<p style='text-align: center; color: gray; margin-top: 10px;'>※ 추천 장소는 시뮬레이션입니다.</p>",
    unsafe_allow_html=True
)
