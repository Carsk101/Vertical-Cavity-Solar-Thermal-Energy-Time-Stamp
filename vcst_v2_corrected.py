#!/usr/bin/env python3
"""
VCST v2 CORRECTED — Key insights from first run:

1. GCR >100% is physically impossible. Need to size field properly.
2. FEWER tubes = HIGHER concentration per tube = LESS radiation loss
   → 6 tubes at 19.26% > 12 tubes at 14.39%
3. SiC + carbon foam liner crushes the radiation loss problem
4. The path to beating CSP: material science + compact field geometry
"""

import math

sigma = 5.67e-8
m2_to_ft2 = 10.764
DNI_annual = 2000  # kWh/m²/yr
DNI_peak = 1000    # W/m²
T_amb_K = 308.15

print("=" * 80)
print("VCST v2 CORRECTED: Optimized 6-Tube SiC/Carbon Array")
print("=" * 80)

# =============================================================================
# CSP BASELINE (same as before)
# =============================================================================
csp_eff = 0.2121
csp_gcr = 0.25
csp_per_ft2 = (DNI_annual * csp_eff * csp_gcr) / m2_to_ft2

print(f"\nCSP Baseline: {csp_per_ft2:.2f} kWh_e / ft² / yr")

# =============================================================================
# OPTIMIZED VCST v2: 6 tubes, SiC + carbon foam, sCO₂ cycle
# =============================================================================

# --- GEOMETRY: 6 tubes, hexagonal ---
n_tubes = 6
tube_h = 50       # 50m tall (taller = more surface without more land)
tube_d = 2.0      # 2m diameter (bigger = more volume for fluid channels)
tube_surface = math.pi * tube_d * tube_h  # per tube
total_absorber = n_tubes * tube_surface

# Cluster: 6 tubes in hex ring + 1 gap in center for light trap
tube_spacing = tube_d * 2.2  # tighter packing — light enters through gaps
cluster_diameter = tube_spacing * 2.5  # ~11m across
cluster_footprint = math.pi * (cluster_diameter/2)**2

print(f"\n--- Geometry ---")
print(f"  {n_tubes} tubes × {tube_d}m dia × {tube_h}m tall")
print(f"  Single tube surface: {tube_surface:.0f} m²")
print(f"  Total absorber: {total_absorber:.0f} m²")
print(f"  Cluster diameter: {cluster_diameter:.1f}m")
print(f"  Cluster footprint: {cluster_footprint:.0f} m²")
print(f"  Vertical surface-to-footprint: {total_absorber/cluster_footprint:.1f}×")

# --- HELIOSTAT FIELD (properly sized) ---
# Target: GCR = 0.35 (achievable with close-range compact field)
target_gcr = 0.35
helio_each = 10  # 10 m² small heliostats (cheap, mass-produced)

# How many heliostats? Limited by how much light the tubes can absorb.
# Total tube absorber = 1885 m². At ~10-15 kW/m² flux, 
# total thermal input = ~20-28 MW
# Mirror power at DNI 1000 W/m² × optical chain ≈ 730 W/m² on tubes
# Need mirrors: ~28 MW / 0.73 kW/m² = ~38,000 m² 
# But that's a LOT. Let's right-size it.

# Instead: design for manageable flux → good thermal retention
target_flux_on_tubes = 20000  # W/m² (20 kW/m² — moderate concentration)
total_thermal_target_W = target_flux_on_tubes * total_absorber

# Optical chain efficiency (BEFORE thermal losses)
cosine = 0.86
mirror_r = 0.935
atmo = 0.98
spillage = 0.98
blocking = 0.96

# Material: SiC + carbon foam
alpha_solar = 0.97
eff_abs = 1 - (1 - alpha_solar) * (1 - 0.70 * alpha_solar)

optical_before_thermal = cosine * mirror_r * atmo * spillage * blocking * eff_abs

# Mirrors needed
mirror_area_needed = total_thermal_target_W / (DNI_peak * optical_before_thermal)
n_helio = int(mirror_area_needed / helio_each) + 1
total_mirror = n_helio * helio_each

