import json, glob, os, datetime, sys
src = sys.argv[1]
arr = []
for f in sorted(glob.glob(os.path.join(src, '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    doc = dict(d.get('data', d))
    doc['id'] = os.path.basename(f)[:-5]
    for k in ('version', '_version'): doc.pop(k, None)
    arr.append(doc)
out = {'app': 'hooni-area', 'version': 3, 'at': datetime.datetime.now().isoformat(), 'places': arr, 'bases': [], 'trips': [], 'photos': {}}
json.dump(out, open('hooni-area-import-claude.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(arr), sorted(arr[0].keys()))
