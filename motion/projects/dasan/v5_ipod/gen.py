import json, urllib.request, base64, sys
model, out, prompt = sys.argv[1], sys.argv[2], sys.argv[3]
body={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["IMAGE","TEXT"]}}
req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
try:
    r=json.load(urllib.request.urlopen(req,timeout=180))
except urllib.error.HTTPError as e:
    print('HTTP',e.code,e.read()[:300]); sys.exit(1)
for c in r.get('candidates',[]):
    for p in c['content'].get('parts',[]):
        if 'inlineData' in p:
            open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',out)
        elif 'text' in p: print(p['text'][:200])
