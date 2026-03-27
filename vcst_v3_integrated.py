#!/usr/bin/env python3
"""
VCST v3: MIRRORS BUILT INTO THE VERTICAL TUBES
================================================
No external heliostat field. The tube cluster IS the power plant.

Three configurations to test:
A) Alternating tubes: some are reflective, some are absorbers
B) Half-and-half tubes: each tube is mirror on one side, absorber on the other
C) Parabolic trough strips between tubes: vertical troughs focus onto absorber tubes

Key question: does eliminating the field save enough land to compensate
for lower concentration and no tracking?
"""

import math

sigma = 5.67e-8
m2_to_ft2 = 10.764
DNI_annual = 2000
DNI_peak = 1000
T_amb_K = 308.15

print("=" * 80)
print("VCST v3: INTEGRATED MIRROR-TUBE ARCHITECTURE")
print("No heliostat field — mirrors built into tube structure")
print("=" * 80)

# Baselines to beat
csp_eff = 0.2121
csp_gcr = 0.25
csp_per_ft2 = (DNI_annual * csp_eff * csp_gcr) / m2_to_ft2

vcst_v2_eff = 0.2295
vcst_v2_gcr = 0.35
vcst_v2_per_ft2 = (DNI_annual * vcst_v2_eff * vcst_v2_gcr) / m2_to_ft2

print(f"\nBaselines:")
print(f"  CSP Tower:  {csp_per_ft2:.2f} kWh_e/ft²/yr  (η={csp_eff*100:.1f}%, GCR={csp_gcr*100:.0f}%)")
print(f"  VCST v2:    {vcst_v2_per_ft2:.2f} kWh_e/ft²/yr (η={vcst_v2_eff*100:.1f}%, GCR={vcst_v2_gcr*100:.0f}%)")

# =============================================================================
# CONFIGURATION A: Alternating mirror tubes + absorber tubes
# =============================================================================
print(f"\n{'='*80}")
print("CONFIG A: Alternating mirror tubes & absorber tubes")
print("="*80)
print("""
  Layout: 6 absorber tubes surrounded by 6 mirror tubes
  Mirror tubes are polished cylindrical reflectors
  They redirect incident sunlight onto adjacent absorber tubes
  No tracking — fixed geometry, works best at certain sun angles
""")

n_absorber = 6
n_mirror = 6
n_total = n_absorber + n_mirror
tube_h = 50  # m
tube_d_abs = 2.0  # m absorber diameter
tube_d_mir = 1.5  # m mirror diameter (can be thinner, just reflective)

# Cluster arrangement: hexagonal, alternating
# Cluster footprint
cluster_diameter = 16  # m across
cluster_area_m2 = math.pi * (cluster_diameter / 2) ** 2

# Absorber surface
abs_surface_each = math.pi * tube_d_abs * tube_h
total_abs_surface = n_absorber * abs_surface_each

# Mirror surface (reflective area facing inward)
mir_surface_each = math.pi * tube_d_mir * tube_h * 0.5  # half faces inward
total_mir_surface = n_mirror * mir_surface_each

# But here's the problem: how much sunlight actually enters the cluster?
# The cluster captures light from its PROJECTED AREA facing the sun
# For a 16m diameter, 50m tall cluster:
# At any sun angle, the projected capture area ≈ cluster_diameter × tube_h
# (it's a cylinder, so projected area = diameter × height regardless of azimuth)

projected_capture_m2 = cluster_diameter * tube_h  # ~800 m²

# But a lot of that is blocked by the tubes themselves (shadows)
# 12 tubes of avg 1.75m diameter in a 16m cluster
total_tube_frontal = n_total * 1.75 * tube_h  # if all in a line
# But they're in a circle, so overlap. Effective blocking:
# Roughly 40-50% of the projected area is solid tube, rest is gaps
gap_fraction = 0.50  # 50% of projected area is gaps where light enters
effective_capture_m2 = projected_capture_m2 * gap_fraction

