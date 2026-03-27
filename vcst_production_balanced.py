#!/usr/bin/env python3
"""
PRODUCTION INTENSITY: PV Solar Farm vs VCST v2 PRO
=====================================================
Fair fight — same microscope on both systems.

PV's dirty secrets:
- Solar-grade silicon: 1000 MJ/kg, Siemens process at 1100°C
- Silver paste: 1500 MJ/kg, 3g per panel, finite global supply
- Fluoropolymer backsheet: toxic, non-recyclable
- Cadmium (CdTe thin-film): toxic heavy metal
- Indium/Gallium (CIGS): rare, competing with electronics

VCST v2 PRO's challenges:
- SiC bulk ceramic: 50 MJ/kg (Acheson process)
- Selective coating: thin film, microns thick
- Vacuum glass envelope: proven but needs scale-up to 2m dia
- sCO₂ turbine: specialized but uses commodity alloys
"""

import math

print("=" * 80)
print("PRODUCTION INTENSITY — Fair comparison, same microscope")
print("PV Solar Farm vs VCST v2 PRO (50 MW plant)")
print("=" * 80)

# =============================================================================
# MATERIAL DATABASE — Element properties
# =============================================================================

# Element crustal abundance (ppm by mass in Earth's crust)
# Source: USGS, CRC Handbook of Chemistry & Physics
abundance = {
    "silicon": 282000,      # 28.2% — second most abundant element
    "aluminum": 82000,      # 8.2%
    "iron": 56000,          # 5.6%
    "titanium": 5600,       # 0.56%
    "chromium": 102,        # 102 ppm
    "nickel": 84,           # 84 ppm
    "copper": 60,           # 60 ppm
    "tungsten": 1.3,        # 1.3 ppm
    "molybdenum": 1.2,      # 1.2 ppm
    "silver": 0.075,        # 0.075 ppm (very rare)
    "hafnium": 3.0,         # 3 ppm (rare but not ultra-rare)
    "indium": 0.25,         # 0.25 ppm (very rare)
    "gallium": 19,          # 19 ppm
    "cadmium": 0.15,        # 0.15 ppm
    "tellurium": 0.001,     # 0.001 ppm (extremely rare)
    "zirconium": 165,       # 165 ppm (hafnium's parent ore)
    "nitrogen": 19,         # in rocks; unlimited in atmosphere
    "carbon": 200,          # 200 ppm in crust; unlimited as CO₂
    "oxygen": 461000,       # 46.1%
}

# Element cost per kg (approximate, 2024-2025)
cost_per_kg = {
    "silicon_metallurgical": 2,        # $2/kg — dirt cheap
    "silicon_solar_grade": 25,         # $25/kg — 99.9999% pure
    "aluminum": 2.5,                   # $2.5/kg
    "iron_steel": 0.50,               # $0.50/kg
    "titanium_metal": 10,             # $10/kg
    "chromium": 12,                    # $12/kg
    "copper": 8,                       # $8/kg
    "silver": 900,                     # $900/kg (precious metal)
    "molybdenum": 60,                  # $60/kg
    "hafnium": 900,                    # $900/kg (specialty metal)
    "indium": 300,                     # $300/kg
    "gallium": 300,                    # $300/kg
    "glass_flat": 0.50,               # $0.50/kg
    "concrete": 0.10,                  # $0.10/kg
    "sic_bulk": 1.50,                  # $1.50/kg (abrasive grade)
    "nitrogen_gas": 0.10,             # $0.10/kg (from air)
}

# Embodied energy per kg (MJ/kg)
EE = {
    "silicon_solar": 1000,     # Siemens process: trichlorosilane → poly-Si
    "silicon_metallurgical": 25, # Arc furnace reduction of quartz
    "aluminum_primary": 170,
    "steel_galvanized": 38,
    "steel_structural": 25,
    "steel_stainless": 56,
    "copper": 100,
    "silver": 1500,
    "glass_flat": 15,
    "glass_vacuum_tube": 25,   # Borosilicate, higher purity
    "concrete": 1.3,
    "sic_bulk": 50,            # Acheson process
    "sputtering_coating": 2000, # MJ per kg of deposited film
    # (sputtering is energy-intensive per kg of film, but film is MICRONS thick)
    "inverter_electronics": 500,
    "turbine_assembly": 60,
}

