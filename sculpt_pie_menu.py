import bpy

from bpy.types import Menu, Operator

bl_info = {
    "name": "Sculpting Brushes",
    "author": "Andrew Merizalde",
    "version": (1, 0, 0),
    "blender": (2, 7, 8),
    "location": "Viewport",
    "description": "Spacebar to access sculpting brushes pie menu.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Pie Menu"}

addon_keymaps = []

class SculptingBrushSelector(Operator):
    """Update the current sculpting brush with the selected brush"""
    bl_idname = "alm.sculpt_brush_select"
    bl_label = "Select Sculpt Brush"
    bl_options = {"REGISTER", "UNDO"}

    # add enum property
    ### When an item only contains 4 items they define (identifier, name, description, number).
    # Tricky...
    mode_options = [
        ("Clay Strips", "Clay Strips", "Clay Strips"),
        ("Crease", "Crease", "Crease"),
        ("Grab", "Grab", "Grab"),
        ("Draw", "Sculpt Draw", "Sculpt Draw"),
        ("Scrape/Peaks", "Scrape/Peaks", "Scrape/Peaks"),
        ("Clay", "Clay", "Clay"),
        ("Flatten/Contrast", "Flatten/Contrast", "Flatten/Contrast"),
        ("Snake Hook", "Snake Hook", "Snake Hook"),
        ("Inflate/Deflate", "Inflate/Deflate", "Inflate/Deflate"),
        ("Mask", "Mask", "Mask"),
        ("Fill/Deepen", "Fill/Deepen", "Fill/Deepen"),
        ("Blob", "Blob", "Blob"),
        ("Layer", "Layer", "Layer"),
        ("Smooth", "Smooth", "Smooth"),
        ("Thumb", "Thumb", "Thumb"),
        ("Nudge", "Nudge", "Nudge"),
        ("Pinch/Magnify", "Pinch/Magnify", "Pinch/Magnify")]

    selected_mode = bpy.props.EnumProperty(
            items=mode_options,
            description="Sculpt Brushes",
            default="Clay Strips")

    def execute(self, context):
        context.tool_settings.sculpt.brush = bpy.data.brushes[self.selected_mode]
        return {"FINISHED"}


class SculptingPieMenu(Menu):
    """Open a pie menu with all the sculpting brushes"""
    bl_idname = "alm.sculpt_pie_menu"
    bl_label = "Select Sculpt Brush"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator_enum("alm.sculpt_brush_select", "selected_mode")


class SculptingMenuCaller(Operator):
    """An operator for keymapping the menu"""
    bl_idname = "alm.sculpt_menu_call"
    bl_label = "Open Sculpt Pie Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="alm.sculpt_pie_menu")
        return {'FINISHED'}

classes = [SculptingBrushSelector, SculptingPieMenu, SculptingMenuCaller]

def register():
    # add operator
    for c in classes:
        bpy.utils.register_class(c)

    # add keymap entry
    kcfg = bpy.context.window_manager.keyconfigs.addon
    if kcfg:
        km = kcfg.keymaps.new(name='Sculpt', space_type='EMPTY')
        kmi = km.keymap_items.new("alm.sculpt_menu_call", 'SPACE', 'PRESS')
        addon_keymaps.append((km, kmi))

def unregister():

    # remove keymap entry
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
