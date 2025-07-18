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
        desired_life = float(request.form.get('desired_life') or 0)
        fz_mode = request.form.get("fz_mode", "auto")
        if fz_mode == "manual":
            fz = float(request.form.get("feed_per_tooth", "0.1"))
        else:
            fz = FEED_TABLE[tool_type][material]


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

    return render_template_string(TEMPLATE, result=result)

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CNC Tool Calculator</title>
  <link rel="manifest" href="/static/manifest.json">
  <meta name="theme-color" content="#0d47a1">
  <style>
    body {
      font-family: sans-serif;
      padding: 1rem;
      margin: 0;
      background: #f7f7f7;
    }
    form {
      max-width: 400px;
      margin: 0 auto;
      background: white;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
    }
    input, select, button {
      width: 100%;
      margin-bottom: 1rem;
      padding: 0.5rem;
      font-size: 1rem;
    }
    h2, h3 {
      text-align: center;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      margin-bottom: 0.5rem;
    }
  </style>
  <script>
  document.addEventListener("DOMContentLoaded", function () {
    const modeSelect = document.querySelector("select[name='fz_mode']");
    const fzInput = document.querySelector("input[name='feed_per_tooth']").closest("label");

    function toggleFzField() {
      if (modeSelect.value === "manual") {
        fzInput.style.display = "block";
      } else {
        fzInput.style.display = "none";
      }
    }

    modeSelect.addEventListener("change", toggleFzField);
    toggleFzField(); // run on load
  });
</script>
<script>
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/static/service-worker.js');
    }
  </script>
</head>
<body>
  <h2>CNC Tool Calculator</h2>
  <form method="POST">
    <label>Tool Diameter (mm): <input type="number" step="0.01" name="diameter" required></label>
    <label>Number of Flutes: <input type="number" name="flutes" required></label>
    <label>Feed Mode:
  <select name="fz_mode">
    <option value="auto">Auto (material/tool based)</option>
    <option value="manual">Manual (use input below)</option>
  </select>
</label>
<label>Feed per Tooth (mm): <input type="number" step="0.01" name="feed_per_tooth"></label>
    <label>Tool Material:
      <select name="tool_type">
        <option value="HSS">HSS</option>
        <option value="Carbide">Carbide</option>
        <option value="Ceramic">Ceramic</option>
      </select>
    </label>
    <label>Work Material:
      <select name="material">
        <option value="EN24">EN24</option>
        <option value="17-4PH">17-4PH</option>
      </select>
    </label>
    <label>Desired Tool Life (min): <input type="number" name="desired_life" step="0.1"></label>
    <button type="submit">Calculate</button>
  </form>

  {% if results %}
    <h3>Results</h3>
    <ul>
      {% for key, value in results.items() %}
        <li><strong>{{ key }}</strong>: {{ value }}</li>
      {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
'''