# =============================================================================
# PV FARM — 50 MW — Detailed BOM with element breakdown
# =============================================================================

print(f"\n{'='*80}")
print("PV SOLAR FARM — 50 MW — Element-level analysis")
print("="*80)

pv_MW = 50
n_panels = pv_MW * 2000  # 100,000 panels

# Per-panel element breakdown
# Source: IEA PVPS, Bhandari et al., manufacturer specs
pv_elements = {
    # MODULE
    "Solar-grade silicon": {
        "mass_per_panel_kg": 0.080,  # ~80g poly-Si per 500W panel
        "ee_mj_kg": EE["silicon_solar"],
        "cost_kg": cost_per_kg["silicon_solar_grade"],
        "abundance_ppm": abundance["silicon"],
        "notes": "99.9999% pure. Siemens process at 1100°C. 90% of energy cost.",
        "toxic": False,
        "critical": True,  # China controls 80%+ of supply chain
    },
    "Silver paste": {
        "mass_per_panel_kg": 0.003,  # ~3g silver per panel
        "ee_mj_kg": EE["silver"],
        "cost_kg": cost_per_kg["silver"],
        "abundance_ppm": abundance["silver"],
        "notes": "0.075 ppm crustal. PV uses ~15% of global silver production.",
        "toxic": False,
        "critical": True,  # Supply limited, price volatile
    },
    "Aluminum frame": {
        "mass_per_panel_kg": 2.5,
        "ee_mj_kg": EE["aluminum_primary"],
        "cost_kg": cost_per_kg["aluminum"],
        "abundance_ppm": abundance["aluminum"],
        "notes": "Primary aluminum at 170 MJ/kg. Recyclable.",
        "toxic": False,
        "critical": False,
    },
    "Cover glass": {
        "mass_per_panel_kg": 10.0,
        "ee_mj_kg": EE["glass_flat"],
        "cost_kg": cost_per_kg["glass_flat"],
        "abundance_ppm": abundance["silicon"],  # SiO₂ based
        "notes": "Tempered low-iron glass. Commodity.",
        "toxic": False,
        "critical": False,
    },
    "Copper (cells+wiring)": {
        "mass_per_panel_kg": 0.15,
        "ee_mj_kg": EE["copper"],
        "cost_kg": cost_per_kg["copper"],
        "abundance_ppm": abundance["copper"],
        "notes": "Interconnects + junction box.",
        "toxic": False,
        "critical": False,
    },
    "EVA encapsulant": {
        "mass_per_panel_kg": 1.0,
        "ee_mj_kg": 90,
        "cost_kg": 3,
        "abundance_ppm": None,  # Petrochemical
        "notes": "Ethylene vinyl acetate. Petrochemical derived.",
        "toxic": False,
        "critical": False,
    },
    "Fluoropolymer backsheet": {
        "mass_per_panel_kg": 0.5,
        "ee_mj_kg": 90,
        "cost_kg": 5,
        "abundance_ppm": None,
        "notes": "PVDF/PET. Contains fluorine compounds. Not recyclable. PFAS concerns.",
        "toxic": True,
        "critical": False,
    },
}

# BOS (per MW)
pv_bos = {
    "Galvanized steel racking": {
        "mass_total_kg": pv_MW * 40000,
        "ee_mj_kg": EE["steel_galvanized"],
        "cost_kg": 1.50,
        "notes": "Commodity galvanized steel.",
    },
    "Concrete foundations": {
        "mass_total_kg": pv_MW * 80000,
        "ee_mj_kg": EE["concrete"],
        "cost_kg": cost_per_kg["concrete"],
        "notes": "Standard ready-mix.",
    },
    "Copper cabling": {
        "mass_total_kg": pv_MW * 4000,
        "ee_mj_kg": EE["copper"],
        "cost_kg": cost_per_kg["copper"],
        "notes": "DC + AC cable runs.",
    },
    "Inverters": {
        "mass_total_kg": pv_MW * 500,
        "ee_mj_kg": EE["inverter_electronics"],
        "cost_kg": 50,
        "notes": "Power electronics. Contains rare earths (small).",
    },
}

# Calculate totals
pv_total_ee = 0
pv_total_cost = 0
pv_total_mass = 0

