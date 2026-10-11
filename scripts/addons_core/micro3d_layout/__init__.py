# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "micro3D Workspace",
    "author": "micro3D",
    "version": (1, 1, 0),
    "blender": (5, 3, 0),
    "location": "3D Viewport header and sidebar",
    "description": "Object-centered workspace, attributes and navigation preset for µ3D",
    "category": "Interface",
}

import os

import bpy
from bpy.app.handlers import persistent

KEYMAP_ITEMS = (
    ("micro3d", "micro3D navigation", "micro3d.py"),
    ("Blender", "Blender", "Blender.py"),
)
VIEWPORT_TOOLS = (
    ("builtin.select", "Select"),
    ("builtin.select_box", "Box select"),
    ("builtin.move", "Move"),
    ("builtin.rotate", "Rotate"),
    ("builtin.scale", "Scale"),
)
COMPONENT_MODES = (
    ("VERT", "Points", "Edit points"),
    ("EDGE", "Edges", "Edit edges"),
    ("FACE", "Faces", "Edit faces"),
)


def _first_preset(filename):
    for directory in bpy.utils.preset_paths("keyconfig"):
        candidate = os.path.join(directory, filename)
        if os.path.exists(candidate):
            return candidate
    return ""


def activate_keymap(item_id):
    filename = dict((item[0], item[2]) for item in KEYMAP_ITEMS).get(item_id, "")
    path = _first_preset(filename)
    if not path:
        return False
    active = bpy.context.window_manager.keyconfigs.active
    if active is not None and active.name == item_id:
        return True
    return bool(bpy.utils.keyconfig_set(path))


def view3d_area(context):
    if context.area is not None and context.area.type == "VIEW_3D":
        return context.area
    window = context.window
    if window is None:
        return None
    for area in window.screen.areas:
        if area.type == "VIEW_3D":
            return area
    return None


def configure_area(area):
    space = area.spaces.active
    if area.type == "OUTLINER":
        space.display_mode = "VIEW_LAYER"
        space.use_sync_select = True
        space.show_restrict_column_enable = False
        space.show_restrict_column_select = False
        space.show_restrict_column_hide = True
        space.show_restrict_column_viewport = True
        space.show_restrict_column_render = True
        space.show_restrict_column_holdout = False
        space.show_restrict_column_indirect_only = False
        space.use_filter_object = True
        space.use_filter_collection = True
        space.use_filter_object_content = True
    elif area.type == "PROPERTIES":
        space.context = "OBJECT"
    elif area.type == "DOPESHEET_EDITOR":
        space.mode = "TIMELINE"


def ensure_layout(context):
    window = context.window
    if window is None:
        return
    screen = window.screen
    present = {area.type for area in screen.areas}
    if {"VIEW_3D", "OUTLINER", "PROPERTIES", "DOPESHEET_EDITOR"}.issubset(present):
        for area in screen.areas:
            configure_area(area)
        return
    for area in list(screen.areas):
        if area.type != "VIEW_3D":
            continue
        with context.temp_override(window=window, area=area):
            bpy.ops.screen.area_split(direction="VERTICAL", factor=0.72)
        right = screen.areas[-1]
        with context.temp_override(window=window, area=right):
            bpy.ops.screen.space_type_set_or_cycle(space_type="OUTLINER")
            bpy.ops.screen.area_split(direction="HORIZONTAL", factor=0.55)
        lower = screen.areas[-1]
        with context.temp_override(window=window, area=lower):
            bpy.ops.screen.space_type_set_or_cycle(space_type="PROPERTIES")
        with context.temp_override(window=window, area=area):
            bpy.ops.screen.area_split(direction="HORIZONTAL", factor=0.78)
        bottom = screen.areas[-1]
        with context.temp_override(window=window, area=bottom):
            bpy.ops.screen.space_type_set_or_cycle(space_type="DOPESHEET_EDITOR")
        break
    for area in screen.areas:
        configure_area(area)


def draw_rotation(layout, obj):
    mode = obj.rotation_mode
    if mode == "QUATERNION":
        layout.prop(obj, "rotation_quaternion")
    elif mode == "AXIS_ANGLE":
        layout.prop(obj, "rotation_axis_angle")
    else:
        layout.prop(obj, "rotation_euler")


def draw_transform(layout, context):
    obj = context.active_object
    selected = list(context.selected_objects)
    if obj is None:
        layout.label(text="No active object")
        return
    layout.prop(obj, "name", text="Name")
    if len(selected) > 1:
        layout.label(text="{0} objects selected".format(len(selected)))
    if obj.library is not None or getattr(obj, "override_library", None) is not None:
        layout.label(text="Linked or overridden data")
    if obj.parent is not None:
        layout.label(text="Parent: {0}".format(obj.parent.name))
    users = getattr(obj.data, "users", 1) if obj.data is not None else 1
    if users > 1:
        layout.label(text="Shared data, {0} users".format(users))
    layout.prop(obj, "location")
    draw_rotation(layout, obj)
    layout.prop(obj, "scale")
    layout.prop(obj, "hide_viewport", text="Hidden in viewport")
    layout.prop(obj, "hide_render", text="Hidden in render")


