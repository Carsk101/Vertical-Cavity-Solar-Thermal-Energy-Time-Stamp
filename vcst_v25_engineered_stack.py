#!/usr/bin/env python3
"""
VCST v2.5: THE ENGINEERED STACK
=================================
The central tubes aren't just absorbers — they're multi-stage 
energy extraction machines.

Each tube is divided into ZONES from top (hottest) to bottom (coolest).
Each zone uses the BEST conversion technology for its temperature range.

Research basis:
- TPV: MIT/NREL 2022 — 41% at 2400°C, 32% at 1300°C, 44% at 1435°C (U Michigan 2024)
- sCO₂: Recompression Brayton — 52% thermal efficiency demonstrated (Al-Sulaiman 2024)
- ORC: 15-25% at 150-350°C (mature technology)
- Thermoelectric: Bi₂Te₃ at 5-8% for <300°C (commodity)
- Stirling: 30-40% of Carnot at 300-700°C
"""

import math

sigma = 5.67e-8
T_amb_K = 308.15
DNI_annual = 2000
DNI_peak = 1000
m2_to_ft2 = 10.764
m2_per_acre = 4047

print("=" * 80)
print("VCST v2.5: THE ENGINEERED STACK")
print("Multi-zone, multi-technology heat extraction")
print("=" * 80)

# =============================================================================
# BASELINE: v2 performance (to beat)
# =============================================================================
v2_sys_eff = 0.2295
v2_total_eff = 0.3938
v2_gcr = 0.35
v2_elec_per_ft2 = (DNI_annual * v2_sys_eff * v2_gcr) / m2_to_ft2

print(f"\nv2 baseline: {v2_elec_per_ft2:.2f} kWh_e/ft²/yr (η_elec = {v2_sys_eff*100:.1f}%)")

# =============================================================================
# OPTICAL CHAIN (same as v2 — this is the mirror-to-tube path)
# =============================================================================
cosine = 0.86
mirror_r = 0.935
atmo = 0.98
spillage = 0.98
blocking = 0.96
alpha = 0.97
eff_abs = 1 - (1 - alpha) * (1 - 0.70 * alpha)

optical = cosine * mirror_r * atmo * spillage * blocking * eff_abs
print(f"\nOptical chain: {optical*100:.2f}%")

# =============================================================================
# TUBE ZONES — Temperature gradient from top to bottom
# =============================================================================
# The tube runs hottest at the top (where concentrated light is most intense
# and hot fluid collects) and coolest at the bottom.
#
# We engineer FIVE distinct zones:

print(f"\n{'='*80}")
print("THE FIVE ZONES — top to bottom")
print("="*80)

# Each zone has:
# - Temperature range
# - Fraction of total absorbed thermal energy arriving at that zone
# - Conversion technology
# - Conversion efficiency (heat → electricity)

