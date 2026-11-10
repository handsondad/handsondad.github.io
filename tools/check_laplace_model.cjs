"use strict";
const assert = require("node:assert/strict");
const model = require("../assets/interactive/laplace-model.js");

assert(Math.abs(model.GM - 39.47692642117669) < 1e-12);
assert(Math.abs(model.slowPhase(0, 1 / model.nS).period - 883.0606653851389) < 1e-8);
assert(Math.abs(model.slowPhase(1800, 2.5 / model.nJ).value - 1) < 1e-12);
const expected = new Map([[1, -.824041506], [10, -5.430574901]]);
const results = [];
for (const factor of [1, 5, 10]) {
  const runs = [.0025, .00125, .000625].map(dt => model.simulate(factor, dt));
  const coarse = runs[0], frames = coarse.frames;
  assert.equal(frames.length, 241);
  assert.equal(frames[0].time, 0);
  assert.equal(frames.at(-1).time, 120);
  frames.forEach((frame, i) => {
    assert.equal(frame.time, i / 2);
    for (let j = 0; j < 2; j++)
      assert(Math.abs(Math.hypot(...frame.reference[j]) - model.radii[j]) < 1e-12);
    assert(Number.isFinite(frame.residual));
  });
  if (expected.has(factor))
    assert(Math.abs(frames.at(-1).residual - expected.get(factor)) < 1e-8, "Independent Python/JS model disagreement");
  assert(coarse.maxError < 2e-8);
  const distance = (a, b) => Math.hypot(...a.map((v, i) => v - b[i]));
  const differences = [0, 1].map(i => distance(runs[i].frames.at(-1).points[0], runs[i + 1].frames.at(-1).points[0]));
  assert(differences[0] < .0002);
  assert(differences[0] / differences[1] > 3.8 && differences[0] / differences[1] < 4.2);
  const {m, finalState} = coarse;
  for (let k = 0; k < 4; k++)
    assert(Math.abs(finalState.reduce((sum, p, i) => sum + m[i] * p[k], 0)) < 1e-10);
  function angularMomentum(p) {
    return p.reduce((sum, q, i) => sum + m[i] * (q[0] * q[3] - q[1] * q[2]), 0);
  }
  const l0 = angularMomentum(model.initial(factor).p);
  assert(Math.abs((angularMomentum(finalState) - l0) / l0) < 1e-11);
  results.push({factor, finalResidualDegrees: frames.at(-1).residual, maxSampledEnergyError: coarse.maxError,
    convergenceRatio: differences[0] / differences[1], coarseFineDistanceAU: differences[0]});
}
assert.throws(() => model.simulate(0), /不支持/);
assert.throws(() => model.slowPhase(0, 0), /正周期/);
console.log(JSON.stringify({slowPeriodYears: model.slowPhase(0, 1 / model.nS).period, results}, null, 2));