# Light that enters through gaps hits mirror tubes → reflects to absorber tubes
# OR hits absorber tubes directly
# Estimate: 40% hits absorber directly, 60% hits mirrors (or misses)
direct_hit_fraction = 0.35
mirror_redirect_fraction = 0.40  # hits a mirror tube and redirects
miss_fraction = 0.25  # goes through without hitting anything useful

# Mirror tube effectiveness: cylindrical mirror is NOT a parabolic concentrator
# A convex mirror DIVERGES light — useless
# A polished cylinder has mixed curvature — some light focuses, some diverges
# Net effectiveness of cylindrical mirror redirect: ~30-40%
mirror_redirect_efficiency = 0.35  # of light hitting a mirror tube, 35% reaches an absorber

# Total light reaching absorber surfaces
frac_reaching_absorber = direct_hit_fraction + mirror_redirect_fraction * mirror_redirect_efficiency

# Solar power entering cluster at peak
solar_into_cluster_W = DNI_peak * effective_capture_m2
power_on_absorbers_W = solar_into_cluster_W * frac_reaching_absorber

# Surface absorptance (SiC + carbon foam)
alpha = 0.97
power_absorbed_W = power_on_absorbers_W * alpha

# Concentration ratio (how concentrated is the light on absorber surfaces?)
concentration = power_on_absorbers_W / (total_abs_surface * DNI_peak)
# This is the "effective suns" on the absorber

# Thermal losses
T_surface_C = 500  # Lower temp because lower concentration
T_surface_K = T_surface_C + 273.15
emittance = 0.15

q_rad = emittance * sigma * (T_surface_K**4 - T_amb_K**4)
q_conv = 15  # W/m² some shielding from tube cluster
q_total = q_rad + q_conv

thermal_loss_W = q_total * total_abs_surface
thermal_retention = max(0.1, 1 - thermal_loss_W / max(1, power_absorbed_W))

# Power block
carnot = 1 - T_amb_K / T_surface_K
pb_eff = 0.38  # Lower temp → lower efficiency
parasitic = 0.04  # Very low — no tracking motors, no pumps for HTF circulation (thermosiphon)

# System efficiency (relative to light ENTERING the cluster footprint)
sys_eff = frac_reaching_absorber * alpha * thermal_retention * pb_eff * (1 - parasitic)

# But the GCR is now effectively 1.0 — the cluster IS the plant!
# Actually: GCR = (projected capture area) / (cluster footprint)
# But we need to account for shading between clusters
# If we tile clusters, they shade each other. Need spacing.
# Spacing needed: ~2× cluster diameter for no shading at reasonable sun angles
cluster_spacing = cluster_diameter * 2.5  # 40m between centers
effective_land_per_cluster = cluster_spacing ** 2  # square grid

gcr_effective = effective_capture_m2 / effective_land_per_cluster

# Energy per ft² of land
per_ft2_A = (DNI_annual * gap_fraction * sys_eff * effective_capture_m2 / effective_land_per_cluster) / m2_to_ft2
# Wait, let me recalculate more carefully
# Annual solar hitting 1m² of land = DNI_annual = 2000 kWh
# Of that, cluster captures: gap_fraction of projected area
# But projected area / land area = cluster_diameter * tube_h / cluster_spacing²
# This doesn't work cleanly because the capture is 3D

# Better approach: total annual energy from one cluster ÷ land per cluster
annual_energy_one_cluster_kWh = (DNI_annual * effective_capture_m2 * 
                                  frac_reaching_absorber * alpha * 
                                  thermal_retention * pb_eff * (1 - parasitic))
per_m2_land = annual_energy_one_cluster_kWh / effective_land_per_cluster
per_ft2_A = per_m2_land / m2_to_ft2

