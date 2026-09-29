import re, json, os
here = os.path.dirname(os.path.abspath(__file__))
p = r'C:\Users\User\Desktop\index.html'
s = open(p, encoding='utf-8').read()
md = open(os.path.join(here, 'mapdata.json'), encoding='utf-8').read()
ex = [e for e in json.load(open(os.path.join(here, 'expw_small.json'))) if e['ref'].isdigit()]
exs = json.dumps(ex, separators=(',', ':'))

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (a[:70], n)
    s = s.replace(a, b)

rep("--sea:#DDE7EA;--land:#FBFBF8;--coast:#B8C3C1;", "--sea:#DDE7EA;--land:#FBFBF8;--coast:#B8C3C1;--land-dim:#ECEFEA;--border:#D3DAD1;--expw:#6E9C82;")
rep("--sea:#0D171B;--land:#1E2622;--coast:#374640;", "--sea:#0D171B;--land:#1E2622;--coast:#374640;--land-dim:#161C19;--border:#2E3A33;--expw:#4E8266;", 2)
rep(".land{fill:var(--land);stroke:var(--coast)}",
    ".land{fill:var(--land);stroke:var(--coast)}\n"
    ".land-dim{fill:var(--land-dim);stroke:var(--coast);stroke-opacity:.5}\n"
    ".muni-line{fill:none;stroke:var(--border)}\n"
    ".expw{fill:none;stroke:var(--expw);stroke-linecap:round;stroke-linejoin:round}\n"
    ".muni-lbl{fill:var(--muted);stroke:var(--land);paint-order:stroke;stroke-linejoin:round}\n"
    ".shield{fill:var(--expw)}\n"
    ".shield-t{fill:#fff;font-weight:700}")

data_js = (
    "/* 시도·시군구 경계: 통계청 2013 경계(southkorea-maps), 고속도로: OpenStreetMap(ODbL). 지도 좌표로 단순화한 델타 인코딩 */\n"
    "var MAPD=" + md + ";\n"
    "var EXPW=" + exs + ";\n"
    "var NK=[[37.78,124.6],[37.8,125.6],[37.84,126.1],[37.86,126.55],[37.93,126.72],[38.0,126.95],[38.18,127.2],[38.2,127.6],[38.22,128.0],[38.34,128.25],[38.55,128.37],[38.8,128.25],[39.3,127.75],[40.2,127.9],[40.2,124.0],[37.78,124.0]];\n"
    "var GEO=null;\n"
    "function geo(){if(GEO)return GEO;\n"
    "  function toD(r,close){var a=r.split(' ');return 'M'+a[0]+' '+a[1]+'l'+a.slice(2).join(' ')+(close?'z':'');}\n"
    "  GEO={prov:MAPD.prov.map(function(p){return p.r.map(function(r){return toD(r,true);}).join('');}),\n"
    "    muni:MAPD.muni.map(function(m){return m.r.map(function(r){return toD(r,true);}).join('');}).join(''),\n"
    "    lbl:MAPD.muni.map(function(m){return {n:m.n.replace(/^.+시(.+구)$/,'$1'),x:m.c[0],y:m.c[1],w:m.c[2]};}).sort(function(a,b){return b.w-a.w;}),\n"
    "    nk:NK.map(function(c,i){return (i?'L':'M')+PX(c[1]).toFixed(1)+' '+PY(c[0]).toFixed(1);}).join(' ')+' Z',\n"
    "    expw:EXPW.map(function(e){return {ref:e.ref,d:e.l.map(function(r){return toD(r,false);}).join(''),at:e.at};})};\n"
    "  return GEO;}\n")
s, n = re.subn(r"var KOREA=\[\[.*?\]\];\nvar JEJU=\[\[.*?\]\];\n", lambda m: data_js, s, flags=re.S)
assert n == 1

rep("  var landK=poly(KOREA),landJ=poly(JEJU);\n", "  var G=geo();\n")
rep("  function poly(pts){return pts.map(function(c,i){return (i?'L':'M')+PX(c[1]).toFixed(1)+' '+PY(c[0]).toFixed(1);}).join(' ')+' Z';}\n", "")

a = s.index("    [landK,landJ].forEach(")
b = s.index("\n", s.index("CITIES.forEach(function(c){if(c[3]===2&&vb.w>2600)return;"))
new = (
"    svg.appendChild(sv('path',{class:'land-dim',d:G.nk,'stroke-width':1,'vector-effect':'non-scaling-stroke'}));\n"
"    G.prov.forEach(function(d){svg.appendChild(sv('path',{class:'land',d:d,'stroke-width':vb.w<1400?1.4:1,'vector-effect':'non-scaling-stroke','stroke-linejoin':'round'}));});\n"
"    if(vb.w<1600)svg.appendChild(sv('path',{class:'muni-line',d:G.muni,'stroke-width':.8,'vector-effect':'non-scaling-stroke','stroke-linejoin':'round'}));\n"
"    var shields=[];G.expw.forEach(function(e){svg.appendChild(sv('path',{class:'expw',d:e.d,'stroke-width':vb.w<1400?2.6:1.5,'vector-effect':'non-scaling-stroke'}));if(vb.w<2200)e.at.forEach(function(a){shields.push({t:e.ref,x:a[0],y:a[1]});});});\n"
"    // 글자 겹침 피하기: 큰 곳부터 놓고, 이미 놓인 글자와 겹치면 건너뜀\n"
"    var placed=[];function free(x,y,w,hh){for(var i=0;i<placed.length;i++){var q=placed[i];if(x<q[0]+q[2]&&x+w>q[0]&&y<q[1]+q[3]&&y+hh>q[1])return false;}placed.push([x,y,w,hh]);return true;}\n"
"    function inView(x,y){return x>vb.x&&x<vb.x+vb.w&&y>vb.y&&y<vb.y+vb.h;}\n"
"    if(vb.w>=1300)CITIES.forEach(function(c){if(c[3]===2&&vb.w>2600)return;var x=PX(c[2]),y=PY(c[1]),fs=(c[3]===1?12.5:11)*sc,w=c[0].length*fs;if(!free(x-w/2,y-fs,w,fs*1.2))return;svg.appendChild(sv('text',{class:'city',x:x,y:y,'text-anchor':'middle','font-size':fs,'font-weight':c[3]===1?700:400},c[0]));});\n"
"    else G.lbl.forEach(function(l){if(l.w<vb.w*0.035||!inView(l.x,l.y))return;var fs=11.5*sc,w=l.n.length*fs;if(!free(l.x-w/2,l.y-fs*0.6,w,fs*1.2))return;\n"
"      svg.appendChild(sv('text',{class:'muni-lbl',x:l.x,y:l.y,'text-anchor':'middle','dominant-baseline':'central','font-size':fs,'stroke-width':3*sc},l.n));});\n"
"    shields.forEach(function(sh){if(!inView(sh.x,sh.y))return;var w=(sh.t.length*6.5+8)*sc,hh=14*sc;if(!free(sh.x-w/2,sh.y-hh/2,w,hh))return;\n"
"      svg.appendChild(sv('rect',{class:'shield',x:sh.x-w/2,y:sh.y-hh/2,width:w,height:hh,rx:3*sc}));svg.appendChild(sv('text',{class:'shield-t',x:sh.x,y:sh.y,'text-anchor':'middle','dominant-baseline':'central','font-size':9.5*sc},sh.t));});")
s = s[:a] + new + s[b:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok', len(s.encode()), 'bytes;', len(ex), 'expressways')
