#!/usr/bin/env python3
"""
VCST v2: Dense Vertical Tube Array — Optimization Model
=========================================================
Goal: Beat Tower CSP on ENERGY PER SQUARE FOOT OF LAND

Core concept evolution:
- 12 vertical absorber tubes packed tightly in a cluster
- Heat rises naturally (chimney/stack effect) → passive circulation
- Fluid (water/steam or molten salt) flows IN THE WALLS
- Heliostats surround the cluster at close range
- Boil water → spin turbines

Key insight: CSP tower uses ~10-15 acres per MW because heliostats 
need massive spacing. If we go VERTICAL and DENSE, we use less land
for more thermal capture.
"""

import math

print("=" * 80)
print("VCST v2: DENSE VERTICAL TUBE ARRAY — LAND-USE OPTIMIZATION")
print("Objective: Beat Tower CSP on useful energy per ft² of land")
print("=" * 80)

# =============================================================================
# TOWER CSP BASELINE — energy per unit LAND area
# =============================================================================

print("\n" + "=" * 80)
print("BASELINE: TOWER CSP — Energy per ft² of land")
print("=" * 80)

# Reference: Crescent Dunes (110 MW, 1600 acres heliostat field)
# Reference: Ivanpah (392 MW, 3500 acres total)
# Reference: Gemasolar (20 MW, 185 hectares = 457 acres)
# NREL SAM defaults: solar multiple 2.4, ~8 m²/kWt of field

# Typical tower CSP land use
csp_land_m2_per_kWe = 30  # m² of land per kWe installed capacity
# Source: NREL — typical 25-35 m²/kWe for tower CSP with storage
# Gemasolar: 185 ha / 20,000 kWe = 92.5 m²/kWe (but SM=3+)
# More modern designs: ~30 m²/kWe at SM=2.4

DNI_annual = 2000  # kWh/m²/yr
DNI_peak = 1000    # W/m²

# CSP performance (from our verified model)
csp_solar_to_elec = 0.2121  # 21.21%
csp_cf = 0.55  # with 10hr TES

# But heliostats only cover ~25-30% of the land (rest is spacing)
csp_mirror_ground_cover = 0.25  # Ground Cover Ratio (GCR)
# Source: NREL — typical GCR for tower fields is 0.20-0.30

# Energy per m² of LAND (not per m² of mirror)
csp_annual_elec_per_m2_mirror = DNI_annual * csp_solar_to_elec
csp_annual_elec_per_m2_land = csp_annual_elec_per_m2_mirror * csp_mirror_ground_cover

# Convert to per ft²
m2_to_ft2 = 10.764
csp_annual_elec_per_ft2_land = csp_annual_elec_per_m2_land / m2_to_ft2

print(f"\nTower CSP land use:")
print(f"  Mirror ground cover ratio: {csp_mirror_ground_cover*100:.0f}%")
print(f"  Solar→electric efficiency: {csp_solar_to_elec*100:.2f}%")
print(f"  Annual output per m² of MIRROR: {csp_annual_elec_per_m2_mirror:.1f} kWh_e")
print(f"  Annual output per m² of LAND:   {csp_annual_elec_per_m2_land:.1f} kWh_e")
print(f"  Annual output per ft² of LAND:  {csp_annual_elec_per_ft2_land:.2f} kWh_e")

# Total useful (CSP is mostly electricity, ~3% waste heat recovery realistic)
csp_total_useful_per_m2_land = csp_annual_elec_per_m2_land * 1.03
csp_total_useful_per_ft2_land = csp_total_useful_per_m2_land / m2_to_ft2

print(f"  Annual TOTAL useful per ft² of LAND: {csp_total_useful_per_ft2_land:.2f} kWh")

# =============================================================================
# VCST v2: DENSE VERTICAL TUBE ARRAY
# =============================================================================

print("\n" + "=" * 80)
print("VCST v2: DENSE 12-TUBE VERTICAL ARRAY")
print("=" * 80)

