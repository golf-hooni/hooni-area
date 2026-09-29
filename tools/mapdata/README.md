# 기본 지도 데이터 만들기 (카카오 키가 없을 때 쓰는 SVG 지도)

`index.html` 안의 `MAPD`(시도·시군구 경계)와 `EXPW`(고속도로)는 이 스크립트로 만들었어요. 이미 index.html에 들어 있으니 **다시 돌릴 필요는 없어요.** 지도를 새로 만들 때만 참고하세요.

| 파일 | 하는 일 |
|---|---|
| `build_map.py` | 통계청 2013 경계(southkorea-maps)를 지도 좌표로 단순화 → `mapdata.json` |
| `build_expw.py` | OpenStreetMap 고속도로(`expw.json`)를 단순화·중복 차로 제거 → `expw_small.json` |
| `patch_map.py` | 처음 한 번 index.html에 지도 그리기 코드와 데이터를 넣은 패치 (이미 적용됨) |
| `swap_expw.py` | 고속도로 데이터만 바꿔 넣기 (경로가 옛 Desktop\index.html로 되어 있으니 바꿔서 사용) |

원본 데이터 받기:
- 경계: `https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo_simple.json`, `.../skorea_municipalities_geo_simple.json`
- 고속도로(약 30MB, Overpass API): `way["highway"="motorway"](33,124.5,38.7,130.0);out tags geom qt;` — overpass-api.de가 바쁘면 `https://overpass.private.coffee/api/interpreter` 사용

지도 좌표: `x=(경도-124)*809`, `y=(39-위도)*1000` (index.html의 `PX`/`PY`와 같음). 고속도로는 OpenStreetMap(ODbL) 데이터예요.
