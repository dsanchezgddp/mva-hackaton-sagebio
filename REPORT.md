# From Genotype to Drug: An Allele-Specific Repurposing Strategy for *BUB1B*-Related Mosaic Variegated Aneuploidy

**Rare Disease, Real Kid — MVA Hackathon 2026 · Track 2 (Drug Repurposing)**

> Research hypothesis generation. **Not clinical advice.**
> No patient-identifying information is contained in this report or in the
> accompanying repository.

---

## Summary

Singleton whole-genome sequencing identifies **compound heterozygous variants in
*BUB1B***, the gene underlying Mosaic Variegated Aneuploidy type 1 (MVA1):

| | Allele 1 | Allele 2 |
|---|---|---|
| GRCh38 | 15:40,209,701 T>G | 15:40,220,612 T>G |
| HGVS | `NM_001211.6:c.2210T>G` | `NM_001211.6:c.3006T>G` |
| Protein | **p.Leu737Ter** | **p.Asn1002Lys** |
| Class | Nonsense (PTC) | Missense |
| ClinVar | **Pathogenic/Likely pathogenic** for MVA1 | Not reported (novel) |

We show that **the two alleles fail by different molecular routes but converge
on the same endpoint: reduced BubR1 protein level.** This reframes MVA1 as a
protein-dosage disease with a defined therapeutic window, and yields an
**allele-specific repurposing strategy using two approved, pediatric-experienced
drugs** — plus a genotype-specific contraindication that the general aneuploidy
literature would otherwise recommend.

---

## 1 · Variant identification

**Method.** Targeted panel extraction from the singleton WGS VCF (5,012,204
variants, GRCh38, Sentieon) across 34 genes covering the spindle assembly
checkpoint, chromosomal instability, and cancer predisposition, followed by
Ensembl VEP annotation. All code in this repository.

**Result — exclusivity.** Across all 3,703 panel variants, **exactly one HIGH
impact variant** was found: `BUB1B` p.Leu737Ter. No other checkpoint or
cancer-predisposition gene carries a truncating variant. Of MODERATE-impact
variants, only `BUB1B` p.Asn1002Lys is simultaneously novel and predicted
damaging by both SIFT and PolyPhen.

**Quality.** Both variants are `PASS`, MQ 60, GQ 99, with balanced allelic depth
(21,25 at DP 46; 15,13 at DP 28). Both are absent from gnomAD.

**Phenotype concordance.** Rhabdomyosarcoma is one of only three malignancies
described in MVA (with Wilms tumour and leukaemia) and is specifically reported
in *BUB1B* families. Severe IUGR, failure to thrive, and parental recurrent
pregnancy loss are all consistent with a constitutional chromosomal instability
syndrome with autosomal recessive inheritance.

---

## 2 · Mechanism characterisation

### 2.1 The domain is a scaffold, not an enzyme

BubR1 is an **unusual pseudokinase**: it retains the catalytic triad but the
glycine-rich loop has degenerated, and **its kinase activity is dispensable for
normal mitotic progression**. Analyses that treat *BUB1B* missense variants as
catalytic-site lesions are therefore mechanistically incorrect.

The pseudokinase domain (residues **766–1050**) is nonetheless functionally
essential: its mutation or deletion **reduces PP2A-B56 recruitment to the outer
kinetochore**, attenuating spindle-checkpoint silencing and causing
chromosome bi-orientation errors through unbalanced Aurora B activity. The
direct PP2A-B56 docking site is the **KARD motif (665–682)**, phosphorylated by
PLK1 (S676) and CDK1 (S670); the pseudokinase domain potentiates this
recruitment.

### 2.2 Allele 1 — `p.Leu737Ter`: loss of function via transcript decay

- Sequence analysis of the canonical CDS shows the substitution converts codon
  737 from `TTA` (Leu) to **`TGA`** — the **most readthrough-permissive** stop
  codon. The **+4 nucleotide is A** (context `CCAGAG [TGA] AGTG`), which is
  *moderate* on the permissiveness hierarchy (C > U > A > G).
- The PTC lies in **exon 17 of 23**, far upstream of the final exon–exon
  junction → **the transcript is predicted to be degraded by nonsense-mediated
  decay (NMD)**.
