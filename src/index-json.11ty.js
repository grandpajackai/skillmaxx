export const data={permalink:"/index.json",eleventyExcludeFromCollections:true};
export function render({skills}){return JSON.stringify(skills.map(s=>({n:s.name,s:s.slug,c:s.category,t:s.typeLabel,d:s.docs})));}
