# Wind turbine on a shaker table: spec

**Blade amplitude** shown in the response plot: the peak blade-tip deflection over time, |S| + |BW| + |FW|, using the course notes' formulas. Over 3000 s of the steady-state response it matches the sampled peak to within 0.1%, in five cases including standstill.

## Physics
- Ronnie with the derived damped, base-excited fixed-frame equations: 2% blade damping, 10% tower damping, constant table displacement amplitude.
- The steady state comes from one 4×4 complex solve whenever a slider moves. When a slider moves, the response jumps to the new steady state, while the table and rotor angle stay continuous. Everything plays in real time.

## Layout
- Reference design: layout B in the mockup canvas (phone size, 390×844).
- One stacked column, top to bottom: title "Wind turbine on a shaker table", turbine scene, response panel with the shaker frequency slider directly under it, rotor speed slider, centre-of-mass checkbox.
- The blocks below the scene are spread evenly over the remaining height.

## Controls
- Shaker frequency: 0–1.5 Hz in steps of 0.01 Hz. Label "Shaker frequency [Hz]", current value with unit on the right (e.g. "0.64 Hz").
- Rotor speed: 0–12 RPM in steps of 0.1 RPM. Label "Rotor speed [RPM]", current value with unit on the right (e.g. "9.6 RPM").
- Both start at 0 for now; we'll revisit after the first working version.
- A checkbox "Show rotor centre of mass". The full-system COM is pinned for later.
- Slider style: dark rectangular handle; grey pill-shaped line with rounded ends, grey on both sides of the handle.
- Each slider's label and value line up with the left and right ends of its grey line.
- The shaker frequency slider doubles as the plot's frequency axis: its grey line spans exactly the plot width, and the handle centre sits at the same frequency as the plot's dashed vertical line.
- The rotor speed slider spans the full width of the app.

## Scene (front view, as in layout B)
- A fixed base slab and a moving table slab: two flat rectangles in front view. The tower is mounted directly on top of the moving table.
- The tower is drawn with a cantilever shape and coloured by its deflection relative to the table.
- Tapered, shaded blades, coloured red or blue by their deflection, with dashed undeflected blades behind them.
- The colour bar and "©Rinker".
- One length scale for everything, sized so the worst case fits on screen. That gives about ±11 px of table motion.

## Response panel
- Heading "Frequency response at <rotor speed> RPM", with "▲ = natural frequencies" on the right.
- Full curves for the current rotor speed, recomputed when the rotor speed changes.
- Lines for the tower (solid; deflection relative to the table) and the blade (dashed; the peak defined above). Vertical axis in multiples of table motion, 0–6×.
- ▲ markers at the natural frequencies and a dashed line at the current shaker frequency.
- Legend "Tower" / "Blade" on two lines inside the top-right corner, without a box.
- Frequency tick labels 0, 0.5, 1, 1.5; no axis title (the shaker frequency slider below carries the label).

## Technical
- One self-contained `index.html` with plain JavaScript and SVG, and no libraries.
- It works on phone browsers (Android and iOS) and on Edge, Chrome and Firefox. It's hosted via GitHub Pages.
- On a desktop it shows as the same centred, phone-width column.

## Implementation phases (steps 4–5)
1. **Core:** the page, scene and sliders, animated from the forced response. The JavaScript's numbers are checked against the Python steady state.
2. **Response panel:** curves, natural-frequency markers and the frequency marker.
3. **Finishing:** the COM toggle, colour scaling and visual polish.
4. **Testing and handover:** testing on the browsers above, then a short README covering how to change parameters and how the code is organized.
