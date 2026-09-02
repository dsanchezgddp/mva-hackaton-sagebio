# MVA Hackathon 2026 — *BUB1B* variant analysis and allele-specific repurposing

Submission for **[Rare Disease, Real Kid: The MVA Hackathon 2026](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026)**
(Sage Bionetworks · MVA Society · Hugging Face · BEACON).

**Tracks:** 1 (Variant Prediction) and 2 (Drug Repurposing)

---

## ⚠️ Data policy

**This repository contains no patient data.** All challenge data is confined to a
git-ignored `data/` directory. Code, gene coordinates, and derived findings only.

Per the hackathon data use agreement, all patient data will be deleted from every
environment within 30 days of hackathon close (**by 23 November 2026**), with
email confirmation to the organisers.

---

## Result

**Compound heterozygous *BUB1B* variants** (MVA1, OMIM 257300):

| | Allele 1 | Allele 2 |
|---|---|---|
| GRCh38 | `15:40,209,701 T>G` | `15:40,220,612 T>G` |
| HGVS | `NM_001211.6:c.2210T>G` | `NM_001211.6:c.3006T>G` |
| Protein | **p.Leu737Ter** | **p.Asn1002Lys** |
| ClinVar | Pathogenic/Likely pathogenic (MVA1) | Novel |

**Mechanism.** Both alleles reduce BubR1 protein by different routes — the
nonsense allele via nonsense-mediated decay, the missense allele via misfolding
and proteasomal degradation. MVA1 is reframed as a **protein-dosage disease**
with a published 40–90% therapeutic window.

**Proposal.** One approved, pediatric-experienced drug per allele:
**amlexanox** (dual NMD inhibition + readthrough) and **4-phenylbutyrate**
(chemical chaperone). Plus a genotype-specific contraindication: **HSP90
inhibitors would be harmful here**, despite appearing in the aneuploidy
literature as aneuploidy-selective agents.

Full reasoning: **[`REPORT.md`](REPORT.md)**

---

## Repository layout

```
REPORT.md                       Track 2 submission report
submission/
  track1_predictions.csv        Track 1 submission
reports/
  01_dossier_biologico.md       MVA biology, genes, therapeutic landscape
  02_hallazgo_principal.md      Variant evidence and structural interpretation
  03_estrategia_track2.md       Repurposing strategy (v2; v1 corrections logged)
  04_hallazgos_secundarios.md   Secondary findings; nephrocalcinosis resolution
  05_aneuploidia_wgs.md         Mosaicism detection attempt and its controls
scripts/
  extract_panel.py              Single-pass VCF extraction over a gene panel
  gene_regions.tsv              34-gene SAC / CIN / cancer-predisposition panel
  nephro_regions.tsv            25-gene nephrocalcinosis panel
  allelic_balance.py            Per-chromosome allelic balance
  ab_control.py                 Depth and bimodality controls
data/                           GIT-IGNORED — patient data never committed
```

> Working documents in `reports/` are written in Spanish; `REPORT.md` — the
> submission — is in English.

---

## Reproducing

Requires Python 3 and network access (Ensembl REST, AlphaFold DB). No cluster,
no GPU, no alignment step.

```bash
# 1. Obtain challenge access, then download ONLY the VCF (320 MB, not the 85 GB set).
#    Replace <VCF_FILENAME> with the .vcf.gz listed on the dataset page.
hf download SageBio/mva-hackathon-2026-data \
    <VCF_FILENAME>.vcf.gz --repo-type dataset --local-dir ./data

# 2. Extract panel variants (single streaming pass)
py scripts/extract_panel.py

# 3. Mosaicism analysis and its controls
py scripts/allelic_balance.py
py scripts/ab_control.py
```

Gene coordinates are fetched programmatically from Ensembl rather than
hard-coded, so the panels are auditable and extensible.

---

## Method

```
phenotype (HPO)
   → targeted gene panel        Ensembl REST, coordinates fetched at runtime
   → single-pass VCF extraction streaming; no realignment
   → VEP annotation             batched REST
   → structural analysis        AlphaFold: burial, environment, pLDDT
   → mechanism classification   LoF route: transcript vs protein
   → mechanism-matched drugs    + genotype-specific contraindications
```

Analysis used **320 MB of the 85 GB dataset (0.4%)** and runs on a laptop.

---

## Notes on rigour

Several intermediate conclusions were **revised against evidence** during the
analysis; the corrections are documented rather than hidden (see §0 of
`reports/03_estrategia_track2.md`):

- BubR1 is a **pseudokinase** — its catalytic activity is dispensable; the domain
  matters as a PP2A-B56 scaffold. An earlier draft treated it as a catalytic lesion.
- **Ataluren** was dropped after confirming its European authorisation was not
  renewed in March 2025.
- **17-AAG** was proposed, then identified as **contraindicated** for this genotype.

Two annotation traps in this dataset are documented as controls: the `VDR` FokI
and `ATP6V1B1` start-lost artefacts, and the chr20/chr22 segmental-duplication
artefact in allelic-balance mosaicism detection.

---

## Licence

Code and findings under **CC BY 4.0**, per hackathon terms.
