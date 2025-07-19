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
