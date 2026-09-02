"""Detecta aneuploidia mosaico via balance alelico por cromosoma.

Logica: en un cromosoma euploide, los sitios heterocigotos tienen
AB = alt/(ref+alt) ~ 0.5. Si una fraccion f de celulas tiene trisomia,
los sitios het se desvian de 0.5 (hacia 1/3 o 2/3 segun que alelo se duplique),
ensanchando la distribucion y desplazando la mediana de |AB-0.5|.
"""
import gzip, collections, statistics as st

import glob as _glob, os as _os
_c = sorted(_glob.glob(_os.path.join('data', '*.vcf.gz')))
if not _c:
    raise SystemExit('No se encontro ningun .vcf.gz en data/. Descarga el VCF del reto primero.')
VCF = _c[0]
MINDP, MAXDP = 20, 100
ab = collections.defaultdict(list)
n=0
with gzip.open(VCF,'rt',errors='replace') as fh:
    for line in fh:
        if line[0]=='#': continue
        f=line.split('\t',10)
        ch=f[0]
        if len(ch)>2 and ch not in ('X','Y','MT'): continue   # solo principales
        if f[6]!='PASS': continue
        if ',' in f[4] or len(f[3])!=1 or len(f[4])!=1: continue  # SNV bialelico
        fmt=f[8].split(':'); smp=f[9].rstrip('\n').split(':')
        d=dict(zip(fmt,smp))
        if d.get('GT') not in ('0/1','0|1','1|0'): continue
        try:
            adr,ada=(int(x) for x in d['AD'].split(',')[:2])
        except Exception: continue
        tot=adr+ada
        if not (MINDP<=tot<=MAXDP): continue
        ab[ch].append(ada/tot)
        n+=1

print(f'sitios heterocigotos analizados: {n:,}\n')
print(f"{'CHR':>4s} {'n_het':>9s} {'AB medio':>9s} {'AB mediana':>11s} {'desv.est':>9s} {'|AB-0.5| med':>13s}")
print('-'*62)
res={}
orden=[str(i) for i in range(1,23)]+['X','Y']
for ch in orden:
    v=ab.get(ch)
    if not v or len(v)<500: continue
    m=st.mean(v); md=st.median(v); sd=st.pstdev(v)
    dev=st.median([abs(x-0.5) for x in v])
    res[ch]=(len(v),m,md,sd,dev)
    print(f'{ch:>4s} {len(v):>9,} {m:>9.4f} {md:>11.4f} {sd:>9.4f} {dev:>13.4f}')

auto={k:v for k,v in res.items() if k not in ('X','Y')}
if auto:
    devs=[v[4] for v in auto.values()]; sds=[v[3] for v in auto.values()]
    mdev, sdev = st.mean(devs), st.pstdev(devs)
    msd,  ssd  = st.mean(sds),  st.pstdev(sds)
    print(f'\nAutosomas: |AB-0.5| medio = {mdev:.4f} (DE {sdev:.4f}) | desv.est. media = {msd:.4f} (DE {ssd:.4f})')
    print('\n=== CROMOSOMAS ATIPICOS (z > 2 en cualquiera de las dos metricas) ===')
    hay=False
    for ch,(nv,m,md,sd,dev) in sorted(auto.items(), key=lambda x:-abs((x[1][4]-mdev)/(sdev or 1))):
        z1=(dev-mdev)/(sdev or 1); z2=(sd-msd)/(ssd or 1)
        if abs(z1)>2 or abs(z2)>2:
            hay=True
            print(f'  chr{ch:<3s} |AB-0.5|={dev:.4f} (z={z1:+.2f})   sd={sd:.4f} (z={z2:+.2f})   n={nv:,}')
    if not hay: print('  NINGUNO — todos los autosomas dentro de +/-2 DE')