print(f"  Cluster: {n_total} tubes ({n_absorber} absorber + {n_mirror} mirror)")
print(f"  Cluster diameter: {cluster_diameter}m, height: {tube_h}m")
print(f"  Projected capture: {cluster_diameter}m × {tube_h}m = {projected_capture_m2:.0f} m²")
print(f"  Effective capture (gaps): {effective_capture_m2:.0f} m²")
print(f"  Light reaching absorbers: {frac_reaching_absorber*100:.1f}%")
print(f"    (direct: {direct_hit_fraction*100:.0f}%, mirror redirect: {mirror_redirect_fraction*mirror_redirect_efficiency*100:.1f}%)")
print(f"  Effective concentration: {concentration:.2f} suns")
print(f"  Thermal retention: {thermal_retention*100:.1f}%")
print(f"  Surface temp: {T_surface_C}°C")
print(f"  Power block: {pb_eff*100:.0f}%")
print(f"  System eff (light in → electric out): {sys_eff*100:.2f}%")
print(f"  Cluster spacing: {cluster_spacing}m → land/cluster: {effective_land_per_cluster:.0f} m²")
print(f"  Annual from one cluster: {annual_energy_one_cluster_kWh:.0f} kWh_e")
print(f"  Per ft² of land: {per_ft2_A:.2f} kWh_e/yr")
print(f"  vs CSP: {per_ft2_A/csp_per_ft2:.2f}×")

# =============================================================================
# CONFIGURATION B: Half-mirror, half-absorber tubes (Janus tubes)
# =============================================================================
print(f"\n{'='*80}")
print("CONFIG B: Janus tubes (mirror one side, absorber the other)")
print("="*80)
print("""
  Each tube: sun-facing half is a parabolic trough reflector
  Back half is the absorber
  Mirror focuses onto the NEXT tube's absorber
  Like nested parabolic troughs, but vertical
""")

n_tubes_B = 8
tube_h_B = 50
tube_d_B = 2.5  # Larger — need room for parabolic shape

# Each tube acts as both mirror and absorber
# Sun-facing side: parabolic strip, focuses light onto neighbor
# Back side: absorber receiving focused light from neighbor

# Effective aperture per tube: tube_diameter × tube_height (projected)
aperture_per_tube = tube_d_B * tube_h_B  # 125 m²
# But a parabolic trough on a 2.5m diameter tube has limited concentration
# Concentration ratio of a half-cylinder → CPC: about 1.5-3× at best
# (Compound parabolic concentrator theory)
concentration_B = 2.5  # conservative for this geometry

# Now: tubes arranged in a row (or slight arc) facing the sun
# Problem: THEY DON'T TRACK
# At solar noon with tubes facing south: great
# At 9am/3pm: cos(45°) = 0.707 loss, plus shadows
# Average effective capture over the day: ~60% of peak

daily_avg_factor = 0.60  # Average over day relative to peak capacity

# Cluster footprint: 8 tubes in a row/arc
row_length = n_tubes_B * tube_d_B * 1.5  # spacing
row_depth = tube_d_B * 3  # need room for light path between rows
cluster_footprint_B = row_length * row_depth

# If we do multiple rows: need spacing for no shading
# At 50m height, sun at 30° altitude: shadow = 50/tan(30°) = 87m
# That's a LOT of wasted space between rows
shadow_spacing = tube_h_B / math.tan(math.radians(35))  # 35° avg sun elevation
row_spacing_B = shadow_spacing * 0.6  # Accept some morning/evening shading
total_land_per_row_B = row_length * (row_depth + row_spacing_B)

# Optical chain for Janus tubes
mirror_reflect_B = 0.92  # Polished aluminum parabolic strip
intercept_factor_B = 0.85  # Some light misses the focus due to imperfect parabola
absorber_alpha_B = 0.96

optical_B = mirror_reflect_B * intercept_factor_B * absorber_alpha_B * daily_avg_factor

# Thermal
absorber_area_per_tube = math.pi * tube_d_B * tube_h_B * 0.5  # half is absorber
total_absorber_B = n_tubes_B * absorber_area_per_tube
flux_on_absorber_B = (DNI_peak * aperture_per_tube * mirror_reflect_B * intercept_factor_B) / absorber_area_per_tube
concentration_actual_B = flux_on_absorber_B / DNI_peak

T_B = 450  # °C — lower concentration = lower achievable temp
T_B_K = T_B + 273.15
q_rad_B = 0.15 * sigma * (T_B_K**4 - T_amb_K**4)
q_total_B = q_rad_B + 15
thermal_loss_total_B = q_total_B * total_absorber_B
thermal_input_B = DNI_peak * n_tubes_B * aperture_per_tube * mirror_reflect_B * intercept_factor_B * absorber_alpha_B
thermal_retention_B = max(0.1, 1 - thermal_loss_total_B / max(1, thermal_input_B))

