(()=>{const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const NAMES=window.SMX_AGENTS,KEY="smx-agent";let agent=localStorage.getItem(KEY)||"",INS=null;
const toast=$(".toast");function copied(btn){btn.textContent="Copied ✓";toast.hidden=false;clearTimeout(copied.t);copied.t=setTimeout(()=>{toast.hidden=true;btn.textContent="Copy"},1400)}
function copy(text,btn){(navigator.clipboard?navigator.clipboard.writeText(text):Promise.reject()).catch(()=>{}).finally(()=>copied(btn))}
// picker + quick install
function setAgent(a,persist=true){agent=a;if(persist){a?localStorage.setItem(KEY,a):localStorage.removeItem(KEY)}
 $$(".ag").forEach(b=>b.setAttribute("aria-checked",b.dataset.agent===a?"true":"false"));
 const sel=$("#agent");if(sel&&sel.value!==a){sel.value=a;}
 const paint=()=>[...$$(".card[data-slug]"),...($("#mc")?$$(".card",$("#mc").content):[])].forEach(c=>{const ins=(INS&&INS[c.dataset.slug])||{},q=$(".quick",c);if(!q)return;const cmd=a&&ins[a];q.hidden=!cmd;if(cmd)$("code",q).textContent=cmd;c.classList.toggle("dim",!!a&&!c.dataset.docs.split(" ").includes(a))});
 if(a&&!INS&&$(".card[data-slug]")){(window.SMX_IDX_P||(window.SMX_IDX_P=fetch(window.SMX_INDEX_URL||"/index.json").then(r=>r.json()))).then(d=>{INS={};d.forEach(x=>INS[x.s]=x.i);if(agent===a)paint()})}else paint();
 $$(".tab").forEach(t=>{if(a&&t.dataset.tab===a)t.click()});
 if(typeof filter==="function")filter();}
$$(".ag").forEach(b=>b.addEventListener("click",()=>setAgent(agent===b.dataset.agent?"":b.dataset.agent)));
document.addEventListener("click",e=>{const b=e.target.closest(".qc");if(b){e.preventDefault();copy($("code",b.parentElement).textContent,b)}
 const c=e.target.closest(".copy");if(c)copy($("code",c.parentElement).textContent,c)});
// tabs
$$(".tab").forEach(t=>t.addEventListener("click",()=>{const box=t.closest(".installbox");$$(".tab",box).forEach(x=>x.setAttribute("aria-selected",x===t));$$(".panel2",box).forEach(p=>p.hidden=p.dataset.panel!==t.dataset.tab)}));
// browse filters
const grid=$("#grid");let filter=null,shown=48;
if(grid){const q=$("#q"),ca=$("#cat"),so=$("#sort"),cards=[...$$(".card",grid),...($("#mc")?$$(".card",$("#mc").content):[])],more=$("#more");
 filter=function(){const t=(q.value||"").toLowerCase().trim(),st=($("input[name=st]:checked")||{}).value||"",types=$$("input[name=type]:checked").map(i=>i.value),a=$("#agent").value;
  let list=cards.filter(c=>{const docs=c.dataset.docs.split(" ");
   if(t&&!t.split(/\s+/).every(w=>c.dataset.text.includes(w)))return false;
   if(ca.value&&c.dataset.cat!==ca.value)return false;if(types.length&&!types.includes(c.dataset.type))return false;
   const tested=(c.dataset.tested||"").split(" ").filter(Boolean);if(st==="tested"&&(a?!tested.includes(a):!tested.length))return false;if(a){if(st==="documented"&&!docs.includes(a))return false;if(st==="unknown"&&docs.includes(a))return false;if(!st&&false)return false}
   else if(st==="documented"&&docs[0]==="")return false;else if(st==="unknown"&&docs.length>=5)return false;return true});
  const key=so.value;list.sort(key==="az"?(x,y)=>x.dataset.name.localeCompare(y.dataset.name):(x,y)=>{const ax=a?(+y.dataset.docs.split(" ").includes(a))-(+x.dataset.docs.split(" ").includes(a)):0;return ax||(y.dataset.n-x.dataset.n)||x.dataset.name.localeCompare(y.dataset.name)});
  cards.forEach(c=>c.hidden=true);list.forEach((c,i)=>{if(i<shown||c.parentNode===grid)grid.appendChild(c);c.hidden=i>=shown});
  $("#n").textContent=list.length;$("#empty").hidden=list.length>0;more.hidden=list.length<=shown;
  const u=new URLSearchParams();if(t)u.set("q",t);if(a)u.set("agent",a);if(ca.value)u.set("cat",ca.value);if(st)u.set("status",st);if(types.length)u.set("type",types.join(","));if(key!=="compat")u.set("sort",key);
  history.replaceState(null,"",(u.toString()?"?"+u:location.pathname)+location.hash)};
 const p=new URLSearchParams(location.search);if(p.get("q"))q.value=p.get("q");if(p.get("cat"))ca.value=p.get("cat");if(p.get("sort"))so.value=p.get("sort");
 if(p.get("status")){const r=$(`input[name=st][value="${p.get("status")}"]`);if(r)r.checked=true}
 (p.get("type")||"").split(",").forEach(v=>{const i=$(`input[name=type][value="${v}"]`);if(i)i.checked=true});
 if(p.get("agent"))agent=p.get("agent");
 [q,ca,so].forEach(e=>{e.addEventListener("input",()=>{shown=48;filter()});e.addEventListener("change",()=>{shown=48;filter()})});
 $("#agent").addEventListener("change",e=>setAgent(e.target.value));
 $$("input[name=st],input[name=type]").forEach(i=>i.addEventListener("change",()=>{shown=48;filter()}));
 more.addEventListener("click",()=>{shown+=48;filter()});
 $("#freset").addEventListener("click",()=>{q.value="";ca.value="";so.value="compat";$("input[name=st][value='']").checked=true;$$("input[name=type]").forEach(i=>i.checked=false);setAgent("")});
 q.addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();document.getElementById("browse").scrollIntoView({behavior:"smooth"})}});
 $("#fopen").addEventListener("click",()=>$("#facets").classList.add("open"));$("#fclose").addEventListener("click",()=>$("#facets").classList.remove("open"));}
