import sys,json,time,random,datetime,os,re,fcntl
sys.path.insert(0,'/workspace/sm-0/growth/scripts'); sys.path.insert(0,os.path.dirname(__file__))
import zoho_mail as z, plan
from zoneinfo import ZoneInfo
RES='/workspace/sm-0/growth/outreach/sent/2026-11-23-email-results.json'
lock=open('/tmp/skillmaxx_outreach.lock','w')
try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except OSError: sys.exit("locked")
def now(): return datetime.datetime.now(ZoneInfo('America/New_York'))
res=json.load(open(RES)) if os.path.exists(RES) else {"date":"2026-11-23","sent":[],"skipped":[],"bounces":[],"stopped":None}
def save(): json.dump(res,open(RES,'w'),indent=1)
def inwin():
    n=now(); return n.weekday()<5 and 9<=n.hour<17
def sentlist(): return z.list_folder("Sent",400)
def addrs(m): return (m.get('toAddress') or '').lower()
start_ms=int(time.time()*1000)
bounce_seen=set()
def check_bounces():
    for m in z.list_folder("Inbox",20):
        if m['messageId'] in bounce_seen: continue
        if int(m.get('receivedTime',0))<start_ms: continue
        fa=(m.get('fromAddress') or '').lower()
        if 'mailer-daemon' in fa or 'postmaster' in fa:
            bounce_seen.add(m['messageId'])
            body=z.content(m['folderId'],m['messageId']).lower()
            rep=any(k in body for k in ('spam','blocklist','blacklist','reputation','blocked','policy','rejected due'))
            tgt=[r['to'] for r in res['sent'] if r['to'].lower() in body]
            res['bounces'].append({"to":tgt,"subject":m.get('subject'),"reputation_flag":rep}); save()
            if rep or len(res['bounces'])>=3:
                res['stopped']="bounce/reputation guard"; save(); sys.exit("STOP bounce")
jobs=[]
for c,to,sub,name,why in plan.NEW: jobs.append(("new",c,to,sub,plan.new_body(name,why)))
fu=[("fu1",c,to) for c,to in plan.FU]
# interleave: 2 new then 1 fu
order=[];n=0;f=0
while n<len(plan.NEW) or f<len(fu):
    for _ in range(2):
        if n<len(plan.NEW): order.append(jobs[n]);n+=1
    if f<len(fu): order.append(fu[f]);f+=1
cap=30; sentc=0
for j in order:
    if sentc>=cap: break
    if not inwin(): res['stopped']="outside window"; save(); print("outside window"); break
    kind,c,to=j[0],j[1],j[2]; dom=to.split('@')[1]
    S=sentlist(); mine=[m for m in S if dom in addrs(m)]
    others=[m for m in z.list_folder("Inbox",300)+z.list_folder("Spam",100) if dom in (m.get('fromAddress') or '').lower()]
    if others and not (kind=='new' and all('mailer' in (m.get('fromAddress') or '') for m in others)):
        res['skipped'].append({"company":c,"reason":"inbound from domain","kind":kind}); save(); continue
    if kind=="new":
        if mine: res['skipped'].append({"company":c,"reason":"already in Sent","kind":kind}); save(); continue
        r=z.send(to,j[3],j[4])
        subj=j[3]
    else:
        if len(mine)!=1: res['skipped'].append({"company":c,"reason":f"{len(mine)} in Sent, expected 1","kind":kind}); save(); continue
        m=mine[0]; age=(time.time()*1000-int(m['receivedTime']))/86400000
        if age<7: res['skipped'].append({"company":c,"reason":"too recent","kind":kind}); save(); continue
        subj=m['subject']; subj=subj if subj.lower().startswith('re:') else 'Re: '+subj
        import html; subj=html.unescape(subj)
        r=z.send(to,subj,plan.FU1,reply_to_mid=m['messageId'])
    st,jr=r
    rec={"company":c,"to":to,"subject":subj,"kind":kind,"http":st,"zoho_messageId":jr.get('data',{}).get('messageId',''),"sent_at":now().strftime('%Y-%m-%d %H:%M:%S ET'),"via":"Zoho Mail API"}
    if st==429 or st>=500:
        res['stopped']=f"HTTP {st}"; res['sent'].append(rec); save(); time.sleep(600); break
    res['sent'].append(rec); save()
    if st==200: sentc+=1
    print(rec,flush=True)
    time.sleep(random.randint(270,420))
    check_bounces()
res['done']=now().isoformat(); save()
