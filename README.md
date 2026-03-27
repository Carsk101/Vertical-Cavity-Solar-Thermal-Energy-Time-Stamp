# VCST — Vertical Cavity Solar Thermal

**A novel concentrated solar architecture that produces 47-93% more electricity per square foot of land than PV solar farms.**

---

## What is this?

VCST uses clusters of vertical SiC absorber tubes surrounded by compact heliostat fields to concentrate sunlight and generate electricity via sCO₂ turbines. No tower. No single-point receiver. No rare materials.

The core insight: tall vertical tubes give you 20× more absorber surface than their ground footprint, and close-range heliostats pack tighter than any existing solar technology. The result is more energy per square foot of land than PV panels, CSP towers, or any combination of the two.

## Key Numbers (Tier 1 — safest configuration)

| Metric | VCST v2 PRO | PV Solar Farm | Advantage |
|---|---|---|---|
| Electricity per ft² of land | 17.36 kWh/yr | 11.80 kWh/yr | +47% |
| Solar-to-electric efficiency | 26.7% | ~18% | +48% |
| 50 MW plant land area | 122 acres | 143 acres | -15% |
| Energy payback time | 1.08 years | 0.85 years | +3 months |
| Lifetime EROI (with degradation) | 31:1 | 27:1 | +15% |
| Rare materials | None | Silver, Indium | — |
| Toxic materials | None | Lead, PFAS | — |

Tier 3 (HfMoN coating + combined cycle) reaches 22.82 kWh/ft²/yr — **93% above PV** — on 101 acres.

## Repository Contents

### Documents
- `VCST_White_Paper.md` — Full research paper covering concept evolution, physics, failed approaches, and final design
- `VCST_Spec_Sheet.md` — Single-page technical reference for the v2 PRO architecture
- `VCST_Copyright.md` — IP notice and inventor disclosure

### Calculation Models (Python)
All numbers in the white paper are reproducible from these scripts.

| Script | Purpose |
|---|---|
| `vcst_calculations.py` | v1 — PV vs CSP vs VCST first-principles comparison |
| `vcst_v2_optimization.py` | v2 — Dense tube array, initial optimization |
| `vcst_v2_corrected.py` | v2 — Corrected field sizing, final v2 numbers |
| `vcst_v3_integrated.py` | v3 — Integrated mirror-tube exploration (failed) |
| `vcst_v2_vs_pv_farms.py` | v2 vs PV — Head-to-head against LBNL fleet data |
| `vcst_v2_production_energy.py` | Embodied energy — Component-level BOM comparison |
| `vcst_v25_engineered_stack.py` | v2.5 — Multi-zone stack (failed — T⁴ losses) |
| `vcst_v3_full_stack.py` | v3 — Full engineered stack with secondary CPCs |
| `vcst_v2_pro.py` | v2 PRO — Material upgrade ladder (TiAlN → ZrC → HfMoN) |
| `vcst_production_balanced.py` | Final — Balanced production intensity vs PV |

### Visual Reports
- `vcst-verified-analysis.html` — Interactive HTML comparison (v1 era)
- `vcst-analysis.html` — Initial analysis report

## How to Run

```bash
python3 vcst_v2_pro.py          # The main material-upgrade analysis
python3 vcst_production_balanced.py  # Production intensity comparison
python3 vcst_v2_vs_pv_farms.py  # Land-use head-to-head vs PV
```

No dependencies beyond Python 3 standard library.

## Design Iterations

```
v1 (cavity)        →  7.68% efficient  →  Killed by second mirror bounce
v2 (tube array)    → 22.95% efficient  →  First design to beat CSP and PV
v2.5 (multi-zone)  → 13.85% efficient  →  Killed by T⁴ radiation losses
v3 (full stack)    → 16.01% efficient  →  CPC helped but still worse than v2
v2 PRO (materials) → 26.7-35.1%        →  Same v2 architecture, better coatings
```

The lesson: architecture was solved at v2. Everything after that is materials science.

## Status

Pre-prototype. All performance figures are first-principles theoretical projections verified against published literature. No hardware has been built. Next step is a 100 kW proof-of-concept (2 tubes, TiAlN coating, small heliostat array).

## Copyright

Copyright (c) 2026 Harsh Patel. All rights reserved. See `VCST_Copyright.md`.