class MICRO3D_OT_apply_layout(bpy.types.Operator):
    bl_idname = "micro3d.apply_layout"
    bl_label = "Restore µ3D layout"
    bl_description = "Arrange viewport, object manager, attributes and timeline without changing scene data"
    bl_options = {"REGISTER"}

    def execute(self, context):
        names = {item.name for item in bpy.data.objects}
        ensure_layout(context)
        if {item.name for item in bpy.data.objects} != names:
            self.report({"ERROR"}, "Layout restore changed scene objects")
            return {"CANCELLED"}
        return {"FINISHED"}


class MICRO3D_OT_keymap(bpy.types.Operator):
    bl_idname = "micro3d.keymap"
    bl_label = "Use navigation preset"
    bl_description = "Switch between µ3D navigation and the included Blender keymap"
    bl_options = {"REGISTER"}
    item: bpy.props.EnumProperty(items=KEYMAP_ITEMS, name="Preset")

    def execute(self, context):
        if not activate_keymap(self.item):
            self.report({"WARNING"}, "Navigation preset was not found")
            return {"CANCELLED"}
        context.preferences.addons[__name__].preferences.keymap = self.item
        if not bpy.app.background:
            bpy.ops.wm.save_userpref()
        return {"FINISHED"}


class MICRO3D_OT_tool(bpy.types.Operator):
    bl_idname = "micro3d.tool"
    bl_label = "Set viewport tool"
    bl_description = "Activate a labeled viewport tool"
    bl_options = {"REGISTER"}
    tool: bpy.props.StringProperty(name="Tool")

    def execute(self, context):
        area = view3d_area(context)
        if area is None:
            self.report({"WARNING"}, "A 3D viewport is required")
            return {"CANCELLED"}
        with context.temp_override(area=area):
            result = bpy.ops.wm.tool_set_by_id(name=self.tool)
        return {"FINISHED"} if "FINISHED" in result else {"CANCELLED"}


class MICRO3D_OT_mode(bpy.types.Operator):
    bl_idname = "micro3d.mode"
    bl_label = "Set object mode"
    bl_description = "Switch between object editing and component editing"
    bl_options = {"REGISTER", "UNDO"}
    mode: bpy.props.EnumProperty(
        items=(("OBJECT", "Object", ""), ("EDIT", "Components", "")),
        name="Mode",
    )

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({"WARNING"}, "Select an object first")
            return {"CANCELLED"}
        result = bpy.ops.object.mode_set(mode=self.mode)
        if "FINISHED" not in result:
            self.report({"WARNING"}, "This object has no component mode")
            return {"CANCELLED"}
        return {"FINISHED"}


class MICRO3D_OT_component(bpy.types.Operator):
    bl_idname = "micro3d.component"
    bl_label = "Choose component"
    bl_description = "Edit points, edges or faces of the active mesh"
    bl_options = {"REGISTER", "UNDO"}
    component: bpy.props.EnumProperty(items=COMPONENT_MODES, name="Component")

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != "MESH":
            self.report({"WARNING"}, "Point, edge and face editing applies to meshes")
            return {"CANCELLED"}
        if obj.mode != "EDIT":
            if "FINISHED" not in bpy.ops.object.mode_set(mode="EDIT"):
                return {"CANCELLED"}
        bpy.ops.mesh.select_mode(type=self.component)
        expected = {"VERT": (True, False, False), "EDGE": (False, True, False), "FACE": (False, False, True)}[self.component]
        if tuple(context.tool_settings.mesh_select_mode) != expected:
            self.report({"WARNING"}, "Component mode was not applied")
            return {"CANCELLED"}
        return {"FINISHED"}


class MICRO3D_OT_view(bpy.types.Operator):
    bl_idname = "micro3d.view"
    bl_label = "Frame or projection"
    bl_description = "Frame the selection or switch perspective and orthographic projection"
    bl_options = {"REGISTER"}
    action: bpy.props.EnumProperty(
        items=(("FRAME", "Frame selection", ""), ("PROJECTION", "Projection", "")),
        name="Action",
    )

    def execute(self, context):
        area = view3d_area(context)
        if area is None:
            return {"CANCELLED"}
        region = next((item for item in area.regions if item.type == "WINDOW"), None)
        with context.temp_override(area=area, region=region):
            if self.action == "FRAME":
                result = bpy.ops.view3d.view_selected(use_all_regions=False)
            else:
                result = bpy.ops.view3d.view_persportho()
        return {"FINISHED"} if "FINISHED" in result else {"CANCELLED"}


class MICRO3D_OT_collection(bpy.types.Operator):
    bl_idname = "micro3d.collection"
    bl_label = "New collection for selection"
    bl_description = "Create a collection and place the selected objects in it. This does not parent them"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected = list(context.selected_objects)
        if not selected:
            self.report({"WARNING"}, "Select at least one object")
            return {"CANCELLED"}
        collection = bpy.data.collections.new("µ3D collection")
        context.scene.collection.children.link(collection)
        for obj in selected:
            if obj.name not in collection.objects:
                collection.objects.link(obj)
        return {"FINISHED"}


