from flask import Flask, render_template, request
from utils.calculations import calculate_all
from utils.pdf_generator import generate_pdf
from data.tool_types import tool_types
from data.material_data import material_defaults
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    tool_types_list = list(tool_types.keys())
    materials = list(material_defaults.keys())
    recommended_fz = 0.05
    recommended_vc = 120

    if request.method == "POST":
        tool_type = request.form.get("tool_type")
        material = request.form.get("material")
        tool_material = request.form.get("tool_material", "Carbide")
        tool_diameter = float(request.form.get("tool_diameter", 0) or 0)
        flutes = int(request.form.get("flutes", 2))
        ap = float(request.form.get("ap", 0))
        ae = float(request.form.get("ae", 0))

        fz_raw = request.form.get("fz", "").strip()
        vc_raw = request.form.get("vc", "").strip()
        tool_life_raw = request.form.get("tool_life", "").strip()

        recommended_fz = tool_types.get(tool_type, {}).get("recommended_fz", {}).get(tool_material, 0.05)
        recommended_vc = tool_types.get(tool_type, {}).get("recommended_vc", {}).get(tool_material, 120)

        fz = float(fz_raw) if fz_raw else recommended_fz
        vc = float(vc_raw) if vc_raw else recommended_vc
        tool_life_override = float(tool_life_raw) if tool_life_raw else None

        result = calculate_all(
            profile=None,
            tool_type=tool_type,
            material=material,
            tool_diameter=tool_diameter,
            flutes=flutes,
            ap=ap,
            ae=ae,
            vc_override=vc,
            fz_override=fz,
            tool_life_override=tool_life_override,
            tool_material=tool_material
        )

    return render_template(
        "index.html",
        result=result,
        tool_types=tool_types_list,
        materials=materials,
        recommended_fz=recommended_fz,
        recommended_vc=recommended_vc
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