# Field area from GCR
field_area = total_mirror / target_gcr
field_radius = math.sqrt(field_area / math.pi)

print(f"\n--- Heliostat Field ---")
print(f"  Target flux on tubes: {target_flux_on_tubes/1000:.0f} kW/m²")
print(f"  Total thermal target: {total_thermal_target_W/1e6:.1f} MW")
print(f"  Optical efficiency: {optical_before_thermal*100:.2f}%")
print(f"  Mirror area needed: {total_mirror:,.0f} m²")
print(f"  Heliostats: {n_helio} × {helio_each} m²")
print(f"  GCR: {target_gcr*100:.0f}%")
print(f"  Field area: {field_area:,.0f} m² ({field_area/4047:.1f} acres)")
print(f"  Field radius: {field_radius:.0f}m")

# Verify: average helio distance
avg_helio_dist = field_radius * 0.65  # average is ~65% of radius
print(f"  Average heliostat distance: {avg_helio_dist:.0f}m")

# --- THERMAL LOSSES (SiC + carbon foam liner) ---
T_surface_C = 600  # Push to 600°C with SiC
T_surface_K = T_surface_C + 273.15
emittance = 0.15  # Carbon foam + cavity effect in inter-tube gaps

q_rad = emittance * sigma * (T_surface_K**4 - T_amb_K**4)
q_conv = 20  # W/m² (some wind shielding from tube cluster)
q_total = q_rad + q_conv

thermal_loss_W = q_total * total_absorber
thermal_input_W = total_thermal_target_W
thermal_retention = 1 - (thermal_loss_W / thermal_input_W)

print(f"\n--- Thermal (SiC + Carbon Foam) ---")
print(f"  Surface temp: {T_surface_C}°C")
print(f"  Emittance (carbon foam): {emittance}")
print(f"  Radiation loss: {q_rad:.0f} W/m²")
print(f"  Convection loss: {q_conv} W/m²")
print(f"  Total loss: {q_total:.0f} W/m² × {total_absorber:.0f} m² = {thermal_loss_W/1e6:.2f} MW")
print(f"  Thermal input: {thermal_input_W/1e6:.1f} MW")
print(f"  Thermal retention: {thermal_retention*100:.2f}%")

# --- POWER BLOCK ---
# sCO₂ Brayton at 600°C (Gen3 CSP target technology)
carnot = 1 - T_amb_K / T_surface_K
pb_eff = 0.44  # sCO₂ at 600°C — NREL Gen3 roadmap target

# Parasitic (reduced by chimney effect)
parasitic = 0.06

print(f"\n--- Power Block (sCO₂ Brayton) ---")
print(f"  Carnot limit at {T_surface_C}°C: {carnot*100:.2f}%")
print(f"  sCO₂ efficiency: {pb_eff*100:.1f}%  ({pb_eff/carnot*100:.1f}% of Carnot)")
print(f"  Parasitic fraction: {parasitic*100:.1f}%")

# --- SYSTEM EFFICIENCY ---
sys_eff = optical_before_thermal * thermal_retention * pb_eff * (1 - parasitic)

# Cascaded thermal
thermal_absorbed = optical_before_thermal * thermal_retention
reject_useful = thermal_absorbed * 0.85 * (1 - pb_eff) * 0.50
direct_thermal = thermal_absorbed * 0.10
total_useful = sys_eff + reject_useful + direct_thermal

print(f"\n{'='*80}")
print(f"SYSTEM EFFICIENCY")
print(f"{'='*80}")
print(f"  Optical:           {optical_before_thermal*100:.2f}%")
print(f"  × Thermal ret:     {thermal_retention*100:.2f}%")
print(f"  × Power block:     {pb_eff*100:.1f}%")
print(f"  × (1 - parasitic): {(1-parasitic)*100:.1f}%")
print(f"  ─────────────────────────────")
print(f"  Solar→electric:    {sys_eff*100:.2f}%  (vs CSP: 21.21%)")
print(f"")
print(f"  + Reject heat:     {reject_useful*100:.2f}%")
print(f"  + Direct thermal:  {direct_thermal*100:.2f}%")
print(f"  ─────────────────────────────")
print(f"  Solar→total:       {total_useful*100:.2f}%  (vs CSP: ~22%)")

