import math

def calculate_spindle_speed(vc, tool_diameter):
    # vc (cutting speed) in m/min, tool_diameter in mm
    return (1000 * vc) / (math.pi * tool_diameter)

def calculate_feedrate(fz, spindle_speed, flutes):
    return fz * spindle_speed * flutes

def calculate_mrr(ap, ae, feedrate):
    # Material Removal Rate (MRR) in mm^3/min
    return ap * ae * feedrate

def calculate_cutting_force(Kc, ap, ae):
    # Cutting Force in N (approx.)
    return Kc * ap * ae / 1000

def calculate_cutting_power(force_N, feedrate_mm_min):
    # Cutting power in kW
    return (force_N * feedrate_mm_min) / (60 * 1000)

def estimate_tool_life(vc, fz, tool_material_factor, material_factor):
    # Simplified tool life estimation model
    try:
        return (tool_material_factor * material_factor) / (vc * fz * 1000)
    except ZeroDivisionError:
        return 0.0

# Manufacturer/Handbook data tables (extend as needed)
MANUFACTURER_KC = {
    # (work_material, tool_material): Kc in N/mm^2
    ("Mild Steel", "Carbide"): 1800,
    ("Mild Steel", "HSS"): 2000,
    ("Stainless Steel", "Carbide"): 2200,
    ("Stainless Steel", "HSS"): 2500,
    ("Aluminum", "Carbide"): 1000,
    ("Aluminum", "HSS"): 1200,
    ("Titanium", "Carbide"): 2800,
    ("Titanium", "HSS"): 3200,
    ("Cast Iron", "Carbide"): 2000,
    ("Cast Iron", "HSS"): 2200,
    # Add more as needed
}

def get_force_coefficient(material, tool_material):
    for (wm, tm), kc in MANUFACTURER_KC.items():
        if wm in material and tm == tool_material:
            return kc
    # fallback to old method
    kc_values = {
        "Mild Steel": 1800,
        "Stainless Steel": 2200,
        "Aluminum": 1000,
        "Titanium": 2800,
        "Cast Iron": 2000,
        "Brass": 1200,
        "Bronze": 1400,
        "Tool Steel": 2500,
        "Inconel": 3000
    }
    for key in kc_values:
        if key in material:
            return kc_values[key]
    return 2000  # default

def get_tool_material_factor(tool_material):
    factors = {
        "Carbide": 1.2,
        "HSS": 0.8,
        "Coated Carbide": 1.5,
        "Ceramic": 1.8,
        "CBN": 2.0,
        "PCD": 2.5
    }
    return factors.get(tool_material, 1.0)

def get_profile_factor(profile):
    if profile == "Beginner":
        return 0.6
    elif profile == "Intermediate":
        return 0.8
    elif profile == "Advanced":
        return 1.0
    elif profile == "Expert":
        return 1.2
    return 1.0

# Taylor tool life data for common tool/material combos
TAYLOR_TOOL_LIFE_DATA = {
    # (tool_material, work_material): (n, C)
    ("Carbide", "Mild Steel"): (0.25, 350),
    ("Carbide", "Stainless Steel"): (0.20, 180),
    ("Carbide", "Aluminum"): (0.35, 650),
    ("Carbide", "Titanium"): (0.18, 120),
    ("Carbide", "Cast Iron"): (0.22, 250),
    ("HSS", "Mild Steel"): (0.18, 90),
    ("HSS", "Stainless Steel"): (0.15, 45),
    ("HSS", "Aluminum"): (0.25, 180),
    ("HSS", "Titanium"): (0.13, 35),
    ("HSS", "Cast Iron"): (0.16, 70),
    # Add more as needed
}

def get_taylor_params(tool_material, material):
    # Try to match by substring for material
    for (tm, wm), (n, C) in TAYLOR_TOOL_LIFE_DATA.items():
        if tm == tool_material and wm in material:
            return n, C
    return None, None

def taylor_tool_life(vc, tool_material, material):
    n, C = get_taylor_params(tool_material, material)
    if n is not None and C is not None and vc > 0:
        return (C / vc) ** (1 / n)
    return None

def taylor_vc_for_life(target_life, tool_material, material):
    n, C = get_taylor_params(tool_material, material)
    if n is not None and C is not None and target_life > 0:
        return C / (target_life ** n)
    return None