- The truncation removes the entire pseudokinase domain. Notably it lies
  *downstream* of the KARD, so any residual truncated protein would retain the
  docking motif but lose its potentiating domain — a moot point if NMD
  eliminates the transcript first.

**Classification: loss of function.**

### 2.3 Allele 2 — `p.Asn1002Lys`: loss of function via protein misfolding

Structural analysis on the AlphaFold model of BubR1 (UniProt O60566, model v6):

| Metric | Value | Interpretation |
|---|---|---|
| pLDDT at residue 1002 | **91.1** | Model is reliable at this position |
| Heavy-atom neighbours < 10 Å | **144** | **Deeply buried** (structural core) |
| Nearest environment (< 6 Å) | Leu1001 (3.4 Å), Val998 (3.5 Å), **Trp978** (3.7 Å), **Phe977** (3.8 Å), Trp973, Phe997, Ile1000 | Closed **hydrophobic** core |
| Distance to nucleotide-binding site (776/795) | **31 Å** | Does **not** affect nucleotide binding — consistent with pseudokinase status |

The substitution places a **positively charged, long-chain lysine into a buried
hydrophobic core**. This is among the most destabilising substitution classes in
protein biophysics. **Prediction: misfolding and destabilisation of the
pseudokinase domain**, not active-site disruption.

**Independent literature validation.** The characterised human MVA variant
**L1012P** acts by exactly this mechanism: *"proteasomal degradation of
BUBR1^L1002P is elevated, consistent with the human BUBR1^L1012P protein being
misfolded and less stable."*

We report the structural comparison honestly: N1002 and L1012 are **14.7 Å apart
(side-chain centroids; 10.3 Å minimum atom–atom)** and share only **one**
common neighbour within 8 Å. They are **distinct structural sites** in the same
domain, both deeply buried (144 and 204 neighbours respectively). **The analogy
is mechanistic, not positional** — L1012P establishes that this class of lesion
occurs in BubR1 and causes MVA.

**Classification: loss of function.**

### 2.4 Convergence: a protein-dosage disease

```
Allele 1 (L737*)   → TGA PTC, exon 17/23 → NMD destroys the mRNA
                                                        ↘
                                                         TOTAL BubR1 LOW
                                                        ↗
Allele 2 (N1002K)  → buried charge in hydrophobic core
                     → misfolding → proteasomal degradation
                              ↓
        PP2A-B56 kinetochore scaffold compromised
                              ↓
        attenuated SAC silencing + bi-orientation errors
                              ↓
        chromosome missegregation → mosaic variegated aneuploidy
                              ↓
        rhabdomyosarcoma · IUGR · failure to thrive · muscle atrophy
```

This is consistent with the published pattern: *"BubR1 protein levels are
usually very low in patients with BUBR1 mutations, **even in those with a
missense mutation**, largely because mutant BubR1 proteins tend to be quite
unstable."* MVA patients characteristically carry **one missense plus one
nonsense allele** — complete BubR1 loss is embryonic lethal, so viable patients
retain partial function.

### 2.5 The therapeutic window is quantified

From murine allelic-series work:

> *"A reduction of approximately **40%–90%** in BUBR1 protein levels results in
> tumour predisposition or mild premature-ageing phenotypes, whereas a reduction
> of **greater than 90%** results in progeroid phenotypes or early postnatal
> lethality."*

**This is the pivotal insight for repurposing.** Readthrough and stabilisation
therapies typically fail because they restore only 1–5% of protein — inadequate
for most diseases. **MVA1 is the inverse case: full restoration is not required;
crossing a threshold is.** A disease whose severity is governed by protein
dosage, in a patient who already retains partial function from the missense
allele, is among the most favourable settings for low-efficiency protein-restoring
therapy.

*Authors' caveat, retained:* the same work notes that "BUBR1 levels do not
closely track with phenotypic severity" — allele-specific effects exist beyond
absolute level.

---

## 3 · Repurposing proposal

The strategy follows directly from §2: **each allele fails differently, so each
allele gets a mechanism-matched drug.** Both candidates are approved and have
pediatric exposure.

### Arm A — rescue the transcript (allele `L737*`)

**AMLEXANOX**