setAgent(agent,false);if(filter)filter();
// newsletter placeholder
const nf=$("#nform");if(nf)nf.addEventListener("submit",e=>{e.preventDefault();$("#nmsg").hidden=false});
// demo card
const dd=$("#demodata");if(dd&&!matchMedia("(prefers-reduced-motion: reduce)").matches||dd){const d=JSON.parse(dd.textContent),order=Object.keys(NAMES);let i=0;
 const step=()=>{const a=order[i%order.length];$$(".dtabs span").forEach(s=>s.classList.toggle("on",s.dataset.a===a));$("#dcode").textContent=d.install[a]||`# No official ${NAMES[a]} instructions yet`;
  $("#dst").innerHTML={tested:'<span class="st tested">Tested ✓</span>',failed:'<span class="st failed">✕ Failed</span>',documented:'<span class="st documented">✓ Verified from docs</span>'}[d.compat[a]]||'<span class="st unknown">Not yet tested</span>';i++};
 step();if(!matchMedia("(prefers-reduced-motion: reduce)").matches)setInterval(step,2200);}
// matrix
const mt=$(".matrix");if(mt&&$("#mq")){const rows=$$("tbody tr",mt),mq=$("#mq"),hu=$("#hideu"),a5=$("#all5");
 const run=()=>{const t=mq.value.toLowerCase();let n=0;rows.forEach(r=>{const ok=(!t||r.dataset.text.includes(t))&&(!hu.checked||!agent||r.dataset.docs.split(" ").includes(agent))&&(!a5.checked||r.dataset.n==="5");r.hidden=!ok;n+=ok});$("#mn").textContent=`${n} shown${hu.checked&&!agent?" (pick your agent on the home page to use 'hide')":""}`};
 if(agent)$$(`[data-a="${agent}"]`,mt).forEach(c=>c.classList.add("mine"));[mq,hu,a5].forEach(e=>e.addEventListener("input",run));run();}
// command palette
const pal=$("#palette"),pq=$("#pq"),pr=$("#pr");let idx=null,sel=0,res=[];
async function openPal(){if(!idx)idx=await (window.SMX_IDX_P||(window.SMX_IDX_P=fetch(window.SMX_INDEX_URL).then(r=>r.json())));pal.showModal();pq.value="";render();pq.focus()}
function render(){const t=pq.value.toLowerCase().trim();const CL=Object.fromEntries(idx.map(x=>[x.c,x.cl]));const cats=[...new Set(idx.map(x=>x.c))].filter(c=>t&&c.includes(t)).slice(0,3).map(c=>({label:"Category: "+CL[c],href:"/?cat="+encodeURIComponent(c)+"#browse"}));
 const ags=Object.entries(NAMES).filter(([k,v])=>t&&v.toLowerCase().includes(t)).map(([k,v])=>({label:"Agent: "+v,href:"/?agent="+k+"#browse"}));
 const sk=idx.map(x=>{const n=x.n.toLowerCase();let s=n.startsWith(t)?3:n.includes(t)?2:t.split("").every((ch,i,arr)=>n.indexOf(ch,i?n.indexOf(arr[i-1]):0)>=0)?1:0;return [s,x]}).filter(([s])=>!t||s>0).sort((a,b)=>b[0]-a[0]).slice(0,8).map(([,x])=>({label:x.n,sub:x.t+" · "+x.cl,href:"/skills/"+x.s+"/"}));
 res=[...ags,...cats,...sk];sel=0;pr.innerHTML=res.map((r,i)=>`<li class="${i?"":"sel"}"><a href="${r.href}">${r.label}${r.sub?`<small>${r.sub}</small>`:""}</a></li>`).join("")||"<li class=muted>No matches</li>"}
if(pal){pq.addEventListener("input",render);pq.addEventListener("keydown",e=>{const li=$$("li",pr);if(e.key==="ArrowDown"||e.key==="ArrowUp"){e.preventDefault();sel=(sel+(e.key==="ArrowDown"?1:-1)+li.length)%li.length;li.forEach((l,i)=>l.classList.toggle("sel",i===sel))}if(e.key==="Enter"&&res[sel])location.href=res[sel].href});
 pal.addEventListener("click",e=>{if(e.target===pal)pal.close()});$$("[data-open-search]").forEach(b=>b.addEventListener("click",openPal));}
document.addEventListener("keydown",e=>{const typing=/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName);
 if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==="k"){e.preventDefault();openPal()}
 else if(e.key==="/"&&!typing){e.preventDefault();const q=$("#q");q?q.focus():openPal()}});
})();