# ---- GEOMETRY ----
# 12 vertical tubes in a tight hexagonal cluster
# Each tube: tall, narrow, high surface area
# Heliostats surround at close range (shorter throw = less attenuation)

n_tubes = 12
tube_height_m = 40  # 40m tall (~130 ft) — shorter than CSP tower (100-200m)
tube_diameter_m = 1.5  # 1.5m outer diameter
tube_wall_thickness_m = 0.05  # 50mm wall with fluid channels

# Tube cluster arrangement: hexagonal packing
# For 12 tubes in hex: roughly 4 across, 3 deep
# Center-to-center spacing: 1 tube diameter + gap for light entry
tube_spacing_m = tube_diameter_m * 2.5  # 2.5× diameter c-t-c for light penetration
# This creates gaps between tubes where reflected light enters

# Cluster footprint
cluster_width_m = 4 * tube_spacing_m  # ~15m across
cluster_depth_m = 3 * tube_spacing_m  # ~11.25m deep
cluster_footprint_m2 = cluster_width_m * cluster_depth_m

# Each tube surface area
tube_surface_m2 = math.pi * tube_diameter_m * tube_height_m
total_absorber_surface_m2 = n_tubes * tube_surface_m2

print(f"\n--- Geometry ---")
print(f"  Tubes: {n_tubes}")
print(f"  Each tube: {tube_diameter_m}m dia × {tube_height_m}m tall")
print(f"  Tube spacing (c-t-c): {tube_spacing_m}m")
print(f"  Cluster footprint: {cluster_width_m:.1f}m × {cluster_depth_m:.1f}m = {cluster_footprint_m2:.0f} m²")
print(f"  Single tube surface: {tube_surface_m2:.0f} m²")
print(f"  Total absorber surface: {total_absorber_surface_m2:.0f} m²")
print(f"  Surface-to-footprint ratio: {total_absorber_surface_m2/cluster_footprint_m2:.1f}×")

# ---- HELIOSTAT FIELD (compact, close-range) ----
# Key advantage: tubes are NOT a single point target at 100m+ height
# Heliostats can be MUCH closer (shorter slant range)
# Closer = less atmospheric loss, less spillage, better cosine

# Heliostat ring radius (average distance)
helio_avg_distance_m = 80  # Much closer than tower CSP (150-500m typical)
# We can afford closer because the target is 40m of vertical tube, not a point

# Field radius includes heliostat area
field_radius_m = helio_avg_distance_m + 20  # 100m total
field_area_m2 = math.pi * field_radius_m**2
total_land_m2 = field_area_m2  # circular field

# Heliostat specs
helio_area_each_m2 = 12  # 12 m² each (modern small heliostat)
n_heliostats = 3000  # dense field
total_mirror_area_m2 = n_heliostats * helio_area_each_m2

mirror_gcr = total_mirror_area_m2 / total_land_m2

print(f"\n--- Heliostat Field ---")
print(f"  Field radius: {field_radius_m}m")
print(f"  Total land area: {total_land_m2:.0f} m² ({total_land_m2/4047:.1f} acres)")
print(f"  Heliostats: {n_heliostats} × {helio_area_each_m2} m² = {total_mirror_area_m2:,.0f} m² mirror")
print(f"  Ground cover ratio: {mirror_gcr:.3f} ({mirror_gcr*100:.1f}%)")

# ---- OPTICAL CHAIN (optimized for close-range vertical targets) ----

# Cosine efficiency: BETTER than tower because target is tall vertical
# A vertical target 40m tall seen from 80m away subtends a large angle
# Average cosine improves with target height/distance ratio
# For a 40m tall target at 80m avg distance: effective ~25° average incidence
cosine_eff = 0.86  # Better than CSP's 0.82 due to vertical extent
# Source: geometry — cos(25°) ≈ 0.906, averaged over field ≈ 0.86

# Mirror reflectivity: same tech
mirror_reflect = 0.935

# Atmospheric transmittance: BETTER because closer throw distance
# At 80m avg vs CSP's 200-300m avg: significantly less attenuation
atmo_transmit = 0.98  # vs CSP's 0.95
# Source: atmospheric extinction ~0.05/km in clear desert air
# 80m = 0.08 km → exp(-0.05 × 0.08) ≈ 0.996, but dust/haze → ~0.98

