"""Embed portraits as data URIs into data.json and inline data.json into index.html."""
import json,base64,os,re,sys
root=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(os.path.join(root,"data.json")))
for e in D["elections"]:
    for p in e.get("people",[]):
        im=p.get("img","")
        if im and not im.startswith("data:"):
            p["img"]="data:image/jpeg;base64,"+base64.b64encode(open(os.path.join(root,im),"rb").read()).decode()
json.dump(D,open(os.path.join(root,"data.json"),"w"),ensure_ascii=False,indent=1)
blob=json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
h=open(os.path.join(root,"index.html")).read()
h,n=re.subn(r'(<script id="urnes-data" type="application/json">).*?(</script>)',lambda m:m.group(1)+blob+m.group(2),h,count=1,flags=re.S)
assert n==1,"marker not found"
open(os.path.join(root,"index.html"),"w").write(h)
print("ok",len(h))
