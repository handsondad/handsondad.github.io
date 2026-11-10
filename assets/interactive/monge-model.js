"use strict";
(() => {
  function profile(depth = 20) {
    if (!Number.isFinite(depth) || depth < 10 || depth > 30) throw new Error("高台深度须在 10 至 30 mm 之间。");
    return [[0,0],[40,0],[40,36],[40-depth,36],[40-depth,12],[0,12]];
  }
  const dot = (a,b) => a.reduce((sum,v,i) => sum+v*b[i],0);
  function geometry(depth = 20) {
    const yz=profile(depth), vertices=[0,60].flatMap(x=>yz.map(([y,z])=>[x,y,z]));
    const faces=[
      {ids:[0,1,2,3,4,5],normal:[-1,0,0],tone:0},
      {ids:[6,7,8,9,10,11],normal:[1,0,0],tone:1}
    ];
    for(let i=0;i<6;i++){
      const j=(i+1)%6;
      faces.push({ids:[i,i+6,j+6,j],normal:[0,yz[j][1]-yz[i][1],yz[i][0]-yz[j][0]],tone:yz[j][1]===yz[i][1]?2:3});
    }
    return {vertices,faces,volume:60*(40*12+depth*24)};
  }
  function camera(yaw, elevation) {
    if (![yaw,elevation].every(Number.isFinite) || elevation<0 || elevation>90)
      throw new Error("相机角度无效。");
    const a=yaw*Math.PI/180,e=elevation*Math.PI/180;
    return {right:[-Math.sin(a),Math.cos(a),0],
      up:[-Math.cos(a)*Math.sin(e),-Math.sin(a)*Math.sin(e),Math.cos(e)],
      normal:[Math.cos(a)*Math.cos(e),Math.sin(a)*Math.cos(e),Math.sin(e)]};
  }
  function project(p, yaw=-55, elevation=30) {
    const c=camera(yaw,elevation),q=p.map((v,i)=>v-[30,20,18][i]);
    return [dot(q,c.right),-dot(q,c.up)];
  }
  function views(p) {
    return {front:[p[0],p[2]],top:[p[0],p[1]],left:[p[1],p[2]]};
  }
  function section(offset) {
    if(!Number.isFinite(offset)||Math.abs(offset)>15)throw new Error("剖切位置须在外圆半径内。");
    const outer=Math.sqrt(Math.max(0,225-offset*offset));
    const inner=Math.sqrt(Math.max(0,64-offset*offset));
    return {outer,inner,area:80*(outer-inner),hasHole:Math.abs(offset)<8};
  }
  const api={profile,geometry,camera,project,views,section,dot};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
  else globalThis.MongeModel=api;
})();