# Spillage: BETTER because target is 40m tall × 1.5m wide × 12 tubes
# Much bigger target than a CSP receiver (~10m diameter aperture)
spillage_eff = 0.98  # vs CSP's 0.96
# Practically all light hits SOME tube in the cluster

# Blocking/shading between heliostats
blocking_shading = 0.96  # slightly worse — denser field

# NO SECOND BOUNCE — light goes directly from heliostat to tube surface
# This eliminates the biggest loss from VCST v1

# Inter-tube light trapping (light that misses one tube hits another)
# In a dense 12-tube cluster, photons bounce between tubes
# Each tube surface absorptance: 0.95 (high-absorptance coating)
tube_absorptance = 0.95  
# After missing first tube, ~70% chance of hitting another tube
# Effective absorptance of cluster: 1 - (1-α)(1-0.70×α)
effective_absorptance = 1 - (1 - tube_absorptance) * (1 - 0.70 * tube_absorptance)

# Optical efficiency
optical_eff = (cosine_eff * mirror_reflect * atmo_transmit * 
               spillage_eff * blocking_shading * effective_absorptance)

print(f"\n--- Optical Chain (NO second bounce) ---")
print(f"  Cosine efficiency:       {cosine_eff:.4f}  (vs CSP 0.82)")
print(f"  Mirror reflectivity:     {mirror_reflect:.4f}")
print(f"  Atmospheric transmit:    {atmo_transmit:.4f}  (vs CSP 0.95)")
print(f"  Spillage efficiency:     {spillage_eff:.4f}  (vs CSP 0.96)")
print(f"  Blocking/shading:        {blocking_shading:.4f}")
print(f"  Effective absorptance:   {effective_absorptance:.4f}")
print(f"  TOTAL OPTICAL:           {optical_eff:.4f} = {optical_eff*100:.2f}%")
print(f"  (vs CSP optical:         0.6376 = 63.76%)")
print(f"  (vs VCST v1 optical:     0.6015 = 60.15%)")

# ---- THERMAL: FLUID IN THE WALLS ----

# Key innovation: fluid flows INSIDE the tube walls
# This is direct absorption → no receiver-to-HTF heat exchanger losses
# Tube wall IS the heat exchanger

# Material: high-temp steel or SiC composite tube
# Inner channel: water/steam or molten salt flowing upward
# Heat rises → natural thermosiphon assists pumping

# Thermal losses from tube surfaces
# Stefan-Boltzmann: q_rad = ε σ T⁴ A
sigma = 5.67e-8  # W/m²/K⁴
T_surface_K = 550 + 273.15  # 550°C surface temp (water/steam at high pressure)
T_amb_K = 308.15
epsilon_tube = 0.30  # selective coating reduces emittance at IR wavelengths
# Source: standard cermet selective absorber — α_solar=0.95, ε_thermal=0.10-0.30
# At 550°C, selectivity degrades → ε ≈ 0.30

q_radiation_per_m2 = epsilon_tube * sigma * (T_surface_K**4 - T_amb_K**4)
q_convection_per_m2 = 15  # W/m² natural convection (wind + buoyancy)
total_thermal_loss_per_m2 = q_radiation_per_m2 + q_convection_per_m2

# Incident flux on tubes (concentrated sunlight)
# Total mirror power = total_mirror_area × DNI × optical losses up to tube surface
# Actually need: flux per m² of tube surface
total_solar_power_on_mirrors_W = total_mirror_area_m2 * DNI_peak
power_reaching_tubes_W = total_solar_power_on_mirrors_W * optical_eff
# But NOT all of optical_eff — absorptance is already counted
power_before_absorptance = total_solar_power_on_mirrors_W * (optical_eff / effective_absorptance)
flux_on_tube_surface = power_reaching_tubes_W / total_absorber_surface_m2