pb_B = 0.36  # Rankine or ORC at 450°C
parasitic_B = 0.04

sys_eff_B = optical_B * thermal_retention_B * pb_B * (1 - parasitic_B)

annual_per_cluster_B = DNI_annual * n_tubes_B * aperture_per_tube * sys_eff_B / 1  # kWh from this config
per_m2_land_B = annual_per_cluster_B / total_land_per_row_B
per_ft2_B = per_m2_land_B / m2_to_ft2

print(f"  {n_tubes_B} Janus tubes, {tube_d_B}m dia × {tube_h_B}m tall")
print(f"  Aperture per tube: {aperture_per_tube:.0f} m²")
print(f"  Effective concentration: {concentration_actual_B:.2f}×")
print(f"  Daily average factor (no tracking): {daily_avg_factor*100:.0f}%")
print(f"  Shadow spacing between rows: {row_spacing_B:.0f}m (at 35° avg elevation)")
print(f"  Optical efficiency: {optical_B*100:.2f}%")
print(f"  Thermal retention: {thermal_retention_B*100:.2f}%")
print(f"  Surface temp: {T_B}°C")
print(f"  System efficiency: {sys_eff_B*100:.2f}%")
print(f"  Land per row: {total_land_per_row_B:.0f} m²")
print(f"  Per ft² of land: {per_ft2_B:.2f} kWh_e/yr")
print(f"  vs CSP: {per_ft2_B/csp_per_ft2:.2f}×")

# =============================================================================
# CONFIGURATION C: Vertical CPC troughs between absorber tubes
# =============================================================================
print(f"\n{'='*80}")
print("CONFIG C: Vertical CPC troughs between absorber tubes")
print("="*80)
print("""
  Absorber tubes connected by vertical compound parabolic concentrators
  CPCs are non-imaging — accept light from wide angles without tracking
  The CPC surfaces ARE the mirror structure between tubes
  Light enters from any direction within acceptance angle → funnels to absorber
""")

# CPC (Compound Parabolic Concentrator) properties:
# Acceptance half-angle θ determines concentration ratio
# C_max = 1/sin(θ) for 2D CPC
# For θ=35° (accepts ±35° from normal): C = 1/sin(35°) = 1.74×
# For θ=25°: C = 1/sin(25°) = 2.37×
# For θ=45°: C = 1/sin(45°) = 1.41×

# Use θ=30°: accepts ±30° (covers ~6 hours of good sun without tracking)
theta_accept = 30  # degrees
C_cpc = 1 / math.sin(math.radians(theta_accept))

n_tubes_C = 6
tube_d_C = 1.5  # m absorber tube diameter
tube_h_C = 50

# CPC aperture between tubes
cpc_width = tube_d_C * C_cpc  # aperture width per CPC unit
n_cpc_panels = n_tubes_C  # one CPC between each pair in the ring

# Total capture aperture = CPC apertures × height
# In a circular arrangement: imagine 6 tubes in a hex, with CPC panels
# filling the gaps between them, funneling light inward onto tube surfaces

# Total CPC aperture (one side of cluster): 
# Cluster presents ~6 CPC panels to the sun at any time (half the hex faces sun)
panels_facing_sun = n_cpc_panels / 2  # 3 panels face sun at any time
total_aperture_m2 = panels_facing_sun * cpc_width * tube_h_C

# CPC optical efficiency
cpc_reflectivity = 0.93  # Silvered CPC panels (1-2 bounces)
cpc_intercept = 0.90  # Some edge rays miss
absorber_alpha_C = 0.96

# Hours of useful collection: ±30° acceptance → ~5-6 peak hours
# vs flat panel gets ~6-8, vs tracking gets 8-10
# Express as daily collection factor relative to tracking:
daily_factor_C = 0.55  # CPC collects ~55% of what a tracking system would

