"""골프장 아침 식당 기능: 아침 가능 표시·여는 시간, 필터, 골프장별 아침 식당 화면, 카카오 후보 찾기."""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (a[:80], n)
    s = s.replace(a, b)

# CSS
rep(".tag{font-size:.74rem;", ".tag.sun{background:var(--flag);color:var(--flag-ink)}\n.gm-note{font-size:.8rem;color:var(--muted);margin:4px 0 0}\n.tag{font-size:.74rem;")

# helpers + golf morning sheet (openBase 앞에)
rep("function openBase(b){", r"""/* ================= golf breakfast ================= */
function isBreakfast(p){return (p.meals||[]).indexOf('아침')>=0;}
function golfSpots(){var out=[];
  S.bases.forEach(function(b){if(b.type==='golf'&&inKorea(b))out.push({key:'B:'+b.id,name:b.name,lat:b.lat,lng:b.lng});});
  S.places.forEach(function(p){if(p.cat==='golf'&&inKorea(p)&&!out.some(function(o){return sameSpot(o,p);}))out.push({key:p.id,name:p.name,lat:p.lat,lng:p.lng});});
  return out;}
function breakfastNear(g,r){return nearby(g,r||15).filter(function(p){return p.cat!=='golf'&&isBreakfast(p);});}
var MORNING_KW=['해장국','국밥','기사식당','콩나물국밥','김밥'];
function kMorning(g){
  var K=kakao.maps.services;
  return Promise.all(MORNING_KW.map(function(kw){return new Promise(function(res){
    KAKAO.places.keywordSearch(kw,function(d,st){res(st===K.Status.OK?d:[]);},{location:new kakao.maps.LatLng(g.lat,g.lng),radius:15000,sort:K.SortBy.DISTANCE,size:15});});}))
  .then(function(all){var seen={},out=[];all.forEach(function(arr){arr.forEach(function(x){if(seen[x.id])return;seen[x.id]=1;if(!/음식점/.test(x.category_name||''))return;out.push(kNorm(x));});});
    return out.sort(function(a,b){return (a.dist||99)-(b.dist||99);}).slice(0,20);});}
function openGolfMorning(g){
  var st={loading:false,res:null};
  function draw(){
    var mine=breakfastNear(g,15);
    var body=[h('div',{cls:'grab'}),h('h2',{text:'☀ '+g.name+' 아침 식당'}),h('p',{cls:'hint',text:'라운딩 전에 들르기 좋은 곳이에요. 반경 15km, 가까운 순서.'}),
      h('h3',{style:'margin:16px 0 8px;font-size:1rem',text:'내 기록 '+mine.length+'곳'}),
      mine.length?h('ul',{cls:'list'},mine.map(function(p){return listRow(p,false,function(){openDetail(placeById(p.id));});})):
        h('p',{cls:'hint',text:'아직 아침 식당으로 표시한 곳이 없어요. 기록할 때 "☀ 아침 돼요"를 눌러두면 여기에 모여요.'})];
    if(KAKAO.ready){
      body.push(h('h3',{style:'margin:22px 0 8px;font-size:1rem',text:'카카오에서 아침 후보 찾기'}),
        h('p',{cls:'hint',text:'해장국·국밥·기사식당·김밥처럼 아침에 여는 곳이 많은 식당을 찾아요. 실제 여는 시간은 카카오 정보에서 꼭 확인하세요.'}));
      if(!st.res)body.push(h('button',{cls:'btn green',disabled:st.loading,onclick:function(){st.loading=true;draw();kMorning(g).then(function(r){st.loading=false;st.res=r;draw();},function(){st.loading=false;st.res=[];toast('카카오 검색에 실패했어요.');draw();});}},st.loading?'찾는 중':'근처 아침 후보 찾기'));
      else if(!st.res.length)body.push(h('p',{cls:'hint',text:'근처에서 찾지 못했어요.'}));
      else body.push(h('ul',{cls:'list'},st.res.map(function(r){
        var saved=S.places.some(function(x){return sameSpot(x,r);});
        return h('li',null,h('div',{cls:'li k-food',style:'cursor:default'},h('div',{cls:'th'},r.name.slice(0,1)),
          h('div',null,h('h4',{text:r.name}),h('div',{cls:'meta'},h('span',{cls:'kt',text:r.catName||'식당'}),r.dist!=null?h('span',{text:kmFmt(r.dist)}):null,h('span',{text:r.area})),
            h('div',{cls:'row',style:'margin-top:6px'},r.url?h('a',{cls:'btn',href:r.url.replace('http://','https://'),target:'_blank',rel:'noopener'},'여는 시간 확인'):null,
              h('button',{cls:'btn primary',disabled:saved,onclick:function(){
                var np={id:newId('places'),name:r.name,cat:'food',status:'wish',revisit:'',tags:['골프'],meals:['아침'],feats:[],price:'',menu:r.catName||'',memo:g.name+' 근처 아침 후보 (카카오 검색)',area:r.area,address:r.addr,list:'골프장 아침',visitedAt:'',photos:[],lat:+r.lat.toFixed(6),lng:+r.lng.toFixed(6),phone:r.phone,kakaoUrl:(r.url||'').replace('http://','https://'),src:'kakao'};
                colSave('places',np).then(function(){toast(r.name+' 저장했어요.');draw();},writeErr);}},saved?'저장됨':'아침 후보로 저장')))));})));
    }
    var y=sheet.scrollTop;sheet.replaceChildren(h('div',{cls:'sheet'},body));sheet.scrollTop=y;if(!sheet.open)sheet.showModal();
  }
  draw();
}
function openBase(b){""")

