"""Control: la desviacion del balance alelico, se explica por profundidad?
Y la distribucion de chr20/22 es bimodal (mosaicismo real) o solo mas ancha (ruido)?
"""
import gzip, collections, statistics as st

import glob as _glob, os as _os
_c = sorted(_glob.glob(_os.path.join('data', '*.vcf.gz')))
if not _c:
    raise SystemExit('No se encontro ningun .vcf.gz en data/. Descarga el VCF del reto primero.')
VCF = _c[0]
dp=collections.defaultdict(list); ab=collections.defaultdict(list)
with gzip.open(VCF,'rt',errors='replace') as fh:
    for line in fh:
        if line[0]=='#': continue
        f=line.split('\t',10); ch=f[0]
        if len(ch)>2 and ch not in ('X','Y'): continue
        if f[6]!='PASS' or ',' in f[4] or len(f[3])!=1 or len(f[4])!=1: continue
        d=dict(zip(f[8].split(':'), f[9].rstrip('\n').split(':')))
        if d.get('GT') not in ('0/1','0|1','1|0'): continue
        try: r,a=(int(x) for x in d['AD'].split(',')[:2])
        except Exception: continue
        t=r+a
        if not (20<=t<=100): continue
        dp[ch].append(t); ab[ch].append(a/t)

orden=[str(i) for i in range(1,23)]
print(f"{'CHR':>4s} {'n':>9s} {'DP medio':>9s} {'|AB-0.5|':>9s}")
print('-'*36)
X=[];Y=[]
for ch in orden:
    if ch not in dp: continue
    md=st.mean(dp[ch]); dev=st.median([abs(x-0.5) for x in ab[ch]])
    X.append(md); Y.append(dev)
    print(f'{ch:>4s} {len(dp[ch]):>9,} {md:>9.2f} {dev:>9.4f}')

# correlacion Pearson entre profundidad y desviacion
n=len(X); mx=st.mean(X); my=st.mean(Y)
num=sum((X[i]-mx)*(Y[i]-my) for i in range(n))
den=(sum((x-mx)**2 for x in X)*sum((y-my)**2 for y in Y))**0.5
r=num/den if den else 0
print(f'\n*** Correlacion profundidad vs desviacion: r = {r:+.3f} ***')
print('    r muy negativo => la desviacion la explica la BAJA PROFUNDIDAD (artefacto)')

print('\n=== FORMA DE LA DISTRIBUCION (bimodalidad = mosaicismo real) ===')
print('Un mosaicismo verdadero produce DOS picos separados de 0.5, no solo mas ancho.\n')
for ch in ('1','20','22'):
    v=ab[ch]
    bins=[0]*20
    for x in v: bins[min(19,int(x*20))]+=1
    tot=len(v)
    print(f'chr{ch}  (n={tot:,}, DP medio={st.mean(dp[ch]):.1f})')
    for i in range(4,16):
        lo=i/20; pct=100*bins[i]/tot
        bar='#'*int(pct*1.6)
        mark=' <-- 0.5' if i==10 else ''
        print(f'   {lo:.2f}-{lo+0.05:.2f} {pct:5.2f}% {bar}{mark}')
    # test de bimodalidad simple: densidad en 0.30-0.40 y 0.60-0.70 vs 0.45-0.55
    centro=sum(bins[9:11])/tot
    flancos=(sum(bins[6:8])+sum(bins[12:14]))/tot
    print(f'   centro(0.45-0.55)={centro*100:.1f}%   flancos(0.30-0.40 y 0.60-0.70)={flancos*100:.1f}%   ratio={flancos/centro:.3f}')
    print()
