import json, math
from collections import defaultdict

def PX(l): return (l-124)*809
def PY(a): return (39-a)*1000

def dp(pts, tol):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy)
    md, mi = 0, 0
    for i in range(1, len(pts)-1):
        p = pts[i]
        d = abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L if L else math.hypot(p[0]-a[0], p[1]-a[1])
        if d > md: md, mi = d, i
    if md > tol: return dp(pts[:mi+1], tol)[:-1] + dp(pts[mi:], tol)
    return [a, b]

d = json.load(open('expw.json', encoding='utf-8'))
byref = defaultdict(list)
for el in d['elements']:
    t = el.get('tags', {}); ref = t.get('ref', '').split(';')[0].strip()
    if not ref or 'geometry' not in el: continue
    pts = [(PX(g['lon']), PY(g['lat'])) for g in el['geometry']]
    byref[ref].append(pts)

CELL = 3
out = []
for ref, ways in byref.items():
    ways.sort(key=lambda w: -sum(math.hypot(w[i][0]-w[i-1][0], w[i][1]-w[i-1][1]) for i in range(1, len(w))))
    covered = set(); lines = []; total = 0
    for w in ways:
        # 반대 방향 차로가 이미 그려진 경우 건너뜀
        dense = [w[0]]
        for i in range(1, len(w)):
            (x0, y0), (x1, y1) = w[i-1], w[i]; n = max(1, int(math.hypot(x1-x0, y1-y0)//2))
            dense += [(x0+(x1-x0)*k/n, y0+(y1-y0)*k/n) for k in range(1, n+1)]
        cells = [(int(x//CELL), int(y//CELL)) for x, y in dense]
        inner = cells[2:-2] or cells
        near = sum(1 for c in inner if c in covered)
        if near >= 0.9*len(inner): continue
        for c in cells: covered.add(c)
        s = [(round(x), round(y)) for x, y in dp(w, 1.5)]
        s2 = [p for i, p in enumerate(s) if i == 0 or p != s[i-1]]
        if len(s2) < 2: continue
        L = sum(math.hypot(s2[i][0]-s2[i-1][0], s2[i][1]-s2[i-1][1]) for i in range(1, len(s2)))
        total += L
        r = [s2[0][0], s2[0][1]]
        for i in range(1, len(s2)): r += [s2[i][0]-s2[i-1][0], s2[i][1]-s2[i-1][1]]
        lines.append((' '.join(map(str, r)), s2, L))
    if total < 40: continue
    # 번호 표지: 긴 구간을 따라 약 450단위(≈45km)마다
    at = []; acc = 225
    for _, s2, _ in sorted(lines, key=lambda x: -x[2]):
        for i in range(1, len(s2)):
            seg = math.hypot(s2[i][0]-s2[i-1][0], s2[i][1]-s2[i-1][1]); acc += seg
            if acc >= 450: at.append([s2[i][0], s2[i][1]]); acc = 0
    if not at:
        s2 = max(lines, key=lambda x: x[2])[1]; at.append(list(s2[len(s2)//2]))
    out.append({'ref': ref, 'l': [x[0] for x in lines], 'at': at})

s = json.dumps(out, separators=(',', ':'))
open('expw_small.json', 'w').write(s)
print(len(out), 'refs', len(s.encode()), 'bytes;', sorted(o['ref'] for o in out)[:60])
