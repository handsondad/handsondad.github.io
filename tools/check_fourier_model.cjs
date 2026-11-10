"use strict";
const assert=require("node:assert/strict");
const m=require("../assets/interactive/fourier-model.js");
const near=(a,b,tol=1e-10)=>assert(Math.abs(a-b)<tol,`${a} != ${b}`);
for(const alpha of [.002,.01,.02])for(const a3 of [0,10,20])for(const t of [0,.5,2,10]){
  const values=Array.from({length:1024},(_,j)=>m.heat(j/1024,t,alpha,a3));
  near(values.reduce((s,v)=>s+v,0)/values.length,50);
  near(m.heat(0,t,alpha,a3),m.heat(1,t,alpha,a3));
  const [a,b]=m.heatAmplitudes(t,alpha,a3);
  near(a,20*Math.exp(-alpha*4*Math.PI**2*t));
  near(b,a3*Math.exp(-alpha*36*Math.PI**2*t));
  assert(Math.min(...values)>=10-1e-10&&Math.max(...values)<=90+1e-10);
  if(t>0){
    const x=.137,h=1e-5,dt=1e-5;
    const ut=(m.heat(x,t+dt,alpha,a3)-m.heat(x,t-dt,alpha,a3))/(2*dt);
    const uxx=(m.heat(x+h,t,alpha,a3)-2*m.heat(x,t,alpha,a3)+m.heat(x-h,t,alpha,a3))/h**2;
    near(ut,alpha*uxx,2e-5);
  }
}
for(const f2 of [10,20,20.5,30])for(const phase of [0,90,180]){
  const a=m.analyze(f2,phase,12),n=m.N;
  assert(a.maxError<1e-12);
  const meanSquare=a.input.reduce((s,v)=>s+v*v,0)/n;
  const spectralSquare=a.coefficients.re.reduce((s,v,k)=>s+v*v+a.coefficients.im[k]**2,0)/n**2;
  near(meanSquare,spectralSquare);
  for(let k=1;k<n;k++){
    near(a.coefficients.re[k],a.coefficients.re[n-k]);
    near(a.coefficients.im[k],-a.coefficients.im[n-k]);
  }
  if(Number.isInteger(f2)){
    near(a.amplitudes[8],1);near(a.amplitudes[f2],.5);
  }
}
const a=m.analyze();
near(a.rms,Math.sqrt(.125));
for(let j=0;j<m.N;j++)near(a.filtered[j],Math.cos(m.TAU*8*j/m.FS));
near(m.analyze(20,90).amplitudes[20],a.amplitudes[20]);
assert(m.analyze(20.5).amplitudes.filter(v=>v>1e-4).length>20);
const dc=m.oneSided(m.dft(Array(128).fill(3)));near(dc[0],3);
const nyquist=m.oneSided(m.dft(Array.from({length:128},(_,j)=>(-1)**j)));near(nyquist[64],1);
for(let j=0;j<64;j++)near(Math.cos(m.TAU*8*j/64),Math.cos(m.TAU*56*j/64));
assert.throws(()=>m.heat(0,-1));assert.throws(()=>m.dft([]));assert.throws(()=>m.signal(0,64));
assert.throws(()=>m.lowPass(a.coefficients,65));
console.log("Verified heat PDE, periodicity and conserved mean; DFT inverse, Parseval, phase, conjugate symmetry, low-pass amplitudes, leakage, DC/Nyquist and aliasing.");