print(f"\n  MODULE MATERIALS (per panel × {n_panels:,} panels):")
print(f"  {'Material':<28s} {'Total kg':>10s} {'EE(TJ)':>8s} {'Cost($M)':>9s} {'Abund':>8s} {'Crit?':>6s}")
print(f"  {'─'*28} {'─'*10} {'─'*8} {'─'*9} {'─'*8} {'─'*6}")

for name, m in pv_elements.items():
    total_kg = m["mass_per_panel_kg"] * n_panels
    total_ee = total_kg * m["ee_mj_kg"]
    total_cost = total_kg * m["cost_kg"]
    pv_total_ee += total_ee
    pv_total_cost += total_cost
    pv_total_mass += total_kg
    abund = f"{m['abundance_ppm']:.1f}" if m['abundance_ppm'] and m['abundance_ppm'] < 10 else (f"{m['abundance_ppm']:.0f}" if m['abundance_ppm'] else "—")
    crit = "YES" if m.get("critical") else ("TOXIC" if m.get("toxic") else "no")
    print(f"  {name:<28s} {total_kg:9,.0f} {total_ee/1e9:7.3f} {total_cost/1e6:8.2f} {abund:>8s} {crit:>6s}")

print(f"\n  BOS MATERIALS:")
for name, m in pv_bos.items():
    total_ee = m["mass_total_kg"] * m["ee_mj_kg"]
    total_cost = m["mass_total_kg"] * m["cost_kg"]
    pv_total_ee += total_ee
    pv_total_cost += total_cost
    pv_total_mass += m["mass_total_kg"]
    print(f"  {name:<28s} {m['mass_total_kg']:9,.0f} {total_ee/1e9:7.3f} {total_cost/1e6:8.2f}")

print(f"\n  PV TOTAL: {pv_total_mass/1000:,.0f} tonnes | {pv_total_ee/1e9:.3f} TJ | ${pv_total_cost/1e6:.1f}M materials")

# =============================================================================
# VCST v2 PRO — 50 MW — with coating options
# =============================================================================

print(f"\n{'='*80}")
print("VCST v2 PRO — 50 MW — Element-level analysis")
print("="*80)

vcst_MW = 50
n_clusters = 5
n_tubes = 6
n_total_tubes = n_clusters * n_tubes  # 30 tubes
tube_h = 50
tube_d = 2.0
tube_surface_each = math.pi * tube_d * tube_h  # 314 m²
total_tube_surface = n_total_tubes * tube_surface_each  # 9,425 m²

# Mirror area: from v2 pro best config (35.09% efficiency)
# 50 MW / (1000 W/m² × 0.3509) = 142,490 m²
mirror_area = 50e6 / (1000 * 0.3509)

# --- SELECTIVE COATING: Three options analyzed ---

print(f"\n  COATING OPTIONS — mass and cost comparison:")
print(f"  (All are thin-film sputtered coatings, ~3 μm thick)")

coating_thickness_m = 3e-6  # 3 micrometers
coating_area_m2 = total_tube_surface

coatings = {
    "TiAlN/TiAlON/Si₃N₄": {
        "density_kg_m3": 4500,  # avg density of multilayer
        "elements": {"titanium": 0.35, "aluminum": 0.25, "nitrogen": 0.25, "silicon": 0.10, "oxygen": 0.05},
        "emittance": 0.07,
        "system_eff": 0.2669,
        "per_ft2": 17.36,
        "cost_per_m2_coating": 15,  # $/m² for industrial sputtering
        "ee_per_m2": 50,  # MJ/m² for sputtering process
        "notes": "All abundant elements. Ti: 5600 ppm, Al: 82000 ppm, N: unlimited, Si: 282000 ppm",
        "abundance_min_ppm": 5600,  # Ti is the rarest element in this coating
        "trl": "5-6",
    },
    "ZrC QOM": {
        "density_kg_m3": 6700,
        "elements": {"zirconium": 0.65, "carbon": 0.25, "oxygen": 0.10},
        "emittance": 0.10,
        "system_eff": 0.3058,  # with combined cycle at 700°C
        "per_ft2": 19.89,
        "cost_per_m2_coating": 20,
        "ee_per_m2": 60,
        "notes": "Zr: 165 ppm (abundant). Carbon: unlimited. Stable to 900°C in vacuum.",
        "abundance_min_ppm": 165,
        "trl": "4-5",
    },
    "HfMoN tandem": {
        "density_kg_m3": 11000,  # Hf is dense
        "elements": {"hafnium": 0.50, "molybdenum": 0.25, "nitrogen": 0.15, "oxygen": 0.05, "aluminum": 0.05},
        "emittance": 0.05,
        "system_eff": 0.3509,
        "per_ft2": 22.82,
        "cost_per_m2_coating": 80,  # Hf sputtering targets are expensive
        "ee_per_m2": 100,
        "notes": "Hf: 3 ppm (rare). Mo: 1.2 ppm (rare). Best performance but most expensive.",
        "abundance_min_ppm": 1.2,  # Mo is the rarest
        "trl": "4",
    },
}

