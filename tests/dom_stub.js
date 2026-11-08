// Shared browser-DOM stub so inline page scripts can be loaded in node to catch
// top-level runtime crashes (the ",," class of bug) and to smoke-test calc funcs.
function makeEl() {
  const e = {
    value: '', checked: false, innerHTML: '', textContent: '', className: '',
    style: {}, dataset: {}, options: [], selectedIndex: 0, files: [], children: [],
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    setAttribute(){}, removeAttribute(){}, getAttribute(){ return null; },
    appendChild(){}, removeChild(){}, insertBefore(){}, insertAdjacentHTML(){}, cloneNode(){ return makeEl(); },
    addEventListener(){}, removeEventListener(){}, click(){}, focus(){}, blur(){},
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    getBoundingClientRect(){ return { top:0,left:0,width:0,height:0,bottom:0,right:0 }; },
    scrollIntoView(){}, closest(){ return null; },
  };
  return e;
}
function install() {
  const elCache = {};
  global.document = {
    getElementById(id){ return elCache[id] || (elCache[id] = makeEl()); },
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    createElement(){ return makeEl(); }, createTextNode(){ return makeEl(); },
    addEventListener(){}, removeEventListener(){},
    body: makeEl(), head: makeEl(), documentElement: makeEl(),
  };
  global.window = { addEventListener(){}, scrollTo(){}, matchMedia(){ return { matches:false, addEventListener(){} }; }, print(){}, location:{ href:'' }, scrollY:0 };
  global.localStorage = { getItem(){ return null; }, setItem(){}, removeItem(){} };
  global.navigator = { userAgent:'node', share:undefined, clipboard:{ writeText(){ return Promise.resolve(); } } };
  global.Event = class { constructor(){} };
  global.CustomEvent = global.Event; global.HTMLElement = class {};
  global.Blob = class { constructor(){} };
  global.URL = { createObjectURL(){ return ''; }, revokeObjectURL(){} };
  global.alert = () => {}; global.confirm = () => true; global.requestAnimationFrame = (f)=>{ try{f();}catch(e){} };
  global.location = { href:'', reload(){}, assign(){}, replace(){} };
  global.history = { pushState(){}, replaceState(){}, back(){} };
  global.getComputedStyle = () => ({ getPropertyValue(){ return ''; } });
  global.FileReader = class { readAsText(){} readAsDataURL(){} };
  global.matchMedia = global.window.matchMedia;
  global.print = () => {};
  class _Obs { observe(){} unobserve(){} disconnect(){} takeRecords(){ return []; } }
  global.MutationObserver = _Obs; global.IntersectionObserver = _Obs; global.ResizeObserver = _Obs;
}
// Load every inline <script>...</script> (bare, no attributes) from an HTML string.
function loadInline(html) {
  const inline = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const code = inline.join('\n;\n');
  try { (0, eval)(code); return { ok: true, blocks: inline.length, err: '' }; }
  catch (e) { return { ok: false, blocks: inline.length, err: (e && e.message) || String(e) }; }
}
module.exports = { makeEl, install, loadInline };
