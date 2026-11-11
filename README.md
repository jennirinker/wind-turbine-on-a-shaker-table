# Wind turbine on a shaker table

https://jennirinker.github.io/wind-turbine-on-a-shaker-table/

An interactive animation for students: a simplified three-bladed wind turbine
("Ronnie") stands on a shaker table that moves sideways. Students choose the
shaker frequency and the rotor speed and see how the tower and blades respond,
together with the frequency response of the whole system.

The whole tool is one file, `index.html`: plain HTML, CSS, JavaScript and SVG,
with no libraries and no network access.

## Using it

- **Locally:** open `index.html` in a browser.
- **Online:** link at top of page. The repository is served with GitHub Pages (repository
  Settings → Pages → Deploy from a branch → main, `/(root)`). Every push to
  that branch updates the site.

On the page:

- **Shaker frequency [Hz]** (0–1.5 Hz): the slider also serves as the
  frequency axis of the plot above it.
- **Rotor speed [RPM]** (0–12 RPM): the curves and the ▲ natural-frequency
  markers are recomputed for this speed.
- **Show rotor centre of mass:** an open circle at the centre of the three
  blade-tip masses.

Blades and tower are coloured by their deflection (blue negative, red
positive). Motion and colour use one fixed scale, set by the largest response
over all slider settings, so resonances look large and off-resonance motion
looks small.

## Files

| File | What it is |
|---|---|
| `index.html` | The tool. |
| `SPEC.md` | The agreed specification. |
| `tests/js_model.mjs` | Runs the model code from `index.html` in Node and prints results as JSON. |
| `tests/compare.py` | Recomputes the same results with NumPy/SciPy and prints the differences. |

## The model

Ronnie has four degrees of freedom: the lateral displacement `x` of the centre
mass (the tower) and the edgewise blade angles, used in the fixed frame after
the Coleman transformation as `a0` (collective), `a1` (horizontal) and `b1`
(vertical). The equations are the damped, base-excited fixed-frame equations
from the course notes (section "Ronnie on a shaker table: damped, forced
response"):

- the table displacement `u(t)` has a constant amplitude at every frequency;
- for each slider setting the steady state is one 4×4 complex linear solve;
- blade angles are rebuilt with the Coleman transformation every frame;
- when a slider moves, the response jumps to the new steady state, while the
  table phase and the rotor angle stay continuous;
- the blade curve shows the peak blade-tip deflection over time,
  `l·(|S| + |BW| + |FW|)`, and the tower curve the tower deflection relative to
  the table, `|X − 1|`, both in multiples of the table amplitude;
- the ▲ markers are the undamped natural frequencies.
- the blades are given 2% critical damping and the tower 10% critical damping to
  keep motion visible at worst case

## Changing things

All settings are near the top of each script section in `index.html`.

| To change | Edit | Notes |
|---|---|---|
| Masses, stiffness, blade length, blade frequency, damping | `PARAMS` | The drawing and colour scales follow automatically. **Also update the parameters at the top of `tests/compare.py`**, which has its own copy. |
| Slider ranges or steps | The `min`/`max`/`step` attributes of the `freq` and `rpm` inputs in the HTML **and** `RPM_MAX`, `RPM_STEP`, `F_MAX`, `F_STEP` | The two must match. If `F_MAX` changes, also change the frequency tick labels `[0, 0.5, 1, 1.5]` in the RESPONSE PANEL section. |
| Vertical range of the plot | `PLOT.yMax` | Also change the tick labels `[0, 2, 4, 6]` and grid lines `[2, 4]` next to it. |
| How large the biggest motion is drawn | `SCENE.maxMotion` | In SVG units (the scene is 390 wide). |
| Deflection colours | `deflectionColour()` | Static colours are in the CSS and the SVG markup. |

## How the code is organised

`index.html` contains, in order: the CSS, the static HTML and SVG, and one
script in four sections.

1. **MODEL** (between the `MODEL START` and `MODEL END` comments): pure
   functions with no page access; the tests run exactly this code.
   - `PARAMS`: model parameters.
   - `fixedFrameMatrices()`: the fixed-frame M, C, K matrices.
   - `steadyState()`: complex amplitudes `[A0, A1, B1, X]` for one setting.
   - `bladeTipPeak()`: the blade curve value.
   - `worstCase()`: largest responses over all slider settings, for the scales.
   - `naturalFrequencies()`, `responseCurves()`: for the plot.
   - `complexSolve()`, `complexDet()` and small complex-number helpers.
2. **DRAWING**: scene geometry (`SCENE`), the fixed scale, colours, and
   `drawScene()`, which places the table, tower, blades, hub and centre of
   mass for one frame.
3. **RESPONSE PANEL**: plot geometry (`PLOT`), axes and legend, and
   `drawResponse()` / `drawFrequencyLine()`.
4. **STATE, CONTROLS AND ANIMATION**: `updateFromSliders()` reads the sliders
   and computes the new steady state; `frame()` advances the table phase and
   rotor angle in real time and draws.

## Tests

From the repository root:

```
node tests/js_model.mjs index.html | python3 tests/compare.py
```

Needs Node.js and Python with NumPy and SciPy. It checks the JavaScript model
against NumPy: steady-state amplitudes, the blade peak, the worst case used for
the scales, the response curves, and the natural frequencies (against the
eigenvalue method of `ronnie_eigenanalysis.py`, with damping set to zero).
Expected: differences around 1e-12 or smaller, and natural frequencies within
1e-6 Hz.

## Browser support

Tested on Chrome (automated, including phone-size emulation from 320 to 430 px
wide), Firefox and Edge on desktop, and Firefox on mobile. Not yet tested on
Safari (iOS).

---

©Rinker
