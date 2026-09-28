"""Artifact 버전 index.html을 독립 웹앱(카카오맵·IndexedDB 사진·PWA) 버전으로 바꾸는 1회용 패치."""
import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (a[:80], n)
    s = s.replace(a, b)

# ---------- head: PWA ----------
rep('<meta name="apple-mobile-web-app-status-bar-style" content="default">',
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="apple-touch-icon" href="icons/icon-192.png">')

# ---------- CSS ----------
rep('.maptools{position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:6px}',
    '.maptools{position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:6px;z-index:3}\n'
    '.kmap{position:absolute;inset:0}\n'
    '.kpin{position:relative;display:grid;place-items:center;width:22px;height:22px;border-radius:50%;border:2px solid var(--surface);background:var(--k);color:#fff;font-size:11px;font-weight:700;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.3);padding:0}\n'
    '.kpin.hollow{background:var(--surface);border:3px solid var(--k);width:18px;height:18px}\n'
    '.kpin.sel{outline:3px solid var(--flag);outline-offset:2px}\n'
    '.kpin .kl,.kflag .kl{position:absolute;left:calc(100% + 5px);top:50%;transform:translateY(-50%);white-space:nowrap;font-size:12px;font-weight:700;color:var(--ink);text-shadow:0 0 3px var(--surface),0 0 3px var(--surface),0 0 3px var(--surface)}\n'
    '.kflag{position:relative;cursor:pointer;width:20px;height:24px}\n'
    '.kmark{display:grid;place-items:center;width:24px;height:24px;border-radius:7px;background:var(--green);color:#fff;font-size:11px;font-weight:700;box-shadow:0 1px 4px rgba(0,0,0,.3)}\n'
    '.kme{width:16px;height:16px;border-radius:50%;background:#1A73E8;border:3px solid #fff;box-shadow:0 0 0 8px rgba(26,115,232,.18)}\n'
    '.namerow{display:flex;gap:8px}\n.namerow input{flex:1;min-width:0}\n.namerow .btn{flex:none}\n'
    '.kres{list-style:none;margin:8px 0 0;padding:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;max-height:320px;overflow-y:auto}\n'
    '.kres li+li{border-top:1px solid var(--line)}\n'
    '.kres button{display:block;width:100%;text-align:left;background:var(--surface);border:none;padding:10px 12px;cursor:pointer}\n'
    '.kres button:hover{background:var(--surface2)}\n'
    '.kres b{display:block;font-size:.95rem}\n.kres span{display:block;font-size:.8rem;color:var(--muted)}\n'
    '.keybox{font-family:ui-monospace,Consolas,monospace}\n'
    '.stat{display:inline-flex;align-items:center;gap:6px;font-size:.84rem;font-weight:700}\n.stat.ok{color:var(--green)}\n.stat.no{color:var(--warn)}\n.stat.off{color:var(--muted)}')
rep('.pickbar{position:absolute;', '.pickbar{z-index:3;position:absolute;')
rep('.mapcard{position:absolute;left:10px;right:10px;bottom:10px}', '.mapcard{position:absolute;left:10px;right:10px;bottom:10px;z-index:3}')

# ---------- icons ----------
rep(" brief:'<rect x=\"3.5\" y=\"7.5\" width=\"17\" height=\"12\" rx=\"2\"/><path d=\"M9 7.5V5h6v2.5\"/>'",
    " brief:'<rect x=\"3.5\" y=\"7.5\" width=\"17\" height=\"12\" rx=\"2\"/><path d=\"M9 7.5V5h6v2.5\"/>',\n"
    " gear:'<circle cx=\"12\" cy=\"12\" r=\"3\"/><path d=\"M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z\"/>'")

# ---------- photos: IndexedDB ----------
rep("function photoSrc(id){return String(id).slice(0,5)==='data:'?id:'/_blob/'+id;}",
"""/* 사진: 이 기기 모드에서는 IndexedDB에 원본(압축본)을 저장하고 'idb:키'로 가리킴 */
var IDB=null,PHURL={},BLANK='data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
function idb(){if(IDB)return IDB;IDB=new Promise(function(res,rej){var r=indexedDB.open('hooni-area',1);r.onupgradeneeded=function(){r.result.createObjectStore('photos');};r.onsuccess=function(){res(r.result);};r.onerror=function(){rej(r.error);};});return IDB;}
function idbReq(mode,fn){return idb().then(function(db){return new Promise(function(res,rej){var t=db.transaction('photos',mode),st=t.objectStore('photos'),out;var r=fn(st);if(r)r.onsuccess=function(){out=r.result;};t.oncomplete=function(){res(out);};t.onerror=function(){rej(t.error);};t.onabort=function(){rej(t.error||{code:'quota_or_state'});};});});}
function idbPut(k,v){return idbReq('readwrite',function(st){st.put(v,k);});}
function idbGet(k){return idbReq('readonly',function(st){return st.get(k);});}
function idbDel(k){return idbReq('readwrite',function(st){st.delete(k);});}
function idbAll(){return idb().then(function(db){return new Promise(function(res,rej){var out={},t=db.transaction('photos','readonly');var c=t.objectStore('photos').openCursor();c.onsuccess=function(){var cur=c.result;if(cur){out[cur.key]=cur.value;cur.continue();}};t.oncomplete=function(){res(out);};t.onerror=function(){rej(t.error);};});});}
function photoSrc(id){id=String(id);if(id.slice(0,5)==='data:')return id;
  if(id.slice(0,4)==='idb:'){if(PHURL[id])return PHURL[id];loadPhoto(id);return BLANK;}
  return '/_blob/'+id;}
function loadPhoto(id){if(PHURL[id]!==undefined)return;PHURL[id]='';
  idbGet(id.slice(4)).then(function(b){if(!b)return;PHURL[id]=URL.createObjectURL(b);
    document.querySelectorAll('img[data-pid="'+id+'"]').forEach(function(im){im.src=PHURL[id];});},function(){});}
function dropPhoto(id){id=String(id);if(id.slice(0,4)==='idb:'){idbDel(id.slice(4)).catch(function(){});if(PHURL[id]){URL.revokeObjectURL(PHURL[id]);}delete PHURL[id];}
  else if(S.assets&&id.slice(0,5)!=='data:')S.assets.delete(id).catch(function(){});}""")

n0 = s.count("h('img',{src:photoSrc(")
s = re.sub(r"h\('img',\{src:photoSrc\(([^)]+)\)", lambda m: "h('img',{'data-pid':" + m.group(1) + ",src:photoSrc(" + m.group(1) + ")", s)
assert n0 == 4, n0

rep("URL.revokeObjectURL(url);if(S.store==='db')c.toBlob(function(b){b?res(b):rej({code:'encode'});},'image/jpeg',q);else res(c.toDataURL('image/jpeg',q));};",
    "URL.revokeObjectURL(url);c.toBlob(function(b){b?res(b):rej({code:'encode'});},'image/jpeg',q);};")
rep("compress(f,S.store==='db'?1600:900,S.store==='db'?0.82:0.7).then(function(out){\n      if(S.store==='db')return S.assets.upload(out,{type:'image/jpeg'}).then(function(r){d.photos.push(r.id);uploaded.push(r.id);});d.photos.push(out);});",
    "compress(f,1600,0.82).then(function(out){\n      if(S.store==='db')return S.assets.upload(out,{type:'image/jpeg'}).then(function(r){d.photos.push(r.id);uploaded.push(r.id);});\n      var k=uid('ph');return idbPut(k,out).then(function(){d.photos.push('idb:'+k);uploaded.push('idb:'+k);});});")
rep("(p.photos||[]).forEach(function(id){if(S.assets&&String(id).slice(0,5)!=='data:')S.assets.delete(id).catch(function(){});});",
    "(p.photos||[]).forEach(dropPhoto);")
rep("uploaded.forEach(function(id){if(S.assets)S.assets.delete(id).catch(function(){});});", "uploaded.forEach(dropPhoto);")
rep("removed.concat(unused).forEach(function(id){if(S.assets&&String(id).slice(0,5)!=='data:')S.assets.delete(id).catch(function(){});});",
    "removed.concat(unused).forEach(dropPhoto);")

# ---------- Kakao: loader, search, map ----------
kakao_js = r"""
/* ================= Kakao ================= */
/* JavaScript 키는 카카오 개발자 콘솔에 등록한 주소에서만 동작해요. 설정 화면에서 바꿀 수 있어요. */
var DEFAULT_KAKAO_KEY='';
var KAKAO={key:lsGet('hooni-kakao-key','')||DEFAULT_KAKAO_KEY,rest:lsGet('hooni-kakao-rest',''),ready:false,err:'',places:null,geocoder:null};
function loadKakao(){
  if(!KAKAO.key||KAKAO.ready)return;
  var s=document.createElement('script');
  s.src='https://dapi.kakao.com/v2/maps/sdk.js?appkey='+encodeURIComponent(KAKAO.key)+'&libraries=services&autoload=false';
  s.onload=function(){try{kakao.maps.load(function(){KAKAO.ready=true;KAKAO.err='';KAKAO.places=new kakao.maps.services.Places();KAKAO.geocoder=new kakao.maps.services.Geocoder();render();});}catch(e){KAKAO.err='load';render();}};
  s.onerror=function(){KAKAO.err='net';render();};
  document.head.appendChild(s);
}
var KCAT={FD6:'food',CE7:'cafe',AT4:'sight',AD5:'stay'};
function kNorm(p){var addr=p.road_address_name||p.address_name||'';var t=(p.address_name||addr).split(' ');
  var cat=/골프/.test(p.category_name||'')?'golf':(KCAT[p.category_group_code]||'etc');
  return {name:p.place_name,addr:addr,area:t.slice(1,3).join(' '),lat:+p.y,lng:+p.x,phone:p.phone||'',url:p.place_url||'',cat:cat,
    catName:(p.category_name||'').split(' > ').slice(-1)[0],dist:p.distance?(+p.distance)/1000:null};}
function kSearch(q,near){return new Promise(function(res,rej){
  if(!KAKAO.ready)return rej({code:'nokakao'});var o={size:15};if(near&&inKorea(near))o.location=new kakao.maps.LatLng(near.lat,near.lng);
  KAKAO.places.keywordSearch(q,function(data,status){var S2=kakao.maps.services.Status;
    if(status===S2.OK)res(data.map(kNorm));else if(status===S2.ZERO_RESULT)res([]);else rej({code:'kakao'});},o);});}
function kAddr(q){return new Promise(function(res,rej){if(!KAKAO.ready)return rej({code:'nokakao'});
  KAKAO.geocoder.addressSearch(q,function(data,status){if(status===kakao.maps.services.Status.OK&&data[0])res({lat:+data[0].y,lng:+data[0].x});else res(null);});});}
/* 실제 자동차 경로 (카카오모빌리티, REST 키가 있을 때만) */
function kRoute(a,b){
  return fetch('https://apis-navi.kakaomobility.com/v1/directions?origin='+a.lng+','+a.lat+'&destination='+b.lng+','+b.lat+'&priority=RECOMMEND',{headers:{Authorization:'KakaoAK '+KAKAO.rest}})
  .then(function(r){if(!r.ok)throw {code:'http'+r.status};return r.json();})
  .then(function(j){var rt=j.routes&&j.routes[0];if(!rt||rt.result_code!==0)throw {code:'noroute'};
    var pts=[],names={};
    rt.sections.forEach(function(sec){sec.roads.forEach(function(rd){if(rd.name)names[rd.name]=(names[rd.name]||0)+rd.distance;
      for(var i=0;i+1<rd.vertexes.length;i+=2)pts.push({lat:rd.vertexes[i+1],lng:rd.vertexes[i]});});});
    var line=[pts[0]];for(var i=1;i<pts.length;i++){if(segKm(line[line.length-1],pts[i])>0.15||i===pts.length-1)line.push(pts[i]);}
    var top=Object.keys(names).sort(function(x,y){return names[y]-names[x];}).slice(0,2);
    return {line:line,km:Math.round(rt.summary.distance/1000),min:Math.round(rt.summary.duration/60),summary:top.length?top.join(' · ')+' 경유':''};});
}
function createKakaoMap(box,opts){
  var K=kakao.maps,el=h('div',{cls:'kmap'});box.appendChild(el);
  var map=new K.Map(el,{center:new K.LatLng(36.3,127.8),level:13});
  var data={line:[],pins:[],marks:[],flags:[],me:null,sel:null},objs=[];
  function ll(p){return new K.LatLng(p.lat,p.lng);}
  function levelFor(w){return Math.max(1,Math.min(14,Math.round(Math.log(Math.max(w,5)/40)/Math.LN2)+5));}
  function view(){if(opts.onView){var c=map.getCenter();opts.onView({lat:c.getLat(),lng:c.getLng(),level:map.getLevel()});}}
  function add(o){o.setMap(map);objs.push(o);return o;}
  function ov(p,node,z,ya){return add(new K.CustomOverlay({position:ll(p),content:node,zIndex:z||1,yAnchor:ya==null?0.5:ya,clickable:true}));}
  function tap(id,p){return function(e){e.stopPropagation();if(opts.onTap)opts.onTap({lat:p.lat,lng:p.lng},id);};}
  function draw(){
    objs.forEach(function(o){o.setMap(null);});objs=[];var lv=map.getLevel(),zoomed=lv<=6;
    if(data.line.length>1){var path=data.line.map(ll);
      add(new K.Polyline({path:path,strokeWeight:9,strokeColor:'#15201A',strokeOpacity:.35}));
      add(new K.Polyline({path:path,strokeWeight:5,strokeColor:'#FFC629',strokeOpacity:1}));}
    data.flags.forEach(function(f){if(!inKorea(f))return;var id='B:'+f.id;
      var n=h('div',{cls:'kflag',onclick:tap(id,f)});n.innerHTML='<svg width="20" height="24" viewBox="0 0 20 24"><path d="M3 23V2" stroke="#0E4428" stroke-width="2"/><path d="M3 2h13l-3.5 4.5L16 11H3z" fill="#FFC629" stroke="#0E4428"/></svg>';
      if(zoomed||data.sel===id)n.appendChild(h('span',{cls:'kl',text:f.name}));ov(f,n,2,1);});
    data.pins.forEach(function(p){if(!inKorea(p))return;
      var b=h('button',{type:'button',cls:'kpin k-'+(p.cat||'etc')+(p.hollow?' hollow':'')+(data.sel===p.id?' sel':''),'aria-label':p.name,onclick:tap(p.id,p)},
        p.n?String(p.n):(p.star&&!p.hollow?'★':''),(zoomed||data.sel===p.id)?h('span',{cls:'kl',text:p.name}):null);
      ov(p,b,data.sel===p.id?5:3);});
    data.marks.forEach(function(m){if(inKorea(m))ov(m,h('div',{cls:'kmark',text:m.t}),4);});
    if(data.me&&inKorea(data.me))ov(data.me,h('div',{cls:'kme'}),6);
  }
  function fit(pts){pts=(pts||[]).filter(inKorea);
    if(!pts.length){map.setLevel(13);map.setCenter(new K.LatLng(36.3,127.8));}
    else if(pts.length===1){map.setLevel(5);map.setCenter(ll(pts[0]));}
    else{var bd=new K.LatLngBounds();pts.forEach(function(p){bd.extend(ll(p));});map.setBounds(bd,40,40,40,40);}
    view();draw();}
  K.event.addListener(map,'click',function(e){if(opts.onTap)opts.onTap({lat:e.latLng.getLat(),lng:e.latLng.getLng()},null);});
  K.event.addListener(map,'idle',view);
  var lastZoomed=null;K.event.addListener(map,'zoom_changed',function(){var z=map.getLevel()<=6;if(z!==lastZoomed){lastZoomed=z;draw();}});
  var vb=opts.vb;
  if(vb&&vb.level!=null){map.setLevel(vb.level);map.setCenter(new K.LatLng(vb.lat,vb.lng));}
  else if(vb&&vb.w){map.setLevel(levelFor(vb.w));map.setCenter(new K.LatLng(toLat(vb.y+vb.h/2),toLng(vb.x+vb.w/2)));}
  box.appendChild(h('div',{cls:'maptools'},
    h('button',{cls:'mt',type:'button','aria-label':'확대',onclick:function(){map.setLevel(map.getLevel()-1,{animate:true});}},'+'),
    h('button',{cls:'mt',type:'button','aria-label':'축소',onclick:function(){map.setLevel(map.getLevel()+1,{animate:true});}},'−'),
    opts.fitPts?h('button',{cls:'mt txt',type:'button','aria-label':'전체 보기',onclick:function(){fit(opts.fitPts());}},'전체'):null,
    opts.locate?h('button',{cls:'mt txt',type:'button','aria-label':'내 위치',onclick:function(){getMe().then(function(m){S.me=m;data.me=m;map.setLevel(5);map.setCenter(ll(m));draw();},function(){toast('현재 위치를 가져오지 못했어요.');});}},'내 위치'):null));
  return {set:function(d){data=Object.assign(data,d);},fit:fit,draw:draw,
    zoomTo:function(p,w){map.setLevel(levelFor(w));map.setCenter(ll(p));view();draw();},
    fixAspect:function(){map.relayout();}};
}
"""
rep("/* ================= map ================= */\nfunction createMap(box,opts){\n",
    kakao_js + "\n/* ================= map ================= */\nfunction createMap(box,opts){\n  if(KAKAO.ready)return createKakaoMap(box,opts);\n")
rep("  var vb=opts.vb||null,data={line:[],pins:[],marks:[],flags:[],me:null,sel:null};",
    "  var vb=(opts.vb&&opts.vb.w)?opts.vb:null,data={line:[],pins:[],marks:[],flags:[],me:null,sel:null};")

# ---------- route: destination via Kakao, real road route ----------
a = s.index("function fallbackRoute(){")
b = s.index("function addRecent(){")
s = s[:a] + r"""function resolvePlace(q,near){q=(q||'').trim();if(!q)return Promise.resolve(null);
  var all=S.places.concat(S.bases);var hit=all.filter(function(p){return inKorea(p)&&(p.name.indexOf(q)>=0||(p.address||'').indexOf(q)>=0);})[0];
  if(hit)return Promise.resolve({name:hit.name,lat:hit.lat,lng:hit.lng});
  if(!KAKAO.ready)return Promise.resolve(null);
  return kSearch(q,near).then(function(r){return r[0]?{name:r[0].name,lat:r[0].lat,lng:r[0].lng}:null;},function(){return null;});}
function fallbackRoute(){
  S.loading='가는 길을 찾고 있어요.';render();
  var startP=S.useMe?getMe().then(function(p){S.me=p;return {name:'현재 위치',lat:p.lat,lng:p.lng};},function(){return null;}):resolvePlace(S.from,S.me);
  startP.then(function(st){
    var destP=S.toPos&&inKorea(S.toPos)?Promise.resolve({name:S.to,lat:S.toPos.lat,lng:S.toPos.lng}):resolvePlace(S.to,st||S.me);
    return destP.then(function(d){
      if(!st){S.loading='';S.routeErr=S.useMe?'현재 위치를 가져오지 못했어요. 출발지를 직접 적어주세요.':'출발지를 찾지 못했어요. 이름을 조금 더 자세히 적어주세요.';if(S.useMe)S.useMe=false;render();return;}
      if(!d){S.loading='';S.routeErr=KAKAO.ready?'목적지를 찾지 못했어요. 지역 이름을 함께 적어주세요. 예) 강릉 초당순두부':'카카오 키가 없어서 내 장소나 거점에 있는 곳만 목적지로 쓸 수 있어요. 설정에서 카카오 키를 넣어주세요.';render();return;}
      S.toPos={lat:d.lat,lng:d.lng};
      var done=function(r){S.route={start:st,dest:d,line:r?r.line:[st,d],summary:r?r.summary:'직선 기준',km:r?r.km:Math.round(lineLen([st,d])),min:r?r.min:0,sit:S.sit};
        S.recs=[];S.rvb=null;S.loading='';addRecent();render();};
      if(KAKAO.rest)kRoute(st,d).then(done,function(e){toast(e&&e.code==='http401'?'REST 키가 맞지 않아서 직선으로 보여줘요.':'도로 경로를 못 받아서 직선으로 보여줘요.');done(null);});
      else done(null);
    });
  });
}
""" + s[b:]

# ---------- home notice ----------
m = re.search(r"  else if\(!S\.sample\)out\.push\(h\('p',\{cls:'notice',text:'테스트 웹에서는[^\n]*\n", s)
assert m
s = s[:m.start()] + ("  else if(!S.sample&&!KAKAO.ready)out.push(h('div',{cls:'notice'},KAKAO.err?'카카오 지도에 연결하지 못했어요. 설정에서 키와 등록한 주소를 확인해 주세요. ':'설정에서 카카오 키를 넣으면 실제 지도, 장소 검색, 목적지 찾기를 쓸 수 있어요. ',"
                     "h('button',{cls:'linkbtn',onclick:openSettings},'설정 열기')));\n") + s[m.end():]

# ---------- locControls: Kakao lookup ----------
rep("    S.sample?h('button',{type:'button',cls:'btn',onclick:function(ev){if(!(d.name",
    "    KAKAO.ready?h('button',{type:'button',cls:'btn',onclick:function(ev){var nm=(d.name||'').trim(),ad=(d.address||'').trim();if(!nm&&!ad){toast('이름이나 주소를 먼저 적어주세요.');return;}var b=ev.currentTarget;b.disabled=true;b.textContent='찾는 중';\n"
    "      (ad?kAddr(ad):Promise.resolve(null)).then(function(g){return g||kSearch(nm+(d.area?' '+d.area:''),S.me).then(function(r){return r[0]||null;});}).then(function(g){if(g&&inKorea(g)){d.lat=+(+g.lat).toFixed(6);d.lng=+(+g.lng).toFixed(6);st.pick=true;toast('위치를 찾았어요. 지도에서 확인해 주세요.');redraw();}else{toast('못 찾았어요. 지도에서 찍어주세요.');b.disabled=false;b.textContent='주소·이름으로 찾기';}},function(){toast('카카오 검색에 실패했어요.');b.disabled=false;b.textContent='주소·이름으로 찾기';});}},'주소·이름으로 찾기'):\n"
    "    S.sample?h('button',{type:'button',cls:'btn',onclick:function(ev){if(!(d.name")

# ---------- editor: name search ----------
rep("      h('label',{cls:'f',text:'이름'}),h('input',{type:'text',value:d.name,placeholder:golf?'예) 남촌CC':'장소 이름',autocomplete:'off',oninput:function(e){d.name=e.target.value;}}),",
    "      h('label',{cls:'f',text:'이름'}),nameField(),")
rep("  var uploaded=[],st={pick:false};var canPhoto=S.store==='local'||!!S.assets;var more=!isNew;",
r"""  var uploaded=[],st={pick:false,results:null,searching:false};var canPhoto=S.store==='local'||!!S.assets;var more=!isNew;
  function runSearch(){var q=(d.name||'').trim();if(!q){toast('가게 이름을 먼저 적어주세요.');return;}st.searching=true;redraw();
    kSearch(q,S.me||(inKorea(d)?d:null)).then(function(r){st.searching=false;st.results=r;redraw();},function(){st.searching=false;st.results=[];toast('카카오 검색에 실패했어요.');redraw();});}
  function pickResult(r){d.name=r.name;d.address=r.addr;d.area=d.area||r.area;d.lat=+r.lat.toFixed(6);d.lng=+r.lng.toFixed(6);if(r.phone)d.phone=r.phone;if(r.url)d.kakaoUrl=r.url;
    if(isNew&&r.cat!=='etc'){d.cat=r.cat;if(r.cat==='golf'&&d.tags.indexOf('골프')<0)d.tags=d.tags.concat(['골프']);}st.results=null;toast(r.name+' 정보를 넣었어요.');redraw();}
  function nameField(){var golf=d.cat==='golf';
    var inp=h('input',{type:'text',value:d.name,placeholder:golf?'예) 남촌CC':'가게 이름',autocomplete:'off',oninput:function(e){d.name=e.target.value;},
      onkeydown:function(e){if(e.key==='Enter'&&KAKAO.ready){e.preventDefault();runSearch();}}});
    if(!KAKAO.ready)return inp;
    var out=[h('div',{cls:'namerow'},inp,h('button',{type:'button',cls:'btn green',disabled:st.searching,onclick:runSearch},st.searching?'찾는 중':'카카오 검색'))];
    if(st.results)out.push(st.results.length?h('ul',{cls:'kres'},st.results.map(function(r){return h('li',null,h('button',{type:'button',onclick:function(){pickResult(r);}},
      h('b',{text:r.name}),h('span',{text:[r.catName,r.dist!=null?kmFmt(r.dist):''].filter(Boolean).join(' · ')}),h('span',{text:r.addr})));})):h('p',{cls:'hint',text:'검색 결과가 없어요. 이름을 바꿔보거나 지도에서 찍어주세요.'}));
    else if(isNew&&!d.address)out.push(h('p',{cls:'hint',text:'이름을 적고 검색하면 주소와 위치가 자동으로 들어가요.'}));
    return out;}""")

# ---------- detail: phone & kakao link ----------
rep("      p.visitedAt?[h('dt',{text:'다녀온 날'}),h('dd',{text:p.visitedAt})]:null,",
    "      p.phone?[h('dt',{text:'전화'}),h('dd',null,h('a',{href:'tel:'+p.phone,text:p.phone}))]:null,\n"
    "      p.visitedAt?[h('dt',{text:'다녀온 날'}),h('dd',{text:p.visitedAt})]:null,")
rep("      h('a',{cls:'btn',href:naverSearch(p),target:'_blank',rel:'noopener'},'네이버지도')),\n    h('div',{cls:'actions'}",
    "      p.kakaoUrl?h('a',{cls:'btn',href:p.kakaoUrl,target:'_blank',rel:'noopener'},'카카오 정보'):null,\n"
    "      h('a',{cls:'btn',href:naverSearch(p),target:'_blank',rel:'noopener'},'네이버지도')),\n    h('div',{cls:'actions'}")

# ---------- backup with photos + settings ----------
a = s.index("/* ================= backup (local mode) ================= */")
b = s.index("/* ================= shell ================= */")
s = s[:a] + r"""/* ================= settings & backup ================= */
function blobToData(b){return new Promise(function(res,rej){var r=new FileReader();r.onload=function(){res(r.result);};r.onerror=rej;r.readAsDataURL(b);});}
function downloadBackup(){
  toast('백업 파일을 만드는 중이에요.');
  idbAll().catch(function(){return {};}).then(function(all){var keys=Object.keys(all);
    return Promise.all(keys.map(function(k){return blobToData(all[k]);})).then(function(urls){var ph={};keys.forEach(function(k,i){ph[k]=urls[i];});return ph;});})
  .then(function(ph){var data={app:'hooni-area',version:3,at:new Date().toISOString(),places:S.places,bases:S.bases,trips:S.trips,photos:ph};
    var b=new Blob([JSON.stringify(data)],{type:'application/json'});var u=URL.createObjectURL(b);
    var a=h('a',{href:u,download:'hooni-area-'+today()+'.json'});document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u);},4000);toast('백업 파일을 내려받았어요.');});
}
function importBackup(f){var r=new FileReader();r.onload=function(){var o;try{o=JSON.parse(r.result);}catch(_){o=null;}
  if(!o||(o.app!=='huni-range'&&o.app!=='hooni-area')||!Array.isArray(o.places)){toast('HooNI Area 백업 파일이 아니에요.');return;}
  var ph=o.photos||{};
  Promise.all(Object.keys(ph).map(function(k){return fetch(ph[k]).then(function(x){return x.blob();}).then(function(b){return idbPut(k,b);});})).then(function(){
    var ok=lsSet('huni2-places',o.places)&&lsSet('huni2-bases',o.bases||[])&&lsSet('huni2-trips',o.trips||[]);
    if(!ok){toast('기기 저장 공간이 부족해요.');return;}
    S.places=o.places;S.bases=o.bases||[];S.trips=o.trips||[];sheet.close();toast('백업을 불러왔어요. 장소 '+o.places.length+'곳');render();},function(){toast('사진을 저장하지 못했어요. 저장 공간을 확인해 주세요.');});};r.readAsText(f);}
function openBackup(){openSettings();}
function openSettings(){
  var key=h('input',{type:'text',cls:'keybox',value:KAKAO.key||'',placeholder:'카카오 JavaScript 키',autocomplete:'off',spellcheck:'false'});
  var rest=h('input',{type:'text',cls:'keybox',value:KAKAO.rest||'',placeholder:'카카오 REST API 키 (선택)',autocomplete:'off',spellcheck:'false'});
  var file=h('input',{type:'file',accept:'.json,application/json',style:'display:none',onchange:function(e){var f=e.target.files&&e.target.files[0];if(f)importBackup(f);}});
  var stat=KAKAO.ready?h('span',{cls:'stat ok',text:'● 카카오 지도 연결됨'}):KAKAO.err?h('span',{cls:'stat no',text:'● 연결 실패: 키가 맞는지, 이 주소('+location.origin+')를 카카오 콘솔 Web 플랫폼에 등록했는지 확인해 주세요'}):h('span',{cls:'stat off',text:KAKAO.key?'● 연결 중':'● 키 없음: 간단한 기본 지도로 보여줘요'});
  sheet.replaceChildren(h('div',{cls:'sheet'},h('div',{cls:'grab'}),h('h2',{text:'설정'}),
    h('label',{cls:'f',text:'카카오 지도'}),stat,
    h('label',{cls:'f',text:'JavaScript 키'}),key,
    h('label',{cls:'f',text:'REST API 키 (실제 도로 경로용, 선택)'}),rest,
    h('p',{cls:'hint',text:'REST 키를 넣으면 가는 길 맛집을 직선이 아니라 실제 자동차 경로 기준으로 찾아요.'}),
    h('div',{cls:'row',style:'margin-top:10px'},h('button',{cls:'btn green',onclick:function(){
      var k=key.value.trim(),rk=rest.value.trim();lsSet('hooni-kakao-key',k);lsSet('hooni-kakao-rest',rk);KAKAO.rest=rk;
      if(k!==KAKAO.key){KAKAO.key=k;toast('저장했어요. 새 키로 다시 불러와요.');setTimeout(function(){location.reload();},600);}else{toast('저장했어요.');sheet.close();render();}}},'키 저장')),
    h('label',{cls:'f',style:'margin-top:26px',text:'백업'}),
    h('p',{cls:'hint',text:'기록과 사진은 이 기기 브라우저에 저장돼요. 브라우저 데이터를 지우면 사라지니 가끔 백업 파일을 내려받아 두세요. 다른 기기로 옮길 때도 이 파일을 불러오면 돼요.'}),
    h('p',{cls:'hint',text:'장소 '+S.places.length+'곳, 거점 '+S.bases.length+'곳, 일정 '+S.trips.length+'개'}),
    h('div',{cls:'row',style:'margin-top:8px'},h('button',{cls:'btn green',onclick:downloadBackup},'백업 내려받기'),h('button',{cls:'btn',onclick:function(){file.click();}},'백업 불러오기'),file),
    h('p',{cls:'hint',style:'margin-top:10px',text:'불러오면 지금 기기에 있는 기록은 백업 파일 내용으로 바뀌어요.'})));
  if(!sheet.open)sheet.showModal();
}

""" + s[b:]

rep("    S.store==='local'?h('button',{cls:'iconbtn','aria-label':'백업',style:who?'':'margin-left:auto',onclick:openBackup},icon('brief')):null));",
    "    h('button',{cls:'iconbtn','aria-label':'설정',style:who?'':'margin-left:auto',onclick:openSettings},icon('gear'))));")

# ---------- boot ----------
rep("}else{S.sampleReady=true;startLocal();}\n})();",
    "}else{S.sampleReady=true;startLocal();}\nloadKakao();\n"
    "if('serviceWorker' in navigator&&/^https?:$/.test(location.protocol))navigator.serviceWorker.register('sw.js').catch(function(){});\n})();")

open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched', len(s.encode()))