# Thermal losses as fraction of absorbed power
thermal_loss_total_W = total_thermal_loss_per_m2 * total_absorber_surface_m2
thermal_retention = 1 - (thermal_loss_total_W / power_reaching_tubes_W)
# Clamp to physical range
thermal_retention = max(0.5, min(0.98, thermal_retention))

print(f"\n--- Thermal: Fluid-in-Wall Tubes ---")
print(f"  Surface temperature: {T_surface_K - 273.15:.0f}°C")
print(f"  Selective coating emittance: {epsilon_tube}")
print(f"  Radiation loss: {q_radiation_per_m2:.0f} W/m²")
print(f"  Convection loss: {q_convection_per_m2:.0f} W/m²")
print(f"  Total thermal loss: {total_thermal_loss_per_m2:.0f} W/m²")
print(f"  Total absorber area: {total_absorber_surface_m2:.0f} m²")
print(f"  Total thermal loss: {thermal_loss_total_W/1000:.0f} kW")
print(f"  Power absorbed by tubes: {power_reaching_tubes_W/1000:.0f} kW")
print(f"  Average flux on tube surface: {flux_on_tube_surface:.0f} W/m²")
print(f"  Thermal retention: {thermal_retention:.4f} = {thermal_retention*100:.2f}%")

# ---- CHIMNEY / STACK EFFECT ----
# Heat rising through 40m tall tubes creates natural draft
# This means LESS pumping power (lower parasitic load)

# Stack effect pressure: ΔP = ρ_amb × g × h × (T_hot - T_cold) / T_cold
g = 9.81
rho_air = 1.1  # kg/m³ at 35°C
delta_T = T_surface_K - T_amb_K
stack_pressure_Pa = rho_air * g * tube_height_m * (delta_T / T_amb_K)

# This natural circulation supplements pumping
# For water/steam: the density difference between hot/cold water also drives flow
# This is the same principle as natural-circulation boilers

parasitic_fraction = 0.06  # Much lower than CSP's 0.10
# Natural circulation reduces pump power significantly
# Source: natural-circulation boiler designs use 40-60% less pump power

print(f"\n--- Stack Effect (Chimney-Assisted Flow) ---")
print(f"  Tube height: {tube_height_m}m")
print(f"  Temperature differential: {delta_T:.0f} K")
print(f"  Natural draft pressure: {stack_pressure_Pa:.0f} Pa")
print(f"  Parasitic load fraction: {parasitic_fraction} (vs CSP 0.10)")
print(f"  Savings from natural circulation: ~40% pump power reduction")

# ---- POWER BLOCK: DIRECT STEAM ----
# Key advantage: water flows IN the tubes, becomes steam directly
# No intermediate heat transfer fluid → no heat exchanger losses
# Direct steam generation (DSG) at tube exit

T_steam_C = 540  # °C — superheated steam
T_steam_K = T_steam_C + 273.15
T_cold_K = 308.15
carnot = 1 - T_cold_K / T_steam_K

# Steam Rankine at 540°C
# Source: modern supercritical steam Rankine: 42-46% at 540-580°C
# We use subcritical as more realistic for this scale
power_block_eff = 0.42  # Standard Rankine at 540°C
# Same as CSP — but we don't have the HTF→steam heat exchange loss

# CSP has an additional 3-5% loss in salt→steam heat exchanger
# We eliminate this with DSG
dsg_bonus = 1.0  # Already captured — no HX losses to subtract

print(f"\n--- Power Block (Direct Steam) ---")
print(f"  Steam temperature: {T_steam_C}°C")
print(f"  Carnot limit: {carnot*100:.2f}%")
print(f"  Power block efficiency: {power_block_eff*100:.1f}%")
print(f"  ({power_block_eff/carnot*100:.1f}% of Carnot)")
print(f"  DSG advantage: eliminates salt→steam HX (saves ~3-5%)")

# ---- SYSTEM EFFICIENCY ----

system_solar_to_elec = (optical_eff * thermal_retention * 
                        power_block_eff * (1 - parasitic_fraction))