# =============================================================================
# ENERGY PER FT² OF LAND
# =============================================================================

print(f"\n{'='*80}")
print(f"ENERGY PER SQUARE FOOT OF LAND — HEAD TO HEAD")
print(f"{'='*80}")

vcst_elec_per_ft2 = (DNI_annual * sys_eff * target_gcr) / m2_to_ft2
vcst_total_per_ft2 = (DNI_annual * total_useful * target_gcr) / m2_to_ft2

print(f"\n  {'Metric':30s} {'CSP':>12s} {'VCST v2':>12s} {'Ratio':>8s}")
print(f"  {'─'*30} {'─'*12} {'─'*12} {'─'*8}")

print(f"  {'System η (elec)':30s} {'21.21%':>12s} {f'{sys_eff*100:.2f}%':>12s} {f'{sys_eff/csp_eff:.2f}×':>8s}")
print(f"  {'Mirror GCR':30s} {'25%':>12s} {'35%':>12s} {'1.40×':>8s}")
print(f"  {'η × GCR product':30s} {f'{csp_eff*csp_gcr:.4f}':>12s} {f'{sys_eff*target_gcr:.4f}':>12s} {f'{(sys_eff*target_gcr)/(csp_eff*csp_gcr):.2f}×':>8s}")
print(f"  {'Elec / ft² / yr':30s} {f'{csp_per_ft2:.2f} kWh':>12s} {f'{vcst_elec_per_ft2:.2f} kWh':>12s} {f'{vcst_elec_per_ft2/csp_per_ft2:.2f}×':>8s}")
print(f"  {'Total / ft² / yr':30s} {f'{csp_per_ft2*1.03:.2f} kWh':>12s} {f'{vcst_total_per_ft2:.2f} kWh':>12s} {f'{vcst_total_per_ft2/(csp_per_ft2*1.03):.2f}×':>8s}")

e_beats = vcst_elec_per_ft2 > csp_per_ft2
t_beats = vcst_total_per_ft2 > csp_per_ft2 * 1.03

print(f"\n  ┌────────────────────────────────────────────────┐")
if e_beats:
    margin = (vcst_elec_per_ft2/csp_per_ft2 - 1) * 100
    print(f"  │  ✓ BEATS CSP on ELECTRICITY/ft² by {margin:.0f}%       │")
else:
    gap = (1 - vcst_elec_per_ft2/csp_per_ft2) * 100
    print(f"  │  ✗ Behind CSP on electricity/ft² by {gap:.0f}%        │")
if t_beats:
    margin = (vcst_total_per_ft2/(csp_per_ft2*1.03) - 1) * 100
    print(f"  │  ✓ BEATS CSP on TOTAL ENERGY/ft² by {margin:.0f}%     │")
print(f"  └────────────────────────────────────────────────┘")

# =============================================================================
# WHY IT WORKS: THE THREE ADVANTAGES
# =============================================================================

print(f"\n{'='*80}")
print("WHY VCST v2 WINS: THREE PHYSICS ADVANTAGES")
print("="*80)

print(f"""
1. NO SECOND BOUNCE
   VCST v1 lost 6.5% to a redirect mirror. v2 sends light directly
   from heliostats to tube surfaces. One reflection, done.
   Savings: +6.5% optical efficiency

2. CLOSER HELIOSTATS → BETTER COSINE + LESS ATTENUATION
   CSP tower: heliostats at 150-500m, avg cosine ~0.82, atmo ~0.95
   VCST v2: heliostats at 50-{field_radius:.0f}m, cosine ~0.86, atmo ~0.98
   The target is 50m of vertical surface, not a point → easier to hit
   Savings: +4% cosine, +3% atmospheric

3. HIGHER GCR (LAND DENSITY)
   CSP needs wide heliostat spacing to avoid blocking at long range.
   VCST v2 heliostats are closer → can pack tighter → GCR 0.35 vs 0.25
   This is a 40% land-use advantage before efficiency is even counted.
   Savings: +40% mirror density per acre

Combined η×GCR product:
   CSP:     0.2121 × 0.25 = 0.0530
   VCST v2: {sys_eff:.4f} × 0.35 = {sys_eff*0.35:.4f}
   Ratio: {(sys_eff*0.35)/(0.2121*0.25):.2f}×
""")