optical_C = cpc_reflectivity * cpc_intercept * absorber_alpha_C * daily_factor_C

# Cluster footprint
cluster_outer_d_C = (tube_d_C + cpc_width) * 2 + tube_d_C  # rough hex diameter
cluster_footprint_C = math.pi * (cluster_outer_d_C/2)**2

# Between-cluster spacing (shadow)
shadow_C = tube_h_C / math.tan(math.radians(35))
spacing_C = shadow_C * 0.5  # Accept more shading — clusters are narrow
land_per_cluster_C = (cluster_outer_d_C + spacing_C) ** 2  # square packing

# Thermal
absorber_area_C = n_tubes_C * math.pi * tube_d_C * tube_h_C
solar_on_absorber_C = DNI_peak * total_aperture_m2 * cpc_reflectivity * cpc_intercept
flux_C = solar_on_absorber_C / absorber_area_C
conc_C = flux_C / DNI_peak

T_C = 400  # °C — low concentration means lower temp
T_C_K = T_C + 273.15
q_rad_C = 0.15 * sigma * (T_C_K**4 - T_amb_K**4)
q_total_C = q_rad_C + 15
thermal_loss_C = q_total_C * absorber_area_C
thermal_retention_C = max(0.1, 1 - thermal_loss_C / max(1, solar_on_absorber_C * absorber_alpha_C))

pb_C = 0.32  # ORC or small Rankine at 400°C
parasitic_C = 0.03  # Very low — no tracking, thermosiphon

sys_eff_C = optical_C * thermal_retention_C * pb_C * (1 - parasitic_C)

annual_cluster_C = DNI_annual * total_aperture_m2 * optical_C * thermal_retention_C * pb_C * (1 - parasitic_C) / daily_factor_C * daily_factor_C
# Simpler: energy from one cluster
annual_C = DNI_annual * total_aperture_m2 * cpc_reflectivity * cpc_intercept * absorber_alpha_C * daily_factor_C * thermal_retention_C * pb_C * (1 - parasitic_C)
per_m2_land_C = annual_C / land_per_cluster_C
per_ft2_C = per_m2_land_C / m2_to_ft2

print(f"  {n_tubes_C} absorber tubes + {n_cpc_panels} CPC panels")
print(f"  CPC acceptance angle: ±{theta_accept}° → C_max = {C_cpc:.2f}×")
print(f"  CPC aperture width: {cpc_width:.2f}m per panel")
print(f"  Total capture aperture: {total_aperture_m2:.0f} m² (sun-facing half)")
print(f"  Effective concentration on absorbers: {conc_C:.2f}×")
print(f"  Daily factor (no tracking, CPC acceptance): {daily_factor_C*100:.0f}%")
print(f"  Optical efficiency: {optical_C*100:.2f}%")
print(f"  Thermal retention: {thermal_retention_C*100:.2f}%")
print(f"  Surface temp: {T_C}°C")
print(f"  System efficiency: {sys_eff_C*100:.2f}%")
print(f"  Cluster footprint: {cluster_footprint_C:.0f} m²")
print(f"  Land per cluster (with shadow spacing): {land_per_cluster_C:.0f} m²")
print(f"  Per ft² of land: {per_ft2_C:.2f} kWh_e/yr")
print(f"  vs CSP: {per_ft2_C/csp_per_ft2:.2f}×")

# =============================================================================
# THE REAL PROBLEM: SHADOWS
# =============================================================================
print(f"\n{'='*80}")
print("THE SHADOW PROBLEM — Why going tall without tracking is expensive")
print("="*80)

print(f"""
Every tall vertical structure casts a shadow proportional to its height.

  Shadow length = height / tan(sun_elevation)

  At 50m tall:
    Sun at 60° (noon, good site):     shadow = {50/math.tan(math.radians(60)):.0f}m
    Sun at 45° (mid-morning):         shadow = {50/math.tan(math.radians(45)):.0f}m  
    Sun at 30° (early morning):       shadow = {50/math.tan(math.radians(30)):.0f}m
    Sun at 20° (near sunrise/set):    shadow = {50/math.tan(math.radians(20)):.0f}m

For clusters NOT to shade each other:
  Minimum spacing ≈ {50/math.tan(math.radians(35)):.0f}m (at 35° average elevation)

This means a 50m-tall cluster needs a ~70m exclusion zone around it.
That exclusion zone is EMPTY LAND producing nothing.

The v2 architecture dodges this because the heliostats are LOW to the ground
(only ~3m tall) and they fill that shadow-zone land with useful mirror area.
The tower casts a shadow, but it's narrow (8m wide), not 50m wide.
""")

