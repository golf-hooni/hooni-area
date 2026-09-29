# HooNI Area — Claude 작업 안내

다녀온 식당·카페·골프장을 간단히 평가해 기록하고, 목적지까지 **가는 길의 맛집(내가 다녀온 곳 강조)** 을 보여주는 모바일 웹앱(PWA). 사용자는 한국어로 대화하고, 앱 문구도 한국어 해요체예요. 지난 작업 내역과 남은 일은 [HANDOFF.md](HANDOFF.md)에 있어요.

- 앱 주소: https://golf-hooni.github.io/hooni-area/
- 저장소: https://github.com/golf-hooni/hooni-area (공개, `main` 브랜치 루트가 GitHub Pages)

## 구조
- `index.html` — 앱 전체(HTML·CSS·JS 한 파일, 약 320KB). 프레임워크 없음. `h()`로 DOM을 만들고 상태 `S`를 바꾼 뒤 `render()`.
  - 기본 SVG 지도 데이터 `MAPD`(시군구 경계)·`EXPW`(고속도로)가 인라인으로 들어 있어 파일이 커요. 수정할 땐 전체를 읽지 말고 `grep -n`으로 위치를 찾아 부분만 고치세요.
- `data/packs.json` + `data/<id>.json` — 앱의 "추천 맛집 목록"(설정 → 추천 맛집 목록 보기)에서 합칠 수 있는 목록
- `icons/` — 앱 아이콘. 원본 `icon.svg`(크루아상 + 골프 깃대 + 깃발 속 자동차). PNG는 `tools/render_icons.ps1`로 만듦
- `sw.js` — 오프라인 캐시. **배포할 때마다 `CACHE` 버전 숫자를 올리세요** (예: `hooni-area-v6` → `v7`)
- `manifest.webmanifest` — 홈 화면 앱 설정
- `tools/` — 과거 1회용 패치 스크립트(이미 적용됨, **다시 실행 금지**)와 도구. `tools/mapdata/`는 기본 지도 데이터 생성용

## 로컬 실행·확인
```bash
python -m http.server 8765 --directory .
```
- 반드시 **포트 8765**를 쓰세요. 카카오 콘솔에 `http://localhost:8765`만 등록돼 있어요.
- 서비스워커가 옛 화면을 줄 수 있어요. 이상하면 콘솔에서 서비스워커를 해제하고 캐시를 지운 뒤 새로고침하세요.
- 테스트한 뒤에는 localStorage와 IndexedDB(`hooni-area`)를 지워 두세요.

## 배포
1. `sw.js`의 `CACHE` 버전 올리기
2. 커밋 후 `git push origin main` → 약 1분 뒤 반영
- 자격증명은 이 PC의 Git Credential Manager에 있어요. `gh` CLI는 없어요.

## 데이터 (모두 각 기기 브라우저에 저장, 서버 없음)
- localStorage: `huni2-places`, `huni2-bases`, `huni2-trips`(이름은 옛 앱과 호환하려고 유지), `huni-recent`
- 카카오 키: `hooni-kakao-key`(JS 키 덮어쓰기용), `hooni-kakao-rest`(REST 키, 선택)
- 추천 목록: `hooni-pack-<id>`(모두 추가됨 표시), `hooni-pack-hidden`(사용자가 뺀 추천 가게, 다시 추가 안 함)
- 사진: IndexedDB `hooni-area` / store `photos`, 기록에는 `idb:<키>`로 저장
- 장소(place) 주요 필드: `name, cat(food|cafe|golf|sight|stay|etc), status(visited|wish), revisit(again|okay|once), tags[], meals[]('아침' = 아침 식당), opens(여는 시간), menu, memo, address, area, list, lat, lng, phone, kakaoUrl, photos[], src('pack:<id>' 등), pk(목록 안 키)`

## 카카오
- 앱 "HooNI Area"(ID 1590938). JavaScript 키는 `index.html`의 `DEFAULT_KAKAO_KEY`에 들어 있어요. 등록한 주소에서만 동작해서 공개돼도 괜찮아요.
- JavaScript SDK 도메인: `http://localhost:8765`, `https://golf-hooni.github.io`
- 제품 설정 → 카카오맵: 켜짐
- **REST API 키는 절대 커밋하지 마세요.** 쓸 때는 사용자가 앱 설정 화면에서 직접 넣어요.
- 가게 확인은 로컬 앱을 연 브라우저 콘솔에서 `new kakao.maps.services.Places().keywordSearch(...)`로 하면 빨라요.

## 지켜야 할 결정
- **다이닝코드는 수집 금지**: robots.txt가 ClaudeBot과 anthropic-ai를 명시적으로 막고 있어요. 사용자가 가게 이름이나 캡처를 주면 그걸 카카오로 확인해서 넣어요.
- 블로그나 목록에서 가게를 넣을 때: 이름이 분명한 곳만, 카카오에서 **도로명 주소까지 일치**하는지 확인하고 넣어요. 못 찾은 곳은 빼고 사용자에게 알려요. 블로그 문장은 복사하지 말고 메뉴와 골프장 이름 정도만 적어요.
- 개인 목록(예: 제주 가족여행)은 **공개 저장소에 올리지 않아요.** `hooni-area-import-*.json`은 .gitignore 대상이에요.
- 커밋 작성자: `golf-hooni`