def calculate_all(
    tool_type,
    material,
    tool_diameter,
    flutes,
    ap,
    ae,
    vc_override=None,
    fz_override=None,
    tool_life_override=None,
    tool_material='Carbide',
    corner_radius=None,
    chamfer_angle=None,
    thread_pitch=None
):
    from data.material_data import MATERIAL_DATA
    from data.tool_types import TOOL_TYPES

    TOOL_MATERIAL_MULTIPLIERS = {
        "HSS": {"vc": 1, "fz": 1},
        "Carbide": {"vc": 2, "fz": 1.1},
        "Coated Carbide": {"vc": 2.5, "fz": 1.15},
        "Ceramic": {"vc": 3, "fz": 1.2},
        "CBN": {"vc": 4, "fz": 1.2},
        "PCD": {"vc": 5, "fz": 1.2}
    }

    # Get base values from material data
    material_props = MATERIAL_DATA.get(material, {"vc": 100, "fz": 0.1})
    mult = TOOL_MATERIAL_MULTIPLIERS.get(tool_material, {"vc": 1, "fz": 1})
    vc = vc_override if vc_override is not None else material_props["vc"] * mult["vc"]
    fz = fz_override if fz_override is not None else material_props["fz"] * mult["fz"]

    tool_material_factor = get_tool_material_factor(tool_material)
    material_factor = 1.0  # Could be refined per material

    # Tool type-specific logic for ap/ae
    # REMOVED: ap and ae should not be capped to corner radius for Corner Radius Mill
    # if tool_type == 'Corner Radius Mill' and corner_radius is not None:
    #     ap = min(ap, corner_radius)
    #     ae = min(ae, corner_radius)
    if tool_type == 'Chamfer Mill' and chamfer_angle is not None and ae > 0:
        ap = ae * math.tan(math.radians(chamfer_angle / 2))
    if tool_type == 'Thread Mill' and thread_pitch is not None:
        # Thread milling: feedrate = thread pitch / number of passes
        # Typically 3-5 passes for thread milling
        passes = 3  # Could be made configurable
        fz = thread_pitch / passes

    # Chip thinning correction
    fz_original = fz
    chip_thinning_applies = False
    if ae < 0.5 * tool_diameter and ae > 0:
        fz = fz * tool_diameter / (2 * ae)
        chip_thinning_applies = True

    # Effective diameter for ball nose/corner radius
    effective_diameter = tool_diameter
    if tool_type == 'Ball Mill' and ap is not None and tool_diameter is not None:
        if ap < (tool_diameter / 2):
            effective_diameter = math.sqrt(2 * ap * tool_diameter - ap ** 2)
        else:
            effective_diameter = tool_diameter
    if tool_type == 'Corner Radius Mill' and corner_radius is not None and ap is not None:
        if ap <= corner_radius:
            # Approximate: effective D = 2*sqrt(r*ap - ap^2/4)
            effective_diameter = 2 * math.sqrt(corner_radius * ap - (ap ** 2) / 4)
        else:
            effective_diameter = tool_diameter

    # Tool life calculation (Taylor equation preferred)
    calculated_tool_life = None
    taylor_life = taylor_tool_life(vc, tool_material, material)
    if tool_life_override is not None:
        # Optimize Vc for target tool life using Taylor if possible
        taylor_vc = taylor_vc_for_life(tool_life_override, tool_material, material)
        if taylor_vc is not None:
            vc = taylor_vc
            calculated_tool_life = tool_life_override
        else:
            if fz > 0 and tool_life_override > 0:
                vc = (tool_material_factor * material_factor) / (tool_life_override * fz * 1000)
            calculated_tool_life = tool_life_override
    else:
        if taylor_life is not None:
            calculated_tool_life = taylor_life
        else:
            calculated_tool_life = estimate_tool_life(vc, fz, tool_material_factor, material_factor)

    # Calculate spindle speed and feedrate
    spindle_speed = calculate_spindle_speed(vc, effective_diameter)
    feedrate = calculate_feedrate(fz, spindle_speed, flutes)
    mrr = calculate_mrr(ap, ae, feedrate)

    # Cutting force and power
    Kc = get_force_coefficient(material, tool_material)
    cutting_force = calculate_cutting_force(Kc, ap, ae)
    cutting_power = calculate_cutting_power(cutting_force, feedrate)

    warnings = []
    # Chipload too low (rubbing risk)
    chipload_check = fz if not chip_thinning_applies else (fz_original if chip_thinning_applies else fz)
    if chipload_check < 0.005:
        warnings.append("Feed per tooth (chipload) is very low. Risk of tool rubbing and rapid wear.")
    # Spindle speed too high
    if spindle_speed > 24000:
        warnings.append("Spindle speed exceeds typical machine maximum (24,000 rpm). Check your machine's limits.")
    # Feedrate too high
    if feedrate > 10000:
        warnings.append("Feedrate exceeds typical machine maximum (10,000 mm/min). Check your machine's limits.")

    return {
        "vc": vc,
        "fz": fz_original,
        "fz_adjusted": fz if chip_thinning_applies else None,
        "chip_thinning_applies": chip_thinning_applies,
        "spindle_speed": spindle_speed,
        "feedrate": feedrate,
        "mrr": mrr,
        "cutting_force": cutting_force,
        "cutting_power": cutting_power,
        "tool_life": calculated_tool_life,
        "ap": ap,
        "ae": ae,
        "flutes": flutes,
        "tool_diameter": tool_diameter,
        "tool_type": tool_type,
        "material": material,
        "tool_material": tool_material,
        "corner_radius": corner_radius,
        "chamfer_angle": chamfer_angle,
        "thread_pitch": thread_pitch,
        "warnings": warnings,
        "effective_diameter": effective_diameter
    }
