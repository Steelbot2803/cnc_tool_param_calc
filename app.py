from flask import Flask, request, render_template_string, make_response, send_file
import csv
import io
import json
from datetime import datetime
import weasyprint

app = Flask(__name__)

# Feed per tooth values in mm for each tool type and material
FEED_TABLE = {
    "Drill": {"EN24": 0.1, "17-4PH": 0.08},
    "Endmill": {"EN24": 0.12, "17-4PH": 0.10},
    "Face Mill": {"EN24": 0.25, "17-4PH": 0.2},
    "Ball Mill": {"EN24": 0.05, "17-4PH": 0.04},
    "Corner Mill": {"EN24": 0.15, "17-4PH": 0.13},
    "Chamfer Mill": {"EN24": 0.08, "17-4PH": 0.07},
    "Taper Mill": {"EN24": 0.07, "17-4PH": 0.06}
}

VC_TABLE = {
    "Drill": {"EN24": 80, "17-4PH": 60},
    "Endmill": {"EN24": 120, "17-4PH": 90},
    "Face Mill": {"EN24": 150, "17-4PH": 110},
    "Ball Mill": {"EN24": 100, "17-4PH": 75},
    "Corner Mill": {"EN24": 110, "17-4PH": 85},
    "Chamfer Mill": {"EN24": 90, "17-4PH": 70},
    "Taper Mill": {"EN24": 95, "17-4PH": 72}
}

TOOL_MATERIAL_FACTORS = {
    "Carbide": 1.0,
    "HSS": 0.6,
    "Ceramic": 1.5
}

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    chart_data = {}
    tool_types = list(FEED_TABLE.keys())
    report_mode = request.form.get("report_mode", "basic")

    if request.method == 'POST':
        if request.form.get("export") == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Parameter", "Value"])
            for key in request.form:
                if key.startswith("csv_"):
                    writer.writerow([key[4:], request.form[key]])
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=cnc_results.csv"
            response.headers["Content-type"] = "text/csv"
            return response

        if request.form.get("export") == "pdf":
            rendered_html = render_template_string(REPORT_TEMPLATE, results=json.loads(request.form['results']), chart_data=json.loads(request.form['chart_data']))
            pdf = weasyprint.HTML(string=rendered_html).write_pdf()
            return send_file(io.BytesIO(pdf), mimetype='application/pdf', as_attachment=True, download_name='cnc_report.pdf')

        tool_type = request.form.get("tool_type")
        tool_material = request.form.get("tool_material")
        material = request.form.get("material")
        diameter = float(request.form.get("diameter"))
        teeth = int(request.form.get("teeth"))
        fz_mode = request.form.get("fz_mode", "auto")
        tool_life_input = request.form.get("tool_life")

        vc_base = VC_TABLE.get(tool_type, {}).get(material, 100)
        vc_factor = TOOL_MATERIAL_FACTORS.get(tool_material, 1.0)
        vc = vc_base * vc_factor

        feed_data = FEED_TABLE.get(tool_type, {}).get(material, 0.1)
        fz = float(request.form.get("feed_per_tooth", 0.1)) if fz_mode == "manual" else feed_data

        if tool_life_input:
            tool_life = float(tool_life_input)
            tool_life = min(max(tool_life, 5), 60)
            adjusted_vc = vc * (30 / tool_life) ** 0.2
            rpm = (adjusted_vc * 1000) / (3.1416 * diameter)
            estimated_life = tool_life
        else:
            adjusted_vc = vc
            rpm = (vc * 1000) / (3.1416 * diameter)
            estimated_life = 30

        feedrate = rpm * teeth * fz
        chipload = fz
        force = feedrate * 0.005
        power = (force * vc) / 60

        results = {
            "Cutting Speed (Vc) [m/min]": round(adjusted_vc, 2),
            "Spindle Speed (RPM)": int(rpm),
            "Feed per Tooth (mm)": round(chipload, 3),
            "Feedrate (mm/min)": round(feedrate, 2),
            "Estimated Tool Life (min)": round(estimated_life, 2)
        }

        if report_mode == "detailed":
            results.update({
                "Estimated Force (N)": round(force, 2),
                "Estimated Power (W)": round(power, 2)
            })

        chart_data = {
            "RPM": int(rpm),
            "Feedrate": round(feedrate, 2),
            "Tool Life": round(estimated_life, 2),
            "Power (W)": round(power, 2)
        }

        return render_template_string(TEMPLATE, results=results, chart_data=chart_data, tool_types=tool_types)

    return render_template_string(TEMPLATE, results=results, chart_data=chart_data, tool_types=tool_types)

REPORT_TEMPLATE = """
<h1>CNC Tool Report</h1>
<ul>
{% for key, value in results.items() %}
    <li><strong>{{ key }}:</strong> {{ value }}</li>
{% endfor %}
</ul>
"""

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CNC Tool Calculator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; padding: 1rem; max-width: 600px; margin: auto; }
        label { display: block; margin-top: 1em; }
        input, select, button { width: 100%; padding: 0.5em; margin-top: 0.3em; }
        canvas { width: 100%; max-width: 100%; height: auto; }
    </style>
</head>
<body>
    <h2>CNC Tool Parameter Calculator</h2>
    <form method="POST">
        <label>Tool Type:
            <select name="tool_type">
                {% for tool in tool_types %}<option value="{{ tool }}">{{ tool }}</option>{% endfor %}
            </select>
        </label>
        <label>Tool Material:
            <select name="tool_material">
                <option>Carbide</option><option>HSS</option><option>Ceramic</option>
            </select>
        </label>
        <label>Job Material:
            <select name="material">
                <option>EN24</option><option>17-4PH</option>
            </select>
        </label>
        <label>Tool Diameter (mm):
            <input name="diameter" type="number" step="0.1" required>
        </label>
        <label>Number of Teeth:
            <input name="teeth" type="number" required>
        </label>
        <label>Feed Mode:
            <select name="fz_mode">
                <option value="auto">Auto (based on tool + material)</option>
                <option value="manual">Manual</option>
            </select>
        </label>
        <label>Feed per Tooth (manual, mm):
            <input name="feed_per_tooth" type="number" step="0.01">
        </label>
        <label>Tool Life Target (min, optional, 5-60):
            <input name="tool_life" type="number" step="1">
        </label>
        <label>Report Mode:
            <select name="report_mode">
                <option value="basic">Basic</option>
                <option value="detailed">Detailed</option>
            </select>
        </label>
        <button type="submit">Calculate</button>
    </form>

    {% if results %}
    <h3>Results</h3>
    <ul>
        {% for key, value in results.items() %}
            <li><strong>{{ key }}:</strong> {{ value }}</li>
        {% endfor %}
    </ul>

    <canvas id="myChart"></canvas>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys({{ chart_data|tojson }}),
                datasets: [{
                    label: 'CNC Results',
                    data: Object.values({{ chart_data|tojson }}),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            }
        });
    </script>

    <form method="POST">
        <input type="hidden" name="export" value="csv">
        {% for key, value in results.items() %}<input type="hidden" name="csv_{{ key }}" value="{{ value }}">{% endfor %}
        <button type="submit">Download CSV</button>
    </form>
    <form method="POST">
        <input type="hidden" name="export" value="pdf">
        <input type="hidden" name="results" value='{{ results|tojson }}'>
        <input type="hidden" name="chart_data" value='{{ chart_data|tojson }}'>
        <button type="submit">Download PDF</button>
    </form>
    {% endif %}
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=10000)
