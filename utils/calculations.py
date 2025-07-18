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

def get_force_coefficient(material):
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

def calculate_all(
    profile,
    tool_type,
    material,
    tool_diameter,
    flutes,
    ap,
    ae,
    vc_override=None,
    fz_override=None,
    tool_life_override=None,
    tool_material="Carbide"
):
    profile_factor = get_profile_factor(profile)
    tool_material_factor = get_tool_material_factor(tool_material)
    force_coeff = get_force_coefficient(material)

    # Defaults or overrides
    vc = vc_override or (120 * profile_factor)
    fz = fz_override or (0.05 * profile_factor)

    spindle_speed = calculate_spindle_speed(vc, tool_diameter)
    feedrate = calculate_feedrate(fz, spindle_speed, flutes)
    mrr = calculate_mrr(ap, ae, feedrate)
    cutting_force = calculate_cutting_force(force_coeff, ap, ae)
    cutting_power = calculate_cutting_power(cutting_force, feedrate)

    tool_life = tool_life_override or estimate_tool_life(vc, fz, tool_material_factor, profile_factor)

    return {
        "Cutting Speed (Vc)": round(vc, 2),
        "Spindle Speed (RPM)": round(spindle_speed),
        "Feedrate (mm/min)": round(feedrate, 2),
        "Material Removal Rate (MRR mm³/min)": round(mrr, 2),
        "Cutting Force (N)": round(cutting_force, 2),
        "Cutting Power (kW)": round(cutting_power, 2),
        "Estimated Tool Life (min)": round(tool_life, 2)
    }