for name, c in coatings.items():
    vol_m3 = coating_area_m2 * coating_thickness_m
    mass_kg = vol_m3 * c["density_kg_m3"]
    total_cost = coating_area_m2 * c["cost_per_m2_coating"]
    total_ee = coating_area_m2 * c["ee_per_m2"]
    
    c["total_mass_kg"] = mass_kg
    c["total_cost"] = total_cost
    c["total_ee_mj"] = total_ee
    
    # Element masses
    element_masses = {el: mass_kg * frac for el, frac in c["elements"].items()}
    rarest = min(c["elements"].keys(), key=lambda e: abundance.get(e, 999999))
    
    print(f"\n  {name}:")
    print(f"    Total coating mass: {mass_kg:.1f} kg ({mass_kg*1000:.0f} grams)")
    print(f"    Total coating cost: ${total_cost:,.0f}")
    print(f"    Total coating energy: {total_ee/1e6:.3f} GJ")
    print(f"    ε = {c['emittance']} → system η = {c['system_eff']*100:.1f}% → {c['per_ft2']:.2f} kWh/ft²")
    print(f"    Rarest element: {rarest} ({abundance.get(rarest, '?')} ppm) — {element_masses.get(rarest, 0)*1000:.0f}g needed")
    print(f"    TRL: {c['trl']}")

# --- REST OF VCST BOM (same regardless of coating choice) ---
print(f"\n  BASE SYSTEM (independent of coating choice):")

vcst_base_bom = {
    "SiC ceramic tubes (bulk)": {
        "mass_kg": 855000,  # from previous calc
        "ee_mj_kg": EE["sic_bulk"],
        "cost_kg": cost_per_kg["sic_bulk"],
        "abundance": "Si: 282000 ppm, C: unlimited",
        "notes": "Acheson process. Commodity abrasive. NOT semiconductor grade.",
    },
    "Mirror glass (silvered)": {
        "mass_kg": mirror_area * 10,  # 10 kg/m²
        "ee_mj_kg": 18,
        "cost_kg": 1.5,
        "abundance": "Si, Na, Ca: all >1%",
        "notes": "Standard silvered float glass. Commodity.",
    },
    "Heliostat steel frames": {
        "mass_kg": mirror_area * 8,  # 8 kg/m²
        "ee_mj_kg": EE["steel_galvanized"],
        "cost_kg": 1.5,
        "abundance": "Fe: 56000 ppm",
        "notes": "Galvanized steel. Commodity.",
    },
    "Vacuum glass envelopes": {
        "mass_kg": total_tube_surface * 15,  # 15 kg/m² borosilicate tube
        "ee_mj_kg": EE["glass_vacuum_tube"],
        "cost_kg": 8,
        "abundance": "Si, B, Na: all abundant",
        "notes": "Borosilicate glass. Schott PTR-70 is commercial. Scale-up needed.",
    },
    "Heliostat tracking electronics": {
        "mass_kg": (mirror_area / 10) * 15,  # 15 kg per heliostat
        "ee_mj_kg": EE["inverter_electronics"],
        "cost_kg": 30,
        "abundance": "Various (Cu, Si, rare earths trace)",
        "notes": "Motors + controllers. Same as any tracking system.",
    },
    "Reinforced concrete": {
        "mass_kg": n_clusters * 500 * 2400,
        "ee_mj_kg": 2.5,
        "cost_kg": 0.10,
        "abundance": "Ca, Si, Al: all >1%",
        "notes": "Standard construction concrete.",
    },
    "Structural steel": {
        "mass_kg": n_clusters * 50000,
        "ee_mj_kg": EE["steel_structural"],
        "cost_kg": 1.0,
        "abundance": "Fe: 56000 ppm",
        "notes": "Standard structural steel.",
    },
    "sCO₂ + steam turbines": {
        "mass_kg": 400000,
        "ee_mj_kg": EE["turbine_assembly"],
        "cost_kg": 25,
        "abundance": "Ni, Cr, Fe alloys",
        "notes": "Superalloy turbomachinery. Higher cost than PV inverters.",
    },
    "Copper cabling": {
        "mass_kg": vcst_MW * 5000,
        "ee_mj_kg": EE["copper"],
        "cost_kg": cost_per_kg["copper"],
        "abundance": "Cu: 60 ppm",
        "notes": "Power cabling.",
    },
    "Piping (stainless)": {
        "mass_kg": 40000,
        "ee_mj_kg": EE["steel_stainless"],
        "cost_kg": 5,
        "abundance": "Fe, Cr, Ni",
        "notes": "Steam + sCO₂ piping.",
    },
}