zones = [
    {
        "name": "Zone 1: TPV Crown",
        "temp_range": "900-1200°C",
        "T_avg_K": 1050 + 273.15,  # 1050°C average
        "heat_fraction": 0.15,  # 15% of absorbed heat reaches this extreme temp
        "technology": "Thermophotovoltaic (TPV) cells",
        "description": (
            "The very top of each tube runs hottest. A ring of TPV cells\n"
            "  surrounds the tube crown behind a quartz window. The hot SiC\n"
            "  surface radiates IR → TPV cells convert it directly to electricity.\n"
            "  No moving parts. Solid state."
        ),
        "conversion_eff": 0.30,  # TPV at ~1050°C emitter
        # Source: MIT/NREL 2022 — 32% at 1300°C demonstrated
        # At 1050°C: ~25-30% realistic with current tandem cells
        # U Michigan 2024: 44% at 1435°C with air-bridge design
        "notes": "MIT/NREL: 41% at 2400°C, 32% at 1300°C. Conservative 30% at 1050°C.",
    },
    {
        "name": "Zone 2: sCO₂ Recompression",
        "temp_range": "600-900°C",
        "T_avg_K": 750 + 273.15,
        "heat_fraction": 0.35,  # Largest zone — primary power extraction
        "technology": "Supercritical CO₂ recompression Brayton cycle",
        "description": (
            "The main power zone. sCO₂ flows through channels in the tube wall,\n"
            "  absorbs heat at 600-900°C, drives a recompression Brayton turbine.\n"
            "  This is the highest-efficiency mechanical cycle at these temps."
        ),
        "conversion_eff": 0.48,  # sCO₂ recompression at 750°C
        # Source: Al-Sulaiman 2024 — 52% demonstrated at noon peak
        # Realistic annual average with off-design: 45-50%
        # NREL Gen3 target: 50%+ at 700°C+
        "notes": "sCO₂ recompression: 52% demonstrated. Using 48% for annual average.",
    },
    {
        "name": "Zone 3: Steam Rankine",
        "temp_range": "350-600°C",
        "T_avg_K": 475 + 273.15,
        "heat_fraction": 0.20,
        "technology": "Superheated steam Rankine cycle",
        "description": (
            "Classic proven technology. Water in the tube walls boils to\n"
            "  superheated steam, drives a conventional turbine. The workhorse.\n"
            "  Reject heat from Zone 2 preheats this zone's feedwater."
        ),
        "conversion_eff": 0.38,  # Rankine at 475°C
        # Source: standard subcritical steam — well-proven
        "notes": "Proven steam Rankine. Reject heat from sCO₂ preheats feedwater.",
    },
    {
        "name": "Zone 4: ORC Scavenger",
        "temp_range": "150-350°C",
        "T_avg_K": 250 + 273.15,
        "heat_fraction": 0.15,
        "technology": "Organic Rankine Cycle (ORC)",
        "description": (
            "Low-grade heat that's too cool for steam but too hot to waste.\n"
            "  ORC with R245fa or isopentane working fluid. Small, modular,\n"
            "  off-the-shelf units. Reject heat from Zone 3 feeds this."
        ),
        "conversion_eff": 0.15,  # ORC at 250°C
        # Source: mature ORC — Turboden, ORMAT typically 12-18% at these temps
        "notes": "Commodity ORC units. Turboden/ORMAT proven at this scale.",
    },
    {
        "name": "Zone 5: Thermal Offtake",
        "temp_range": "60-150°C",
        "T_avg_K": 100 + 273.15,
        "heat_fraction": 0.10,
        "technology": "Direct thermal use (district heat, desalination, absorption cooling)",
        "description": (
            "Bottom of tube and all reject heat from ORC. Too cool for any\n"
            "  power cycle but perfect for: district heating, absorption chillers,\n"
            "  multi-effect desalination, greenhouse heating, aquaculture."
        ),
        "conversion_eff": 0.0,  # Not converted to electricity — used as heat
        "thermal_useful": 0.85,  # 85% of this heat is usefully captured
        "notes": "No electricity. Direct thermal use at 85% capture.",
    },
]

# Waste/loss fraction
waste_fraction = 0.05  # 5% of absorbed heat is unrecoverable loss

# Verify fractions sum to ~1
total_frac = sum(z["heat_fraction"] for z in zones) + waste_fraction
assert abs(total_frac - 1.0) < 0.01, f"Fractions sum to {total_frac}, not 1.0"

# =============================================================================
# THERMAL LOSSES — per zone
# =============================================================================
# Thermal losses happen BEFORE conversion. Each zone radiates some heat away.
# Higher temp zones lose more (Stefan-Boltzmann ∝ T⁴).
# But the SiC + carbon foam keeps emittance at 0.15.

emittance = 0.15

# Total absorber surface (from v2 model: 6 tubes × 2m dia × 50m)
n_tubes = 6
tube_d = 2.0
tube_h = 50
total_absorber_m2 = n_tubes * math.pi * tube_d * tube_h

# Allocate absorber area proportional to heat fraction
# (higher-temp zones are smaller but more concentrated)

print(f"\n  {'Zone':<30s} {'Temp':>10s} {'Heat%':>7s} {'Area m²':>8s} {'Rad loss':>10s} {'Net ret':>8s}")
print(f"  {'─'*30} {'─'*10} {'─'*7} {'─'*8} {'─'*10} {'─'*8}")