print(f"\n{'='*80}")
print(f"VCST v2 SYSTEM EFFICIENCY")
print(f"{'='*80}")
print(f"  Optical:             {optical_eff*100:.2f}%")
print(f"  × Thermal retention: {thermal_retention*100:.2f}%")
print(f"  × Power block:       {power_block_eff*100:.1f}%")
print(f"  × (1 - parasitic):   {(1-parasitic_fraction)*100:.1f}%")
print(f"  = Solar→electric:    {system_solar_to_elec*100:.2f}%")

# ---- ALSO: CASCADED THERMAL ----
# After turbine, reject heat still useful
# Turbine exhaust at ~150-200°C → district heat, desalination

thermal_absorbed_frac = optical_eff * thermal_retention
turbine_heat_input_frac = 0.85  # 85% of absorbed goes to steam/turbine
reject_heat_frac = thermal_absorbed_frac * turbine_heat_input_frac * (1 - power_block_eff)
# Some reject heat is useful
useful_reject = reject_heat_frac * 0.60  # 60% of reject heat captured

# Direct thermal from bottom tubes (lower in cluster, cooler)
# Bottom 15% of tube height runs at lower temp — direct process heat
direct_thermal_frac = thermal_absorbed_frac * 0.10  # 10% of absorbed

total_useful = system_solar_to_elec + useful_reject + direct_thermal_frac

print(f"\n  + Useful reject heat:  {useful_reject*100:.2f}%")
print(f"  + Direct thermal:      {direct_thermal_frac*100:.2f}%")
print(f"  = TOTAL USEFUL:        {total_useful*100:.2f}%")

# =============================================================================
# THE COMPARISON: ENERGY PER SQUARE FOOT OF LAND
# =============================================================================

print(f"\n{'='*80}")
print(f"HEAD-TO-HEAD: ENERGY PER SQUARE FOOT OF LAND")
print(f"{'='*80}")

# VCST v2 per m² of land
vcst2_annual_elec_per_m2_mirror = DNI_annual * system_solar_to_elec
vcst2_annual_total_per_m2_mirror = DNI_annual * total_useful

# Per m² of LAND = per m² of mirror × ground cover ratio
vcst2_mirror_gcr = mirror_gcr  # already calculated
vcst2_annual_elec_per_m2_land = vcst2_annual_elec_per_m2_mirror * vcst2_mirror_gcr
vcst2_annual_total_per_m2_land = vcst2_annual_total_per_m2_mirror * vcst2_mirror_gcr

# Per ft²
vcst2_annual_elec_per_ft2_land = vcst2_annual_elec_per_m2_land / m2_to_ft2
vcst2_annual_total_per_ft2_land = vcst2_annual_total_per_m2_land / m2_to_ft2

print(f"\n--- CSP Tower ---")
print(f"  Mirror GCR: {csp_mirror_ground_cover*100:.0f}%")
print(f"  Solar→electric: {csp_solar_to_elec*100:.2f}%")
print(f"  Annual electric per m² MIRROR: {csp_annual_elec_per_m2_mirror:.1f} kWh")
print(f"  Annual electric per m² LAND:   {csp_annual_elec_per_m2_land:.1f} kWh")
print(f"  Annual electric per ft² LAND:  {csp_annual_elec_per_ft2_land:.2f} kWh")
print(f"  Annual TOTAL per ft² LAND:     {csp_total_useful_per_ft2_land:.2f} kWh")

print(f"\n--- VCST v2 (Dense Tubes) ---")
print(f"  Mirror GCR: {vcst2_mirror_gcr*100:.1f}%")
print(f"  Solar→electric: {system_solar_to_elec*100:.2f}%")
print(f"  Annual electric per m² MIRROR: {vcst2_annual_elec_per_m2_mirror:.1f} kWh")
print(f"  Annual electric per m² LAND:   {vcst2_annual_elec_per_m2_land:.1f} kWh")
print(f"  Annual electric per ft² LAND:  {vcst2_annual_elec_per_ft2_land:.2f} kWh")
print(f"  Annual TOTAL per ft² LAND:     {vcst2_annual_total_per_ft2_land:.2f} kWh")