vcst_total_ee = 0
vcst_total_cost = 0
vcst_total_mass = 0

print(f"\n  {'Component':<30s} {'Total kg':>10s} {'EE(TJ)':>8s} {'Cost($M)':>9s}")
print(f"  {'─'*30} {'─'*10} {'─'*8} {'─'*9}")

for name, m in vcst_base_bom.items():
    total_ee = m["mass_kg"] * m["ee_mj_kg"]
    total_cost = m["mass_kg"] * m["cost_kg"]
    vcst_total_ee += total_ee
    vcst_total_cost += total_cost
    vcst_total_mass += m["mass_kg"]
    print(f"  {name:<30s} {m['mass_kg']:9,.0f} {total_ee/1e9:7.3f} {total_cost/1e6:8.2f}")

# =============================================================================
# THREE VCST CONFIGS — with each coating
# =============================================================================

print(f"\n{'='*80}")
print("BALANCED COMPARISON — Three VCST coating options vs PV")
print("="*80)

pv_per_ft2 = 11.80
pv_annual_MWh = 63857  # From LBNL data

print(f"\n  {'Config':<42s} {'η':>6s} {'kWh/ft²':>8s} {'Prod TJ':>8s} {'EPBT yr':>8s} {'Mat $M':>7s} {'Rarest':>10s}")
print(f"  {'─'*42} {'─'*6} {'─'*8} {'─'*8} {'─'*8} {'─'*7} {'─'*10}")

# PV baseline
print(f"  {'PV solar farm (reference)':<42s} {'18%':>6s} {pv_per_ft2:7.2f} {pv_total_ee/1e9:7.3f} {pv_total_ee/(pv_annual_MWh*3600):7.2f} {pv_total_cost/1e6:6.1f} {'Ag 0.075':>10s}")

DNI_yr = 2000  # kWh/m²/yr

for cname, c in coatings.items():
    total_ee = vcst_total_ee + c["total_ee_mj"]
    total_cost = vcst_total_cost + c["total_cost"]
    total_mass = vcst_total_mass + c["total_mass_kg"]
    
    # Annual energy output
    sys_eff = c["system_eff"]
    gcr = 0.35
    # Annual from same-size plant (mirror area × DNI × eff)
    annual_MWh = mirror_area * DNI_yr * sys_eff / 1000
    
    epbt = total_ee / (annual_MWh * 3600)
    
    rarest_str = f"{min(c['elements'].keys(), key=lambda e: abundance.get(e, 999999))} {c['abundance_min_ppm']}"
    
    label = f"VCST + {cname}"
    print(f"  {label:<42s} {sys_eff*100:5.1f}% {c['per_ft2']:7.2f} {total_ee/1e9:7.3f} {epbt:7.2f} {total_cost/1e6:6.1f} {rarest_str:>10s}")

# =============================================================================
# THE BALANCED RECOMMENDATION
# =============================================================================

print(f"\n{'='*80}")
print("THE BALANCED RECOMMENDATION")
print("="*80)

