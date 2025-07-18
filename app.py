# CNC Tool Calculator - Flask PWA App

import math
from flask import Flask, render_template_string, request, send_from_directory

app = Flask(__name__)

# Cutting speed reference table (flood cooled, m/min)
cutting_speeds = {
    "EN24": {
        "HSS": (30, 40),
        "Carbide": (120, 180)
    },
    "17-4PH": {
        "HSS": (20, 30),
        "Carbide": (100, 150)
    }
}

# Presets for feed per tooth (mm/tooth)
fz_presets = {
    "roughing": 0.12,
    "finishing": 0.05
}

# Tool life estimation constants (simplified Taylor's Tool Life Equation)
taylor_constants = {
    "HSS": (80, 0.125),     # C, n
    "Carbide": (300, 0.25)
}

def get_cutting_speed(material, tool_type):
    speeds = cutting_speeds.get(material, {}).get(tool_type)
    if not speeds:
        raise ValueError("Invalid combination of material/tool type.")
    return sum(speeds) / 2  # Use average value

def calculate_spindle_speed(vc, diameter):
    return (1000 * vc) / (math.pi * diameter)

def calculate_feedrate(n, fz, flutes):
    return n * fz * flutes

def estimate_tool_life(vc, tool_type):
    C, n = taylor_constants.get(tool_type, (0, 0))
    if C == 0:
        return "Unknown"
    return round((C / vc) ** (1 / n), 2)  # in minutes

def calculate_vc_for_tool_life(tool_type, desired_life):
    C, n = taylor_constants.get(tool_type, (0, 0))
    if C == 0 or desired_life <= 0:
        return None
    return round(C / (desired_life ** n), 2)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        material = request.form['material']
        tool_type = request.form['tool_type']
        diameter = float(request.form['diameter'])
        flutes = int(request.form['flutes'])
        fz_mode = request.form['fz_mode']
        desired_life = float(request.form.get('desired_life') or 0)
        fz = float(request.form['fz']) if fz_mode == 'manual' else fz_presets[fz_mode]

        try:
            if desired_life > 0:
                vc = calculate_vc_for_tool_life(tool_type, desired_life)
                if vc is None:
                    raise ValueError("Invalid tool type or desired tool life.")
            else:
                vc = get_cutting_speed(material, tool_type)
            n = calculate_spindle_speed(vc, diameter)
            feedrate = calculate_feedrate(n, fz, flutes)
            life = estimate_tool_life(vc, tool_type)

            result = {
                'Vc': round(vc, 2),
                'RPM': round(n),
                'Feedrate': round(feedrate, 2),
                'ToolLife': life
            }
        except Exception as e:
            result = {'error': str(e)}

    return render_template_string(template, result=result)

template = """
<!doctype html>
<html lang=\"en\">
<head>
  <title>CNC Tool Calculator</title>
  <link rel=\"manifest\" href=\"/static/manifest.json\">
  <meta name=\"theme-color\" content=\"#0d47a1\">
  <script>
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/static/service-worker.js');
    }
  </script>
</head>
<body>
<h2>CNC Tool Parameter Calculator</h2>
<form method=\"post\">
  <label>Material:</label>
  <select name=\"material\">
    <option value=\"EN24\">EN24</option>
    <option value=\"17-4PH\">17-4PH</option>
  </select><br><br>

  <label>Tool Type:</label>
  <select name=\"tool_type\">
    <option value=\"HSS\">HSS</option>
    <option value=\"Carbide\">Carbide</option>
  </select><br><br>

  <label>Tool Diameter (mm):</label>
  <input type=\"number\" step=\"0.1\" name=\"diameter\" required><br><br>

  <label>Flutes:</label>
  <input type=\"number\" name=\"flutes\" required><br><br>

  <label>Feed per Tooth:</label>
  <select name=\"fz_mode\">
    <option value=\"roughing\">Roughing Preset</option>
    <option value=\"finishing\">Finishing Preset</option>
    <option value=\"manual\">Manual</option>
  </select>
  <input type=\"number\" step=\"0.01\" name=\"fz\" placeholder=\"Manual input if selected\"><br><br>

  <label>Desired Tool Life (min):</label>
  <input type=\"number\" step=\"0.1\" name=\"desired_life\" placeholder=\"Optional\"><br><br>

  <button type=\"submit\">Calculate</button>
</form>

{% if result %}
  <h3>Results:</h3>
  {% if result.error %}
    <p style=\"color:red;\">Error: {{ result.error }}</p>
  {% else %}
    <ul>
      <li>Cutting Speed (Vc): {{ result.Vc }} m/min</li>
      <li>Spindle Speed (RPM): {{ result.RPM }}</li>
      <li>Feedrate: {{ result.Feedrate }} mm/min</li>
      <li>Estimated Tool Life: {{ result.ToolLife }} minutes</li>
    </ul>
  {% endif %}
{% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