| | |
|---|---|
| Status | **Approved in Japan since 1987** (Solfa, oral tablet) for bronchial asthma **in adults and children**; also allergic rhinitis |
| Mechanism | **Dual: inhibits NMD (via UPF1) *and* induces translational readthrough** |
| Safety | ~39 years of clinical use; favourable adverse-event profile |
| Systemic data | Phase II trials in obesity/T2D (IKKε/TBK1 inhibition) — **documented systemic human exposure** |
| Renal | Not nephrotoxic ✓ |

**Why this molecule specifically.** Allele 1 fails twice over: the ribosome
terminates early **and** the transcript is destroyed by NMD. Reading through a
transcript that has already been degraded accomplishes nothing. Amlexanox is one
of very few agents acting on **both axes with a single molecule**, avoiding a
two-drug combination and its compounded toxicity.

Repurposing precedent in other PTC diseases: **COL7A1** (recessive dystrophic
epidermolysis bullosa), **GDAP1** (Charcot-Marie-Tooth, in patient
iPSC-derived neurons), **PAX6** (aniridia — identified as the most promising
agent in a screen), **CFTR** (identified among 1,200 marketed drugs).

Favourable here: the PTC is **TGA**, the most permissive stop codon.
Honest limitation: the **+4 = A** context is only moderate.

### Arm B — rescue the fold (allele `N1002K`)

**4-PHENYLBUTYRATE (4-PBA)**

| | |
|---|---|
| Status | **Approved** for urea cycle disorders — **established pediatric use** |
| Mechanism | Chemical chaperone: inhibits aggregation of denatured protein and reverses intracellular retention of misfolded protein |
| Precedent | Myocilin (glaucoma), coagulation factor deficiencies, secretion-defective mutants |

If the lesion is a destabilised fold cleared by the proteasome (§2.3), assisting
folding is the mechanism-matched intervention. **Arms A and B are complementary,
not redundant: Arm A produces new protein, Arm B protects protein that already
exists.** Both raise the same quantity — total functional BubR1.

### Arm C — gene-independent adjunct

MVA is **mosaic**: euploid and aneuploid cells coexist. Aneuploid cells suffer
proteotoxic, metabolic, replicative and mitotic stress from gene-dosage
imbalance, rendering them **selectively vulnerable**. Shifting cellular
competition against them moves the mosaic fraction toward euploidy without
touching the gene.

| Compound | Status | Assessment |
|---|---|---|
| AICAR | Investigational | Most potent aneuploidy-selective agent in screening; also selected karyotypically normal cells in Pallister-Killian fibroblasts |
| **Metformin** | **Approved, pediatric** | AMPK activator; reported effect on trisomic cells is **subtle** — presented as such, not overstated |
| **Chloroquine** | **Approved** | Autophagy inhibitor |

---

## 4 · Genotype-specific contraindications

This section is the safety argument. Each exclusion derives from *this*
patient's genotype or phenotype, not generic caution.

### 🚫 HSP90 inhibitors (17-AAG, tanespimycin, geldanamycin)

> *"HSP90 activity is needed for folding of BUBR1 substitution mutants and for
> preventing their clearance via proteasomal degradation."*

**BubR1 missense mutants depend on HSP90 to fold.** Inhibiting HSP90 would
destroy the residual protein this patient depends on.

17-AAG appears in the aneuploidy literature as an *aneuploidy-selective* agent
and would be a natural Arm C candidate. **For this genotype it would be actively
harmful.** This error is avoidable only by reasoning from genotype to drug, never
the reverse. *(We proposed it ourselves in an earlier draft; the correction is
documented in the repository history.)*

### 🚫 Aminoglycosides (gentamicin, amikacin)

Induce readthrough, but are **nephrotoxic** — and this patient has
**nephrocalcinosis**. Efficacy is also low (~0.51% readthrough, median of the
top decile) relative to alternatives.

### 🚫 Ataluren (Translarna)

European marketing authorisation **not renewed (28 March 2025)** after five
successive negative CHMP opinions: efficacy was never confirmed. It does not
qualify as an approved medicine for this purpose.

---

## 5 · Supporting analyses

### 5.1 Secondary findings

