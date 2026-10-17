export const data={permalink:"/index.json",eleventyExcludeFromCollections:true};
export function render({skills}){return JSON.stringify(skills.map(s=>({n:s.name,s:s.slug,c:s.category,cl:s.catLabel,t:s.typeLabel,d:s.docs,i:Object.fromEntries(Object.entries(s.install||{}).filter(([k,v])=>v))})));}
