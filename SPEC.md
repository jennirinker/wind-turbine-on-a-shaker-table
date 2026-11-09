# Wind turbine on a shaker table: spec

**Blade amplitude** shown in the response plot: the peak blade-tip deflection over time, |S| + |BW| + |FW|, using the course notes' formulas. Over 3000 s of the steady-state response it matches the sampled peak to within 0.1%, in five cases including standstill.

## Physics
- Ronnie with the derived damped, base-excited fixed-frame equations: 2% blade damping, 10% tower damping, constant table displacement amplitude.
- The steady state comes from one 4×4 complex solve whenever a slider moves. When a slider moves, the response jumps to the new steady state, while the table and rotor angle stay continuous. Everything plays in real time.

## Controls
- Shaker frequency: 0–1.5 Hz in steps of 0.01 Hz.
- Rotor speed: 0–12 RPM in steps of 0.1 RPM.
- Both start at 0 for now; we'll revisit after the first working version.
- A checkbox to show the rotor's centre of mass. The full-system COM is pinned for later.

## Scene (front view, as in layout B)
- A fixed base slab and a moving table slab.
- The tower is drawn with a cantilever shape and coloured by its deflection relative to the table.
- Tapered, shaded blades, coloured red or blue by their deflection, with dashed undeflected blades behind them.
- The colour bar and "©Rinker".
- One length scale for everything, sized so the worst case fits on screen. That gives about ±11 px of table motion.

## Response panel
- Full curves for the current rotor speed, recomputed when the rotor speed changes.
- Lines for the tower (deflection relative to the table) and the blade (the peak defined above).
- ▲ markers at the natural frequencies and a dashed line at the current shaker frequency.
- The legend sits inside the top-right corner.

## Technical
- One self-contained `index.html` with plain JavaScript and SVG, and no libraries.
- It works on phone browsers (Android and iOS) and on Edge, Chrome and Firefox. It's hosted via GitHub Pages.
- On a desktop it shows as the same centred, phone-width column.

## Implementation phases (steps 4–5)
1. **Core:** the page, scene and sliders, animated from the forced response. The JavaScript's numbers are checked against the Python steady state.
2. **Response panel:** curves, natural-frequency markers and the frequency marker.
3. **Finishing:** the COM toggle, colour scaling and visual polish.
4. **Testing and handover:** testing on the browsers above, then a short README covering how to change parameters and how the code is organized.