Two variants are reported for transparency; neither reaches causality:
**`ATM` p.Ser978Pro** (single heterozygote in a recessive cancer-predisposition
gene) and a **novel in-frame insertion in `PCNT`** (biallelic *PCNT* causes MOPD
II with severe growth restriction — phenotypically relevant, but only one allele
is present).

### 5.2 Nephrocalcinosis is explained without a second diagnosis

Nephrocalcinosis is not a described MVA feature. We tested for an independent
genetic cause with a **25-gene renal panel** (primary hyperoxaluria, distal RTA,
Bartter, Dent, FHHNC, infantile hypercalcaemia, and others): **2,840 variants
annotated, no biallelic finding.**

Two apparent HIGH-impact calls are annotation artefacts, not pathogenic:
**`VDR` p.Met1Thr is the common FokI polymorphism** (~40% population frequency;
translation reinitiates at the next ATG yielding functional VDR), and
`ATP6V1B1` p.Met1Thr follows the same pattern. Teams reporting these as
pathogenic would be reporting noise.

The parsimonious explanation is **prematurity**: nephrocalcinosis occurs in
**17.1%** of very-low-birth-weight infants, with **gestational age < 32 weeks**
and **birth weight < 1500 g** as principal risk factors — both met exactly by
this patient — alongside furosemide and prolonged parenteral nutrition.

This places nephrocalcinosis **inside** the diagnosis as a second-order
consequence rather than outside it:

```
BUB1B biallelic → MVA → severe IUGR → preterm birth at 32 wk, ~1 kg
                → prolonged neonatal course → NEPHROCALCINOSIS
```

**One diagnosis explains the entire presentation**, including the feature that
appeared discordant.

*Open question for the organisers:* the phenotype document records
nephrocalcinosis as *"present since birth."* Prematurity-associated
nephrocalcinosis develops **postnatally**. If the finding was genuinely present
*at* birth, this explanation does not hold and the question must be reopened.
This distinction should not be assumed.

### 5.3 Mosaic aneuploidy is not detectable in this WGS — and why that matters

The dataset contains **no karyotype**, yet cytogenetic demonstration of mosaic
aneuploidy is the classical diagnostic criterion for MVA. We tested whether
mosaicism is recoverable from the WGS via per-chromosome allelic balance across
**2,225,130 heterozygous sites**.

Chromosomes 20 and 22 initially exceeded z > 2. **Both controls refute the
signal:**

1. **Depth confounding:** deviation correlates with mean depth at **r = +0.832**.
   The "deviant" chromosomes are the most segmental-duplication- and GC-rich;
   paralogous read pile-up inflates depth and creates spurious allelic imbalance
   simultaneously.
2. **Distribution shape:** true mosaic trisomy produces **two peaks** flanking
   0.5. chr20 and chr22 are **unimodal**; their excess mass sits in the extreme
   0.20–0.30 tail (2.9% vs 0.69% on chr1) — the signature of paralogous
   misalignment, not trisomy.

**Conclusion: no high-fraction mosaic aneuploidy in blood.** This does not
exclude MVA — mosaicism in MVA is tissue-variable and often low in blood,
aneuploid cells may be selected against in haematopoietic lineages, and the
detection floor of this approach is roughly **15–25% mosaic fraction** at 44×.

It does establish a **methodological control**: any submission reporting chr20 or
chr22 as mosaic aneuploidy from this VCF is reporting a segmental-duplication
artefact.

---

## 6 · Limitations

1. **Phase is not experimentally demonstrated.** Singleton WGS; the variants are
   ~11 kb apart, beyond read-based phasing, and no parental sequencing is
   available. Biallelic inheritance is inferred from recessive disease
   architecture, the rarity of both alleles, and phenotype concordance — not proven.
2. **`N1002K` is unclassified.** Under ACMG it would reach *likely pathogenic*
   (PM2 + PP3 + PP4; PM3 if phase is confirmed).
3. **Destabilisation is predicted, not measured.** AlphaFold geometry and burial
   analysis support misfolding; experimental confirmation is required.
4. **Amlexanox has never been tested against *BUB1B*.** All readthrough evidence
   derives from other genes. The link is mechanistic, not empirical.
