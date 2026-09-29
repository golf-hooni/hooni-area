import re, json, os
here = os.path.dirname(os.path.abspath(__file__))
p = r'C:\Users\User\Desktop\index.html'
s = open(p, encoding='utf-8').read()
ex = [e for e in json.load(open(os.path.join(here, 'expw_small.json'))) if e['ref'].isdigit()]
s, n = re.subn(r"var EXPW=\[.*?\];\n", lambda m: "var EXPW=" + json.dumps(ex, separators=(',', ':')) + ";\n", s, count=1, flags=re.S)
assert n == 1
a = ".city{fill:var(--muted)}"
if s.count(a) == 1: s = s.replace(a, ".city{fill:var(--muted);stroke:var(--land);paint-order:stroke;stroke-linejoin:round}")
# 도시 이름에도 테두리(halo) 두께 지정
b = "svg.appendChild(sv('text',{class:'city',x:x,y:y,'text-anchor':'middle','font-size':fs,'font-weight':c[3]===1?700:400},c[0]));"
if s.count(b) == 1: s = s.replace(b, "svg.appendChild(sv('text',{class:'city',x:x,y:y,'text-anchor':'middle','font-size':fs,'font-weight':c[3]===1?700:400,'stroke-width':3*sc},c[0]));")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok', len(s.encode()))