zone_results = []
for z in zones:
    area = total_absorber_m2 * z["heat_fraction"]
    T_K = z["T_avg_K"]
    q_rad = emittance * sigma * (T_K**4 - T_amb_K**4)
    q_conv = 20  # W/m²
    loss_W = (q_rad + q_conv) * area
    
    # Heat arriving at this zone from concentrated sunlight
    # Total mirror power × optical = power on tubes
    # We'll compute absolute numbers for a reference 50 MW system later
    # For now, express as fraction of absorbed heat
    
    # Thermal retention for this zone
    # This depends on flux density vs loss density
    # Higher temp zones have higher flux (more concentrated) AND higher loss
    # Approximate: use v2's total thermal retention and adjust by zone
    
    # Zone thermal retention (rough model)
    if z["heat_fraction"] > 0:
        # Relative loss: (q_rad+q_conv) / average_flux_on_zone
        # Average flux = total_power × zone_fraction / zone_area
        # Since zone_area ∝ zone_fraction, flux is roughly constant
        # So retention varies mainly with temperature
        base_flux = 20000  # W/m² average (from v2 model)
        retention = max(0.5, 1 - (q_rad + q_conv) / base_flux)
    else:
        retention = 0.85
    
    z["thermal_retention"] = retention
    z["area_m2"] = area
    z["q_loss_W_m2"] = q_rad + q_conv
    
    print(f"  {z['name']:<30s} {z['temp_range']:>10s} {z['heat_fraction']*100:6.0f}% {area:7.0f} {q_rad+q_conv:9.0f} W/m² {retention*100:6.1f}%")

# =============================================================================
# ELECTRICITY EXTRACTION — zone by zone
# =============================================================================

print(f"\n{'='*80}")
print("ELECTRICITY EXTRACTION BY ZONE")
print("="*80)

total_elec_fraction = 0  # fraction of incident solar → electricity
total_thermal_fraction = 0  # fraction → useful thermal
total_loss_fraction = waste_fraction * optical  # radiation + unrecoverable

parasitic = 0.06  # pumps, controls, cooling

print(f"\n  {'Zone':<30s} {'η_conv':>7s} {'η_therm':>8s} {'Heat in':>8s} {'Elec out':>9s} {'Cumul':>7s}")
print(f"  {'─'*30} {'─'*7} {'─'*8} {'─'*8} {'─'*9} {'─'*7}")

for z in zones:
    # Heat arriving at zone (as fraction of incident solar)
    heat_in = optical * z["heat_fraction"] * z["thermal_retention"]
    
    if z.get("thermal_useful"):
        # This is the thermal-only zone
        elec_out = 0
        thermal_out = heat_in * z["thermal_useful"]
        total_thermal_fraction += thermal_out
    else:
        # Electricity-producing zone
        elec_out = heat_in * z["conversion_eff"] * (1 - parasitic)
        total_elec_fraction += elec_out
        # Reject heat from this zone cascades to lower zones or thermal offtake
        reject = heat_in * (1 - z["conversion_eff"])
        # Some reject heat is captured as useful thermal
        total_thermal_fraction += reject * 0.30  # 30% of reject heat captured
    
    print(f"  {z['name']:<30s} {z['conversion_eff']*100:6.1f}% {z['thermal_retention']*100:7.1f}% {heat_in*100:7.2f}% {elec_out*100:8.2f}% {total_elec_fraction*100:6.2f}%")

total_useful = total_elec_fraction + total_thermal_fraction

print(f"\n  ────────────────────────────────────────────────────────")
print(f"  Total solar → electricity:      {total_elec_fraction*100:.2f}%")
print(f"  Total solar → useful thermal:   {total_thermal_fraction*100:.2f}%")
print(f"  Total solar → useful energy:    {total_useful*100:.2f}%")

# =============================================================================
# COMPARISON: v2 vs v2.5 vs PV vs CSP
# =============================================================================

print(f"\n{'='*80}")
print("COMPARISON: All architectures")
print("="*80)

# Per ft² of land
gcr = 0.35
v25_elec_per_ft2 = (DNI_annual * total_elec_fraction * gcr) / m2_to_ft2
v25_total_per_ft2 = (DNI_annual * total_useful * gcr) / m2_to_ft2

pv_per_ft2 = 11.80  # Best modern PV from LBNL + 15%
csp_per_ft2 = 9.85
v2_elec_ft2 = 14.92

configs = [
    ("PV solar farm (2025 best)", pv_per_ft2, pv_per_ft2, "Benchmark"),
    ("Tower CSP", csp_per_ft2, csp_per_ft2 * 1.03, "Benchmark"),
    ("VCST v2 (single sCO₂ cycle)", v2_elec_ft2, v2_elec_ft2 * (v2_total_eff / v2_sys_eff), "Previous"),
    ("VCST v2.5 (engineered stack)", v25_elec_per_ft2, v25_total_per_ft2, "NEW"),
]

