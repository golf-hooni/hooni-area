"""가게 빼기: 상세 화면 바로 빼기, 뺀 추천 가게 기억(다시 안 들어옴), 추천 목록 '안 가본 곳 모두 빼기'."""
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n == count, (a[:80], n)
    s = s.replace(a, b)

# 1) 추천 목록에서 온 가게를 지우면 기억
rep("function colDel(name,obj){\n",
    "function colDel(name,obj){\n"
    "  if(name==='places'&&obj&&obj.pk&&String(obj.src||'').indexOf('pack:')===0){var hid=lsGet('hooni-pack-hidden',{});hid[obj.src+'/'+obj.pk]=1;lsSet('hooni-pack-hidden',hid);}\n")

# 공통 빼기 함수 (사진도 정리)
rep("function colDel(name,obj){\n",
    "function removePlace(p,msg){return colDel('places',p).then(function(){(p.photos||[]).forEach(dropPhoto);if(sheet.open)sheet.close();toast(msg||(p.name+' 뺐어요.'));},writeErr);}\n"
    "function colDel(name,obj){\n")

# 2) 상세 화면: 바로 빼기 (두 번 눌러 확인)
rep("    h('div',{cls:'actions'},h('span'),h('div',null,h('button',{cls:'btn',onclick:function(){sheet.close();}},'닫기'),h('button',{cls:'btn primary',onclick:function(){openEditor(p);}},'수정'))));",
    "    h('div',{cls:'actions'},armedDelete(p.status==='wish'?'별로예요, 빼기':'삭제',function(){removePlace(p);}),h('div',null,h('button',{cls:'btn',onclick:function(){sheet.close();}},'닫기'),h('button',{cls:'btn primary',onclick:function(){openEditor(p);}},'수정'))));")

# 3) 추천 목록 추가 시 뺀 가게 건너뜀
rep("      if(S.places.some(function(p){return (p.src==='pack:'+id&&p.pk===x.key)||sameSpot(p,x);})){skipped++;return;}",
    "      if(hid['pack:'+id+'/'+x.key]){hidden++;return;}\n"
    "      if(S.places.some(function(p){return (p.src==='pack:'+id&&p.pk===x.key)||sameSpot(p,x);})){skipped++;return;}")
rep("    var now=Date.now(),added=0,skipped=0,chain=Promise.resolve();",
    "    var now=Date.now(),added=0,skipped=0,hidden=0,chain=Promise.resolve(),hid=lsGet('hooni-pack-hidden',{});")
rep("return {added:added,skipped:skipped,title:pk.title};", "return {added:added,skipped:skipped,hidden:hidden,title:pk.title};")
rep("toast(r.title+' '+r.added+'곳 추가'+(r.skipped?', '+r.skipped+'곳은 이미 있어요':''));",
    "toast(r.title+' '+r.added+'곳 추가'+(r.skipped?', '+r.skipped+'곳은 이미 있어요':'')+(r.hidden?', 뺀 '+r.hidden+'곳은 제외':''));")

# 4) 추천 목록: 안 가본 곳 모두 빼기
rep("          have?h('button',{cls:'btn',onclick:function(){sheet.close();S.tab='lists';S.llist=pk.list||'all';S.lstat='all';S.lq='';render();}},'리스트에서 보기'):null)));})));",
    "          have?h('button',{cls:'btn',onclick:function(){sheet.close();S.tab='lists';S.llist=pk.list||'all';S.lstat='all';S.lq='';render();}},'리스트에서 보기'):null),\n"
    "        wishN(pk.id)?h('div',{cls:'row',style:'margin-top:8px'},armedDelete('안 가본 '+wishN(pk.id)+'곳 모두 빼기',function(){\n"
    "          var arr=S.places.filter(function(x){return x.src==='pack:'+pk.id&&x.status==='wish';}),c=Promise.resolve();\n"
    "          arr.forEach(function(x){c=c.then(function(){return colDel('places',x);});});\n"
    "          c.then(function(){toast(arr.length+'곳 뺐어요. 다녀온 곳은 그대로 뒀어요.');draw();},writeErr);})):null));})));")
rep("function openPacks(){\n",
    "function wishN(id){return S.places.filter(function(x){return x.src==='pack:'+id&&x.status==='wish';}).length;}\n"
    "function openPacks(){\n")

open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched')