5. **Readthrough efficiency is low in absolute terms** (0.5%–4.3% across agents).
   The argument depends on the dosage threshold of §2.5, which comes from murine
   models.
6. **This is hypothesis generation for research, not clinical advice.**

---

## 7 · Proposed experimental validation

A minimal design converting hypothesis into data, in patient-derived fibroblasts:

1. **Baseline:** quantify BubR1 protein (western blot) and aneuploid fraction
   (karyotype / multicolour FISH)
2. **Arm A:** amlexanox → measure (a) `L737*` transcript level by allele-specific
   qPCR (is it rescued from NMD?), (b) full-length BubR1 protein
3. **Arm B:** 4-PBA → measure N1002K protein stability (cycloheximide chase
   ± MG132)
4. **Combination:** measure **aneuploid fraction** as the functional endpoint
5. **Mechanistic negative control:** **17-AAG should worsen** BubR1 levels

Step 5 is what converts the contraindication of §4 from an assertion into a
**falsifiable prediction**. If 17-AAG does not reduce BubR1, the model is wrong.

---

## 8 · Impact

**For this child.** The analysis supplies (a) a molecular diagnosis where none is
recorded in the dataset, (b) two mechanism-matched candidates that are already
approved with pediatric exposure — the shortest available path to a
compassionate-use conversation — and (c) a **safety exclusion that would not be
obvious from the aneuploidy literature**, where HSP90 inhibitors are recommended
as aneuploidy-selective agents but would deplete the very protein he depends on.

**For MVA.** The reframing of MVA1 as a **protein-dosage disorder with a
quantified 40–90% therapeutic window** is generalisable across the *BUB1B*
allelic series. Any MVA1 patient carrying one nonsense and one missense allele —
the characteristic MVA genotype — falls under the same two-arm logic.

**For the diagnostic community.** Two concrete controls are contributed: the
`VDR` FokI / `ATP6V1B1` start-lost annotation artefacts, and the chr20/chr22
segmental-duplication artefact in allelic-balance mosaicism detection. Both are
traps a competent pipeline can fall into on this dataset.

**Negative results are reported as results.** The absence of a second genetic
diagnosis for nephrocalcinosis, and the absence of detectable mosaicism in blood,
are stated with their detection limits rather than omitted.

---

## 9 · Scalability

The method is a **transferable pipeline**, not a one-off analysis. All code is in
this repository and runs on a laptop.

```
phenotype (HPO)
   → targeted gene panel  (Ensembl REST, coordinates fetched programmatically)
   → single-pass VCF extraction  (streaming; no realignment, no cluster)
   → VEP annotation  (batched REST)
   → structural analysis  (AlphaFold: burial, environment, pLDDT confidence)
   → mechanism classification  (LoF route: transcript vs protein)
   → mechanism-matched drug search  (+ genotype-specific contraindications)
```

**Applies beyond this case:**

- **Any recessive disease with a nonsense + missense genotype.** This
  architecture is common across rare disease; the two-arm logic (rescue the
  transcript, rescue the fold) transfers directly.
- **Any PTC.** Stop-codon identity and +4 context, NMD prediction from exon
  position, and readthrough-permissiveness ranking are computed from sequence
  alone.
- **Any buried missense.** The AlphaFold burial analysis distinguishing
  *core-destabilising* from *interface* from *active-site* substitutions is
  gene-agnostic.
- **Any dosage-sensitive disease.** Where a protein-level threshold is published,
  the same argument applies: low-efficiency restoration may suffice.

**Resource footprint:** the full analysis used the **320 MB VCF, not the 85 GB
dataset** — 0.4% of the data. No alignment, no cloud compute, no GPU. This
matters for scalability: rare-disease analysis should not be gated on
infrastructure access.

---

## Data handling

Patient data was confined to a git-ignored `data/` directory and never committed.
This repository contains code, coordinates, and derived findings only. All data
will be deleted within 30 days of hackathon close (**by 23 November 2026**) and
confirmed by email to the organisers.

---

## References

Full source list with links: [`reports/`](reports/) — each analysis document
carries its own references. Primary sources include Ensembl VEP and REST,
AlphaFold DB (UniProt O60566), ClinVar, gnomAD, UniProt, and the peer-reviewed
literature cited inline above.
