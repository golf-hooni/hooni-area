// 앱 화면 파일만 캐시해서 오프라인·느린 통신에서도 열리게 함. 카카오 지도 등 외부 요청은 건드리지 않음.
const CACHE = 'hooni-area-v2';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

// 같은 주소의 파일은 네트워크 우선(새 버전 바로 반영), 실패하면 캐시
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith(
    // no-cache: 브라우저 HTTP 캐시가 옛 파일을 주지 않도록 매번 서버에 확인
    fetch(e.request.url, { cache: 'no-cache' }).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy));
      return res;
    }).catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});
