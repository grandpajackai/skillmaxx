import csv,os,json,sys
# usage: mark_sent.py "Company|HH:MM AM" ...
b={x['company']:x for x in json.load(open('outreach/queue-2026-11-02/batch.json'))}
p='sponsors/PIPELINE.csv'; rows=list(csv.DictReader(open(p))); f=list(rows[0].keys())
resf='outreach/sent/2026-11-02-email-results.json'
res=json.load(open(resf)) if os.path.exists(resf) else []
for a in sys.argv[1:]:
  c,t=a.split('|'); x=b[c]
  for r in rows:
    if r['company']==c:
      r['status']='Contacted'; r['date_contacted']='2026-11-02'
      r['outreach_sent']=f'Cold email #1 from skillmaxx@gilventures.ai (Zoho webmail; box SMTP blocked) to {x["to"]} (subject "{x["subject"]}") at {t} ET Nov 2'
      r['next_follow_up']='2026-11-09, then 2026-11-16 (final)'
  res=[y for y in res if y['company']!=c]+[dict(company=c,to=x['to'],subject=x['subject'],status='sent',error='',route='zoho-webmail',sent_at_et=f'2026-11-02 {t} ET')]
w=csv.DictWriter(open(p+'.tmp','w',newline=''),fieldnames=f); w.writeheader(); w.writerows(rows); os.replace(p+'.tmp',p)
json.dump(res,open(resf,'w'),indent=2); print('ok',len(res))