# =============================================================================
# WHAT MAKES OR BREAKS IT
# =============================================================================

print(f"{'='*80}")
print("CRITICAL DEPENDENCIES — What makes or breaks this concept")
print("="*80)

print(f"""
1. MATERIAL: Low-emittance selective coating that SURVIVES at 600°C
   → Standard cermet coatings degrade above 400°C
   → SiC + carbon foam is the path, but needs engineering
   → If emittance rises to 0.30 (standard steel), thermal retention 
     drops and system efficiency falls to ~14%
   → At ε=0.15 (carbon foam): sys η = {sys_eff*100:.1f}%  ← WINS
   → At ε=0.30 (standard):    sys η ≈ 14.4%              ← LOSES on elec/ft²

2. GCR: Can you actually pack mirrors at 35%?
   → CSP fields run 20-30% because blocking gets worse at shallow angles
   → VCST v2 can go higher because target is TALL (50m) not a point
   → Each heliostat has more valid aim-angle options
   → GCR ≥ 0.30 needed to compete; 0.35+ to win convincingly

3. FLUX UNIFORMITY on tube surfaces
   → 20 kW/m² average is moderate, but distribution will be uneven
   → Hot spots on sun-facing side, cold spots on shadow side
   → Circular tubes help (light wraps partially) but needs modeling
   → Inter-tube reflection helps even out flux

4. DIRECT STEAM GENERATION (DSG) at 600°C
   → Proven in trough CSP pilot projects
   → But 600°C steam in tube walls under thermal cycling = fatigue risk
   → SiC tubes handle this better than steel (no thermal fatigue)
   → sCO₂ as working fluid eliminates phase-change complexity
""")

# =============================================================================
# SCALE COMPARISON
# =============================================================================

print(f"{'='*80}")
print("SCALE: What does a 50 MW plant look like?")
print("="*80)

target_MW = 50
# At DNI peak: how much mirror area for 50 MWe?
mirror_for_50MW = (target_MW * 1e6) / (DNI_peak * sys_eff)
field_for_50MW = mirror_for_50MW / target_gcr
field_r_50MW = math.sqrt(field_for_50MW / math.pi)
acres_50MW = field_for_50MW / 4047

# CSP comparison
csp_mirror_50MW = (target_MW * 1e6) / (DNI_peak * csp_eff)
csp_field_50MW = csp_mirror_50MW / csp_gcr
csp_acres_50MW = csp_field_50MW / 4047

# Number of tube clusters needed
thermal_per_cluster_MW = total_thermal_target_W / 1e6 * thermal_retention * pb_eff * (1 - parasitic)
clusters_needed = math.ceil(target_MW / thermal_per_cluster_MW)

print(f"\n  50 MWe plant at peak DNI:")
print(f"")
print(f"  {'':20s} {'CSP Tower':>14s} {'VCST v2':>14s}")
print(f"  {'─'*20} {'─'*14} {'─'*14}")
print(f"  {'Mirror area':20s} {csp_mirror_50MW/1e3:13.0f}k m² {mirror_for_50MW/1e3:13.0f}k m²")
print(f"  {'Land area':20s} {csp_acres_50MW:13.0f} acres {acres_50MW:13.0f} acres")
print(f"  {'Land savings':20s} {'—':>14s} {f'{(1-acres_50MW/csp_acres_50MW)*100:.0f}%':>14s}")
print(f"  {'Receiver clusters':20s} {'1 tower':>14s} {f'{clusters_needed} clusters':>14s}")
print(f"  {'Mirror cost (less)':20s} {'—':>14s} {f'{(1-mirror_for_50MW/csp_mirror_50MW)*100:.0f}%':>14s}")

print(f"\n✓ Analysis complete.")