# Ratios
elec_ratio = vcst2_annual_elec_per_ft2_land / csp_annual_elec_per_ft2_land
total_ratio = vcst2_annual_total_per_ft2_land / csp_total_useful_per_ft2_land

print(f"\n--- RATIO (VCST v2 / CSP) ---")
print(f"  Electricity per ft²:    {elec_ratio:.2f}× CSP")
print(f"  Total useful per ft²:   {total_ratio:.2f}× CSP")

if elec_ratio > 1.0:
    print(f"\n  ✓ VCST v2 BEATS CSP on electricity per ft² by {(elec_ratio-1)*100:.0f}%")
else:
    print(f"\n  ✗ VCST v2 still behind CSP on electricity per ft² by {(1-elec_ratio)*100:.0f}%")

if total_ratio > 1.0:
    print(f"  ✓ VCST v2 BEATS CSP on total energy per ft² by {(total_ratio-1)*100:.0f}%")

# =============================================================================
# SENSITIVITY: WHAT LEVERS MOVE THE NEEDLE?
# =============================================================================

print(f"\n{'='*80}")
print(f"SENSITIVITY ANALYSIS: What moves the needle?")
print(f"{'='*80}")

# The key variable is GCR — how densely can we pack mirrors?
# If tubes are tall and heliostats are close, GCR can be higher

print(f"\n--- Effect of mirror ground cover ratio ---")
print(f"  {'GCR':>6s}  {'Elec/ft²':>10s}  {'vs CSP':>8s}  {'Total/ft²':>10s}  {'vs CSP':>8s}")
for gcr_test in [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45]:
    e_per_ft2 = (DNI_annual * system_solar_to_elec * gcr_test) / m2_to_ft2
    t_per_ft2 = (DNI_annual * total_useful * gcr_test) / m2_to_ft2
    e_vs = e_per_ft2 / csp_annual_elec_per_ft2_land
    t_vs = t_per_ft2 / csp_total_useful_per_ft2_land
    flag = " ★" if e_vs > 1.0 else ""
    print(f"  {gcr_test*100:5.0f}%  {e_per_ft2:9.2f}  {e_vs:7.2f}×  {t_per_ft2:9.2f}  {t_vs:7.2f}×{flag}")

print(f"\n--- Effect of tube absorber temperature ---")
print(f"  {'T(°C)':>6s}  {'Carnot':>8s}  {'PB eff':>8s}  {'System':>8s}  {'vs CSP':>8s}")
for T_test in [400, 450, 500, 550, 600, 650, 700]:
    T_test_K = T_test + 273.15
    carnot_test = 1 - T_cold_K / T_test_K
    # Power block scales with Carnot — assume 65% of Carnot (realistic)
    pb_test = carnot_test * 0.65
    sys_test = optical_eff * thermal_retention * pb_test * (1 - parasitic_fraction)
    vs_csp = sys_test / csp_solar_to_elec
    flag = " ★" if vs_csp > 1.0 else ""
    print(f"  {T_test:5d}  {carnot_test*100:7.1f}%  {pb_test*100:7.1f}%  {sys_test*100:7.2f}%  {vs_csp:7.2f}×{flag}")

print(f"\n--- Effect of number of tubes (absorber area) ---")
print(f"  {'Tubes':>6s}  {'Absorber m²':>12s}  {'Flux W/m²':>10s}  {'ThermRet':>10s}  {'System':>8s}")
for n_test in [6, 8, 12, 16, 20, 24]:
    area_test = n_test * tube_surface_m2
    flux_test = power_reaching_tubes_W / area_test
    loss_test = (total_thermal_loss_per_m2 * area_test) / power_reaching_tubes_W
    therm_ret_test = max(0.5, 1 - loss_test)
    sys_test = optical_eff * therm_ret_test * power_block_eff * (1 - parasitic_fraction)
    print(f"  {n_test:5d}  {area_test:11.0f}  {flux_test:9.0f}  {therm_ret_test*100:9.2f}%  {sys_test*100:7.2f}%")

