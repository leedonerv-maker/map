import googlemaps
import folium

# --- 1. 구글 API 키 ---
API_KEY = 'w0Io8/rTa6xdXjwUJo7tpUErGBOLHNhtf0+zvCRUnaQbcGPZan/bzRSXpIqgct/qHGbqTsl10DxsGKlc6y4kRA=='  # 본인 API 키로 교체
gmaps = googlemaps.Client(key=API_KEY)

# --- 2. 출발지(회사) / 도착지(집) ---
origin = "서울시청"
destination = "남산타워"

# --- 3. 경로 계산 ---
directions = gmaps.directions(origin, destination, mode="driving")
route_points = directions[0]['overview_polyline']['points']

# --- 4. 폴리라인 디코딩 ---
import polyline
decoded_route = polyline.decode(route_points)

# --- 5. 지도 생성 ---
m = folium.Map(location=decoded_route[0], zoom_start=13)

# --- 6. 경로 표시 ---
folium.PolyLine(decoded_route, color="blue", weight=5).add_to(m)

# --- 7. 경로 주변 추천 장소 검색 ---
# 경로 좌표에서 일정 간격으로 장소 검색
for i, point in enumerate(decoded_route):
    if i % 10 == 0:  # 10번째 좌표마다 검색
        places_result = gmaps.places_nearby(location=point, radius=500, type='cafe')
        for place in places_result.get('results', []):
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            name = place['name']
            folium.Marker([lat, lng], popup=name).add_to(m)

# --- 8. 지도 저장 ---
m.save("commute_map.html")
print("지도 생성 완료! commute_map.html 파일을 브라우저에서 열어보세요.")
