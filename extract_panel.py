"""Extrae variantes del panel de genes candidatos en una sola pasada sobre el VCF.
No contiene datos del paciente: solo codigo. Seguro para GitHub.
"""
import gzip, sys, collections

import glob as _glob, os as _os
_c = sorted(_glob.glob(_os.path.join('data', '*.vcf.gz')))
if not _c:
    raise SystemExit('No se encontro ningun .vcf.gz en data/. Descarga el VCF del reto primero.')
VCF = _c[0]
PANEL = 'scripts/gene_regions.tsv'
OUT   = 'data/panel_variants.tsv'   # <-- en data/, ignorado por git
PAD   = 5000  # bases de margen para captar splicing/regulador cercano

# --- cargar regiones ---
regions = collections.defaultdict(list)
with open(PANEL) as f:
    next(f)
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) < 4: continue
        gene, chrom, start, end = p[0], p[1], int(p[2]), int(p[3])
        regions[chrom].append((start - PAD, end + PAD, gene))
for c in regions: regions[c].sort()
print(f'Panel: {sum(len(v) for v in regions.values())} genes en {len(regions)} cromosomas', flush=True)

total = 0
kept  = 0
per_gene = collections.Counter()
chrom_counts = collections.Counter()

with gzip.open(VCF, 'rt', errors='replace') as fh, open(OUT, 'w') as out:
    out.write('gene\tCHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n')
    for line in fh:
        if line.startswith('#'):
            continue
        total += 1
        if total % 1000000 == 0:
            print(f'  ... {total:,} variantes leidas, {kept} en panel', flush=True)
        f = line.rstrip('\n').split('\t')
        chrom, pos = f[0], int(f[1])
        chrom_counts[chrom] += 1
        rs = regions.get(chrom)
        if not rs: continue
        for start, end, gene in rs:
            if start <= pos <= end:
                out.write(gene + '\t' + '\t'.join(f[:9]) + '\t' + (f[9] if len(f) > 9 else '') + '\n')
                kept += 1
                per_gene[gene] += 1
                break
            if pos < start:
                break

print(f'\nTOTAL variantes en el VCF: {total:,}')
print(f'Variantes dentro del panel: {kept:,}\n')
print('Por gen:')
for g, n in per_gene.most_common():
    print(f'  {g:10s} {n:5d}')
faltan = [g for c in regions for _,_,g in regions[c] if g not in per_gene]
if faltan: print('\nSin variantes (cobertura o region limpia):', ', '.join(sorted(faltan)))
print(f'\nCromosomas en el VCF: {len(chrom_counts)}')