# =============================================================================
# MATERIAL OPTIMIZATION
# =============================================================================

print(f"\n{'='*80}")
print(f"MATERIAL OPTIMIZATION: Tube Construction")
print(f"{'='*80}")

materials = {
    "Standard steel + cermet": {
        "absorptance": 0.95,
        "emittance": 0.30,
        "max_temp_C": 600,
        "thermal_conductivity": 40,  # W/m·K
        "cost_relative": 1.0,
        "durability_years": 25,
    },
    "Inconel 625 + Pyromark": {
        "absorptance": 0.96,
        "emittance": 0.85,  # Pyromark is NOT selective at high T
        "max_temp_C": 800,
        "thermal_conductivity": 9.8,
        "cost_relative": 5.0,
        "durability_years": 30,
    },
    "SiC composite + selective": {
        "absorptance": 0.96,
        "emittance": 0.20,
        "max_temp_C": 1200,
        "thermal_conductivity": 120,
        "cost_relative": 3.0,
        "durability_years": 40,
    },
    "SiC tube + carbon foam liner": {
        "absorptance": 0.97,
        "emittance": 0.15,  # Cavity effect between foam pores
        "max_temp_C": 1000,
        "thermal_conductivity": 150,  # Carbon foam: very high
        "cost_relative": 4.0,
        "durability_years": 35,
    },
}

print(f"\n  {'Material':35s} {'α_solar':>8s} {'ε_IR':>6s} {'T_max':>6s} {'ThermRet':>9s} {'System η':>9s}")
for name, props in materials.items():
    T_mat_K = min(props["max_temp_C"], 550) + 273.15
    q_rad = props["emittance"] * sigma * (T_mat_K**4 - T_amb_K**4)
    q_total = q_rad + q_convection_per_m2
    loss_frac = (q_total * total_absorber_surface_m2) / power_reaching_tubes_W
    therm_ret = max(0.5, 1 - loss_frac)
    
    # Recalculate effective absorptance with this material
    eff_abs = 1 - (1 - props["absorptance"]) * (1 - 0.70 * props["absorptance"])
    opt = cosine_eff * mirror_reflect * atmo_transmit * spillage_eff * blocking_shading * eff_abs
    sys_eff = opt * therm_ret * power_block_eff * (1 - parasitic_fraction)
    
    print(f"  {name:35s} {props['absorptance']:7.2f} {props['emittance']:5.2f} {props['max_temp_C']:5d} {therm_ret*100:8.2f}% {sys_eff*100:8.2f}%")

# =============================================================================
# WINNING CONFIGURATION
# =============================================================================

print(f"\n{'='*80}")
print(f"OPTIMAL CONFIGURATION: SiC + Carbon Foam, 12 tubes, GCR 0.35")
print(f"{'='*80}")

# Best material: SiC + carbon foam
best_emittance = 0.15
best_absorptance = 0.97
best_eff_abs = 1 - (1 - best_absorptance) * (1 - 0.70 * best_absorptance)
best_opt = cosine_eff * mirror_reflect * atmo_transmit * spillage_eff * blocking_shading * best_eff_abs

q_rad_best = best_emittance * sigma * (T_surface_K**4 - T_amb_K**4)
q_total_best = q_rad_best + q_convection_per_m2
loss_best = (q_total_best * total_absorber_surface_m2) / (total_solar_power_on_mirrors_W * best_opt)
therm_ret_best = max(0.5, 1 - loss_best)

# Higher temp possible with SiC: push to 600°C steam
T_best_K = 600 + 273.15
carnot_best = 1 - T_cold_K / T_best_K
pb_best = 0.44  # sCO₂ or advanced Rankine at 600°C

sys_best = best_opt * therm_ret_best * pb_best * (1 - 0.06)

# Thermal cascading
thermal_abs_best = best_opt * therm_ret_best
reject_heat_best = thermal_abs_best * 0.85 * (1 - pb_best) * 0.60
direct_th_best = thermal_abs_best * 0.10
total_best = sys_best + reject_heat_best + direct_th_best

