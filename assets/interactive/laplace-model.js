/* Synthetic, coplanar Newtonian initial conditions, not JPL ephemerides. */
"use strict";
(() => {
  const GM = 1.32712440041279419e20 * (365.25 * 86400) ** 2 / 149597870700 ** 3;
  const masses = [1, 126712764.1 / 1.32712440041279419e11, 37940584.8418 / 1.32712440041279419e11];
  const radii = [5.202887, 9.53667594];
  const nJ = 3034.90371757 / 36000, nS = 1222.11494724 / 36000;
  function initial(factor) {
    const m = [1, masses[1] * factor, masses[2] * factor];
    const p = [[0, 0, 0, 0]];
    for (let i = 0; i < 2; i++) {
      const a = i * Math.PI / 3, r = radii[i], v = Math.sqrt(GM * (1 + m[i + 1]) / r);
      p.push([r * Math.cos(a), r * Math.sin(a), -v * Math.sin(a), v * Math.cos(a)]);
    }
    for (let k = 0; k < 4; k++) {
      const center = p.reduce((sum, point, i) => sum + m[i] * point[k], 0) / m.reduce((a, b) => a + b);
      p.forEach(point => { point[k] -= center; });
    }
    return {m, p};
  }
  function acceleration(p, m) {
    const a = p.map(() => [0, 0]);
    for (let i = 0; i < 3; i++) for (let j = i + 1; j < 3; j++) {
      const dx = p[j][0] - p[i][0], dy = p[j][1] - p[i][1], r = Math.hypot(dx, dy);
      if (!Number.isFinite(r) || r < .1) throw new Error("模型出现近距离相遇，当前步长不再适用。");
      for (let k = 0; k < 2; k++) {
        const d = k === 0 ? dx : dy;
        a[i][k] += GM * m[j] * d / r ** 3;
        a[j][k] -= GM * m[i] * d / r ** 3;
      }
    }
    return a;
  }
  function energy(p, m) {
    let e = p.reduce((sum, q, i) => sum + m[i] * (q[2] ** 2 + q[3] ** 2) / 2, 0);
    for (let i = 0; i < 3; i++) for (let j = i + 1; j < 3; j++)
      e -= GM * m[i] * m[j] / Math.hypot(p[i][0] - p[j][0], p[i][1] - p[j][1]);
    return e;
  }
  function simulate(factor = 1, dt = .0025) {
    if (![1, 5, 10].includes(factor) || ![.0025, .00125, .000625].includes(dt))
      throw new Error("不支持的质量倍率或积分步长。");
    const {m, p} = initial(factor), e0 = energy(p, m), frames = [];
    let a = acceleration(p, m), maxError = 0;
    const count = Math.round(120 / dt), stride = Math.round(.5 / dt);
    for (let step = 0; step <= count; step++) {
      if (step % stride === 0) {
        const time = step * dt;
        const points = p.slice(1).map(q => [q[0] - p[0][0], q[1] - p[0][1]]);
        const reference = radii.map((r, i) => {
          const angle = i * Math.PI / 3 + Math.sqrt(GM * (1 + m[i + 1]) / r ** 3) * time;
          return [r * Math.cos(angle), r * Math.sin(angle)];
        });
        const phase = Math.atan2(points[0][1], points[0][0]) - Math.atan2(reference[0][1], reference[0][0]);
        const residual = Math.atan2(Math.sin(phase), Math.cos(phase)) * 180 / Math.PI;
        const error = Math.abs((energy(p, m) - e0) / e0);
        maxError = Math.max(maxError, error);
        frames.push({time, points, reference, residual, error});
      }
      if (step === count) break;
      p.forEach((q, i) => {
        for (let k = 0; k < 2; k++) {
          q[k] += q[k + 2] * dt + a[i][k] * dt ** 2 / 2;
          q[k + 2] += a[i][k] * dt / 2;
        }
      });
      a = acceleration(p, m);
      p.forEach((q, i) => {
        for (let k = 0; k < 2; k++) q[k + 2] += a[i][k] * dt / 2;
      });
    }
    if (maxError > 2e-6) throw new Error("能量误差超过教学模型的验收阈值。");
    return {frames, maxError, m, finalState: p};
  }
  function slowPhase(time, saturnPeriod) {
    if (!Number.isFinite(time) || !Number.isFinite(saturnPeriod) || saturnPeriod <= 0)
      throw new Error("慢相位模型需要有限时间和正周期。");
    const frequency = 2 * nJ - 5 / saturnPeriod;
    return {frequency, period: frequency === 0 ? Infinity : 1 / Math.abs(frequency),
      value: Math.cos(2 * Math.PI * frequency * time), angle: 2 * Math.PI * frequency * time};
  }
  const api = {GM, masses, radii, nJ, nS, initial, simulate, slowPhase};
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else globalThis.LaplaceModel = api;
})();
