"use strict";
const assert=require("node:assert/strict");
const m=require("../assets/interactive/monge-model.js");
const near=(a,b)=>assert(Math.abs(a-b)<1e-9,`${a} != ${b}`);
const distance=(a,b)=>Math.hypot(...a.map((v,i)=>v-b[i]));
for(const depth of [10,20,30]){
  const g=m.geometry(depth);
  assert.equal(g.vertices.length,12);assert.equal(g.faces.length,8);
  near(g.volume,28800+1440*depth);
  const edges=new Map();
  for(const f of g.faces){
    const plane=m.dot(g.vertices[f.ids[0]],f.normal);
    for(const id of f.ids)near(m.dot(g.vertices[id],f.normal),plane);
    f.ids.forEach((id,i)=>{
      const key=[id,f.ids[(i+1)%f.ids.length]].sort((a,b)=>a-b).join(",");
      edges.set(key,(edges.get(key)||0)+1);
    });
  }
  assert.equal(edges.size,18);assert([...edges.values()].every(count=>count===2));
  assert.equal(g.vertices.length-edges.size+g.faces.length,2);
  for(let yaw=-180;yaw<=180;yaw+=15)for(const el of [0,30,60,90]){
    const c=m.camera(yaw,el);
    near(m.dot(c.right,c.right),1);near(m.dot(c.up,c.up),1);near(m.dot(c.normal,c.normal),1);
    near(m.dot(c.right,c.up),0);near(m.dot(c.up,c.normal),0);
    for(const p of g.vertices)for(const q of g.vertices)
      assert(distance(m.project(p,yaw,el),m.project(q,yaw,el))<=distance(p,q)+1e-9);
  }
  for(const p of g.vertices){
    const v=m.views(p);
    assert.deepEqual([v.front[0],v.top[1],v.front[1]],p);
  }
}
const front=depth=>JSON.stringify([...new Set(m.geometry(depth).vertices.map(p=>JSON.stringify(m.views(p).front)))].sort());
assert.equal(front(10),front(20));assert.equal(front(20),front(30));
for(let d=-14;d<=14;d+=.5){
  const s=m.section(d);
  near(s.outer*s.outer+d*d,225);
  if(s.hasHole)near(s.inner*s.inner+d*d,64);
  else assert.equal(s.inner,0);
  near(s.area,m.section(-d).area);
  near(s.area,40*2*(s.outer-s.inner));
}
near(m.section(0).area,560);near(m.section(10).area,80*Math.sqrt(125));
assert.equal(m.section(8).hasHole,false);
near(m.section(15).area,0);
assert.throws(()=>m.geometry(0));assert.throws(()=>m.section(16));
const a=m.project([0,0,0],-90,0),b=m.project([30,40,20],-90,0);
near(distance(a,b),Math.sqrt(1300));
console.log("Verified watertight stepped mesh, projection bases and length bounds, corresponding views, identical front projections, and analytical sleeve sections.");
