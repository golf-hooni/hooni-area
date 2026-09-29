import json,math
def PX(l): return (l-124)*809
def PY(a): return (39-a)*1000
def dp(pts,tol):
    if len(pts)<3: return pts
    a,b=pts[0],pts[-1];dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy)
    md,mi=0,0
    for i in range(1,len(pts)-1):
        p=pts[i]
        d=abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L if L else math.hypot(p[0]-a[0],p[1]-a[1])
        if d>md: md,mi=d,i
    if md>tol: return dp(pts[:mi+1],tol)[:-1]+dp(pts[mi:],tol)
    return [a,b]
def enc(ring,tol,minarea):
    pts=[(PX(x),PY(y)) for x,y in ring]
    s=dp(pts,tol); s=[(round(x),round(y)) for x,y in s]
    out=[];prev=None
    for p in s:
        if p!=prev: out.append(p);prev=p
    if len(out)<4: return None
    A=abs(sum(out[i][0]*out[i-1][1]-out[i-1][0]*out[i][1] for i in range(len(out))))/2
    if A<minarea: return None
    # delta encode
    r=[out[0][0],out[0][1]]
    for i in range(1,len(out)): r+= [out[i][0]-out[i-1][0], out[i][1]-out[i-1][1]]
    return ' '.join(map(str,r)),out
def feats(fn,tol,minarea):
    res=[]
    for f in json.load(open(fn,encoding='utf-8'))['features']:
        g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
        rings=[];allp=[];best=None
        for poly in polys:
            e=enc(poly[0],tol,minarea)
            if e: rings.append(e[0]);allp+=e[1]
            if e and (best is None or len(e[1])>len(best)): best=e[1]
        if not rings: continue
        # label point: centroid of largest ring
        xs=[p[0] for p in best];ys=[p[1] for p in best]
        cx=round(sum(xs)/len(xs));cy=round(sum(ys)/len(ys))
        bw=max(xs)-min(xs)
        res.append({'n':f['properties']['name'],'r':rings,'c':[cx,cy,bw]})
    return res
prov=feats('skorea_provinces_geo_simple.json',1.2,6)
muni=feats('skorea_municipalities_geo_simple.json',1.0,3)
d={'prov':[{'n':p['n'],'r':p['r']} for p in prov],'muni':[{'n':m['n'],'r':m['r'],'c':m['c']} for m in muni]}
s=json.dumps(d,ensure_ascii=False,separators=(',',':'))
open('mapdata.json','w',encoding='utf-8').write(s)
print(len(prov),len(muni),len(s.encode()), sum(len(r.split())//2 for p in prov for r in p['r']), sum(len(r.split())//2 for p in muni for r in p['r']))