# =============================================================================
# HYBRID: INTEGRATED MIRRORS + SMALL TRACKING MIRRORS
# =============================================================================
print(f"{'='*80}")
print("CONFIG D (HYBRID): CPC tubes + small tracking mirrors in shadow zone")
print("="*80)
print("""
  Combine the best of both:
  - CPC panels between tubes capture wide-angle light (no tracking needed)
  - Small, cheap heliostats fill the shadow-exclusion zone
  - Heliostats are LOW (2m) so they don't shade each other much
  - They aim at the upper portions of the tubes (above the CPCs)
  
  Result: CPC captures nearby diffuse + direct, heliostats add concentrated
""")

# CPC component (same as Config C but smaller role)
cpc_annual_kWh = annual_C  # from the CPC panels

# Heliostat component filling the exclusion zone
helio_zone_inner_r = cluster_outer_d_C / 2 + 5  # 5m gap from cluster
helio_zone_outer_r = 60  # 60m radius (within shadow zone)
helio_zone_area = math.pi * (helio_zone_outer_r**2 - helio_zone_inner_r**2)

# Small heliostats in this zone
helio_gcr_D = 0.40  # Can pack tight — they're low and close
helio_mirror_D = helio_zone_area * helio_gcr_D
helio_each_D = 6  # m², small
n_helio_D = int(helio_mirror_D / helio_each_D)

# Heliostat optical chain (aiming at tubes at ~40m avg distance)
h_cosine = 0.88  # Short range, tall target
h_reflect = 0.935
h_atmo = 0.99  # Very close
h_spillage = 0.97
h_blocking = 0.96
h_absorptance = 0.96  # Tube surface

h_optical = h_cosine * h_reflect * h_atmo * h_spillage * h_blocking * h_absorptance

# Thermal (heliostats deliver concentrated light → higher temp possible)
# Focus adds ~5-10× concentration on top portion of tubes
h_flux = DNI_peak * helio_mirror_D * h_optical / (n_tubes_C * math.pi * tube_d_C * tube_h_C * 0.3)
# Upper 30% of tubes receive heliostat light
h_conc = h_flux / DNI_peak

T_D_helio = 550  # °C on upper tube sections
T_D_K = T_D_helio + 273.15
q_rad_D = 0.15 * sigma * (T_D_K**4 - T_amb_K**4)
upper_absorber_area = n_tubes_C * math.pi * tube_d_C * tube_h_C * 0.3
thermal_loss_D = (q_rad_D + 15) * upper_absorber_area
h_thermal_input = DNI_peak * helio_mirror_D * h_optical
h_thermal_retention = max(0.3, 1 - thermal_loss_D / max(1, h_thermal_input))

pb_D = 0.40  # Better turbine at higher temp
parasitic_D = 0.05  # Some tracking motors

h_annual = DNI_annual * helio_mirror_D * h_optical * h_thermal_retention * pb_D * (1 - parasitic_D)

# TOTAL from hybrid
total_annual_D = cpc_annual_kWh + h_annual
total_land_D = math.pi * helio_zone_outer_r**2  # Total circle
per_m2_land_D = total_annual_D / total_land_D
per_ft2_D = per_m2_land_D / m2_to_ft2