# openBase golf: 아침 버튼
rep("      inKorea(b)?h('button',{cls:'btn',onclick:function(){goRouteTo(b);}},'가는 길 맛집'):null,\n      h('button',{cls:'btn',onclick:function(){openBaseEditor(b);}},'수정'))];",
    "      inKorea(b)?h('button',{cls:'btn',onclick:function(){goRouteTo(b);}},'가는 길 맛집'):null,\n"
    "      b.type==='golf'&&inKorea(b)?h('button',{cls:'btn',onclick:function(){openGolfMorning({key:'B:'+b.id,name:b.name,lat:b.lat,lng:b.lng});}},'☀ 아침 식당'):null,\n"
    "      h('button',{cls:'btn',onclick:function(){openBaseEditor(b);}},'수정'))];")

# openDetail golf: 아침 버튼
rep("    h('div',{cls:'row'},inKorea(p)?h('a',{cls:'btn green',href:kakaoTo(p),target:'_blank',rel:'noopener'},'길안내'):null,\n      inKorea(p)?h('button',{cls:'btn',onclick:function(){goRouteTo(p);}},'가는 길 맛집'):null,\n      inKorea(p)?h('button',{cls:'btn',onclick:function(){sheet.close();",
    "    h('div',{cls:'row'},inKorea(p)?h('a',{cls:'btn green',href:kakaoTo(p),target:'_blank',rel:'noopener'},'길안내'):null,\n"
    "      p.cat==='golf'&&inKorea(p)?h('button',{cls:'btn',onclick:function(){openGolfMorning({key:p.id,name:p.name,lat:p.lat,lng:p.lng});}},'☀ 아침 식당'):null,\n"
    "      inKorea(p)?h('button',{cls:'btn',onclick:function(){goRouteTo(p);}},'가는 길 맛집'):null,\n      inKorea(p)?h('button',{cls:'btn',onclick:function(){sheet.close();")
