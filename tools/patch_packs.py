"""추천 목록(data/packs.json)을 앱에서 골라 기존 기록에 합치는 기능."""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (a[:80], n)
    s = s.replace(a, b)

rep("function blobToData(b){", r"""/* 추천 목록: 앱과 같이 올린 data/*.json 을 불러와 이미 있는 곳은 건너뛰고 추가 */
function packHave(pk){return S.places.filter(function(x){return x.src===pk.src;}).length;}
function addPack(id){
  return fetch('data/'+id+'.json',{cache:'no-cache'}).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(pk){
    var now=Date.now(),added=0,skipped=0,chain=Promise.resolve();
    pk.places.forEach(function(x,i){
      if(S.places.some(function(p){return (p.src==='pack:'+id&&p.pk===x.key)||sameSpot(p,x);})){skipped++;return;}
      var rec={id:newId('places'),name:x.name,cat:x.cat||'food',status:'wish',revisit:'',tags:['골프'],meals:x.breakfast?['아침']:[],feats:[],price:'',
        menu:x.menu||'',memo:[x.golf?x.golf+' 근처':'',x.check||''].filter(Boolean).join(' · '),area:x.area||'',address:x.address||'',list:pk.list||pk.title,
        visitedAt:'',photos:[],lat:x.lat,lng:x.lng,phone:x.phone||'',kakaoUrl:x.kakaoUrl||'',src:'pack:'+id,pk:x.key,createdAt:now+i};
      added++;chain=chain.then(function(){return colSave('places',rec);});
    });
    return chain.then(function(){return {added:added,skipped:skipped,title:pk.title};});
  });
}
function openPacks(){
  var st={packs:null,busy:''};
  function draw(){
    var body=[h('div',{cls:'grab'}),h('h2',{text:'추천 맛집 목록'}),h('p',{cls:'hint',text:'골라서 누르면 "가고 싶은 곳"으로 한 번에 들어가요. 이미 있는 곳은 건너뛰고, 내 기록은 그대로 둬요.'})];
    if(!st.packs)body.push(h('p',{cls:'loading',text:'목록을 불러오는 중이에요.'}));
    else if(!st.packs.length)body.push(h('p',{cls:'hint',text:'목록이 없어요.'}));
    else body.push(h('ul',{cls:'list',style:'margin-top:12px'},st.packs.map(function(pk){var have=S.places.filter(function(x){return x.src==='pack:'+pk.id;}).length;
      return h('li',null,h('div',{cls:'dcard'},h('h4',{text:pk.title+' · '+pk.count+'곳'}),h('p',{cls:'why',text:pk.desc}),
        h('div',{cls:'row'},h('button',{cls:'btn green',disabled:!!st.busy||have>=pk.count,onclick:function(){st.busy=pk.id;draw();
          addPack(pk.id).then(function(r){st.busy='';toast(r.title+' '+r.added+'곳 추가'+(r.skipped?', '+r.skipped+'곳은 이미 있어요':''));draw();},function(){st.busy='';toast('목록을 불러오지 못했어요. 인터넷 연결을 확인해 주세요.');draw();});}},
          st.busy===pk.id?'추가하는 중':have>=pk.count?'모두 추가됨':have?'나머지 추가':'목록 추가'),
          have?h('button',{cls:'btn',onclick:function(){sheet.close();S.tab='lists';S.llist=pk.listName||'all';S.lstat='all';S.lq='';render();}},'리스트에서 보기'):null)));})));
    var y=sheet.scrollTop;sheet.replaceChildren(h('div',{cls:'sheet'},body));sheet.scrollTop=y;if(!sheet.open)sheet.showModal();
  }
  draw();
  fetch('data/packs.json',{cache:'no-cache'}).then(function(r){return r.json();}).then(function(a){st.packs=a;draw();},function(){st.packs=[];toast('목록을 불러오지 못했어요.');draw();});
}
function blobToData(b){""")

# 설정 화면에 진입 버튼
rep("    h('label',{cls:'f',style:'margin-top:26px',text:'백업'}),",
    "    h('label',{cls:'f',style:'margin-top:26px',text:'추천 목록'}),\n"
    "    h('div',{cls:'row'},h('button',{cls:'btn',onclick:openPacks},'추천 맛집 목록 보기')),\n"
    "    h('label',{cls:'f',style:'margin-top:26px',text:'백업'}),")

# 홈: 기록이 적을 때 안내
rep("  // golf breakfast\n",
    "  if(S.store!=='init'&&S.places.length<15)out.push(h('div',{cls:'notice',style:'margin-top:16px'},'골프장 주변 맛집 같은 추천 목록을 한 번에 넣을 수 있어요. ',h('button',{cls:'linkbtn',onclick:openPacks},'추천 목록 보기')));\n"
    "  // golf breakfast\n")

open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched')
