TOOL_DATA = {
    "Drill": {
        "type": "Drill",
        "default_flutes": 2,
        "fz_range": [0.05, 0.2],
        "default_ap": 2.0,
        "notes": "Use 2-flute for general drilling. Peck drill deeper holes."
    },
    "Endmill": {
        "type": "Endmill",
        "default_flutes": 4,
        "fz_range": [0.03, 0.15],
        "default_ap": 1.0,
        "notes": "More flutes = stronger tool but worse chip evacuation."
    },
    "Ball Mill": {
        "type": "Ball Mill",
        "default_flutes": 2,
        "fz_range": [0.01, 0.08],
        "default_ap": 0.5,
        "notes": "Ideal for 3D profiles. Use low feed/speed."
    },
    "Face Mill": {
        "type": "Face Mill",
        "default_flutes": 5,
        "fz_range": [0.1, 0.3],
        "default_ap": 1.5,
        "notes": "Insert count often equals flute count. Use balanced engagement."
    },
    "Corner Mill": {
        "type": "Corner Mill",
        "default_flutes": 3,
        "fz_range": [0.05, 0.12],
        "default_ap": 0.8,
        "notes": "Great for pockets and sharp inside corners."
    },
    "Chamfer Tool": {
        "type": "Chamfer Tool",
        "default_flutes": 1,
        "fz_range": [0.01, 0.05],
        "default_ap": 0.2,
        "notes": "Used to break edges. Feed lightly to avoid chatter."
    },
    "Thread Mill": {
        "type": "Thread Mill",
        "default_flutes": 3,
        "fz_range": [0.01, 0.04],
        "default_ap": 1.0,
        "notes": "Run slowly. Multiple passes needed."
    },
    "Reamer": {
        "type": "Reamer",
        "default_flutes": 6,
        "fz_range": [0.01, 0.03],
        "default_ap": 0.5,
        "notes": "High flute count. Needs minimal feed and shallow DOC."
    }
}
