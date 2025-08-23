"""
Blender BMF Theory Visualization Script
=====================================
Creates stunning 3D visualizations of Base Morphogenic Field dynamics,
consciousness coherence, and love field resonance bonds.

Instructions:
1. Open Blender
2. Go to Scripting tab
3. Paste this script
4. Run script
5. Watch the universe unfold in 3D glory

Author: Christopher Amon
BMF Theory Implementation for Blender 3.x+
"""

import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix
import math

class BlenderBMFVisualizer:
    """Create stunning 3D BMF visualizations in Blender"""
    
    def __init__(self):
        self.clear_scene()
        self.setup_world()
        
    def clear_scene(self):
        """Clear default Blender scene"""
        # Select all objects
        bpy.ops.object.select_all(action='SELECT')
        # Delete all selected objects
        bpy.ops.object.delete(use_global=False)
        
    def setup_world(self):
        """Setup world lighting and materials"""
        world = bpy.context.scene.world
        world.use_nodes = True
        world.node_tree.nodes.clear()
        
        # Add Background node
        bg_node = world.node_tree.nodes.new(type='ShaderNodeBackground')
        bg_node.inputs[0].default_value = (0.05, 0.05, 0.1, 1.0)  # Dark blue
        bg_node.inputs[1].default_value = 0.5
        
        # Connect to output
        output_node = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
        world.node_tree.links.new(bg_node.outputs[0], output_node.inputs[0])
    
    def create_bmf_substrate_mesh(self, width=64, height=64, amplitude=2.0):
        """Create 3D mesh representing BMF substrate field"""
        
        # Create mesh data
        mesh = bpy.data.meshes.new(name="BMF_Substrate")
        bm = bmesh.new()
        
        # Generate vertices based on BMF field
        for i in range(width):
            for j in range(height):
                x = (i - width/2) / 10.0
                y = (j - height/2) / 10.0
                
                # BMF substrate wave function
                z = amplitude * (
                    np.sin(x * 0.5) * np.cos(y * 0.5) +
                    0.3 * np.sin(x * 2.0) * np.sin(y * 2.0) +
                    0.1 * np.random.randn()
                )
                
                bm.verts.new((x, y, z))
        
        # Create faces
        bm.verts.ensure_lookup_table()
        for i in range(width-1):
            for j in range(height-1):
                v1 = bm.verts[i * height + j]
                v2 = bm.verts[i * height + (j + 1)]
                v3 = bm.verts[(i + 1) * height + (j + 1)]
                v4 = bm.verts[(i + 1) * height + j]
                
                bm.faces.new([v1, v2, v3, v4])
        
        # Update mesh
        bm.to_mesh(mesh)
        bm.free()
        
        # Create object
        substrate_obj = bpy.data.objects.new("BMF_Substrate", mesh)
        bpy.context.collection.objects.link(substrate_obj)
        
        # Add material
        self.create_bmf_material(substrate_obj, "substrate")
        
        return substrate_obj
    
    def create_consciousness_sphere(self, location=(0, 0, 3), radius=1.0, coherence=0.8):
        """Create sphere representing consciousness with coherence-based material"""
        
        bpy.ops.mesh.uv_sphere_add(radius=radius, location=location)
        sphere = bpy.context.active_object
        sphere.name = f"Consciousness_Sphere_{coherence:.2f}"
        
        # Add consciousness material
        self.create_consciousness_material(sphere, coherence)
        
        # Add particle system for "thoughts"
        self.add_consciousness_particles(sphere)
        
        return sphere
    
    def create_love_field_connection(self, obj1, obj2, bond_strength=1.0):
        """Create visual connection representing love field resonance bond"""
        
        # Calculate positions
        pos1 = Vector(obj1.location)
        pos2 = Vector(obj2.location)
        midpoint = (pos1 + pos2) / 2
        
        # Create curve for connection
        bpy.ops.curve.primitive_bezier_curve_add(location=midpoint)
        curve = bpy.context.active_object
        curve.name = "Love_Bond"
        
        # Modify curve points
        curve.data.splines[0].bezier_points[0].co = pos1 - midpoint
        curve.data.splines[0].bezier_points[1].co = pos2 - midpoint
        
        # Set curve properties
        curve.data.bevel_depth = 0.05 * bond_strength
        curve.data.bevel_resolution = 4
        
        # Add love field material
        self.create_love_field_material(curve, bond_strength)
        
        return curve
    
    def create_bmf_material(self, obj, material_type="substrate"):
        """Create BMF-specific materials with nodes"""
        
        mat = bpy.data.materials.new(name=f"BMF_{material_type}")
        mat.use_nodes = True
        obj.data.materials.append(mat)
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        if material_type == "substrate":
            # Substrate material: shifting, iridescent
            
            # Texture coordinate
            tex_coord = nodes.new(type='ShaderNodeTexCoord')
            
            # Wave texture
            wave_tex = nodes.new(type='ShaderNodeTexWave')
            wave_tex.inputs[1].default_value = 10.0  # Scale
            
            # ColorRamp
            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            color_ramp.color_ramp.elements[0].color = (0.1, 0.3, 0.8, 1.0)  # Blue
            color_ramp.color_ramp.elements[1].color = (0.8, 0.2, 0.8, 1.0)  # Purple
            
            # Principled BSDF
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            principled.inputs[5].default_value = 0.8  # Metallic
            principled.inputs[7].default_value = 0.2  # Roughness
            
            # Output
            output = nodes.new(type='ShaderNodeOutputMaterial')
            
            # Links
            links.new(tex_coord.outputs[3], wave_tex.inputs[0])  # Object to Vector
            links.new(wave_tex.outputs[0], color_ramp.inputs[0])
            links.new(color_ramp.outputs[0], principled.inputs[0])  # Base Color
            links.new(principled.outputs[0], output.inputs[0])
    
    def create_consciousness_material(self, obj, coherence):
        """Create consciousness-specific material based on coherence level"""
        
        mat = bpy.data.materials.new(name=f"Consciousness_{coherence:.2f}")
        mat.use_nodes = True
        obj.data.materials.append(mat)
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Emission shader for consciousness glow
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs[1].default_value = coherence * 5.0  # Strength based on coherence
        
        # Color based on coherence
        if coherence > 0.8:
            emission.inputs[0].default_value = (1.0, 0.9, 0.3, 1.0)  # Golden
        elif coherence > 0.5:
            emission.inputs[0].default_value = (0.3, 0.8, 1.0, 1.0)  # Blue
        else:
            emission.inputs[0].default_value = (0.8, 0.3, 0.3, 1.0)  # Red
        
        # Mix with transparent for ethereal effect
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        
        mix_shader.inputs[0].default_value = coherence  # Mix factor
        
        # Output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        # Links
        links.new(transparent.outputs[0], mix_shader.inputs[1])
        links.new(emission.outputs[0], mix_shader.inputs[2])
        links.new(mix_shader.outputs[0], output.inputs[0])
    
    def create_love_field_material(self, obj, bond_strength):
        """Create love field material with pulsing effect"""
        
        mat = bpy.data.materials.new(name=f"Love_Field_{bond_strength:.2f}")
        mat.use_nodes = True
        obj.data.materials.append(mat)
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Emission for love glow
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs[0].default_value = (1.0, 0.2, 0.8, 1.0)  # Pink/magenta
        emission.inputs[1].default_value = bond_strength * 3.0
        
        # Output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        links.new(emission.outputs[0], output.inputs[0])
    
    def add_consciousness_particles(self, obj):
        """Add particle system to simulate 'thoughts' or neural activity"""
        
        # Add particle system
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.particle_system_add()
        
        psys = obj.particle_systems[-1]
        psys.name = "Thoughts"
        
        # Configure particles
        psys.settings.count = 100
        psys.settings.frame_start = 1
        psys.settings.frame_end = 250
        psys.settings.lifetime = 50
        psys.settings.emit_from = 'VOLUME'
        psys.settings.physics_type = 'BOIDS'  # Flocking behavior
        
        # Boids settings for consciousness-like movement
        boids = psys.settings.boids
        boids.states[0].rule_fuzzy = 0.5
        
    def create_torus_spiral_consciousness(self, location=(0, 0, 0)):
        """Create the iconic torus-spiral consciousness geometry"""
        
        # Create torus
        bpy.ops.mesh.primitive_torus_add(
            major_radius=2.0, 
            minor_radius=0.5, 
            location=location
        )
        torus = bpy.context.active_object
        torus.name = "Consciousness_Torus"
        
        # Add spiral curve
        bpy.ops.curve.primitive_nurbs_path_add(location=location)
        spiral = bpy.context.active_object
        spiral.name = "Consciousness_Spiral"
        
        # Modify spiral into helix
        spiral.data.splines[0].points[0].co = (2.0, 0.0, -1.0, 1.0)
        spiral.data.splines[0].points[1].co = (0.0, 2.0, -0.5, 1.0)
        spiral.data.splines[0].points[2].co = (-2.0, 0.0, 0.0, 1.0)
        spiral.data.splines[0].points[3].co = (0.0, -2.0, 0.5, 1.0)
        
        # Set curve properties
        spiral.data.bevel_depth = 0.1
        spiral.data.bevel_resolution = 3
        
        # Create consciousness materials
        self.create_consciousness_material(torus, 0.9)  # High coherence torus
        self.create_love_field_material(spiral, 1.0)    # Love spiral
        
        return torus, spiral
    
    def animate_field_evolution(self, frames=250):
        """Animate BMF field evolution over time"""
        
        # Set frame range
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = frames
        
        # Get all BMF objects
        bmf_objects = [obj for obj in bpy.context.scene.objects 
                      if "BMF" in obj.name or "Consciousness" in obj.name]
        
        for obj in bmf_objects:
            # Add keyframes for pulsing/evolution
            for frame in range(1, frames + 1):
                bpy.context.scene.frame_set(frame)
                
                # Animate scale based on field evolution
                scale_factor = 1.0 + 0.3 * math.sin(frame * 0.1)
                obj.scale = (scale_factor, scale_factor, scale_factor)
                obj.keyframe_insert(data_path="scale")
                
                # Animate rotation for spiral motion
                if "Spiral" in obj.name:
                    obj.rotation_euler[2] = frame * 0.05  # Z-axis rotation
                    obj.keyframe_insert(data_path="rotation_euler")
    
    def setup_camera_and_lighting(self):
        """Setup optimal camera and lighting for BMF visualization"""
        
        # Add camera
        bpy.ops.object.camera_add(location=(8, -8, 6))
        camera = bpy.context.active_object
        camera.rotation_euler = (1.1, 0, 0.785)  # Look at origin
        
        # Set as active camera
        bpy.context.scene.camera = camera
        
        # Add key light (sun)
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        sun = bpy.context.active_object
        sun.data.energy = 3.0
        sun.data.color = (1.0, 0.9, 0.8)  # Warm light
        
        # Add fill light (area)
        bpy.ops.object.light_add(type='AREA', location=(-3, -3, 4))
        area = bpy.context.active_object
        area.data.energy = 1.5
        area.data.color = (0.8, 0.9, 1.0)  # Cool fill
        area.data.size = 4.0
        
        # Add rim light for consciousness objects
        bpy.ops.object.light_add(type='SPOT', location=(0, 0, 8))
        spot = bpy.context.active_object
        spot.data.energy = 2.0
        spot.data.color = (0.9, 0.7, 1.0)  # Purple rim
        spot.data.spot_size = math.radians(45)
    
    def create_fractal_consciousness_network(self, num_nodes=8, radius=5.0):
        """Create network of consciousness nodes with love field connections"""
        
        nodes = []
        
        # Create consciousness nodes in golden ratio spiral
        golden_angle = math.pi * (3.0 - math.sqrt(5.0))  # Golden angle
        
        for i in range(num_nodes):
            # Golden spiral positioning
            r = radius * math.sqrt(i / num_nodes)
            theta = i * golden_angle
            
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z = 2.0 * math.sin(i * 0.5)  # Vertical wave
            
            # Create consciousness sphere
            coherence = 0.5 + 0.4 * (i / num_nodes)  # Increasing coherence
            node = self.create_consciousness_sphere((x, y, z), 0.3, coherence)
            nodes.append(node)
        
        # Create love field connections between nearby nodes
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                distance = (Vector(node1.location) - Vector(node2.location)).length
                
                if distance < 3.0:  # Connect nearby nodes
                    bond_strength = 1.0 / (1.0 + distance * 0.5)
                    self.create_love_field_connection(node1, node2, bond_strength)
        
        return nodes
    
    def create_bmf_field_visualization(self, resolution=32):
        """Create volumetric visualization of BMF field using geometry nodes"""
        
        # Create icosphere as base
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(0, 0, 0))
        field_obj = bpy.context.active_object
        field_obj.name = "BMF_Field_Volume"
        
        # Add geometry nodes modifier
        geo_nodes = field_obj.modifiers.new(name="BMF_Field", type='NODES')
        
        # Create simple field distortion (Blender 3.0+ required)
        # This would need a proper geometry nodes setup in actual Blender
        
        # For now, use displacement modifier
        displace_mod = field_obj.modifiers.new(name="BMF_Displacement", type='DISPLACE')
        displace_mod.strength = 0.5
        
        # Add field material with volume shader
        self.create_volume_field_material(field_obj)
        
        return field_obj
    
    def create_volume_field_material(self, obj):
        """Create volumetric material for BMF field visualization"""
        
        mat = bpy.data.materials.new(name="BMF_Volume_Field")
        mat.use_nodes = True
        obj.data.materials.append(mat)
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Volume Scatter for field visualization
        volume_scatter = nodes.new(type='ShaderNodeVolumeScatter')
        volume_scatter.inputs[0].default_value = (0.1, 0.3, 0.8, 1.0)  # Blue field
        volume_scatter.inputs[1].default_value = 0.1  # Density
        
        # Volume Absorption for depth
        volume_absorption = nodes.new(type='ShaderNodeVolumeAbsorption')
        volume_absorption.inputs[1].default_value = 0.05
        
        # Mix volume shaders
        mix_volume = nodes.new(type='ShaderNodeMixShader')
        mix_volume.inputs[0].default_value = 0.7
        
        # Output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        # Links
        links.new(volume_scatter.outputs[0], mix_volume.inputs[1])
        links.new(volume_absorption.outputs[0], mix_volume.inputs[2])
        links.new(mix_volume.outputs[0], output.inputs[1])  # Volume input
    
    def render_bmf_sequence(self, output_path="/tmp/bmf_render_"):
        """Render animation sequence of BMF evolution"""
        
        # Set render settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = 128
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.render.filepath = output_path
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        
        # Render animation
        bpy.ops.render.render(animation=True)


