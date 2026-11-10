"""Compare the JavaScript model (JSON on stdin from js_model.mjs) with NumPy.

Usage, from the repo root:
    node tests/js_model.mjs index.html | python3 tests/compare.py

Prints the largest relative differences of the steady-state amplitudes and
the blade peak, the worst case over the full slider grid from both, the
response curves, and the natural frequencies (compared with the
eigenvalue method of ronnie_eigenanalysis.py, with damping set to zero).
Expected: differences around 1e-15 (curves) and below 1e-6 Hz (frequencies).

NOTE: the parameters below must match PARAMS in index.html.
"""
import json, sys, numpy as np
d = json.load(sys.stdin)
M,kx,m,l=50_000.,200_000.,500.,30.;w0=2*np.pi*0.8;ml,ml2=m*l,m*l**2
ct=2*0.02*ml2*w0;cx=2*0.10*np.sqrt(kx*(M+3*m))
def Q(rpm,f):
    Om=rpm*2*np.pi/60;w=2*np.pi*f
    Mf=np.array([[ml2,0,0,0],[0,ml2,0,ml],[0,0,ml2,0],[0,1.5*ml,0,M+3*m]])
    Cf=np.array([[ct,0,0,0],[0,ct,2*ml2*Om,0],[0,-2*ml2*Om,ct,0],[0,0,0,cx]])
    Kf=np.array([[ml2*w0**2,0,0,0],[0,ml2*(w0**2-Om**2),Om*ct,0],[0,-Om*ct,ml2*(w0**2-Om**2),0],[0,0,0,kx]])
    return np.linalg.solve(-w**2*Mf+1j*w*Cf+Kf,[0,0,0,kx+1j*w*cx])
err=0;perr=0
for g in d["grid"]:
    q=Q(g["rpm"],g["f"]); qj=np.array([a+1j*b for a,b in g["Q"]])
    err=max(err,np.max(np.abs(qj-q))/max(np.max(np.abs(q)),1e-30))
    pk=l*(abs(q[0])+.5*abs(q[1]-1j*q[2])+.5*abs(q[1]+1j*q[2]))
    perr=max(perr,abs(pk-g["peak"])/max(pk,1e-30))
print(f"{len(d['grid'])} cases: max rel. error amplitudes {err:.1e}, blade peak {perr:.1e}")
# worst case over the exact slider grid
wt=wx=wb=0
for rpm in np.arange(121)*0.1:
    for f in np.arange(151)*0.01:
        q=Q(rpm,f); wt=max(wt,abs(q[3]-1)); wx=max(wx,abs(q[3]))
        wb=max(wb,l*(abs(q[0])+.5*abs(q[1]-1j*q[2])+.5*abs(q[1]+1j*q[2])))
W=d["worst"]
print(f"worst case JS  : towerDefl {W['towerDefl']:.4f} towerTop {W['towerTop']:.4f} bladeTip {W['bladeTip']:.4f} ({d['worstMs']} ms)")
print(f"worst case NumPy: towerDefl {wt:.4f} towerTop {wx:.4f} bladeTip {wb:.4f}")

# response curves
cerr=0
for cv in d["curves"]:
    for fk,t,b in zip(cv["f"],cv["tower"],cv["blade"]):
        q=Q(cv["rpm"],fk); tn=abs(q[3]-1); bn=l*(abs(q[0])+.5*abs(q[1]-1j*q[2])+.5*abs(q[1]+1j*q[2]))
        cerr=max(cerr,abs(t-tn)/max(tn,1e-12),abs(b-bn)/max(bn,1e-12))
print(f"response curves ({len(d['curves'])} rotor speeds x {len(d['curves'][0]['f'])} points): max rel. error {cerr:.1e}")

# natural frequencies, as in ronnie_eigenanalysis.py (state-space eig), undamped
from scipy.linalg import eig
def fn_eig(rpm, damped=False):
    Om=rpm*2*np.pi/60
    c_t = ct if damped else 0.0; c_x = cx if damped else 0.0
    Mf=np.array([[ml2,0,0,0],[0,ml2,0,ml],[0,0,ml2,0],[0,1.5*ml,0,M+3*m]])
    Cf=np.array([[c_t,0,0,0],[0,c_t,2*ml2*Om,0],[0,-2*ml2*Om,c_t,0],[0,0,0,c_x]])
    Kf=np.array([[ml2*w0**2,0,0,0],[0,ml2*(w0**2-Om**2),Om*c_t,0],[0,-Om*c_t,ml2*(w0**2-Om**2),0],[0,0,0,kx]])
    I,O=np.eye(4),np.zeros((4,4))
    L=eig(np.block([[O,I],[-Kf,-Cf]]),np.block([[I,O],[O,Mf]]))[0]
    return np.sort(np.abs(L))[::2]/2/np.pi
ferr=0
for nf in d["natural"]:
    ref=np.array([f for f in fn_eig(nf["rpm"]) if f<=1.5]); js=np.array(nf["fn"])
    ok = len(ref)==len(js)
    e = np.max(np.abs(ref-js)) if ok else float("nan"); ferr=max(ferr,e)
    dmp = fn_eig(nf["rpm"],damped=True)
    print(f"  {nf['rpm']:4.1f} RPM: JS {np.round(js,4)}  eig {np.round(ref,4)}  (with damping |lambda|: {np.round(dmp,4)})")
print(f"natural frequencies: max abs. error {ferr:.1e} Hz")
