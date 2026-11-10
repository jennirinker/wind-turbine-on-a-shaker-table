// Checks the model section of index.html against NumPy (see compare.py).
// Extracts the code between "MODEL START" and "MODEL END", evaluates the
// steady state on a grid of rotor speeds and shaker frequencies, the response
// curves and the natural frequencies, and prints JSON.
//
// Usage, from the repo root:
//   node tests/js_model.mjs index.html | python3 tests/compare.py
//
// Needs Node.js (any recent version) and Python with NumPy.

import fs from "fs";
const html = fs.readFileSync(process.argv[2], "utf8");
const src = html.split("// MODEL START")[1].split("// MODEL END")[0];
const f = new Function(src.replace(/^[^\n]*\n/, "") + "\nreturn {PARAMS, steadyState, bladeTipPeak, worstCase, naturalFrequencies, responseCurves};");
const m = f();
const out = [];
for (const rpm of [0, 2.5, 6, 9.6, 12]) for (const fr of [0, 0.05, 0.31, 0.5, 0.64, 0.8, 0.96, 1.2, 1.5]) {
  const Q = m.steadyState(m.PARAMS, rpm * 2 * Math.PI / 60, 2 * Math.PI * fr);
  out.push({ rpm, f: fr, Q: Q.map((z) => [z.re, z.im]), peak: m.bladeTipPeak(m.PARAMS, Q) });
}
const t0 = Date.now(); const W = m.worstCase(m.PARAMS, 12, 0.1, 1.5, 0.01);
const curves = [], natural = [];
for (const rpm of [0, 3, 6, 9.6, 12]) {
  const Om = rpm * 2 * Math.PI / 60;
  curves.push({ rpm, ...m.responseCurves(m.PARAMS, Om, 1.5, 600) });
  natural.push({ rpm, fn: m.naturalFrequencies(m.PARAMS, Om, 1.5) });
}
console.log(JSON.stringify({ grid: out, worst: W, worstMs: Date.now() - t0, curves, natural }));