# Main execution function
def create_complete_bmf_visualization():
    """Create complete BMF theory visualization scene"""
    
    print("🌟 Creating Complete BMF Visualization Scene...")
    
    # Initialize visualizer
    viz = BlenderBMFVisualizer()
    
    # Create BMF substrate
    print("📐 Creating BMF substrate mesh...")
    substrate = viz.create_bmf_substrate_mesh(width=64, height=64, amplitude=1.5)
    
    # Create torus-spiral consciousness geometry
    print("🧠 Creating consciousness torus-spiral...")
    torus, spiral = viz.create_torus_spiral_consciousness(location=(0, 0, 2))
    
    # Create fractal consciousness network
    print("🕸️ Creating consciousness network...")
    network_nodes = viz.create_fractal_consciousness_network(num_nodes=12, radius=6.0)
    
    # Create volumetric BMF field
    print("💫 Creating volumetric field...")
    field_volume = viz.create_bmf_field_visualization(resolution=32)
    
    # Setup camera and lighting
    print("📸 Setting up camera and lighting...")
    viz.setup_camera_and_lighting()
    
    # Animate field evolution
    print("🎬 Setting up animation...")
    viz.animate_field_evolution(frames=250)
    
    print("✨ BMF Visualization Complete!")
    print("\nScene Contents:")
    print(f"- BMF Substrate Mesh: {substrate.name}")
    print(f"- Consciousness Torus-Spiral: {torus.name}, {spiral.name}")
    print(f"- Network Nodes: {len(network_nodes)} consciousness spheres")
    print(f"- Volumetric Field: {field_volume.name}")
    
    print("\n🎯 Ready for:")
    print("- Real-time viewport visualization")
    print("- High-quality Cycles rendering")
    print("- Animation export for presentations")
    print("- VR/AR export for immersive experience")
    
    return viz