print(f"  CPC tubes: {annual_C:.0f} kWh_e/yr")
print(f"  Heliostat ring: {n_helio_D} × {helio_each_D}m² = {helio_mirror_D:.0f} m²")
print(f"  Heliostat optical: {h_optical*100:.2f}%")
print(f"  Heliostat concentration: {h_conc:.1f}× on upper tubes")
print(f"  Heliostat thermal retention: {h_thermal_retention*100:.1f}%")
print(f"  Heliostat annual: {h_annual:.0f} kWh_e/yr")
print(f"  TOTAL annual: {total_annual_D:.0f} kWh_e/yr")
print(f"  Total land (60m radius): {total_land_D:.0f} m² ({total_land_D/4047:.2f} acres)")
print(f"  Per ft² of land: {per_ft2_D:.2f} kWh_e/yr")
print(f"  vs CSP: {per_ft2_D/csp_per_ft2:.2f}×")
print(f"  vs VCST v2: {per_ft2_D/vcst_v2_per_ft2:.2f}×")

# =============================================================================
# GRAND COMPARISON
# =============================================================================
print(f"\n{'='*80}")
print("GRAND COMPARISON: All configs vs baselines")
print("="*80)

configs = [
    ("Tower CSP (baseline)", csp_per_ft2, "Reference"),
    ("VCST v2 (heliostats→tubes)", vcst_v2_per_ft2, "Previous best"),
    ("v3-A: Alternating mirror/absorber", per_ft2_A, "No tracking"),
    ("v3-B: Janus half-mirror tubes", per_ft2_B, "No tracking"),
    ("v3-C: CPC vertical troughs", per_ft2_C, "No tracking"),
    ("v3-D: CPC + mini heliostats", per_ft2_D, "Hybrid"),
]

print(f"\n  {'Configuration':<36s} {'kWh_e/ft²/yr':>14s} {'vs CSP':>8s} {'vs v2':>8s}")
print(f"  {'─'*36} {'─'*14} {'─'*8} {'─'*8}")
for name, val, note in configs:
    vs_csp = val / csp_per_ft2
    vs_v2 = val / vcst_v2_per_ft2
    flag = " ★" if val > csp_per_ft2 else ""
    print(f"  {name:<36s} {val:13.2f} {vs_csp:7.2f}× {vs_v2:7.2f}×{flag}")

# =============================================================================
# HONEST CONCLUSION
# =============================================================================
print(f"\n{'='*80}")
print("HONEST CONCLUSION")
print("="*80)
print(f"""
Integrating mirrors into the tubes eliminates the heliostat field BUT introduces
two problems that are hard to solve:

1. NO TRACKING = BIG DAILY LOSSES
   A fixed vertical structure captures ~55-60% of what a tracking system gets.
   Heliostats rotate to face the sun all day. Fixed CPCs only work within their
   acceptance angle. This alone costs you 40-45% of your daily energy.

2. TALL SHADOWS = WASTED LAND
   A 50m tube cluster casts a 70m+ shadow. To avoid shading the next cluster,
   you need that spacing. The shadow-zone land produces nothing.
   This kills the land-use advantage that was the whole point.

3. LOW CONCENTRATION = LOW TEMPERATURE = LOW CARNOT = LOW EFFICIENCY
   Without tracking mirrors aiming at a focal point, you get 1.5-3× concentration
   vs CSP's 600-1000×. Lower concentration → lower peak temp → worse Carnot.

THE WINNING MOVE is Config D (hybrid): keep the CPC panels for passive capture,
but fill the shadow-exclusion zone with small tracking heliostats that would
otherwise be wasted space. This gives you:
  - CPC base load (passive, no maintenance)
  - Heliostat boost (tracked, higher concentration)
  - Shadow zone used productively
  
But even Config D ({per_ft2_D:.2f} kWh/ft²) only reaches {per_ft2_D/csp_per_ft2:.2f}× CSP
and {per_ft2_D/vcst_v2_per_ft2:.2f}× of your v2 design.

The v2 architecture (separate heliostats → vertical tubes) remains the best
configuration because heliostats are cheap, trackable, and fill land that
integrated-mirror designs waste as shadow zones.

The insight: mirrors and absorbers want to be at DIFFERENT heights.
Mirrors belong on the ground (cheap, replaceable, trackable).
Absorbers belong high up (hot, vertical, thermosiphon-friendly).
Combining them into one structure forces both into the same geometry,
and neither works optimally.
""")
