from flask import Flask, render_template, request, send_file
from io import BytesIO
from utils.calculations import calculate_all
from utils.pdf_generator import generate_pdf_report
from data.material_data import MATERIAL_DATA
from data.tool_types import TOOL_TYPES

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    selected_tool = 'End Mill'

    if request.method == 'POST':
        try:
            # Get user input
            tool_type = request.form.get('tool_type', 'End Mill')
            material = request.form.get('material')
            diameter_val = request.form.get('tool_diameter')
            diameter = float(diameter_val) if diameter_val not in (None, "") else 0
            flutes_val = request.form.get('flutes')
            flutes = int(flutes_val) if flutes_val not in (None, "") else TOOL_TYPES[tool_type]['default_flutes']
            ap_val = request.form.get('ap')
            ap = float(ap_val) if ap_val not in (None, "") else 0
            ae_val = request.form.get('ae')
            ae = float(ae_val) if ae_val not in (None, "") else 0
            tool_life_val = request.form.get('tool_life')
            tool_life = float(tool_life_val) if tool_life_val not in (None, "") else None
            detailed = request.form.get('report_type', 'basic') == 'detailed'

            # Optional overrides
            vc_val = request.form.get('vc')
            vc = float(vc_val) if vc_val not in (None, "") else None
            fz_val = request.form.get('fz')
            fz = float(fz_val) if fz_val not in (None, "") else None
            tool_material = request.form.get('tool_material', 'Carbide')

            result = calculate_all(
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

        selected_tool = tool_type

    return render_template(
        'index.html',
        result=result,
        materials=list(MATERIAL_DATA.keys()),
        tool_types=list(TOOL_TYPES.keys()),
        selected_tool=selected_tool
    )

if __name__ == '__main__':
    app.run(debug=True)