rep("      p.phone?[h('dt',{text:'전화'}),h('dd',null,h('a',{href:'tel:'+p.phone,text:p.phone}))]:null,",
    "      isBreakfast(p)&&p.cat!=='golf'?[h('dt',{text:'아침'}),h('dd',{text:p.opens?p.opens+'부터 영업':'아침 식사 가능'})]:null,\n"
    "      p.phone?[h('dt',{text:'전화'}),h('dd',null,h('a',{href:'tel:'+p.phone,text:p.phone}))]:null,")

# 홈: 골프장 아침 식당 섹션
rep("  // again\n",
    "  // golf breakfast\n"
    "  var gs=golfSpots();\n"
    "  if(gs.length){out.push(h('section',{cls:'sec'},h('div',{cls:'sech'},h('h3',{text:'☀ 골프장 아침 식당'})),\n"
    "    h('div',{cls:'hscroll'},gs.map(function(g){var n=breakfastNear(g,15).length;return h('button',{cls:'base',type:'button',onclick:function(){openGolfMorning(g);}},h('div',{cls:'ic'},icon('flag',20)),h('b',{text:g.name}),h('span',{text:n?'아침 '+n+'곳':'아침 식당 찾기'}));}))));}\n"
    "  // again\n")

# 리스트 칩 + 필터
rep("[['all','전부'],['visited','다녀온 곳'],['again','또 갈래'],['wish','가고 싶은 곳']]",
    "[['all','전부'],['visited','다녀온 곳'],['again','또 갈래'],['wish','가고 싶은 곳'],['breakfast','☀ 아침 가능']]")
rep("    if(S.lstat==='again'&&p.revisit!=='again')return false;",
    "    if(S.lstat==='again'&&p.revisit!=='again')return false;\n    if(S.lstat==='breakfast'&&!isBreakfast(p))return false;")

# 지도 칩 + 필터
rep("mf:'all',msit:'',msel:null,mvb:null,", "mf:'all',msit:'',mbf:false,msel:null,mvb:null,")
rep("var list=S.places.filter(function(p){if(S.mf!=='all'&&p.cat!==S.mf)return false;",
    "var list=S.places.filter(function(p){if(S.mbf&&!isBreakfast(p))return false;if(S.mf!=='all'&&p.cat!==S.mf)return false;")
rep("    SITS.map(function(s){return h('button',{cls:'chip','aria-pressed':S.msit===s?'true':'false',onclick:function(){S.msit=S.msit===s?'':",
    "    h('button',{cls:'chip','aria-pressed':S.mbf?'true':'false',onclick:function(){S.mbf=!S.mbf;S.msel=null;render();}},'☀ 아침'),\n"
    "    SITS.map(function(s){return h('button',{cls:'chip','aria-pressed':S.msit===s?'true':'false',onclick:function(){S.msit=S.msit===s?'':")

# 목록 행: 아침 표시
rep("typeof p.dist==='number'?h('span',{text:kmFmt(p.dist)}):null",
    "typeof p.dist==='number'?h('span',{text:kmFmt(p.dist)}):null,isBreakfast(p)&&p.cat!=='golf'?h('span',{cls:'tag sun',text:'☀ '+(p.opens?p.opens+' 오픈':'아침')}):null")

# 기록 화면: 간단 영역에 아침 토글 + 여는 시간
rep("      h('label',{cls:'f',text:'한 줄 평'}),",
    "      food?[h('label',{cls:'f',text:'아침 식사'}),h('div',{cls:'row'},optGroup([['y','☀ 아침 돼요']],isBreakfast(d)?['y']:[],true,function(v){var m=(d.meals||[]).filter(function(x){return x!=='아침';});if(v.length)m.push('아침');else d.opens='';d.meals=m;redraw();}),\n"
    "        isBreakfast(d)?h('label',{cls:'row',style:'gap:6px;font-size:.86rem;color:var(--muted)'},'여는 시간',h('input',{type:'time',value:d.opens||'',style:'width:auto;padding:8px 10px',onchange:function(e){d.opens=e.target.value;}})):null)]:null,\n"
    "      h('label',{cls:'f',text:'한 줄 평'}),")

open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched')
