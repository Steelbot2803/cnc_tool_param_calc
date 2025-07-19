from flask import Flask, render_template, request
from utils.calculations import *
from utils.pdf_generator import *
from data.tool_types import *
from data.material_data import *
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    tool_types_list = list(TOOL_TYPES.keys())
    material_list = list(MATERIAL_DATA.keys())

    if request.method == 'POST':
        tool_type = request.form['TOOL_TYPES']
        tool_material = request.form['tool_material']
        material = request.form['MATERIAL_DATA']

        # Extract user inputs or fall back to recommended defaults
        defaults = tool_types.get(tool_type, {})
        recommended_fz = defaults.get("recommended_fz", {}).get(tool_material, 0.05)
        recommended_vc = defaults.get("recommended_vc", {}).get(tool_material, 120)
        recommended_ap = defaults.get("recommended_ap", 1.0)
        recommended_ae_ratio = defaults.get("recommended_ae_ratio", 0.5)
        recommended_flutes = defaults.get("default_flutes", 2)
        recommended_tool_diameter = defaults.get("default_diameter", 10.0)

        tool_diameter = float(request.form.get("tool_diameter", recommended_tool_diameter))
        flutes = int(request.form.get("flutes", recommended_flutes))
        fz = float(request.form.get("fz", recommended_fz))
        vc = float(request.form.get("vc", recommended_vc))
        ap = float(request.form.get("ap", recommended_ap))
        ae = float(request.form.get("ae", recommended_ae_ratio * tool_diameter))

        tool_life_input = request.form.get("tool_life")
        tool_life = float(tool_life_input) if tool_life_input else None

        spindle_speed = calculate_spindle_speed(vc, tool_diameter)
        feedrate = calculate_feedrate(fz, spindle_speed, flutes)
        mrr = calculate_mrr(ap, ae, feedrate)
        Kc = get_force_coefficient(material)
        force = calculate_cutting_force(Kc, ap, ae)
        power = calculate_cutting_power(force, feedrate)

        tool_material_factor = get_tool_material_factor(tool_material)
        material_factor = get_profile_factor("Expert")  # Default to expert for now
        estimated_tool_life = tool_life or estimate_tool_life(vc, fz, tool_material_factor, material_factor)

        result = {
            "Cutting Speed (Vc)": f"{vc:.2f} m/min",
            "Spindle Speed (RPM)": f"{spindle_speed:.0f}",
            "Feedrate": f"{feedrate:.2f} mm/min",
            "Material Removal Rate": f"{mrr:.2f} mm³/min",
            "Cutting Force": f"{force:.2f} N",
            "Cutting Power": f"{power:.2f} kW",
            "Estimated Tool Life": f"{estimated_tool_life:.2f} minutes"
        }

    return render_template('index.html',
        tool_types=tool_types_list,
        materials=material_list,
        result=result,
        recommended_fz=recommended_fz if request.method == 'POST' else '',
        recommended_vc=recommended_vc if request.method == 'POST' else '',
        recommended_ap=recommended_ap if request.method == 'POST' else '',
        recommended_ae=recommended_ae_ratio * recommended_tool_diameter if request.method == 'POST' else '',
        recommended_flutes=recommended_flutes if request.method == 'POST' else '',
        recommended_tool_diameter=recommended_tool_diameter if request.method == 'POST' else ''
    )

if __name__ == '__main__':
    app.run(debug=True)