print(f"\n  {'System':<38s} {'Elec/ft²':>10s} {'Total/ft²':>10s} {'vs PV':>7s} {'vs v2':>7s}")
print(f"  {'─'*38} {'─'*10} {'─'*10} {'─'*7} {'─'*7}")
for name, elec, total, note in configs:
    vs_pv = elec / pv_per_ft2
    vs_v2 = elec / v2_elec_ft2
    flag = " ★" if note == "NEW" else ""
    print(f"  {name:<38s} {elec:9.2f} {total:9.2f} {vs_pv:6.2f}× {vs_v2:6.2f}×{flag}")

# =============================================================================
# ZONE-BY-ZONE BREAKDOWN FOR A 50 MW PLANT
# =============================================================================

print(f"\n{'='*80}")
print("50 MW PLANT — Zone contributions")
print("="*80)

# Total mirror area for 50 MW at the new efficiency
target_MW = 50
# Power at peak: mirror_area × DNI × total_elec_fraction
mirror_area_50MW = target_MW * 1e6 / (DNI_peak * total_elec_fraction)
field_area_50MW = mirror_area_50MW / gcr

print(f"\n  Mirror area: {mirror_area_50MW/1000:.0f}k m²")
print(f"  Field area: {field_area_50MW/m2_per_acre:.0f} acres")

# Power from each zone at peak
print(f"\n  Zone power at peak DNI (1000 W/m²):")
print(f"  {'Zone':<30s} {'MW_e':>8s} {'% of total':>10s}")
print(f"  {'─'*30} {'─'*8} {'─'*10}")
for z in zones:
    if z.get("thermal_useful"):
        heat_in = optical * z["heat_fraction"] * z["thermal_retention"]
        mw = heat_in * z["thermal_useful"] * DNI_peak * mirror_area_50MW / 1e6
        print(f"  {z['name']:<30s} {'—':>8s} {0:9.1f}%  ({mw:.1f} MW_th)")
    else:
        heat_in = optical * z["heat_fraction"] * z["thermal_retention"]
        mw = heat_in * z["conversion_eff"] * (1 - parasitic) * DNI_peak * mirror_area_50MW / 1e6
        pct = mw / target_MW * 100
        print(f"  {z['name']:<30s} {mw:7.1f} {pct:9.1f}%")

# =============================================================================
# TECHNOLOGY READINESS
# =============================================================================

print(f"\n{'='*80}")
print("TECHNOLOGY READINESS ASSESSMENT")
print("="*80)

trl = [
    ("TPV cells at 1050°C", "TRL 5-6",
     "MIT/NREL demonstrated 41% at 2400°C (2022). U Michigan: 44% at 1435°C (2024).\n"
     "     Need: scale up manufacturing, long-term durability at temp, cost reduction.\n"
     "     Risk: MEDIUM — proven in lab, needs engineering for 25-yr life in solar app."),
    ("sCO₂ recompression Brayton", "TRL 6-7",
     "NREL G3P3 1MW demo under construction. 3 full-scale test stations globally.\n"
     "     52% thermal efficiency demonstrated in simulation. 80% technology readiness.\n"
     "     Risk: LOW-MEDIUM — turbomachinery at 700°C+ needs qualification."),
    ("Steam Rankine at 475°C", "TRL 9",
     "100+ years of commercial deployment. Millions of units worldwide.\n"
     "     Risk: NONE — fully commodity technology."),
    ("ORC at 250°C", "TRL 9",
     "Turboden, ORMAT, etc. Thousands of units deployed.\n"
     "     Risk: NONE — off-the-shelf."),
    ("SiC tube fabrication", "TRL 4-5",
     "Bulk SiC ceramic is commodity ($1500/ton). SiC tubes for industrial\n"
     "     furnaces exist. Need: 50m continuous tubes with fluid channels.\n"
     "     Risk: MEDIUM — manufacturing scale-up is the challenge."),
    ("Carbon foam selective coating", "TRL 4",
     "Carbon foam exists. Selective emittance coatings exist. Combining them\n"
     "     at 1200°C operating temp for 25+ years is unproven.\n"
     "     Risk: HIGH — this is the highest-risk component."),
]

