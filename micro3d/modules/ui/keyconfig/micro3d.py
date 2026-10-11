# SPDX-License-Identifier: GPL-3.0-or-later
# µ3D navigation preset.
# Left click selects. Alt+left orbits, Alt+right and the wheel zoom, and Alt+middle pans.
# Ctrl+Alt+left pans when the pointing device has no middle button.
# Q, W, E and R activate box select, move, rotate and scale. Keys 1, 2 and 3 select
# points, edges and faces. During a transform, digits enter a number and X, Y or Z
# constrain the axis. macOS command bindings are applied by the platform helper.

import os

import bpy
from bl_keymap_utils.io import keyconfig_init_from_data

DIRNAME, FILENAME = os.path.split(__file__)
IDNAME = os.path.splitext(FILENAME)[0]
industry_compatible = bpy.utils.execfile(os.path.join(DIRNAME, "keymap_data", "industry_compatible_data.py"))


def add_pointing_fallbacks(data):
    for entry in data:
        if len(entry) < 3 or entry[0] != "3D View":
            continue
        space = entry[1]
        if space.get("space_type") != "VIEW_3D" or space.get("region_type") != "WINDOW":
            continue
        items = entry[2].get("items")
        if items is None:
            continue
        items.append(("view3d.move", {"type": "LEFTMOUSE", "value": "PRESS", "ctrl": True, "alt": True}, None))
        items.append(("view3d.view_persportho", {"type": "NUMPAD_5", "value": "PRESS"}, None))
        return


def load():
    from sys import platform

    prefs = bpy.context.preferences
    existing = bpy.context.window_manager.keyconfigs.get(IDNAME)
    if existing is not None:
        bpy.context.window_manager.keyconfigs.remove(existing)
    keymap = bpy.context.window_manager.keyconfigs.new(IDNAME)
    params = industry_compatible.Params(use_mouse_emulate_3_button=prefs.inputs.use_mouse_emulate_3_button)
    data = industry_compatible.generate_keymaps(params)
    add_pointing_fallbacks(data)
    if platform == "darwin":
        from bl_keymap_utils.platform_helpers import keyconfig_data_oskey_from_ctrl_for_macos
        data = keyconfig_data_oskey_from_ctrl_for_macos(data)
    keyconfig_init_from_data(keymap, data)


if __name__ == "__main__":
    load()
