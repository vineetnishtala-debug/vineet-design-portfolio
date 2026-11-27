import bpy
import math
from mathutils import Vector

OUT = r"C:\Users\Vinee\Documents\Codex\2026-11-26\1-final-project-choose-a-direction\work\portfolio-work\assets\environment"


def material(name, color, metallic=0.0, roughness=0.55, emission=None):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.0
    return mat


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def box(name, location, scale, mat, bevel=0.12):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel_mod = obj.modifiers.new("Soft edges", "BEVEL")
    bevel_mod.width = bevel
    bevel_mod.segments = 3
    assign(obj, mat)
    return obj


def cylinder(name, location, radius, depth, mat, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    bevel_mod = obj.modifiers.new("Soft edges", "BEVEL")
    bevel_mod.width = min(0.08, radius * 0.2)
    bevel_mod.segments = 3
    return obj


def ico(name, location, scale, mat):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    return obj


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


teal = material("V2 Deep Teal", (0.07, 0.26, 0.28), roughness=0.42)
sage = material("V2 Sage", (0.37, 0.52, 0.39), roughness=0.65)
terracotta = material("V2 Terracotta", (0.55, 0.24, 0.16), roughness=0.62)
pale_wood = material("V2 Pale Wood", (0.76, 0.57, 0.34), roughness=0.52)
charcoal = material("V2 Charcoal", (0.045, 0.065, 0.075), metallic=0.15, roughness=0.4)
cream = material("V2 Warm Cream", (0.87, 0.82, 0.70), roughness=0.7)
felt = material("V2 Acoustic Felt", (0.25, 0.38, 0.43), roughness=0.92)
green = material("V2 Living Green", (0.12, 0.43, 0.18), roughness=0.8)
warm_light = material("V2 Warm Light", (1.0, 0.58, 0.22), roughness=0.25, emission=(1.0, 0.38, 0.08))

# Make the continuous loop slimmer, calmer, and more believable as accessible circulation.
loop = bpy.data.objects["Continuous 1.6m Accessible Loop"]
loop.data.bevel_depth = 0.48
loop.data.bevel_resolution = 6
assign(loop, teal)
assign(bpy.data.objects["Cream Wayfinding Inlay"], cream)

# Unify the material language across the existing functional zones.
for obj in bpy.context.scene.objects:
    n = obj.name
    if n.startswith("Maker Table") or n.startswith("Repair Workbench"):
        assign(obj, pale_wood)
    elif n.startswith("Table ") and "Leg" in n:
        assign(obj, charcoal)
    elif n.startswith("Movable Stool"):
        assign(obj, terracotta)
    elif n.startswith("Commons Seat"):
        assign(obj, terracotta)
    elif n.startswith("Quiet Pod") or n.startswith("Pod ") and ("Side" in n or "Back" in n or "Roof" in n):
        assign(obj, sage)
    elif n.startswith("Lockable Tool Cabinet") or n.startswith("Grow Frame"):
        assign(obj, charcoal)
    elif n.startswith("Grow Shelf"):
        assign(obj, pale_wood)
    elif n.startswith("Repair Pegboard"):
        assign(obj, felt)

# Three quiet floor fields make the program legible without adding walls.
cylinder("V2 Maker Zone Field", (-5.8, 0.1, 0.19), 4.0, 0.055, material("V2 Maker Floor", (0.48, 0.29, 0.18), roughness=0.86), 64)
cylinder("V2 Quiet Zone Field", (6.7, -3.0, 0.19), 3.1, 0.055, material("V2 Quiet Floor", (0.22, 0.38, 0.37), roughness=0.86), 64)
cylinder("V2 Grow Zone Field", (6.8, 5.4, 0.19), 2.7, 0.055, material("V2 Grow Floor", (0.24, 0.42, 0.24), roughness=0.86), 64)

# Acoustic felt clouds weave through the timber canopy and improve visual rhythm.
for i, x in enumerate((-6.0, -3.0, 0.0, 3.0, 6.0)):
    panel = box(f"V2 Acoustic Cloud {i+1}", (x, 0.4, 6.15), (0.72, 3.0, 0.09), felt, 0.18)
    panel.rotation_euler[2] = math.radians(4 if i % 2 == 0 else -4)

# Warm pendants clarify the active maker zone.
for i, y in enumerate((-3.2, 0.1, 3.35)):
    cylinder(f"V2 Maker Pendant Stem {i+1}", (-6.0, y, 4.45), 0.025, 1.9, charcoal, 24)
    cylinder(f"V2 Maker Pendant {i+1}", (-6.0, y, 3.52), 0.34, 0.12, warm_light, 48)
    bpy.ops.object.light_add(type="AREA", location=(-6.0, y, 3.35))
    light = bpy.context.object
    light.name = f"V2 Maker Area Light {i+1}"
    light.data.energy = 280
    light.data.color = (1.0, 0.58, 0.30)
    light.data.shape = "DISK"
    light.data.size = 1.8
    light.rotation_euler = (0, 0, 0)

# A planted threshold softens the transition from commons to quiet-focus pods.
for i, y in enumerate((-1.2, 0.1, 1.4, 2.7)):
    box(f"V2 Threshold Planter {i+1}", (5.15, y, 0.43), (0.52, 0.42, 0.34), charcoal, 0.12)
    ico(f"V2 Threshold Plant {i+1}", (5.15, y, 1.02), (0.52, 0.44, 0.62), green)

# Add a compact material/sample library beside the repair zone.
box("V2 Material Library", (-9.28, -2.35, 1.35), (0.26, 2.15, 1.15), charcoal, 0.08)
for row in range(3):
    for col in range(4):
        swatch_mat = (terracotta, sage, pale_wood, felt)[col]
        box(f"V2 Material Sample {row+1}-{col+1}", (-8.98, -3.72 + col * 0.9, 0.72 + row * 0.62), (0.07, 0.32, 0.20), swatch_mat, 0.04)

# Improve render fidelity while retaining the original stylized character.
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.view_settings.look = "AgX - Medium High Contrast"

views = [
    ("overall-refined.png", "Hero Camera", None, None),
    ("maker-zone-refined.png", "V2 Maker Camera", (2.8, -5.6, 3.6), (-5.2, 0.0, 1.15)),
    ("quiet-grow-refined.png", "V2 Quiet Grow Camera", (-3.8, 5.4, 3.8), (6.5, 2.0, 1.2)),
]

for filename, camera_name, location, target in views:
    if camera_name == "Hero Camera":
        camera = bpy.data.objects[camera_name]
    else:
        cam_data = bpy.data.cameras.new(camera_name)
        camera = bpy.data.objects.new(camera_name, cam_data)
        scene.collection.objects.link(camera)
        camera.location = location
        camera.data.lens = 26
        look_at(camera, target)
    scene.camera = camera
    scene.render.filepath = OUT + "\\" + filename
    bpy.ops.render.render(write_still=True)

# Preserve every modeled revision and the new detail cameras in the deliverable.
bpy.ops.wm.save_as_mainfile(filepath=OUT + r"\source\The_Canopy_Loop_refined_v2.blend")

print("REFINEMENT_COMPLETE")
