"use strict";
(() => {
  const TAU=2*Math.PI,N=128,FS=128;
  function heatAmplitudes(time=0,alpha=.01,a3=10){
    if(![time,alpha,a3].every(Number.isFinite)||time<0||alpha<=0||a3<0||a3>20)
      throw new RangeError("热模型参数无效。时间须非负，扩散率须为正，三阶振幅须在 0 至 20 之间。");
    return [20*Math.exp(-alpha*TAU**2*time),a3*Math.exp(-alpha*(3*TAU)**2*time)];
  }
  function heat(x,time=0,alpha=.01,a3=10){
    if(!Number.isFinite(x))throw new RangeError("位置须为有限数。");
    const [a,b]=heatAmplitudes(time,alpha,a3);
    return 50+a*Math.cos(TAU*x)+b*Math.cos(3*TAU*x);
  }
  function signal(t,f2=20,phase=0){
    if(![t,f2,phase].every(Number.isFinite)||f2<=0||f2>=FS/2)
      throw new RangeError("信号频率须介于 0 与奈奎斯特频率之间。");
    return Math.cos(TAU*8*t)+.5*Math.cos(TAU*f2*t+phase*Math.PI/180);
  }
  function validateCoefficients(c){
    if(!c||!Array.isArray(c.re)||!Array.isArray(c.im)||!c.re.length||c.re.length!==c.im.length||
      !c.re.every(Number.isFinite)||!c.im.every(Number.isFinite))
      throw new RangeError("频谱须包含等长、非空的有限实部与虚部数组。");
  }
  function dft(samples){
    if(!Array.isArray(samples)||!samples.length||!samples.every(Number.isFinite))
      throw new RangeError("DFT 输入须为非空有限数数组。");
    const n=samples.length,re=Array(n).fill(0),im=Array(n).fill(0);
    for(let k=0;k<n;k++)for(let j=0;j<n;j++){
      const angle=TAU*k*j/n;
      re[k]+=samples[j]*Math.cos(angle);im[k]-=samples[j]*Math.sin(angle);
    }
    return {re,im};
  }
  function inverse(c){
    validateCoefficients(c);
    const n=c.re.length;
    return Array.from({length:n},(_,j)=>{
      let sum=0;
      for(let k=0;k<n;k++){
        const a=TAU*k*j/n;sum+=c.re[k]*Math.cos(a)-c.im[k]*Math.sin(a);
      }
      return sum/n;
    });
  }
  function oneSided(c){
    validateCoefficients(c);
    const n=c.re.length;
    return Array.from({length:Math.floor(n/2)+1},(_,k)=>
      Math.hypot(c.re[k],c.im[k])/n*(k===0||(n%2===0&&k===n/2)?1:2));
  }
  function lowPass(c,cutoff,fs=FS){
    validateCoefficients(c);
    if(![cutoff,fs].every(Number.isFinite)||fs<=0||cutoff<0||cutoff>fs/2)
      throw new RangeError("截止频率须在 0 与采样率的一半之间。");
    const n=c.re.length,keep=k=>Math.min(k,n-k)*fs/n<=cutoff;
    return {re:c.re.map((v,k)=>keep(k)?v:0),im:c.im.map((v,k)=>keep(k)?v:0)};
  }
  function analyze(f2=20,phase=0,cutoff=12){
    const input=Array.from({length:N},(_,j)=>signal(j/FS,f2,phase));
    const coefficients=dft(input),restored=inverse(coefficients);
    const filtered=inverse(lowPass(coefficients,cutoff));
    return {input,coefficients,amplitudes:oneSided(coefficients),restored,filtered,
      maxError:Math.max(...input.map((v,j)=>Math.abs(v-restored[j]))),
      rms:Math.sqrt(input.reduce((s,v,j)=>s+(v-filtered[j])**2,0)/N)};
  }
  const api={TAU,N,FS,heatAmplitudes,heat,signal,dft,inverse,oneSided,lowPass,analyze};
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
  else globalThis.FourierModel=api;
})();