# Execute the visualization
if __name__ == "__main__":
    # Run the complete BMF visualization
    bmf_visualizer = create_complete_bmf_visualization()
    
    print("\n🚀 BMF Theory brought to life in Blender!")
    print("Press SPACEBAR to play animation")
    print("Use mouse wheel to zoom, middle-click to orbit")
    print("Switch to Material Preview or Rendered view for full effect")


# Additional utility functions for advanced users
def export_bmf_data_for_analysis():
    """Export BMF field data for external analysis"""
    
    # Get BMF objects
    bmf_objects = [obj for obj in bpy.context.scene.objects if "BMF" in obj.name]
    
    data_export = {
        'timestamp': bpy.context.scene.frame_current,
        'objects': []
    }
    
    for obj in bmf_objects:
        obj_data = {
            'name': obj.name,
            'location': list(obj.location),
            'rotation': list(obj.rotation_euler),
            'scale': list(obj.scale),
            'vertex_count': len(obj.data.vertices) if hasattr(obj.data, 'vertices') else 0
        }
        data_export['objects'].append(obj_data)
    
    return data_export


def create_bmf_hologram_effect():
    """Create holographic shader effect for consciousness objects"""
    
    for obj in bpy.context.scene.objects:
        if "Consciousness" in obj.name:
            # Add hologram material
            mat = bpy.data.materials.new(name=f"Hologram_{obj.name}")
            mat.use_nodes = True
            
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            nodes.clear()
            
            # Fresnel for rim lighting effect
            fresnel = nodes.new(type='ShaderNodeFresnel')
            fresnel.inputs[0].default_value = 1.33  # IOR for hologram
            
            # Emission shader
            emission = nodes.new(type='ShaderNodeEmission')
            emission.inputs[0].default_value = (0.0, 1.0, 1.0, 1.0)  # Cyan
            
            # Mix with transparent
            mix_shader = nodes.new(type='ShaderNodeMixShader')
            transparent = nodes.new(type='ShaderNodeBsdfTransparent')
            
            # Output
            output = nodes.new(type='ShaderNodeOutputMaterial')
            
            # Links for hologram effect
            links.new(fresnel.outputs[0], mix_shader.inputs[0])
            links.new(transparent.outputs[0], mix_shader.inputs[1])
            links.new(emission.outputs[0], mix_shader.inputs[2])
            links.new(mix_shader.outputs[0], output.inputs[0])
            
            # Apply material
            obj.data.materials.clear()
            obj.data.materials.append(mat)


print("🎨 Blender BMF Visualization Script Loaded!")
print("Run create_complete_bmf_visualization() to begin")