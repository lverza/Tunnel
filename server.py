import os, time, json, base64
os.makedirs('responses', exist_ok=True)

while True:
    os.system('git pull -q')
    for f in os.listdir('requests'):
        if not f.endswith('.json'): continue
        with open(f'requests/{f}') as fh:
            req = json.load(fh)
        try:
            import urllib.request
            r = urllib.request.urlopen(urllib.request.Request(
                req['url'], 
                data=base64.b64decode(req.get('body','')) if req.get('body') else None,
                headers=req.get('headers',{}), 
                method=req.get('method','GET')
            ), timeout=15)
            resp = {'s':r.status, 'h':dict(r.headers), 'b':base64.b64encode(r.read()).decode()}
        except Exception as e:
            resp = {'s':502, 'h':{}, 'b':base64.b64encode(str(e).encode()).decode()}
        with open(f'responses/{f}', 'w') as fh:
            json.dump(resp, fh)
        os.remove(f'requests/{f}')
    os.system('git add -A && git commit -m "r" && git push -q')
    time.sleep(2)