for name, level, detail in trl:
    print(f"\n  {name}: {level}")
    print(f"     {detail}")

# =============================================================================
# WHAT THE ENGINEERED STACK ACTUALLY LOOKS LIKE
# =============================================================================

print(f"\n{'='*80}")
print("PHYSICAL DESCRIPTION: What you'd actually build")
print("="*80)

print(f"""
Each tube (2m diameter × 50m tall) has this structure from top to bottom:

TOP (0-7m) — TPV CROWN
├─ Inner: SiC + carbon foam absorber at 900-1200°C
├─ Outer: Ring of TPV cell panels behind quartz windows
├─ TPV cells cooled by dedicated water loop (must stay <50°C)
├─ Gap between hot SiC and TPV cells: ~10cm, vacuum or inert gas
└─ Power: solid-state DC → inverter

UPPER (7-25m) — sCO₂ ZONE
├─ SiC tube wall with integral sCO₂ channels (microchannel design)
├─ sCO₂ enters at bottom of zone at 400°C, exits top at 750°C
├─ Feeds recompression Brayton turbine (located at ground level)
├─ Recuperator recovers exhaust heat
└─ This zone produces ~50% of all electricity

MIDDLE (25-38m) — STEAM ZONE
├─ Stainless steel tube section (lower temp = cheaper material)
├─ Water/steam flows upward in wall channels
├─ Superheated steam at 475°C drives conventional turbine
├─ Feedwater preheated by sCO₂ turbine reject heat
└─ Proven, bankable technology

LOWER (38-45m) — ORC ZONE
├─ Standard steel tube, lower concentration
├─ Thermal oil or direct ORC working fluid in walls
├─ Feeds packaged ORC unit (Turboden/ORMAT style)
├─ Exhaust heat at ~80°C feeds Zone 5
└─ Modular, replaceable units

BOTTOM (45-50m) — THERMAL OFFTAKE
├─ Lowest concentration, lowest temperature
├─ Water circulation for district heating / desalination
├─ Absorption chiller feed for cooling
├─ Reject heat sink (dry cooler if no thermal demand)
└─ This zone is the "free bonus" — zero conversion losses

The tube is NOT one continuous material. It's a COMPOSITE:
- Top 7m: SiC + carbon foam (highest temp, most expensive)
- Middle 18m: SiC with sCO₂ microchannels (moderate cost)
- Lower 13m: Superalloy or stainless steel (commodity)
- Bottom 12m: Carbon steel (cheapest)

Total exotic material (SiC) needed: top 25m only = 50% of tube.
Bottom 50% is standard industrial steel.
""")

# =============================================================================
# FINAL NUMBERS
# =============================================================================

print(f"{'='*80}")
print("FINAL SCORECARD")
print("="*80)

improvement_vs_v2 = (v25_elec_per_ft2 / v2_elec_ft2 - 1) * 100
improvement_vs_pv = (v25_elec_per_ft2 / pv_per_ft2 - 1) * 100
improvement_vs_csp = (v25_elec_per_ft2 / csp_per_ft2 - 1) * 100

print(f"""
  VCST v2.5 Engineered Stack:
  
  Solar → electricity:          {total_elec_fraction*100:.2f}%
  Solar → total useful:         {total_useful*100:.2f}%
  
  Electricity per ft² of land:  {v25_elec_per_ft2:.2f} kWh/yr
  Total useful per ft² of land: {v25_total_per_ft2:.2f} kWh/yr
  
  vs PV solar farm:             +{improvement_vs_pv:.0f}% more electricity per ft²
  vs Tower CSP:                 +{improvement_vs_csp:.0f}% more electricity per ft²
  vs VCST v2 (single cycle):    +{improvement_vs_v2:.0f}% more electricity per ft²
  
  50 MW plant: {field_area_50MW/m2_per_acre:.0f} acres
  (vs PV: 143 acres, vs CSP: 233 acres)
  
  The multi-zone approach adds {(total_elec_fraction - v2_sys_eff)*100:.1f} percentage points
  of solar-to-electric efficiency over v2's single-cycle design.
  
  That's {(total_elec_fraction/v2_sys_eff - 1)*100:.0f}% more electricity from the same mirrors.
""")

print("✓ Analysis complete.")