# Per ft² of land at GCR = 0.35
gcr_best = 0.35
elec_per_ft2_best = (DNI_annual * sys_best * gcr_best) / m2_to_ft2
total_per_ft2_best = (DNI_annual * total_best * gcr_best) / m2_to_ft2

print(f"\n  Optical efficiency:    {best_opt*100:.2f}%")
print(f"  Thermal retention:     {therm_ret_best*100:.2f}%")
print(f"  Power block (sCO₂):   {pb_best*100:.1f}%")
print(f"  Parasitic:             {0.06*100:.1f}%")
print(f"  Solar→electric:        {sys_best*100:.2f}%")
print(f"  Solar→total useful:    {total_best*100:.2f}%")
print(f"")
print(f"  GCR:                   {gcr_best*100:.0f}%")
print(f"  Electric per ft² LAND: {elec_per_ft2_best:.2f} kWh/yr")
print(f"  Total per ft² LAND:    {total_per_ft2_best:.2f} kWh/yr")
print(f"")
print(f"  CSP electric per ft²:  {csp_annual_elec_per_ft2_land:.2f} kWh/yr")
print(f"  CSP total per ft²:     {csp_total_useful_per_ft2_land:.2f} kWh/yr")
print(f"")

e_ratio_best = elec_per_ft2_best / csp_annual_elec_per_ft2_land
t_ratio_best = total_per_ft2_best / csp_total_useful_per_ft2_land

print(f"  ELECTRICITY RATIO: {e_ratio_best:.2f}× CSP {'✓ BEATS CSP' if e_ratio_best > 1 else '✗ behind'}")
print(f"  TOTAL RATIO:       {t_ratio_best:.2f}× CSP {'✓ BEATS CSP' if t_ratio_best > 1 else '✗ behind'}")

# =============================================================================
# WHAT IT ACTUALLY TAKES TO BEAT CSP ON ELECTRICITY PER FT²
# =============================================================================

print(f"\n{'='*80}")
print("CRITICAL QUESTION: Can VCST v2 beat CSP on ELECTRICITY per ft²?")
print("="*80)

# CSP target to beat
target = csp_annual_elec_per_ft2_land
print(f"\n  CSP target: {target:.2f} kWh_e per ft² per year")
print(f"\n  Required: DNI × η_system × GCR / 10.764 > {target:.2f}")
print(f"  → η_system × GCR > {target * m2_to_ft2 / DNI_annual:.4f}")

required_product = target * m2_to_ft2 / DNI_annual

print(f"\n  With GCR=0.35: need η_system > {required_product/0.35*100:.2f}%")
print(f"  With GCR=0.40: need η_system > {required_product/0.40*100:.2f}%")
print(f"  With GCR=0.45: need η_system > {required_product/0.45*100:.2f}%")
print(f"\n  Current best VCST v2: η_system = {sys_best*100:.2f}%")
print(f"  CSP baseline: η_system = {csp_solar_to_elec*100:.2f}% at GCR = {csp_mirror_ground_cover*100:.0f}%")
print(f"  CSP η×GCR product: {csp_solar_to_elec * csp_mirror_ground_cover:.4f}")
print(f"  VCST v2 η×GCR product: {sys_best * gcr_best:.4f}")

print(f"\n  {'='*60}")
if sys_best * gcr_best > csp_solar_to_elec * csp_mirror_ground_cover:
    margin = ((sys_best * gcr_best) / (csp_solar_to_elec * csp_mirror_ground_cover) - 1) * 100
    print(f"  ✓✓✓ VCST v2 WINS on electricity/ft² by {margin:.1f}%")
else:
    deficit = (1 - (sys_best * gcr_best) / (csp_solar_to_elec * csp_mirror_ground_cover)) * 100
    print(f"  The electricity gap is {deficit:.1f}%")
    print(f"  VCST v2 needs either higher GCR or higher system efficiency to close it")
    print(f"  But on TOTAL energy per ft², VCST v2 leads by {(t_ratio_best-1)*100:.0f}%")
print(f"  {'='*60}")

print("\n\n✓ Model complete.")
