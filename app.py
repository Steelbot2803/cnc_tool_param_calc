from flask import Flask, render_template, request, send_file
from io import BytesIO
from util.calculations import calculate_all
from util.pdf_generator import generate_pdf_report
from data.material_data import MATERIAL_DATA
from data.profiles import PROFILES
from data.tool_types import TOOL_TYPES

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    selected_profile = 'Beginner'
    selected_tool = 'End Mill'

    if request.method == 'POST':
        try:
            # Get user input
            profile = request.form.get('profile', 'Beginner')
            tool_type = request.form.get('tool_type', 'End Mill')
            material = request.form.get('material')
            diameter = float(request.form.get('tool_diameter', 0))
            flutes = int(request.form.get('flutes', TOOL_TYPES[tool_type]['default_flutes']))
            ap = float(request.form.get('ap', 0))
            ae = float(request.form.get('ae', 0))
            tool_life = float(request.form.get('tool_life', 0)) or None
            detailed = request.form.get('report_type', 'basic') == 'detailed'

            # Optional overrides
            vc = float(request.form.get('vc')) if request.form.get('vc') else None
            fz = float(request.form.get('fz')) if request.form.get('fz') else None
            tool_material = request.form.get('tool_material', 'Carbide')

            result = calculate_all(
                profile=profile,
                tool_type=tool_type,
                material=material,
                tool_diameter=diameter,
                flutes=flutes,
                ap=ap,
                ae=ae,
                vc_override=vc,
                fz_override=fz,
                tool_life_override=tool_life,
                tool_material=tool_material
            )

            if 'export_pdf' in request.form:
                pdf_data = generate_pdf_report(result, detailed=detailed)
                return send_file(BytesIO(pdf_data), as_attachment=True, download_name="cnc_report.pdf")

        except Exception as e:
            result = {'error': str(e)}

        selected_profile = profile
        selected_tool = tool_type

    return render_template(
        'index.html',
        result=result,
        profiles=list(PROFILES.keys()),
        selected_profile=selected_profile,
        materials=list(MATERIAL_DATA.keys()),
        tool_types=list(TOOL_TYPES.keys()),
        selected_tool=selected_tool
    )

if __name__ == '__main__':
    app.run(debug=True)