class MICRO3D_OT_parent(bpy.types.Operator):
    bl_idname = "micro3d.parent"
    bl_label = "Parent to active object"
    bl_description = "Parent the other selected objects to the active object and keep their transforms"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if context.active_object is None or len(context.selected_objects) < 2:
            self.report({"WARNING"}, "Select the children and the parent last")
            return {"CANCELLED"}
        return {"FINISHED"} if "FINISHED" in bpy.ops.object.parent_set(type="OBJECT", keep_transform=True) else {"CANCELLED"}


class MICRO3D_MT_workspace(bpy.types.Menu):
    bl_label = "µ3D"
    bl_idname = "MICRO3D_MT_workspace"

    def draw(self, _context):
        layout = self.layout
        layout.operator("micro3d.apply_layout", icon="WINDOW")
        layout.separator()
        for tool, label in VIEWPORT_TOOLS:
            op = layout.operator("micro3d.tool", text=label)
            op.tool = tool
        layout.operator("micro3d.view", text="Frame selection").action = "FRAME"
        layout.operator("micro3d.view", text="Perspective / Orthographic").action = "PROJECTION"
        layout.separator()
        layout.operator("micro3d.mode", text="Object mode").mode = "OBJECT"
        layout.operator("micro3d.mode", text="Component mode").mode = "EDIT"
        for component, label in COMPONENT_MODES:
            op = layout.operator("micro3d.component", text=label)
            op.component = component
        layout.separator()
        layout.operator("micro3d.parent", text="Parent to active")
        layout.operator("micro3d.collection", text="New collection")
        layout.separator()
        layout.operator("micro3d.keymap", text="µ3D navigation").item = "micro3d"
        layout.operator("micro3d.keymap", text="Blender keymap").item = "Blender"


def draw_header(self, _context):
    self.layout.menu("MICRO3D_MT_workspace")


class MICRO3DPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    keymap: bpy.props.EnumProperty(items=KEYMAP_ITEMS, name="Navigation", default="micro3d")

    def draw(self, _context):
        self.layout.prop(self, "keymap")


class MICRO3D_PT_layout(bpy.types.Panel):
    bl_label = "µ3D"
    bl_idname = "MICRO3D_PT_layout"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "µ3D"

    def draw(self, context):
        layout = self.layout
        layout.operator("micro3d.apply_layout")
        row = layout.row(align=True)
        for tool, label in VIEWPORT_TOOLS:
            op = row.operator("micro3d.tool", text=label)
            op.tool = tool
        layout.operator("micro3d.view", text="Frame selection").action = "FRAME"
        layout.operator("micro3d.view", text="Perspective / Orthographic").action = "PROJECTION"
        row = layout.row(align=True)
        row.operator("micro3d.mode", text="Object").mode = "OBJECT"
        row.operator("micro3d.mode", text="Components").mode = "EDIT"
        row = layout.row(align=True)
        for component, label in COMPONENT_MODES:
            op = row.operator("micro3d.component", text=label)
            op.component = component
        layout.operator("micro3d.parent")
        layout.operator("micro3d.collection")
        layout.separator()
        draw_transform(layout, context)
        layout.separator()
        layout.operator("micro3d.keymap", text="µ3D navigation").item = "micro3d"
        layout.operator("micro3d.keymap", text="Blender keymap").item = "Blender"


@persistent
def on_factory_startup(_dummy):
    addon = bpy.context.preferences.addons.get(__name__)
    activate_keymap(addon.preferences.keymap if addon is not None else "micro3d")
    ensure_layout(bpy.context)


@persistent
def on_load(_dummy):
    addon = bpy.context.preferences.addons.get(__name__)
    if addon is None:
        return
    active = bpy.context.window_manager.keyconfigs.active
    wanted = addon.preferences.keymap
    if active is None or active.name != wanted:
        activate_keymap(wanted)


classes = (
    MICRO3D_OT_apply_layout,
    MICRO3D_OT_keymap,
    MICRO3D_OT_tool,
    MICRO3D_OT_mode,
    MICRO3D_OT_component,
    MICRO3D_OT_view,
    MICRO3D_OT_collection,
    MICRO3D_OT_parent,
    MICRO3D_MT_workspace,
    MICRO3DPreferences,
    MICRO3D_PT_layout,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_HT_header.append(draw_header)
    if on_factory_startup not in bpy.app.handlers.load_factory_startup_post:
        bpy.app.handlers.load_factory_startup_post.append(on_factory_startup)
    if on_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_load)


def unregister():
    if on_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_load)
    if on_factory_startup in bpy.app.handlers.load_factory_startup_post:
        bpy.app.handlers.load_factory_startup_post.remove(on_factory_startup)
    bpy.types.VIEW3D_HT_header.remove(draw_header)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