print(f"""
THREE TIERS — pick your risk tolerance:

┌─────────────────────────────────────────────────────────────────────┐
│ TIER 1: SAFE BET — TiAlN/TiAlON/Si₃N₄ coating                    │
│                                                                     │
│ All elements abundant (Ti: 5600 ppm, Al: 82000 ppm, Si: 282000)   │
│ Magnetron sputtering is a mature industrial process                 │
│ Proven stable at 600°C in air — doesn't even need vacuum           │
│ Coating mass: {coatings['TiAlN/TiAlON/Si₃N₄']['total_mass_kg']:.0f} kg total for 30 tubes (trivial)                   │
│ Coating cost: ${coatings['TiAlN/TiAlON/Si₃N₄']['total_cost']:,.0f} for entire plant                         │
│                                                                     │
│ Performance: 17.36 kWh/ft² (+47% vs PV)                           │
│ TRL: 5-6 — lowest risk, still crushes PV                          │
│                                                                     │
│ NO rare materials. NO toxic materials. NO supply chain risk.       │
│ THIS IS THE ANSWER for a first plant.                              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ TIER 2: MEDIUM RISK — ZrC QOM + vacuum + combined cycle            │
│                                                                     │
│ Zirconium: 165 ppm (abundant — it's in beach sand)                 │
│ Needs vacuum envelope (proven tech, needs scale-up)                │
│ Needs combined cycle turbine (proven in gas plants)                │
│ Coating mass: {coatings['ZrC QOM']['total_mass_kg']:.0f} kg total (still trivial)                     │
│                                                                     │
│ Performance: 19.89 kWh/ft² (+69% vs PV)                           │
│ TRL: 4-5 for coating, 7-8 for combined cycle                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ TIER 3: MAXIMUM PERFORMANCE — HfMoN + vacuum + combined cycle      │
│                                                                     │
│ Hafnium: 3 ppm (rare). Molybdenum: 1.2 ppm (rare).               │
│ BUT: only {coatings['HfMoN tandem']['total_mass_kg']*1000:.0f}g total coating = {coatings['HfMoN tandem']['total_mass_kg']*coatings['HfMoN tandem']['elements']['hafnium']*1000:.0f}g Hf + {coatings['HfMoN tandem']['total_mass_kg']*coatings['HfMoN tandem']['elements']['molybdenum']*1000:.0f}g Mo                │
│ A PV farm uses {n_panels * 0.003:.0f} kg (300 kg) of SILVER at 0.075 ppm         │
│ This uses {coatings['HfMoN tandem']['total_mass_kg']*coatings['HfMoN tandem']['elements']['hafnium']:.2f} kg of hafnium at 3 ppm = 40× more abundant          │
│ So even the "rare material" option uses LESS rare stuff than PV    │
│                                                                     │
│ Performance: 22.82 kWh/ft² (+93% vs PV)                           │
│ TRL: 4 — highest risk, highest reward                              │
└─────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# HEAD-TO-HEAD: CRITICAL MATERIAL COMPARISON
# =============================================================================

print(f"{'='*80}")
print("CRITICAL MATERIAL SHOWDOWN — PV vs VCST (Tier 1)")
print("="*80)

tier1_coating = coatings["TiAlN/TiAlON/Si₃N₄"]

pv_silver_kg = n_panels * 0.003
pv_silicon_kg = n_panels * 0.080
pv_aluminum_kg = n_panels * 2.5
pv_fluoro_kg = n_panels * 0.5

vcst_sic_kg = 855000
vcst_coating_kg = tier1_coating["total_mass_kg"]
vcst_glass_vac_kg = 0  # Tier 1 doesn't need vacuum

print(f"""
  RARE / CRITICAL MATERIALS:
  
  PV Farm:
    Silver:           {pv_silver_kg:.0f} kg  (0.075 ppm crustal abundance)
    Solar-grade Si:   {pv_silicon_kg:.0f} kg  (abundant element, extreme processing)
    Indium (CIGS):    varies  (0.25 ppm — if thin-film used)
    
  VCST Tier 1:
    Hafnium:          0 kg
    Silver:           0 kg  
    Rare earths:      0 kg
    Rarest element:   Ti at {abundance['titanium']} ppm ({abundance['titanium']/abundance['silver']:.0f}× more abundant than Ag)
  
  TOXIC / HAZARDOUS:
  
  PV Farm:
    Lead solder:      ~{n_panels * 0.010:.0f} kg Pb in cell interconnects
    Fluoropolymers:   {pv_fluoro_kg:.0f} kg (PFAS-related, not recyclable)
    Cadmium:          0 for mono-Si (major concern for CdTe thin-film)
    
  VCST Tier 1:
    Toxic materials:  NONE
    
  SUPPLY CHAIN RISK:
  
  PV Farm:
    China controls:   ~80% of polysilicon, ~90% of wafer/cell production
    Silver:           Finite global supply, competing with jewelry/electronics
    
  VCST Tier 1:
    All materials:    Globally distributed commodity supply chains
    SiC:              Produced in US, EU, China (multiple sources)
    Steel + glass:    Universal availability
    Ti, Al, Si, N:    Among Earth's most abundant elements
""")

# =============================================================================
# PRODUCTION ENERGY FINAL COMPARISON
# =============================================================================

print(f"{'='*80}")
print("PRODUCTION ENERGY FINAL — Tier 1 (safest) vs PV")
print("="*80)

# Tier 1 VCST total
vcst_t1_ee = vcst_total_ee + tier1_coating["total_ee_mj"]
vcst_t1_cost = vcst_total_cost + tier1_coating["total_cost"]
vcst_t1_annual = mirror_area * 2000 * tier1_coating["system_eff"] / 1000
vcst_t1_epbt = vcst_t1_ee / (vcst_t1_annual * 3600)

# Lifetime EROI
pv_lifetime_MJ = sum(pv_annual_MWh * 3600 * (1-0.007)**y for y in range(25))
vcst_t1_lifetime_MJ = sum(vcst_t1_annual * 3600 * (1-0.003)**y for y in range(35))

pv_eroi = pv_lifetime_MJ / pv_total_ee
vcst_t1_eroi = vcst_t1_lifetime_MJ / vcst_t1_ee

ratio_ee = vcst_t1_ee / pv_total_ee

print(f"""
  {'Metric':<35s} {'PV Farm':>12s} {'VCST Tier 1':>12s} {'Ratio':>8s}
  {'─'*35} {'─'*12} {'─'*12} {'─'*8}
  Embodied energy (TJ)               {pv_total_ee/1e9:11.3f} {vcst_t1_ee/1e9:11.3f} {ratio_ee:7.1f}×
  Material cost ($M)                  {pv_total_cost/1e6:11.1f} {vcst_t1_cost/1e6:11.1f} {vcst_t1_cost/pv_total_cost:7.1f}×
  Total mass (tonnes)                 {pv_total_mass/1000:11,.0f} {vcst_total_mass/1000:11,.0f} {vcst_total_mass/pv_total_mass:7.1f}×
  
  Annual electric (MWh)               {pv_annual_MWh:11,.0f} {vcst_t1_annual:11,.0f} {vcst_t1_annual/pv_annual_MWh:7.1f}×
  Energy payback (years)              {pv_total_ee/(pv_annual_MWh*3600):11.2f} {vcst_t1_epbt:11.2f} {vcst_t1_epbt/(pv_total_ee/(pv_annual_MWh*3600)):7.1f}×
  EROI (lifetime)                     {pv_eroi:11.0f}:1 {vcst_t1_eroi:11.0f}:1
  
  Rare materials                       Ag, In        NONE
  Toxic materials                      Pb, PFAS      NONE
  Supply chain risk                    HIGH (China)  LOW (global)
  kWh electricity / ft² / yr          {pv_per_ft2:11.2f} {tier1_coating['per_ft2']:11.2f} {tier1_coating['per_ft2']/pv_per_ft2:7.2f}×
""")

print(f"  VERDICT: VCST Tier 1 costs {ratio_ee:.1f}× more energy to build,")
print(f"  produces {vcst_t1_annual/pv_annual_MWh:.1f}× more electricity per year,")
print(f"  uses ZERO rare or toxic materials,")
print(f"  and generates {tier1_coating['per_ft2']/pv_per_ft2:.0f}% more electricity per ft² of land.")
print(f"  Lifetime EROI is {vcst_t1_eroi:.0f}:1 vs PV's {pv_eroi:.0f}:1.")

print(f"\n✓ Analysis complete.")
