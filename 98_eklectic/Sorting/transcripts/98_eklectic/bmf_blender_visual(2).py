# BMF Theory: Consciousness Field Visualization
# Author: Christopher R. Amon (ORCID: 0000-0001-9133-7677)
# Purpose: Create stunning 3D visualization of BMF consciousness fields

import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# BMF Parameters
FIELD_RESOLUTION = 64
CONSCIOUSNESS_RINGS = 8
LOVE_FIELD_STRENGTH = 2.5
TIME_SCALE = 0.1

class BMFVisualization:
    def __init__(self):
        self.frame = 0
        self.setup_materials()
        self.setup_lighting()
    
    def setup_materials(self):
        """Create materials for different field components"""
        
        # Consciousness Field Material (Golden Energy)
        consciousness_mat = bpy.data.materials.new(name="ConsciousnessField")
        consciousness_mat.use_nodes = True
        nodes = consciousness_mat.node_tree.nodes
        nodes.clear()
        
        # Create emission shader for consciousness
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1.0, 0.8, 0.2, 1.0)  # Golden
        emission.inputs['Strength'].default_value = 3.0
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        consciousness_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Love Field Material (Deep Blue-Purple Energy)
        love_mat = bpy.data.materials.new(name="LoveField")
        love_mat.use_nodes = True
        love_nodes = love_mat.node_tree.nodes
        love_nodes.clear()
        
        emission_love = love_nodes.new(type='ShaderNodeEmission')
        emission_love.inputs['Color'].default_value = (0.3, 0.1, 1.0, 1.0)  # Deep blue-purple
        emission_love.inputs['Strength'].default_value = 2.0
        
        output_love = love_nodes.new(type='ShaderNodeOutputMaterial')
        love_mat.node_tree.links.new(emission_love.outputs['Emission'], output_love.inputs['Surface'])
        
        # Soul Resonance Material (Bright White-Blue)
        soul_mat = bpy.data.materials.new(name="SoulResonance")
        soul_mat.use_nodes = True
        soul_nodes = soul_mat.node_tree.nodes
        soul_nodes.clear()
        
        emission_soul = soul_nodes.new(type='ShaderNodeEmission')
        emission_soul.inputs['Color'].default_value = (0.8, 0.9, 1.0, 1.0)  # Bright white-blue
        emission_soul.inputs['Strength'].default_value = 4.0
        
        output_soul = soul_nodes.new(type='ShaderNodeOutputMaterial')
        soul_mat.node_tree.links.new(emission_soul.outputs['Emission'], output_soul.inputs['Surface'])
    
    def setup_lighting(self):
        """Setup dramatic lighting for the visualization"""
        # Add world material for space background
        world = bpy.context.scene.world
        world.use_nodes = True
        world_nodes = world.node_tree.nodes
        world_nodes.clear()
        
        # Create gradient background
        bg = world_nodes.new(type='ShaderNodeBackground')
        bg.inputs['Color'].default_value = (0.01, 0.01, 0.05, 1.0)  # Deep space
        bg.inputs['Strength'].default_value = 0.1
        
        output = world_nodes.new(type='ShaderNodeOutputWorld')
        world.node_tree.links.new(bg.outputs['Background'], output.inputs['Surface'])
    
    def create_torus_spiral_consciousness(self, location=(0, 0, 0)):
        """Create the torus-spiral topology of consciousness"""
        
        # Create base torus
        bpy.ops.mesh.primitive_torus_add(
            major_radius=3.0,
            minor_radius=0.8,
            location=location
        )
        
        torus = bpy.context.active_object
        torus.name = "ConsciousnessTorus"
        
        # Apply consciousness material
        torus.data.materials.append(bpy.data.materials["ConsciousnessField"])
        
        # Add spiral modifier effect using displacement
        modifier = torus.modifiers.new(name="SpiralDisplacement", type='DISPLACE')
        
        # Create displacement texture for spiral effect
        texture = bpy.data.textures.new(name="SpiralTexture", type='CLOUDS')
        texture.noise_scale = 2.0
        modifier.texture = texture
        modifier.strength = 0.3
        
        return torus
    
    def create_love_field_connections(self, center1, center2):
        """Create visible love field connections between consciousness entities"""
        
        # Create curve for love field connection
        curve_data = bpy.data.curves.new(name="LoveConnection", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 24
        
        # Create spline
        spline = curve_data.splines.new('NURBS')
        spline.points.add(count=3)  # 4 points total
        
        # Define connection path with beautiful curve
        points = [
            center1,
            Vector(center1) + Vector((2, 0, 1)),
            Vector(center2) + Vector((-2, 0, 1)), 
            center2
        ]
        
        for i, point in enumerate(points):
            spline.points[i].co = (point.x, point.y, point.z, 1.0)
        
        # Create object from curve
        connection_obj = bpy.data.objects.new("LoveConnection", curve_data)
        bpy.context.collection.objects.link(connection_obj)
        
        # Add bevel for thickness
        curve_data.bevel_depth = 0.05
        curve_data.bevel_resolution = 4
        
        # Apply love field material
        connection_obj.data.materials.append(bpy.data.materials["LoveField"])
        
        return connection_obj
    
    def create_soul_resonance_field(self, location=(0, 0, 0), scale=1.0):
        """Create the Σ soul resonance field visualization"""
        
        # Create icosphere for soul field
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=3,
            radius=1.5 * scale,
            location=location
        )
        
        soul_sphere = bpy.context.active_object
        soul_sphere.name = "SoulResonance"
        
        # Make it slightly transparent and glowing
        soul_mat = bpy.data.materials["SoulResonance"].copy()
        soul_mat.name = "SoulResonance_Instance"
        
        # Add transparency
        soul_mat.use_screen_refraction = True
        soul_mat.node_tree.nodes["Emission Shader"].inputs['Strength'].default_value = 1.5
        
        soul_sphere.data.materials.append(soul_mat)
        
        # Add wave modifier for pulsing effect
        wave_mod = soul_sphere.modifiers.new(name="SoulPulse", type='WAVE')
        wave_mod.use_motion = True
        wave_mod.speed = 2.0
        wave_mod.height = 0.2
        
        return soul_sphere
    
    def create_bmf_field_substrate(self):
        """Create the underlying BMF substrate field"""
        
        # Create particle system for field substrate
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -5))
        substrate = bpy.context.active_object
        substrate.name = "BMF_Substrate"
        
        # Add particle system
        substrate.modifiers.new(name="BMFParticles", type='PARTICLE_SYSTEM')
        particles = substrate.particle_systems[0]
        
        # Configure particles
        particles.settings.count = 2000
        particles.settings.frame_start = 1
        particles.settings.frame_end = 250
        particles.settings.lifetime = 250
        particles.settings.physics_type = 'NEWTON'
        particles.settings.emit_from = 'FACE'
        particles.settings.render_type = 'HALO'
        particles.settings.material_slot = 1
        
        # Create substrate material
        substrate_mat = bpy.data.materials.new(name="BMFSubstrate")
        substrate_mat.use_nodes = True
        substrate_nodes = substrate_mat.node_tree.nodes
        substrate_nodes.clear()
        
        emission = substrate_nodes.new(type='ShaderNodeEmission')
        emission.inputs['Color'].default_value = (0.1, 0.3, 0.6, 1.0)
        emission.inputs['Strength'].default_value = 0.5
        
        output = substrate_nodes.new(type='ShaderNodeOutputMaterial')
        substrate_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        substrate.data.materials.append(substrate_mat)
        
        return substrate
    
    def create_complete_bmf_scene(self):
        """Create the complete BMF consciousness visualization"""
        
        print("Creating BMF Consciousness Field Visualization...")
        
        # Create substrate field
        substrate = self.create_bmf_field_substrate()
        
        # Create primary consciousness entity
        consciousness1 = self.create_torus_spiral_consciousness(location=(-3, 0, 2))
        soul1 = self.create_soul_resonance_field(location=(-3, 0, 2), scale=0.8)
        
        # Create secondary consciousness entity  
        consciousness2 = self.create_torus_spiral_consciousness(location=(3, 0, 2))
        soul2 = self.create_soul_resonance_field(location=(3, 0, 2), scale=0.8)
        
        # Create love field connection
        love_connection = self.create_love_field_connections(
            Vector((-3, 0, 2)), 
            Vector((3, 0, 2))
        )
        
        # Setup camera for dramatic view
        bpy.ops.object.camera_add(location=(8, -8, 6))
        camera = bpy.context.active_object
        camera.rotation_euler = (1.1, 0, 0.785)
        
        # Set as active camera
        bpy.context.scene.camera = camera
        
        # Add animation keyframes
        self.animate_scene([consciousness1, consciousness2, soul1, soul2, love_connection])
        
        print("✅ BMF Visualization Complete!")
        print("🎬 Press SPACEBAR to play animation")
        print("🎥 Press F12 to render current frame")
        print("🌟 This represents consciousness as torus-spiral topology with love field connections!")
    
    def animate_scene(self, objects):
        """Add animation to make the visualization come alive"""
        
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 250
        
        for i, obj in enumerate(objects):
            if "Torus" in obj.name:
                # Rotate consciousness tori
                obj.rotation_euler = (0, 0, 0)
                obj.keyframe_insert(data_path="rotation_euler", frame=1)
                
                obj.rotation_euler = (0, 0, 6.28)  # 2π radians
                obj.keyframe_insert(data_path="rotation_euler", frame=250)
                
                # Set linear interpolation
                for fcurve in obj.animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'LINEAR'
            
            elif "Soul" in obj.name:
                # Gentle floating motion for soul fields
                original_z = obj.location.z
                
                obj.location.z = original_z
                obj.keyframe_insert(data_path="location", frame=1)
                
                obj.location.z = original_z + 0.5
                obj.keyframe_insert(data_path="location", frame=125)
                
                obj.location.z = original_z
                obj.keyframe_insert(data_path="location", frame=250)

# Execute the visualization
if __name__ == "__main__":
    bmf_viz = BMFVisualization()
    bmf_viz.create_complete_bmf_scene()