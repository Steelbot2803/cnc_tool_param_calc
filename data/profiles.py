PROFILES = {
    "Beginner": {
        "description": "Minimal inputs, safe conservative defaults",
        "adjustments": {
            "vc_factor": 0.6,
            "fz_factor": 0.6
        },
        "editable": ["material", "tool_type", "tool_diameter", "flutes"]
    },
    "Intermediate": {
        "description": "Standard inputs with material/tool presets",
        "adjustments": {
            "vc_factor": 0.8,
            "fz_factor": 0.8
        },
        "editable": ["material", "tool_type", "tool_diameter", "flutes", "ap", "ae"]
    },
    "Advanced": {
        "description": "Adjust most machining parameters",
        "adjustments": {
            "vc_factor": 1.0,
            "fz_factor": 1.0
        },
        "editable": ["material", "tool_type", "tool_diameter", "flutes", "ap", "ae", "vc", "fz"]
    },
    "Expert": {
        "description": "Full control of all parameters",
        "adjustments": {
            "vc_factor": 1.2,
            "fz_factor": 1.2
        },
        "editable": ["material", "tool_type", "tool_diameter", "flutes", "ap", "ae", "vc", "fz", "tool_life"]
    }
}
